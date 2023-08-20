# HomeAssistantSecurityTools
ha_dos.py
Options:
        -s: Specify the server's address with port number.
            If port is not provided, the port will be selected appropriately according to the protocol (i.e. HTTP vs HTTPS).
        -d: Specify the number of concurrent DOS attack processes. The default is 20.
        -m: Specify DOS attack method. 1 is for GET, 2 is for POST, and 0 is for both. Default is 0.

Example: python ha_dos.py -s 192.168.1.1:8080 -d 20 -m 1


ha_bruteforce
Options:
        -s: Specify the server's address with port number.
            If port is not provided, the port will be selected appropriately according to the protocol (i.e. HTTP vs HTTPS).
        -u: Specify the username.
        -p: Specify the password.
        -P: Specify the list of password.
        -b: Specify the number of concurrent bruteforce processes. The default is 20.
            Lower the number if HomeAssistant server is running on a low-end machine.

Example: python ha_bruteforce.py -s 192.168.1.1:8080 -u admin -P passwords.txt
