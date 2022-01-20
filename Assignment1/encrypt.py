import os
import re
import numpy as np


textTodigit = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}
digitTotext = dict([(value, key) for key, value in textTodigit.items()])

def encryption(plaintext, key):
    text = plaintext
    terms = re.split(r'[\n;,\s.:"\'\[\](){}!]\s*', text)
    terms = [terms[i].upper() for i in range(len(terms))]
    text = ''.join(terms)
    n = len(key)
    
    digits = [textTodigit[text[i]] for i in range(len(text))]

    chunks = []
    i = 0
    while i<len(digits):
        chunks.append(digits[i:i+n])
        i+=n

    extra = n-len(chunks[len(chunks)-1])
    for i in range(extra):
        chunks[len(chunks)-1].append(23)

    encrypted = []
    for chunk in chunks:
        transposed = np.transpose(chunk)
        temp = np.mod(key.dot(transposed),26)
        entry = ''
        for digit in temp:
            entry = entry + digitTotext[digit]
        encrypted.append(entry)
    encrypted = ''.join(encrypted)
    
    return encrypted
    
plaintext = "ATTACKISTODAYXX"
key = np.array([[2, 4, 5], [9, 2, 1], [3, 17, 7]])
#key = np.array([[3,2],[3,5]])
print(encryption(plaintext,key))

