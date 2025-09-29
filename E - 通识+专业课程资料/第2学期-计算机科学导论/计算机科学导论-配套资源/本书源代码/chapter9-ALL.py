#=========================================================
#第8章 信息安全（Information Security）的python程序
#=========================================================

#====================
#8.3 措施和技术
#====================

#++++++++++++++++++++
#8.3.1 密码学
#++++++++++++++++++++

#非对称加密

#<程序：把n分解成p*q>
import math
n = 221
m = int(math.ceil(math.sqrt(n)))
flag = 0
for i in range(2,m+1,1):
    if n % i == 0:
        print(i,int(n/i))
        flag = 1
        break
if flag == 0:
    print ("Cannot find!")



#<程序：RSA加密解密实现>
# All the functions are written by Edwin Sha
def change_number (x, b): #这个函数把一个十进制数x转换成一串二进制数
    if x < b: L=[x]; return(L)
    a=x % b; x=x//b
    return([a]+change_number(x,b))   #the least one goes first!
def mod (a,x,b): #计算 a^x mod b
    L=change_number(x,2)
    #print("x in binary = ",L)
    r=a % b; final=1
    for i in L:
        if i ==1: final= (final*r) % b
        r = (r*r) % b
    return(final)
def GCD(x,y): #计算 x与y的最大公约数
    if x>y: a=x;b=y
    else: a=y;b=x
    if a%b ==0: return(b)
    return(GCD(a%b,b))
def Extended_Euclid(x,y,Vx,Vy): #return [a, b] s.t. ax + by = GCD(x,y)
    #by Edwin Sha
        r=x%y; z=x//y
        if r==0: return(y,Vy)
        Vx[0]=Vx[0]-z*Vy[0]
        Vx[1]=Vx[1]-z*Vy[1]        
        return(Extended_Euclid(y, r, Vy, Vx))
def Mod_inverse(e, n): # return x : e*x mod n = 1  by Edwin Sha
    Vx=[1,0]
    Vy=[0,1]
    if e>n:
        G,X=Extended_Euclid(e,n,Vx,Vy)
        d=X[0]%n        
    else:
        G,X=Extended_Euclid(n,e,Vx,Vy)
        d=X[1]%n
    return(d)


import random
def RSA_key_generation(p,q): #p and q are primes, compute keys e and d
    phi=(p-1)*(q-1)
    e=random.randint(3,phi)
    if e%2==0: e+=1
    while(GCD(e,phi) !=1):
        e=random.randint(3,phi)
        if e%2==0: e+=1
    d=Mod_inverse(e,phi)
    if e*d % phi !=1: print("ERROR: e and d are not generated correctly")
    return (e,d)

def RSA_test(p,q):
    e,d=RSA_key_generation(p,q)
    n=p*q
    print("e, d, n: ", e, d, n)
    M=int(input("Please enter M (<n): "));
    while M>=n: M=int(input("Please enter M (< n)"))
    C=mod(M,e,n)
    print("Before transmission, original M=",M," is encrypted to Cipher=",C)
    M1=mod(C,d,n)
    if M!=M1:print("!!! Error  !!!")
    print("After transmission, Cipher",C, "is decrypted back to:",M1,"\n\n")
p=19
q=97
RSA_test(p,q) 
