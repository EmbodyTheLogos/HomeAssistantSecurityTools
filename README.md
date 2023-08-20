# HomeAssistantSecurityTools
ha_dos.py<br />
Options:<br />
        -s: Specify the server's address with port number.<br />
            If port is not provided, the port will be selected appropriately according to the protocol (i.e. HTTP vs HTTPS).<br />
        -d: Specify the number of concurrent DOS attack processes. The default is 20.<br />
        -m: Specify DOS attack method. 1 is for GET, 2 is for POST, and 0 is for both. Default is 0.<br />

Example: python ha_dos.py -s 192.168.1.1:8080 -d 20 -m 1<br />
<br />

ha_bruteforce<br />
Options:<br />
        -s: Specify the server's address with port number.<br />
            If port is not provided, the port will be selected appropriately according to the protocol (i.e. HTTP vs HTTPS).<br />
        -u: Specify the username.<br />
        -p: Specify the password.<br />
        -P: Specify the list of password.<br />
        -b: Specify the number of concurrent bruteforce processes. The default is 20.<br />
            Lower the number if HomeAssistant server is running on a low-end machine.<br />

Example: python ha_bruteforce.py -s 192.168.1.1:8080 -u admin -P passwords.txt
