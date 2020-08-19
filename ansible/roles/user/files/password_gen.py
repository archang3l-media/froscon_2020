#! /usr/bin/env python3
# Needs following packages:
# xkcd_password, pillow, qrcode, PublicKey
# Just enter pip install {package}

import re,sys, struct,os
import argparse
import logging
from xkcdpass import xkcd_password as xp
import qrcode
from Crypto.PublicKey import RSA
import crypt
import datetime

#directory_default = "roles/user/files/"
directory_default = "credentials/"
name_default = "testing_machine"

def anfangssachen():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--public", help="Place of the public keyfile to be saved")
    parser.add_argument("-s", "--private", help="Place of the private keyfile to be saved")
    parser.add_argument("-t", "--password", help="Place of the password to be saved")
    parser.add_argument("-f", "--fqdn", help="Full qualified domain name")
    parser.add_argument("-n", "--name", help="Name of the machine")
    parser.add_argument("-k", "--key", action="store_true", help="Generate a keypair")
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = anfangssachen()
    logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.INFO)
    if (not args.public): directory_public = directory_default 
    else: directory_public = args.public
    if (not args.private): directory_private = directory_default 
    else: directory_private = args.private
    if (not args.password): directory_password = directory_default 
    else: directory_password = args.password
    if (not args.name): name = name_default 
    else: name = args.name
    
    if (args.key):
        now = datetime.datetime.now()
        key = RSA.generate(2048) #key.exportKey('PEM') (private key)
        qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        private_key = key.exportKey('PEM').decode("utf-8")
        #print(private_key)
        pubkey = key.publickey()
        public_key = pubkey.exportKey('PEM').decode("utf-8")
        #print (public_key)

        qr.add_data(private_key)
        qr.make(fit=True)

        img = qr.make_image()
        img.save(directory_private+name+".png")
          
        with open("temp", 'w') as content_file:
            content_file.write(public_key)
        os.system("echo $(ssh-keygen -f temp -i -m PKCS8) rescue_"+ str(now.day) +"."+ str(now.month) +"."+ str(now.year) +"@" + name + " > " + directory_public + name+".pub")
        os.remove("temp")
        
    else:
        wordfile = xp.locate_wordfile()
        mywords = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8,valid_chars='[a-z]')
        new_password = xp.generate_xkcdpassword(mywords,delimiter="",numwords=8)
        #with open(directory_password+name+".pass", 'w') as content_file:
        with open(directory_password+"passworts.txt", 'a+') as content_file:
            content_file.write(args.fqdn + "( "+ name + "): " + new_password + "\n")
        with open(directory_password+name, 'a') as content_file:
            content_file.write("Saved")
        with open(directory_password+name+".sha512", 'w') as content_file:
            content_file.write(crypt.crypt(new_password, crypt.mksalt(crypt.METHOD_SHA512)))
        
    
    
