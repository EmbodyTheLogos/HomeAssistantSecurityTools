# Reference: https://www.geeksforgeeks.org/how-to-get-current-cpu-and-ram-usage-in-python/

# Importing the library
import psutil
import time
import os
import threading

def get_request():
    host = "192.168.1.137:8123"
    os.system("curl " + host)

def get_logbook():

    host = "192.168.1.109:8123/api/logbook/2022-08-16T15:00:00.000Z?end_time=2022-08-16T18%3A00%3A00.000Z "
    authorize_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI2OTk4ZGE2MDMxZjQ0YTE2OWNlYTFmODRlMjEyYTY2OSIsImlhdCI6MTY2MDY3NjI2NiwiZXhwIjoxNjYwNjc4MDY2fQ.p7IJWkAEUyDpMF5axt24X59J3ZCtds7vaQJkgSlkk-g"
    headers = "-H \"Connection: keep-alive\" -H \"authorization: Bearer " + authorize_token + "\" -H \"Accept: */*\" -H \"Referer: http://192.168.1.109:8123/logbook?start_date=2022-08-15T13%3A00%3A00.000Z&end_date=2022-09-09T16%3A00%3A00.000Z\" -H \"Accept-Encoding: gzip, deflate\" -H \"Accept-Language: en-US,en;q=0.9\" --compressed"


    count = 0
    response_time = 0
    while True:
        time.sleep(30-response_time)
        count = count + 30
        # Server response time
        s_response = time.time()
        #os.system("curl " + host + headers)
        get_request()
        e_response = time.time()
        response_time = e_response - s_response
        result = "\nServer response time after " + str(count) + " seconds: " + str(response_time) + " seconds"
        print(result)
        print("__________________________")




print("*******Initial resources' usage:*******")

print('The CPU usage is: ', psutil.cpu_percent(5))
# Getting % usage of virtual_memory ( 3rd field)
print('RAM memory % used:', psutil.virtual_memory()[2])
print('RAM memory used:', psutil.virtual_memory()[3] / 1_000_000_000, "GB")

host = "192.168.1.109:8123/api/logbook/2022-08-16T15:00:00.000Z?end_time=2022-08-16T18%3A00%3A00.000Z "
authorize_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI2OTk4ZGE2MDMxZjQ0YTE2OWNlYTFmODRlMjEyYTY2OSIsImlhdCI6MTY2MDY3NjI2NiwiZXhwIjoxNjYwNjc4MDY2fQ.p7IJWkAEUyDpMF5axt24X59J3ZCtds7vaQJkgSlkk-g"
headers = "-H \"Connection: keep-alive\" -H \"authorization: Bearer " + authorize_token + "\" -H \"Accept: */*\" -H \"Referer: http://192.168.1.142:8123/logbook\" -H \"Accept-Encoding: gzip, deflate\" -H \"Accept-Language: en-US,en;q=0.9\" --compressed"


# Server response time
s_response = time.time()
#os.system("curl " + host + headers)
get_request()
e_response = time.time()
response_time = e_response - s_response
result = "\nServer response time after 0 seconds: " + str(response_time) + " seconds"
print(result)

# count down
print("__________________________")
print("Please be prepare to launch DOS attacks in")
for i in range(10,0,-1):
    time.sleep(1)
    print("                ",i)

s = time.time()
count = 10


threading.Thread(target=get_logbook).start()
while True:

    print('The CPU usage is: ', psutil.cpu_percent(30))
    # Getting % usage of virtual_memory ( 3rd field)
    print('RAM memory % used:', psutil.virtual_memory()[2])
    print('RAM memory used:', psutil.virtual_memory()[3]/1_000_000_000, "GB")






