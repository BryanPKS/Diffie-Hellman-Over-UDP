# Chat Encryption Helper - ch9_crypto_chat.py
import os, base64, json
#from Crypto.Cipher import PKCS1_OAEP, AES
#from Crypto.PublicKey import RSA, ECC
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
 
# encryption method used by all calls
def encrypt(message, usePKI, useDH, dhSecret):
    em=cipherEncrypt(message, dhSecret, 1)
    return em
 
# decryption method used by all calls
def decrypt(message, usePKI, useDH, dhSecret):
    dm=cipherEncrypt(message, dhSecret, -1)
    return dm
 
# decrypt using RSA (for future reference, not needed for this homework)
#def decrypt_rsa(ciphertext):
#    return ciphertext
 
# encrypt using RSA (for future reference, not needed for this homework)
#def encrypt_rsa(message):
#    return message
 
# check client commands (for future reference, not needed for this homework)
def check_client_command(data):
    return 1
 
# check server commands (for future reference, not needed for this homework)
def check_server_command(data):
    return 1
    
def reversed_string(a_string):
    return a_string[::-1]

def cipherEncrypt(inputText, N, D):
    ceasar = ""
    if (D == 1):
        for i in range(len(inputText)):
                char = inputText[i]
                if char.isspace() or char == '!': #extra redundency for space and ! inputs
                    pass
                else:
                    ceasar += chr((ord(char) + N-34) % 92 + 34) # this makes sure starting at 32 we get all the characters
        return ceasar
    
    if (D == -1):
        for i in range(len(inputText)):
                char = inputText[i]
                if char.isspace() or char == '!': #extra redundency for space and ! inputs
                    pass
                else:
                    ceasar += chr((ord(char) - N-34) % 92 + 34) # this makes sure starting at 32 we get all the characters
        return ceasar
