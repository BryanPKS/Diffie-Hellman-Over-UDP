# Message Sender - crypto_chat_client.py
import hashlib, random, os, time
from binascii import hexlify
from socket import *
import lab6_support as ct
import dh

#P and G are agreed upon by both Bob and Alice. They are not shared over a network connection, so Darth does not know about it.
P = 13; # A prime number P is taken 
G = 7; # A primitive root for P, G is taken 
a = 21	
bobPublicKey = 6 #assume received earlier from Bob for the UDP connection setup simplicity of this lab. In real-world, Bob would send it over UDP.   

def get_dh_sharedsecret():
    x = dh.dh_generateSecretKey(bobPublicKey, a, P)
    return x
 
def get_dh_sharedkey():
    #Alice's private key
    
    x = dh.dh_generatePublicKey(P,G,a)
    return x
   
def encrypt(plaintext, usePKI, useDH, clientSecret):
    msg = ct.encrypt(plaintext, usePKI, useDH, clientSecret)
    return msg
 
def main():
    host = "192.168.56.1" # set to IP address of target computer
    port = 8080
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
 
    # initiate the encryption variables
    sendUsingPrivate = False;
    sendUsingDH = True;
    skipEncryption = False;
    # Bob and Alice have agreed upon the public keys G and P  

    # no matter what, get the ECC shared key, only use it if the user enables
    x=get_dh_sharedkey()
    print("Alice key for sharing is", x)
    clientSecret = str(get_dh_sharedkey()).encode()
    #print(clientSecret)
    
    sharedSecret = get_dh_sharedsecret()
    print("Shared secret between Bob and Alice as calculated by Alice is", sharedSecret)
    #print(sharedSecret)
    # send the packet over UDP
    print("shared secret: ", clientSecret)
    UDPSock.sendto(clientSecret, addr)
    
    print ("Welcome to Crypto-Chat! \n")
    print ()
    flag=True	
   
    # sending loop
    while flag:
        if sendUsingPrivate == True or sendUsingDH == True:
            data = str(input("Enter secure message to send or type 'exit': "))#.encode()
        else:
            data = str(input("Enter message to send or type 'exit': "))#.encode()
        
        # determine if the user initiated a special command
        result = ct.check_client_command(data)
 
        # handle any custom commands
        if data == 'exit':
           flag=False
        if result == 0:
            break
 
 	
        ciphertext = (encrypt(data, sendUsingPrivate, sendUsingDH, sharedSecret)).encode()
        if skipEncryption:
            ciphertext = data;
            skipEncryption = False;
 	
        #print("Message being sent", ciphertext)
        # send the packet over UDP
        UDPSock.sendto(ciphertext, addr)
 
    # close UDP connection
    UDPSock.close()
    os._exit(0)
 
if __name__ == '__main__': 
 main() 
