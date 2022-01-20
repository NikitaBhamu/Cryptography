# Cryptography
This folder contains all the assignment of the course COL759 : "Cryptography &amp; Computer Security"

## Assignment 1 :  
### Encyption, Decryption & Analysis of Hill Cipher
1) encrypt.py :- This file contains the method to encrypt the plaintext by the key using the Hill Cipher algorithm.<br />
2) decrypt.py :- This file contains the method to decrypt the ciphertext by the key using the Hill Cipher algorithm.<br />
3) analysis.py :- This file contains the method to use the Index Of Coincidence of the english language to get the complete plaintext from the known plaintext attack, where the plaintext corresponding to the ciphertext of size n^2 (where n is the size of the key) is known.<br />

## Assignment 2 :  
### Authenticate encryption using Symmetric & Assymetric cryptosystem together
1) First we generate strong primes using "Gordon Method".<br />
2) Then we generate the public and private keys for both the users using that.<br />
3) Then the digital signature of the all the keys is generated and finally the keys concatenated with their digital signature with '@' in between is stored in the keys folder.<br />
4) Then first we verify the authenticity of the sender A and after that we will start encrypting the plaintext by using Vignere encryption technique and RSA together as given in the problem statement.<br />
5) Then we verify the authenticity of the receiver B and after that we will start decrypting the ciphertext by using Vignere encryption technique and RSA together as given in the problem statement.<br />
6) We also used the Chinese Remainder Theoram (CRT) to make the computations of RSA less time costly.<br /> 
