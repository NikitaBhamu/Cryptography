from genKeys import *
import re

def getBlockSize(n,charSize):
    k = 1
    p26k = pow(charSize,k)
    while p26k <= n:
        k += 1
        p26k = pow(charSize,k)
    return k-1

textTodigit = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,'@':26}

digitTotext = dict([(value, key) for key, value in textTodigit.items()])

def getChunks(text,bsize,decrypt):
    digits = [textTodigit[text[i]] for i in range(len(text))]
    chunks = []
    i = 0
    while i<len(digits):
        chunks.append(digits[i:i+bsize])
        i+=bsize

    if decrypt:
        extra = bsize-len(chunks[-1])
        for i in range(extra):
            chunks[-1].append(26)
    return chunks

def crt(c,d,p,q):
    dp = pow(d,1,p-1)
    dq = pow(d,1,q-1)
    qinv = pow(q,-1,p)
    m1 = pow(c,dp,p)
    m2 = pow(c,dq,q)
    h = pow(qinv*(m1-m2),1,p)
    m = pow(m2 + h*q, 1, p*q)
    return m

def rsaencryptblock(block,e,n,charSize,binp,bout):
    l = len(block)-1
    m = np.sum([block[i]*(charSize**(i)) for i in range(len(block))])
    c = pow(int(m),e,n)
    cipherd = []
    #c = 14105
    cmod26 = c%charSize
    for k in range(bout):
        cipherd.append(cmod26)
        c = c//(charSize)
        cmod26 = c%charSize
    cipher = [digitTotext[cipherd[i]] for i in range(len(cipherd))]
    #print('ENCRYPTING ',''.join(digitTotext[block[i]] for i in range(len(block))),''.join(cipher))
    return cipher

def rsadecryptblock(block,d,n,charSize,binp,bout,p,q):
    c = np.sum([block[i]*(charSize**i) for i in range(len(block))])
    #USE CRT
    #m = pow(int(c),d,n)
    m = crt(c,d,p,q)
    plaind = []
    #m = 7108
    mmod26 = m%charSize
    for k in range(bout):
        plaind.append(mmod26)
        m =m//(charSize)
        mmod26 = m%charSize
    l = len(plaind) - 1
    plain = [digitTotext[plaind[i]] for i in range(len(plaind))]
    #print('DECRYPTING ',''.join(digitTotext[block[i]] for i in range(len(block))),''.join(plain))
    return plain

def encryptRSA(plaintext,e,n,binp,bout,charSize):
    blocks = getChunks(plaintext,binp,1)
    #print(blocks)
    cipher = []
    for block in blocks:
        cblock = ''.join(rsaencryptblock(block,e,n,charSize,binp,bout))
        cipher.append(cblock)
    ciphertext = ''.join(cipher)
    return ciphertext.rstrip('@')

def decryptRSA(ciphertext,d,n,binp,bout,charSize,p,q):
    blocks = getChunks(ciphertext,binp,1)
    plain = []
    for block in blocks:
        plain.append(''.join(rsadecryptblock(block,d,n,charSize,binp,bout,p,q)))
    plaintext = ''.join(plain)
    return plaintext.rstrip('@')

def encryptVig(plaintext,key,charSize):
    plaintext = [textTodigit[plaintext[i]] for i in range(len(plaintext))]
    key = [textTodigit[key[i]] for i in range(len(key))]
    c = []
    m = len(key)
    for i in range(len(plaintext)):
        c.append(pow(plaintext[i] + key[i%m],1,charSize))
    cipher = ''.join([digitTotext[c[i]] for i in range(len(c))])
    return cipher

def decryptVig(cipher,key,charSize):
    cipher = [textTodigit[cipher[i]] for i in range(len(cipher))]
    key = [textTodigit[key[i]] for i in range(len(key))]
    p = []
    m = len(key)
    for i in range(len(cipher)):
        p.append(pow(cipher[i] - key[i%m],1,charSize))
    plain = ''.join([digitTotext[p[i]] for i in range(len(p))])
    return plain

def run(plaintext,vigkey,charSize):

    eCA,nCA,dCA,pCA,qCA = genSign(8,10,'CA')
    eA,nA,dA,pA,qA = genKeys(4,6,'A',dCA,nCA)
    eB,nB,dB,pB,qB = genKeys(4,6,'B',dCA,nCA)
    bA = getBlockSize(nA,27)
    bB = getBlockSize(nB,27)
    
    #USER A
    #validations to check whether user B is true or not?
    f_nB = open('keys/n'+'B'+'.txt','r+')
    f_eB = open('keys/e'+'B'+'.txt','r+')
    nB_read = f_nB.read().replace('\n', '')
    nB_arr = nB_read.split('@')
    eB_read = f_eB.read().replace('\n', '')
    eB_arr = nB_read.split('@')
    if(int(nB_arr[0]) != unsign(int(nB_arr[1]), eCA, nCA)):
        print("User B's digital signature is not authentic")
        return ""
    vigcipher = encryptVig(plaintext,vigkey,charSize)
    c = encryptRSA(decryptRSA(vigcipher,dA,nA,bA,bA+1,charSize,pA,qA),eB,nB,bB,bB+1,charSize)
    kprime = encryptRSA(decryptRSA(vigkey,dA,nA,bA,bA+1,charSize,pA,qA),eB,nB,bB,bB+1,charSize)
    
    #USER B
    #validations to check whether user A is true or not?
    f_nA = open('keys/n'+'A'+'.txt','r+')
    f_eA = open('keys/e'+'A'+'.txt','r+')
    nA_read = f_nA.read().replace('\n', '')
    nA_arr = nA_read.split('@')
    eA_read = f_eA.read().replace('\n', '')
    eA_arr = eA_read.split('@')
    if(int(nA_arr[0]) != unsign(int(nA_arr[1]), eCA, nCA)):
        print("User A's digital signature is not authentic")
        return ""
    vigciphernew = encryptRSA(decryptRSA(c,dB,nB,bB+1,bB,charSize,pB,qB),eA,nA,bA+1,bA,charSize)
    vigkeynew = encryptRSA(decryptRSA(kprime,dB,nB,bB+1,bB,charSize,pB,qB),eA,nA,bA+1,bA,charSize)
    mnew = decryptVig(vigciphernew,vigkeynew,charSize)
    print(vigkeynew,'\n',mnew)
    return mnew

with open('inp.txt') as f: 
    plaintext = f.readlines()
plaintext = (''.join(re.split(r'[^a-zA-Z]*', ''.join(plaintext)))).upper()
vigkey = 'DAENERYS'
run(plaintext,vigkey,27)
