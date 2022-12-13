
def power(a, b, p):
    if (b == 1):
        return a
    else:
        return pow(a,b,p)

def dh_generatePublicKey(P,G,privateKey):
    return power(G, privateKey, P)

def dh_generateSecretKey(publicKey, privateKey, P):
    return power(publicKey, privateKey, P)
