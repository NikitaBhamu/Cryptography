import numpy as np
import sympy as sp
import random
import math

def genST(a,b):
    s = sp.randprime(10**a, 10**b)
    t = sp.randprime(10**a, 10**b)
    return s,t

def genStrongP(s,t):
    i = random.randint(0,200)
    r = 2*i*t + 1
    while not sp.isprime(r):
        i+=1
        r = 2*i*t + 1
    po = 2*(pow(s, r-2, r))*s - 1
    j = random.randint(0,200)
    p = po + 2*j*r*s
    while not sp.isprime(p):
        j+=1
        p = po + 2*j*r*s
    return p

def genKeys(a,b,user, dCA,nCA):
    s,t = genST(a,b)
    p = genStrongP(s,t)
    q = genStrongP(s,t)
    n = p*q
    phin = (p-1)*(q-1)
    d = 0
    e = sp.randprime(1, 100)
    
    while 1:
        try:
            e = sp.randprime(1, 100)
            d = pow(e, -1, phin)
            break
        except:
            continue
    
    signed_e = sign(e,dCA,nCA)
    signed_n = sign(n,dCA,nCA)
    
    print( str(e)+'@'+str(signed_e), file=open('keys/e'+user+'.txt','w+') )
    print( str(n)+'@'+str(signed_n), file=open('keys/n'+user+'.txt','w+') )
    return e,n,d,p,q


def genSign(a,b,user):
    s,t = genST(a,b)
    p = genStrongP(s,t)
    q = genStrongP(s,t)
    n = p*q
    phin = (p-1)*(q-1)
    d = 0
    e = sp.randprime(1, 100)
    
    while 1:
        try:
            e = sp.randprime(1, 100)
            d = pow(e, -1, phin)
            break
        except:
            continue
    
    print(e, file=open('keys/e'+user+'.txt','w+'))
    print(n, file=open('keys/n'+user+'.txt','w+'))
    return e,n,d,p,q
    
    
def sign(n,dCA,nCA):
    return pow(n,dCA,nCA)
    
def unsign(nn,eCA,nCA):
    return pow(nn,eCA,nCA)
