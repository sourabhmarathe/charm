from toolbox.PKSig import PKSig
from charm.integer import *
import hashlib

def SHA1(bytes1):
    s1 = hashlib.new('sha1')
    s1.update(bytes1)
    return s1.digest()

def randomQR(n):
    return random(n) ** 2

class Sig_CL03(PKSig):
    def __init__(self, lmin=160, lin=160, secparam=512):
        global ln, lm, le, l
        ln = 2 * secparam
        lm = lmin
        le = lm + 2
        l = lin
        
    def keygen(self, secparam=512):
        pprime = randomPrime(secparam)
        while(not isPrime(2*pprime + 1)):
            pprime = randomPrime(secparam)
        p = 2 * pprime + 1

        qprime = randomPrime(secparam)
        while(not isPrime(2*qprime + 1)):
            qprime = randomPrime(secparam)
        q = 2 * qprime + 1

        N = p * q

        a = randomQR(N)
        b = randomQR(N)
        c = randomQR(N)

        pk = { 'N':N, 'a':a, 'b':b, 'c':c }
        sk = { 'p':p, 'q':q }

        return (pk, sk)
    
    def sign(self, pk, sk, m):
        e = randomPrime(le)

        ls = ln + lm + l
        s = integer(randomBits(ls))

        phi_N = (sk['p']-1)*(sk['q']-1)
        e2 = e % phi_N
    
        v = (((pk['a'] ** m)*(pk['b'] ** s)*pk['c']) ** (e2 ** -1)) % pk['N']

        sig = { 'e':e, 's':s, 'v':v }

        return sig

    def signCommit(self, pk, sk, Cx):
        e = randomPrime(le)

        ls = ln + lm + l
        rprime = integer(randomBits(ls))

        phi_N = (sk['p']-1)*(sk['q']-1)
        e2 = e % phi_N
    
        v = (((Cx)*(pk['b'] ** rprime)*pk['c']) ** (e2 ** -1)) % pk['N']

        sig = { 'e':e, 'rprime':rprime, 'v':v }

        return sig

    def verify(self, pk, m, sig):
        print("\nVERIFY\n\n")

        lhs = (sig['v'] ** sig['e']) % pk['N']
        rhs = ((pk['a'] ** m)*(pk['b'] ** sig['s'])*pk['c']) % pk['N']

        #do size check on e

        if(lhs == rhs):
            return True

        return False


if __name__ == "__main__":
    pksig = Sig_CL03() 

    (pk, sk) = pksig.keygen(512)
    print("Public parameters...")
    print("pk =>", pk)
    print("sk =>", sk)
    
    m = integer(SHA1(b'This is the message I want to hash.'))
    sig = pksig.sign(pk, sk, m)
    print("Signature...")
    print("sig =>", sig)
    
    assert pksig.verify(pk, m, sig), "FAILED VERIFICATION!!!"
    print("Successful Verification!!!")
