import numpy as np

def multiplicative_inverse(a, m):
    if(a < 0):
        while(a < 0):
            a += m
    for i in range(1,m+1):
        if(((a%m)*(i%m))%m == 1):
            return i
    return -1

def decryption(ciphertext, key):

    message = ""
    ciphertext_size = len(ciphertext)
    chunk_size = len(key)
    
    #dictionary containing the numbers associated with the characters
    dictionary = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}
    reverse_dict = dict([(value, key) for key, value in dictionary.items()])
    character_set_size = len(dictionary)

    det = round(np.linalg.det(key))
    multinv_of_det = multiplicative_inverse(det, character_set_size)
    if(multinv_of_det == -1):
        return ""
        
    k = np.linalg.inv(key)
    k = np.multiply(k,multinv_of_det*det)
    
    inverse_of_key = np.mod(k, character_set_size)
    #print(inverse_of_key)
    
    ptr = 0
    while(ptr != ciphertext_size):
        str = ciphertext[ptr:(ptr+chunk_size)]
        lst = []
        for i in range(0,chunk_size):
            lst.append(dictionary[str[i]])
        mat = []
        mat.append(lst)
        matrix = np.transpose(mat)
        #print(matrix)
        res = np.dot(inverse_of_key, matrix)
        #print(res)
        res = np.mod(res, character_set_size)
        #print(res)
        
        for row in res:
            for c in row:
                #print(c)
                message += reverse_dict[round(c)]
            
        ptr += chunk_size
    return message

ciphertext = "PFOGOABXVOCPVZA"
key = np.array([[2, 4, 5], [9, 2, 1], [3, 17, 7]])
print(decryption(ciphertext,key))
