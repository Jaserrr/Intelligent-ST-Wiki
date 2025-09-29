#============================================
#5.1 计算思维是什么
#============================================

#<程序: 找假币的第一种方法> by Edwin Sha
def findcoin_1(L):
    if len(L) <=1:
        print("Error: coins are too few"); quit()
    i=0
    while i<len(L):
        if L[i] < L[i+1]: return (i)
        elif L[i] > L[i+1]: return (i+1)
        i=i+1
    print("All coins are the same")
    return(len(L))   #should not reach this point



#<主要程序>
import random
n=int(input("Enter the number of coins >=2: "))
w_normal=random.randint(2,5)
index_faked=random.randint(0,n-1)  # 0<= index <=n-1
L=[]
for i in range(0,n):
    L.append(w_normal)
L[index_faked]=w_normal-1
print(L)
print("The index of faked coin:",findcoin_1(L))


#============================================
#5.2 递归（Rcurrence）的基本概念
#============================================

#<程序：递归加法>
def F(a):
    if len(a) ==1: return(a[0])   #终止条件非常重要
    return(F(a[1:])+a[0])
a=[1,4,9,16]
print(F(a))



#<程序：汉诺塔_递归>
count=1
def main():
    n_str=input('请输入盘子个数：')
    n=int(n_str)
    Hanoi(n,'A','C','B')
def Hanoi(n, A, C, B):
    global count
    if n < 1:
        print('False')
    elif n == 1:
        print ("%d:\t%s -> %s" % (count, A, C))
        count += 1
    elif n > 1:
        Hanoi (n - 1, A, B, C)
        Hanoi (1, A, C, B)
        Hanoi (n - 1, B, C, A)
if(__name__=="__main__"):
    main()




#<程序：merge函数> by Edwin Sha
def merge(L1,L2):
    if len(L1) ==0: return(L2)
    if len(L2) ==0: return(L1)
    if L1[0] < L2[0]:
        return([L1[0]]+merge(L1[1:len(L1)],L2))
    else:
        return([L2[0]]+merge(L1,L2[1:len(L2)]))

X=merge([1,4,9],[10])
print(X)


#============================================
#5.3 分治法(Divide-and-Conquer Algorithm)
#============================================

#<程序：最小值_循环>
def M(a):
    m=a[0]
    for i in range(1,len(a)):
        if a[i]<m:
            m=a[i]
        return m
a=[4,1,3,5]

print(M(a))



#<程序：最小值_递归> a是个数组
def M(a):
        print(a)
        if len(a) ==1: return a[0]
        return (min(a[len(a)-1], M(a[0:len(a)-1])))

L=[4,1,3,5]
print(M(L))



#<程序：最小值_分治>
def M(a):
    #print(a)   可以列出程序执行的顺序]
    if len(a) ==1: return a[0]
    return ( min(M(a[0:len(a)//2]),M(a[len(a)//2:len(L)])))
L=[4,1,3,5]
print(M(L))



#<程序：最小值和最大值_分治>
A=[3,8,9,4,10,5,1,17]
def Smin_max(a):
    if len(a)==1:
        return(a[0],a[0])
    elif len(a)==2:
        return(min(a),max(a))
    m=len(a)//2
    lmin,lmax=Smin_max(a[:m])
    rmin,rmax=Smin_max(a[m:])
    return min(lmin,rmin),max(lmax,rmax)

print("Minimum and Maximum:%d,%d"%(Smin_max(A)))



#<程序：归并排序merge sort>
def msort(L):
    k=len(L)
    if k==0: return(L)
    if k==1: return(L)
    X1=L[0:k//2]; X2=L[k//2:k]  #X1,X2 are local variables
    print("X1=",X1,"   X2=",X2)  #看看输出是什么？知道递归是如何执行的。
    X1=msort(X1); X2=msort(X2)
    return(merge(X1,X2))



#<程序: 全加器>
def FA(a,b,c):  # Full adder
    carry = (a and b) or (b and c) or (a and c)
    sum = (a and b and c) or (a and (not b) and (not c)) \
           or ((not a) and b and (not c)) or ((not a) and (not b) and c)
    return carry, sum



#<程序：二进制加法-二分法算法> by Edwin Sha 
def add_divide(x,y,c=False):
    # x, y are lists of True or False, c is True or False
    # return carry and a list of x+y
    while len(x) < len(y): x = [False]+x
    while len(y) < len(x): y = [False]+y
    if len(x) ==1:
        ctemp, stemp=FA(x[0],y[0],c)
        return (ctemp, [stemp])
    if len(x) ==0: return c, []
    c1,s1=add_divide(x[len(x)//2:len(x)],y[len(y)//2:len(y)],c)
    c2,s2=add_divide(x[0:len(x)//2],y[0:len(y)//2],c1) #依赖关系！
    return(c2,s2+s1)


#============================================
#5.4 贪心算法(Greedy Algorithm)
#============================================

#<程序：找零钱_贪心>
v=[25,10,5,1]
n=[0,0,0,0]
def change():
    T_str=input('要找给顾客的零钱，单位：分：')
    T=int(T_str)
    greedy(T)
    for i in range(len(v)):
        print('要找给顾客',v[i],'分的硬币：',n[i])
    s=0
    for i in n:
        s=s+i
    print('找给顾客的硬币数最少为：',s)
def greedy(T):
    if T==0:return
    elif T>=v[0]:
        T=T-v[0]; n[0]=n[0]+1
        greedy(T)
    elif v[0]>T>=v[1]:
        T=T-v[1]; n[1]=n[1]+1
        greedy(T)
    elif v[1]>T>=v[2]:
        T=T-v[2]; n[2]=n[2]+1
        greedy(T)
    else:
        T=T-v[3]; n[3]=n[3]+1
        greedy(T)

if(__name__=="__main__"):
    change()



#<程序：GCD_贪心>
def main():
    x_str=input('请输入正整数x的值：')
    x=int(x_str)
    y_str=input('请输入正整数y的值：')
    y=int(y_str)
    print(x,'和',y,'的最大公约数是：', GCD(x,y))

def GCD(x,y):
    if x>y: a=x;b=y
    else:   a=y;b=x
    if a%b ==0: return(b)
    return(GCD(a%b,b))

if(__name__=="__main__"):
    main()


#============================================
#5.5 动态规划(Dynamic Programming)
#============================================

#<程序：最长递增子序列_动态规划>
def LIS(L):  #LIS (L)：Longest Increasing Sub-list of List L
    Asc=[1]*len(L);Tra=[-1]*len(L)   #设定起始值
        #Asc[i] 存放从L[0]到L[i]以L[i]为最大值的最长递增子序列的长度，
        #       这个最长数列肯定以L[i]结尾
        #Tra[i] 存此最长数列的前一个索引，以后好连起整个递增序列。
    for i in range(1,len(L)):
        X=[]
        for j in range(0,i):
            if L[i] > L[j]: X.append(j)   #所有比L[i]小L[j]的索引放在X
        for k in X:     #Asc[i]= max Asc[k]+1, for each k in X
            if Asc[i] < Asc[k]+1: Asc[i]=Asc[k]+1; Tra[i]=k
    print("Asc:",Asc)
    print("Tra:",Tra)
    max=0   #找到Asc中的最大值
    for i in range(1,len(Asc)):
        if Asc[i]>Asc[max]: max=i
    print("最长递增子序列的长度是",Asc[max])

    #将最长递增数列存到X
    X=[L[max]]; i=max;
    while (Tra[i] >=0):
        X=[L[Tra[i]]]+X
        i=Tra[i]
    print("最长递增子数列=",X)

L=[5,2,4,7,6,3,8,9]
LIS(L)



#<程序：直接用递归函数计算Asc(k)>
def Asc(k):
    if k==0: return(1)
    X=[]
    for i in range(0,k):
        if L[k] > L[i]: X.append(Asc(i))   #记录所有比L[k]小的Asc（）
    if len(X) >0: return (max(X)+1)
    else: return(1)

def LIS_R(L):
    X=[]
    for k in range(0, len(L)):
        X.append(Asc(k))
    print(X)
    print(max(X))

L=[5,2,4,7,6,3,8,9]
LIS_R(L)




#<程序：背包问题_递归>
w=[0,4,5,2,1,6] 		#w[i]是物品的重量
v=[0,45,57,22,11,67]	#v[i]是物品的价值
n=len(w)-1
j=8 				#背包的容量
x=[False for raw in range(n+1)]#x[i]为True，表示物品被放入背包
def knap_r(n,j):
    if (n==0)or(j==0):
        x[n]=False
        return 0
    elif (j>=w[n])and(knap_r(n-1,j-w[n])+v[n]>knap_r(n-1,j)):
        x[n]=True
        return knap_r(n-1,j-w[n])+v[n]
    else:
        x[n]=False
        return knap_r(n-1,j)
print("最大价值为：",knap_r(n,j))
print("物品的装入情况为：",x[1:])



#<程序：背包问题_动态规划>
w=[0,4,5,2,1,6] 		#w[i]是物品的重量
v=[0,45,57,22,11,67]	#v[i]是物品的价值
n=len(w)-1
m=8				#背包的容量
x=[False for raw in range(n+1)]#x[i]为True，表示物品被放入背包
#a[i][j]是i个物品中能够装入容量为j的背包的物品所能形成的最大价值
a=[[0 for col in range(m+1)] for raw in range(n+1)]
def knap_DP(n,m):
    #创建动态规划表
    for i in range(1,n+1):
        for j in range(1,m+1):
            a[i][j]=a[i-1][j]
            if (j>=w[i]) and(a[i-1][j-w[i]]+v[i]>a[i-1][j]):
                a[i][j]=a[i-1][j-w[i]]+v[i]
		#回溯a[i][j]的生成过程，找到装入背包的物品
    j=m
    for i in range(n,0,-1):
        if a[i][j]>a[i-1][j]:
            x[i]=True
            j=j-w[i]
    Mv=a[n][m]
    return Mv


#============================================
#5.6 以老鼠走迷宫为例
#============================================

#<程序：老鼠走迷宫_递归>
m=[[1,1,1,0,1,1,1,1,1,1],
   [1,0,0,0,0,0,0,0,1,1],
   [1,0,1,1,1,1,1,0,0,1],
   [1,0,1,0,0,0,0,1,0,1],
   [1,0,1,0,1,1,0,0,0,1],
   [1,0,0,1,1,0,1,0,1,1],
   [1,1,1,1,0,0,0,0,1,1],
   [1,0,0,0,0,1,1,1,0,0],
   [1,0,1,1,0,0,0,0,0,1],
   [1,1,1,1,1,1,1,1,1,1]]

sta1=0;sta2=3;fsh1=7;fsh2=9;success=0
def LabyrinthRat():
    print('显示迷宫：')
    for i in range(len(m)): print(m[i])
    print('入口：m[%d][%d]：出口：m[%d][%d]'%(sta1,sta2,fsh1,fsh2))
    if (visit(sta1,sta2))==0:	print('没有找到出口')
    else:
        print('显示路径：')
        for i in range(10):print(m[i])
def visit(i,j):
    m[i][j]=2
    global success
    if(i==fsh1)and(j==fsh2): success=1
    if(success!=1)and(m[i-1][j]==0): visit(i-1,j)
    if(success!=1)and(m[i+1][j]==0): visit(i+1,j)
    if(success!=1)and(m[i][j-1]==0): visit(i,j-1)
    if(success!=1)and(m[i][j+1]==0): visit(i,j+1)
    if success!=1: m[i][j]=3
    return success

if(__name__=="__main__"):
    LabyrinthRat()

#============================================
#5.7 谈计算思维的美
#============================================

#++++++++++++++++++++++++++++++++++++++++++++
#5.7.3 问题复杂度的研究之美
#++++++++++++++++++++++++++++++++++++++++++++

#<程序:Find all the factors of x and put them in list L>
import math
def factors(x,L):
    y=int(math.sqrt(x))   #x的平方根
    for i in range(2,y+1):  #一个个找
        if (x %i ==0):  	#找到一个因数i
            print(i)
            L.append(i)
            factors(x//i,L)		#递归找
            break				#跳出for循环
    else:  #cannot find a factor, so x is a prime
        L.append(int(x))
        print(int(x))
L=[]
factors(18,L)
