import numpy as np
from collections import Counter
from decrypt import decryption
import math

def ic(text):
    frequencies = Counter(text)
    numerator = 0
    for char in frequencies:
        numerator += (frequencies[char])*(frequencies[char] - 1)
    return numerator/(len(text)*(len(text)-1))

#a*b = mk+1
def multiplicative_inverse(a, m):
    if(a < 0):
        while(a < 0):
            a += m
    for i in range(1,m+1):
        if(((a%m)*(i%m))%m == 1):
            return i
    return -1


def cryptanalysis(ciphertext, plaintext, complete_ciphertext):
    max_dim = math.sqrt(len(ciphertext))
    i = 1
    while(i <= 10):
        if(i > max_dim): 
            return
        ciphermat = np.ones((i,i))
        plainmat = np.ones((i,i))
        for margin in range(len(ciphertext)):
            for j in range(i):
                if(j*i + i + margin >= len(ciphertext)): continue
                chars = list(ciphertext[j*i + margin:j*i + i + margin])
                ciphermat[j] = [textToDigit[char] for char in chars]
                chars = list(plaintext[j*i + margin:j*i + i + margin])
                plainmat[j] = [textToDigit[char] for char in chars]

            plainmat = np.transpose(plainmat)
            ciphermat = np.transpose(ciphermat)
            # K x P = C
            det = round(np.linalg.det(plainmat))
            if(det == 0):
                continue
            multinv_of_det = multiplicative_inverse(det, 26)
            if(multinv_of_det == -1):
                continue
            p = np.linalg.inv(plainmat)
            p = np.multiply(p,multinv_of_det*det)
            plainmatinv = np.mod(p, 26)
            key = np.dot(ciphermat, plainmatinv)
            key = np.mod(key,26)
            l = len(complete_ciphertext)
            encrypted = complete_ciphertext[:]
            extra_added = i-(l%i)
            for t in range(l%i, i):
                encrypted += 'X'
                
            deciphered = decryption(encrypted , key)
            if(deciphered == ""):
                continue
            deciphered = deciphered[:len(deciphered)-extra_added]
            if(ic(deciphered)>=0.065):
                return key
        i+=1
    print("key size exceeded")
    return

textToDigit = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}
digitToText = dict([(value, key) for key, value in textToDigit.items()])

ciphertext = "MRFFAEIKHXJJ"
plaintext =  "ATTACKISTODA"
encrypted = "MRFFAEIKHXJJAMNMMMFZCNUTWMVH"

print(cryptanalysis(ciphertext, plaintext, encrypted))
