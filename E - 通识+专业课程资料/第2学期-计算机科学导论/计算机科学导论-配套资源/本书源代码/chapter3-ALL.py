#===================================
#3.4 关于Python的函数调用
#===================================

#+++++++++++++++++++++++++++++++++++
#3.4.2 Python函数入门
#+++++++++++++++++++++++++++++++++++

#<程序：计算4+3*22>
#函数f
def  f(x, y):
    return x*y*y

#主函数部分
c=4+f(3, 2)
print (c)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#3.4.3 局部变量(Local variables)与全局变量(Global variables)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#<程序：打印局部变量a和全局变量a>
a=10		#函数外
def func():
    a=20    #函数内，局部变量的赋值，不会改变全局变量。
    print(a)  #函数内
func()
print(a)   #函数外的a



#<程序：关键字global引用全局变量>
a=10
def func():
    global  a    #宣告这个是全局变量。
    a=20
    print(a)
func()
print(a)



#<程序：a, b, c是否为局部变量？>
b,c=2,4
def g_func():
    a=b*c		#a是局部变量
    d=a		#d是局部变量，其他都是全局变量。
    print(a,d)
g_func()
print(b,c)



#练习题3.4.1

b, c=2, 4
def g_func(d):
    global a
    a=d*c
g_func(b)
print(a)



#练习题3.4.2

a=10
def func():
    x=a
    print(x)
func()
print(a)



#练习题3.4.3

a=10           
def func(b):
    c=a+b
    print(c)
func(1)



#<程序：四则运算例子>
def do_div(a, b):
    c=a//b               #a, b, c都是do_div()中的局部变量
    print (c)
    return c

def do_mul(a, b):
    global c
    c=a*b               #a, b是do_mul()的局部变量，c是全局变量
    print (c)
    return c

def do_sub(a, b):       
    c=a-b           		#a, b, c都是do_sub()中的局部变量
    c=do_mul(c, c)     
    c=do_div(c, 2)
    print (c)
    return c          

def do_add(a, b):      		#参数a和b是do_add()中的局部变量
    global c           
    c=a+b             	#全局变量c，修改了c的值
    c=do_sub(c, 1)      	#再次修改了全局变量c的值
    print (c)       
  
#所有函数外先执行:
a=3                   	#全局变量a
b=2                   	#全局变量b
c=1                   	#全局变量c
do_add(a, b)            	#全局变量a和b作为参数传递给do_add()
print (c)     				#全局变量c



#===================================
#3.5 函数调用过程的分析
#===================================

#+++++++++++++++++++++++++++++++++++
#3.5.2 函数调用时栈的管理
#+++++++++++++++++++++++++++++++++++
#<程序：因数分解>   Print all the prime factors (>=2) of x.  By Edwin Sha
import math			#为了要调用平方根函数，此函数在math包里
def factors(x):  		#找到x的因数
    y=int(math.sqrt(x))
    for i in range(2,y+1):		#检查从2 到 x的平方根是否为x的因数
        if (x %i ==0):                  #发现i是x的因数
            print("Factor:",i);
            factors(x//i)		#递归调用自己，参数变小是x//i
            break  		#跳出for循环
    else:  #假如离开循环正常，没有碰到break，就执行else内的print，x是质数
        print("Prime Factor:",x)
    print("局部变量：参数x:%d, 变量y:%d" %(x,y))
    return
factors(18)



