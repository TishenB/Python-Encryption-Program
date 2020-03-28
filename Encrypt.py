#Brandon Tishendorf
#CS 485, Project 2

from random import randrange, getrandbits

ENCODING = 'utf-8'

def get_prime(lengthInBits=32):
    primePrimitive = 0
    p = 0

    pFound = False
    while(not pFound):
        primePrimitive = generate_random_num(lengthInBits-1)
        p = 2*primePrimitive - 1
        if(is_prime(p, 100)):
            pFound = True
        
    return p


def generate_random_num(lengthInBits):
    primeCandidate = 0

    while(primeCandidate % 12 != 5 and not is_prime(primeCandidate, 100)):
        primeCandidate = getrandbits(lengthInBits)
        #Make sure rightmost bit is 1 (all even nums are prime)
        primeCandidate |= (1 << lengthInBits - 1) | 1
    
    return primeCandidate


def is_prime(numToCheck, numOfTimesToCheckIfPrime):
    #Miller-Rabin primality test
    if numToCheck == 2 or numToCheck == 3:
        return True
    
    if numToCheck <= 1 or numToCheck % 2 == 0:
        return False

    s = 0
    r = numToCheck - 1

    while r & 1 == 0:
        s += 1
        r //= 2
    
    for i in range(numOfTimesToCheckIfPrime):
        a = randrange(2, numToCheck - 1)
        x = pow(a, r, numToCheck)

        if x != 1 and x != numToCheck - 1:
            j = 1
            while j < s and x != numToCheck - 1:
                x = pow(x, 2, numToCheck)

                if x == 1:
                    return False

                j += 1

            if x != numToCheck - 1:
                return False

    return True


def get_d(p):
    return randrange(1, p-2)

#Generate a 32 bit prime, get user input for the e1, pick d >=1 <= p-2, generate e2 (pow(e1, d, p))
#pubkey text is p e1 e2
#privkey is p e1 d
def key_generation():
    seed = input('Input seed value: ')
    p = get_prime()
    d = get_d(p)
    g = 2
    e2 = pow(int(g), d, p)

    print("pubkey")
    print(str(p) + ' ' + str(g) + ' ' + str(e2) + '\n')

    print("prikey")
    print(str(p) + ' ' + str(g) + ' ' + str(d) + '\n')

    print("p = " + str(p) + ", g = " + str(g) + ", d = " + str(d) + ", e2 = " + str(e2) + ".")
    with open('pubkey.txt', 'w+') as f:
        f.write(str(p) + ' ' + str(g) + ' ' + str(e2))

    with open('prikey.txt', 'w+') as f:
        f.write(str(p) + ' ' + str(g) + ' ' + str(d))


def encryption():

    with open('pubkey.txt', 'r') as f:
        publicKeyParts = f.readline()
    
    with open('ptext.txt', 'r') as f:
        plaintext = f.readline()

    publicKeyParts = publicKeyParts.split(' ')
    p  = int(publicKeyParts[0])
    g  = int(publicKeyParts[1])
    e2 = int(publicKeyParts[2])
    
    #binaryPlainText = ''.join(format(ord(i), 'b') for i in plaintext)
    plaintext = plaintext.encode(ENCODING)
   
    plaintextBlocks = []
    #t = int.from_bytes(plaintext, 'big')
    for i in range(0, len(plaintext)):
        t = plaintext[i]
        plaintextBlocks.append(t)
        
    cipherBlocks = []

    for block in plaintextBlocks:
        r = randrange(1, 10000)
        c1 = pow(g, r, p)
        c2 = pow((block * e2**r), 1,  p)
        cipherBlocks.append(c1)
        cipherBlocks.append(c2)

    print("Cipher blocks:")
    print(cipherBlocks)
    print("")
    with open('ctext.txt', 'a+') as f:
        f.truncate(0)
        for block in cipherBlocks:
            f.write(str(block))
            f.write(' ')
    

    return 0


def decryption():
    with open('ctext.txt', 'r') as f:
        cipherText = f.readline()
    
    with open('prikey.txt', 'r') as f:
        line = f.readline()
    
    cipherTextBlocksTemp = cipherText.split(' ')
    line = line.split(' ')
    p = int(line[0])
    d = int(line[2])

    cipherTextBlocks = []
    
    for block in cipherTextBlocksTemp:
        if(block != ''):
            cipherTextBlocks.append(int(block))
        
    pBlocks = []
    for i in range(0, len(cipherTextBlocks), 2):
        P = (cipherTextBlocks[i+1] * pow(cipherTextBlocks[i], (p-1-d), p)) % p
        
        pBlocks.append(P.to_bytes(1, 'big'))

    print("Decrypted text below: ")
    for block in pBlocks:
        print(block.decode(ENCODING), end='')
    print("")
    with open('dtext.txt', 'a+') as f:
        f.truncate(0)
        for block in pBlocks:
            f.write(block.decode(ENCODING))
    
    return 0


##MAIN

go = True
while(go):
    mode = input('What mode? (k = Key Generation, e = Encryption, d = Decryption): ')
    if(mode == 'k'):
        key_generation()

    elif(mode == 'e'):
        encryption()

    elif(mode == 'd'):
        decryption()

    else:
        print('Input \'' + str(mode) + '\' not recognized.')
