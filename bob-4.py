# Message Receiver - crypto_chat_server.py
import hashlib, random, os, time
from binascii import hexlify
from socket import *
import lab6_support as ct 
import dh

#P and G are agreed upon by both Bob and Alice to be 13 and 9 respectively. They are not shared over a network connection, so Darth does not know about it.
P = 13; # A prime number P is taken 
G = 7; # A primitive root for P, G is taken 
b = 7 #Bob's private key	
 
def get_dh_sharedsecret(sharedKey):
    x = dh.dh_generateSecretKey(sharedKey, b, P)
    return x
 
def get_dh_sharedkey():
    x = dh.dh_generatePublicKey(P,G,b)
    return x
 
def decrypt(ciphertext, usePKI, useDH, serverSecret):
    #msg = ct.decrypt(ciphertext, usePKI, useDH, serverSecret)
    try:
        msg = ct.decrypt(ciphertext, usePKI, useDH, serverSecret)
    except:
        msg = ciphertext
    return msg
 
def main(): 
    # set variables used to determine scheme
    useClientPKI = False;
    useDHKey = True;
    serverSecret = 0

  
    # set the variables used for the server components
    key = ""
    host = "192.168.56.1"
    port = 8080
    buf = 1024 * 2
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Enable broadcasting mode
    UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    UDPSock.bind(addr)
    print ("Waiting to received shared key from Alice...")
    (data, addr) = UDPSock.recvfrom(buf)
    
    sharedKey = int(str(data, 'utf-8'))
    print("Shared key between Bob and Alice is", sharedKey)
    sharedSecret = get_dh_sharedsecret(sharedKey)
    
    print("Shared secret between Bob and Alice as calculated by Bob is", sharedSecret)
 
    # welcome to the server message
    print ("Waiting to receive messages...")
    flag=True
    # listening loop
    while flag:
        # read the data sent from the client
        (data, addr) = UDPSock.recvfrom(buf)

        # messages are received encoded so you must decode the message for processing
        msg = str(data, 'utf-8')

        # if any encryption is used, change the message to 'secure' message
        if useClientPKI == True or useDHKey == True:
            # send the data packet for decryption
            plaintext = decrypt(msg, useClientPKI, useDHKey, sharedSecret)
            #print("Plaintext after decrypt", plaintext)
            print ("Received secured message: " + plaintext)
            if(plaintext == "exit"): flag=False
        else:
            print ("Received message: " + msg)
            if(msg == "exit"): flag=False
        
 
    UDPSock.close()
    os._exit(0) 
 
if __name__ == '__main__': 
    main() 
