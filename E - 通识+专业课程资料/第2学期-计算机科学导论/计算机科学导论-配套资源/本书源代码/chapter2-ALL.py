#===================================
#2.2 不同进制间的转换
#===================================


#+++++++++++++++++++++++++++++++++++
#2.2.1.	二进制数转换为十进制数
#+++++++++++++++++++++++++++++++++++

#<程序：2-to-10进制转换>
b=input("Please enter a binary number:")
d=0; 
for i in range(0,len(b)):
    if b[i] == '1':
        weight = 2**(len(b)-i-1)
        d = d+weight;
print(d)



#<程序：改进后的2-to-10进制转换>
b=input("Please enter a binary number:")
d=0; weight=2**(len(b)-1);
for i in range(0,len(b)):
    if b[i] == '1':
        d = d+weight;
    weight=weight//2;       #‘//’是整数除法
print(d)




#+++++++++++++++++++++++++++++++++++
#2.2.2. 十进制数转换为二进制数
#+++++++++++++++++++++++++++++++++++

#<程序：整数的10-to-2进制转换>
x= int(input("Please enter a decimal number:"))
r = 0;
Rs = [];
while(x != 0):
    r = x% 2
    x = x//2
    Rs = [r]+Rs
for i in range(0,len(Rs)):   
#从最高位到最低位依次输出；Rs[0]存的是最高位， Rs[len(Rs)-1]存的是最低位。
    print(Rs[i],end='')



#<程序：整数的10-to-2进制转换-递归>
def convert(x):		 #把10进制数x转换为2进制数，并返回结果列表。
    if x<2: return([x])     #x=0 或 1，所以返回x
    r= x%2; 			#r 是2除x的余数
    return(convert(x//2)+[r])   # 结果=[x//2的二进制，r]

num = int(input("Please enter a decimal number:"))
Rs= convert(num)
for i in range(0, len(Rs)):
    print (Rs[i],end='')


#=====================================================================================
    


#===================================
#2.4. 一切都是逻辑（Logic）
#===================================

#+++++++++++++++++++++++++++++++++++
#2.4.3. 用逻辑做加法
#+++++++++++++++++++++++++++++++++++


#<程序: 全加器>
def FA(a,b,c):  # Full adder
     Carry = (a and b) or (b and c) or (a and c)
     Sum = (a and b and c) or (a and (not b) and (not c)) \
           or ((not a) and b and (not c)) or ((not a) and (not b) and c)
     return Carry, Sum



#<程序：完整的加法器 Carry Ripple adder>
def  add(x,y): # x, y are lists of True or False, c is True or False
                # return carry and a list of x+y
    while len(x) < len(y): x = [False]+x    #前面补0
    while len(y) < len(x): y = [False]+y	#前面补0
    L=[];Carry=False
    for i in range(len(x)-1,-1,-1):  #从最后一位一个个往前加
        Carry,Sum=FA(x[i],y[i],Carry)
        L=L+[Sum]
    return (Carry, L)



#<程序：乘法器>
def multiplier(x,y):    # 求x*y
     S=[];
     for i in range(len(y)-1,-1,-1):
         if y[i] == True:     	#y[i]是 1，要将x加进到S
             C, S=add(S,x)
             if C==True: S=[C]+S
         x=x+[False]			#每一次x都要向左移一位，后面补0
     return(S)

