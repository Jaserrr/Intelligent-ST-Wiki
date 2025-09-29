#=========================================
#第四章的python程序
#=========================================

#=========================================
#4.1 简洁的Python
#=========================================

#<程序：Python数组各元素加1>
arr = [0,1,2,3,4]
for e in arr:
	tmp=e+1
	print (tmp)

#==================================================================================================

#=========================================
#4.2 Python内置数据结构
#=========================================

#+++++++++++++++++++++++++++++++++++++++++
#4.2.1 Python基本数据类型
#+++++++++++++++++++++++++++++++++++++++++

#<程序：产生10-20的随机浮点数>
import random
f = random.uniform(10,20)
print(f)



#<程序：产生10-20的随机整数>
import random
i = random.randint(10,20)
print(i)



#<程序：布尔类型例子>
b = 100<101
print (b)


#+++++++++++++++++++++++++++++++++++++++++
#4.2.2 列表（list）
#+++++++++++++++++++++++++++++++++++++++++

#<程序：序列索引>
L=[1,1.3,"2","China",["I","am","another","list"]]
print(L[0])



#<程序：序列加法>
L1= [1,1.3]
L2= ["2","China",["I","am","another","list"]]
L = L1 +L2
print(L)



#<程序：字符串专用方法调用>
L=[1,1.3,"2","China",["I","am","another","list"]]
L.append("Hello world!")
print(L)



#<程序：while循环对列表进行遍历>
L = [1,3,5,7,9,11]
mlen = len(L)
i =0
while(i<mlen):
    print(L[i]+1)
    i += 1



#<程序：for循环对列表进行遍历>
L = [1,3,5,7,9,11]
for e in L:
    e+=1
    print(e)


#+++++++++++++++++++++++++++++++++++++++++
#4.2.3 再谈字符串
#+++++++++++++++++++++++++++++++++++++++++

#第一种方式
S=input("1. Enter 1,2, , , :")#Enter: 1,2,3,4
L = S.split(sep=',')		#['1','2','3','4']
X=[]
for a in L:
    X.append(int(a))
print("Use split:", X)



#第二种方式
S=input("2. Enter 1,2, , , :")#Enter: 1,2,3,4
L = S.split(sep=',')			#['1','2','3','4']
L= [int(e) for e in L]
print("Use split and embedded for:", L)



#+++++++++++++++++++++++++++++++++++++++++
#4.2.4 字典（Dictionary）——类似数据库的结构
#+++++++++++++++++++++++++++++++++++++++++

#<程序：统计字符串中各字符出现次数>
mstr = "Hello world, I am using Python to program, it is very easy to implement."
mlist = list(mstr)
mdict = {}
for e in mlist:
    if mdict.get(e,-1)==-1:	#还没出现过
        mdict[e]=1
    else:					#出现过
        mdict[e]+=1
for key,value in mdict.items():
    print (key,value)


#练习题4.2.13

#程序1
d_info1={'XiaoMing':[ 'stu','606866'],'AZhen':[ 'TA','609980']}
print(d_info1['XiaoMing'])
print(d_info1['XiaoMing'][1])



#程序2
d_info2={'XiaoMing':{ 'role': 'stu','phone':'606866'},
'AZhen':{ 'role': 'TA','phone':'609980'}}
print(d_info2['XiaoMing'])
print(d_info2['XiaoMing']['phone'])



#练习题4.2.14

#程序1
di={'fruit':['apple','banana']}
di['fruit'].append('orange')
print(di)



#程序2
D={'name':'Python','price':40}
D['price']=70
print(D)
del D['price']
print(D)



#程序3
D={'name':'Python','price':40}
print(D.pop('price'))
print(D)



#程序4
D={'name':'Python','price':40}
D1={'author':'Dr.Li'}
D.update(D1)
print(D)


#==================================================================================================

#=========================================
#4.3 Python赋值语句
#=========================================

#+++++++++++++++++++++++++++++++++++++++++
#4.3.1 基本赋值语句
#+++++++++++++++++++++++++++++++++++++++++

#<程序：基本赋值语句>
x=1; y=2
k=x+y
print(k)


#+++++++++++++++++++++++++++++++++++++++++
#4.3.2 序列赋值
#+++++++++++++++++++++++++++++++++++++++++

#<程序：序列赋值语句>
a,b=4,5
print(a,b)
a,b=(6,7)
print(a,b)
a,b="AB"
print(a,b)
((a,b),c)=('AB','CD') #嵌套序列赋值
print(a,b,c)


#+++++++++++++++++++++++++++++++++++++++++
#4.3.3 扩展序列赋值
#+++++++++++++++++++++++++++++++++++++++++

#<程序：扩展序列赋值语句>
i,*j=range(3)
print(i,j)


#+++++++++++++++++++++++++++++++++++++++++
#4.3.4 多目标赋值
#+++++++++++++++++++++++++++++++++++++++++

#<程序：多目标赋值语句1>
i=j=k=3
print(i,j,k)
i=i+2 #改变i的值，并不会影响到j, k
print(i,j,k)



#<程序：多目标赋值语句2>
i=j=[] 	#[]表示空的列表，定义i和j都是空列表，i和j指向同一个空的列表地址
i.append(30)  #向列表i中添加一个元素30，列表j也受到影响
print(i,j)
i=[];j=[]
i.append(30)
print(i,j)


#+++++++++++++++++++++++++++++++++++++++++
#4.3.5 增强赋值语句
#+++++++++++++++++++++++++++++++++++++++++

#<程序：增强赋值语句1>
i=2
i*=3       #等价于i=i*3
print(i)



#<程序：增强赋值语句2>
L=[1,2]; L1=L; L+=[4,5]
print(L,L1)



#<程序：增强赋值语句3>
L=[1,2]; L1=L; L=L+[4,5]
print(L,L1)


#==================================================================================================


#=========================================
#4.4 Python控制结构
#=========================================

#+++++++++++++++++++++++++++++++++++++++++
#4.4.1 if语句
#+++++++++++++++++++++++++++++++++++++++++

#<程序：if语句实现百分制转等级制>
def if_test(score):
	if(score>=90):
		print('Excellent')
	elif(score>=80):
		print('Very Good')
	elif(score>=70):
		print('Good')
	elif(score>=60):
		print('Pass')
	else:
		print('Fail')
if_test(88)



#<程序：if语句举例—扩展>
def if_test(score):
    if(score>=90):
        print('Excellent',end=' ')
        if(score>=95):
            print('*')
        else:
            print(' ')
if_test(98)


#+++++++++++++++++++++++++++++++++++++++++
#4.4.2 While循环语句
#+++++++++++++++++++++++++++++++++++++++++

#<程序：while循环实现从大到小输出2*x，0<x<=10 >
x=10
while x>0:
    print(2*x,end=' ')
    x=x-1



#<程序：while循环实现从大到小输出2*x，x不是3的倍数>
x=10
while x>0:
    if x%3 == 0:
        x=x-1
        continue
    print(2*x,end=' ')
    x=x-1



#<程序：while循环实现从大到小输出2*x，x第一次为6的倍数时退出循环>
x=10
while x>0:
    if x%6 == 0:
        break
    print(2*x,end=' ')
    x=x-1



#<程序：while循环例子1改进>
i = 1
while True:
    print(i,'printing')
    if i==2:
        break
    i=i+1



#<程序：判断是否为质数>
b=7
a=b//2
while a>1:
    if b%a==0:
        print('b is not prime')
        break
    a=a-1
else:    #没有执行break，则执行else
    print('b is prime')


#+++++++++++++++++++++++++++++++++++++++++
#4.4.3 for循环语句
#+++++++++++++++++++++++++++++++++++++++++

#<程序：for的目标<target>变量>
i=1
m=[1,2,3,4,5]
def func():
    x=200
    for x in m:
        print(x);
    print(x);
func ()



#<程序：while循环改变列表2>
words=['cat','window', 'defenestrate']
for w in words[:]:
    if len(w)>6:
        words.append(w)
print(words)



#<程序：使用range遍历列表>
L=['Python','is','strong']
for i in range(len(L)):
    print(i,L[i],end=' ')


#==================================================================================================

#=========================================
#4.5 Python函数调用
#=========================================
    

#+++++++++++++++++++++++++++++++++++++++++
#4.5.1 列表做参数
#+++++++++++++++++++++++++++++++++++++++++

#<程序：列表的append方法>
def func(L1):
    L1.append(1)
L=[2]
func(L)
print(L)



#<程序：加法(+)合并列表>
def func(L1):
    x=L1+[1]
    print(x,L1)
L=[2]
func(L)
print (L)



#<程序：列表分片的例子>
def func(L1):
    x=L1[1:3]
    print(x,L1)
L=[2,'a',3,'b',4]
func(L)
print(L)


#<程序: L=X>
def F0():
     X=[9,9]   #X是局部变量，这个指针在局部栈上，但是[9,9]在外面heap上。
     L.append(8)    #L是全局变量
X=[1,2,3]
L=X
F0()
print("X=",X,"L=",L)



#<程序: L=X[:]>
def F0():
     X=[9,9]   #X 这个指针在局部栈上，但是[9,9]在外面heap上。
     L.append(8)   #L是全局变量
X=[1,2,3]; L=X[:]		#L是X的全新拷贝
F0()		#改变L不会改变X
print("X=",X,"L=",L)



#<程序: 返回(return)列表>
def F1():
     L=[3,2,1]	#L是局部变量，而[3,2,1]内容是在栈的外面，heap上
     return(L)   # 传回指针指到[3,2,1]。这个[3,2,1]内容不会随F1结束而消失。
L=F1()
print("L=",L)



#<程序: L做函数参数传递>
def F2(L):		#参数L是个指针，是存在栈上的局部变量
     L=[2,1]		#L 指向一个全新的内容，和原来的参数L完全分开了。
     return(L)
def F3(L):		#参数L是个指针，是存在栈上的局部变量
     L.append(1)    #L 指向的是原来的全局内容。会改变全局L
     L[0]=0
L= [3, 2, 1]
L=F2(L);print("L=",L)
F3(L);print("L=",L)



#<程序: list为参数的递归函数>
def recursive(L): 
    if L ==[]: return 
    L=L[0:len(L)-1]   # L指向新产生的一个list，和原来的List完全脱钩了
    print("L=",L) 
    recursive(L) 
    print("L:",L) 
    return 
X=[1,2,3] 
recursive(X) 
print("outside  recursive, X=",X)



#练习题4.5.2

def recursive_2(L): 
    if L ==[]: return 
    print("L=",L) 
    recursive_2(L[0:len(L)-1]) 
    print("L:",L) 
    return 
X=[1,2,3] 
recursive_2(X) 
print("outside  recursive_2, X=",X)


#==================================================================================================

#=========================================
#4.6 Python自定义数据结构
#=========================================

#+++++++++++++++++++++++++++++++++++++++++
#4.6.2 面向对象基本概念——类(Class)与对象(Object)
#+++++++++++++++++++++++++++++++++++++++++

#<程序：自定义学生student类，并将该类实例化>
class student:	 #学生类型：包含成员变量和成员函数
	def __init__ (self,mname,mnumber):#当新对象object产生时所自动执行的函数
		self.name = mname				#self代表这个object。名字
		self.number = mnumber			#ID号码
		self.Course_Grade = {}			#字典存课程和其分数
		self.GPA = 0					#平均分数
	def getInfo(self):
		print(self.name,self.number)
XiaoMing = student("XiaoMing","1")		
#每一个学生是一个object，参数给__init()__
A_Zhen = student("A_Zhen","2")
XiaoMing.getInfo()
A_Zhen.getInfo()


#==================================================================================================

#=========================================
#4.7 基于Python面向对象编程实现数据库功能
#=========================================

#+++++++++++++++++++++++++++++++++++++++++
#4.7.1 Python面向对象方式实现数据库的学生类
#+++++++++++++++++++++++++++++++++++++++++

#<程序：扩展后的Student类>
class student:
	def __init__ (self,mname,studentID):
		self.name = mname; self.StuID = studentID;	self.Course_Grade = {};
		self.Course_ID = []; self.GPA = 0;	self.Credit = 0
	def selectCourse(self,CourseName,CourseID):
		self.Course_Grade[CourseID]=0;			#CourseID:0 加入字典
		self.Course_ID.append(CourseID)			# CourseID 加入列表
		self.Credit = self.Credit+ CourseDict[CourseID].Credit #总学分数更新
	def getInfo(self):
		print("Name:",self.name);print("StudentID",self.StuID);print("Course:")
		for courseID,grade in self.Course_Grade.items():
			print(CourseDict[courseID].courseName,grade)
			print("GPA",self.GPA); 	print("Credit",self.Credit); print("")
	def TakeExam(self, CourseID):
		self.Course_Grade[CourseID]=random.randint(50,100)
		self.calculateGPA()
	def Grade2GPA(self,grade):
		if(grade>=90):
			return 4
		elif(grade>=80):
			return 3
		elif(grade>=70):
			return 2
		elif(grade>=60):
			return 1
		else:
			return 0
	def calculateGPA(self):
		g = 0;
		#遍历每一门所修的课程
		for courseID,grade in self.Course_Grade.items():
			g = g + self.Grade2GPA(grade)* CourseDict[courseID].Credit
		self.GPA = round(g/self.Credit,2)



#+++++++++++++++++++++++++++++++++++++++++
#4.7.2 Python面向对象方式实现数据库的课程类
#+++++++++++++++++++++++++++++++++++++++++
		
#<程序：课程类>
class Course:
	def __init__ (self,cid,mname,CourseCredit,FinalDate):
		self.courseID = cid
		self.courseName = mname
		self.studentID = []
		self.Credit = CourseCredit
		self.ExamDate = FinalDate
	def SelectThisCourse(self,stuID):	#记录谁修了这门课，在studentID列表里
		self.studentID.append(stuID)


#+++++++++++++++++++++++++++++++++++++++++
#4.7.3 Python创建数据库的学生与课程类组
#+++++++++++++++++++++++++++++++++++++++++
		
#<程序：建立课程信息>
def setupCourse (CourseDict):	#建立CourseList: list of Course objects
    CourseDict[1]=Course(1,"Introducation to Computer Science",4,1)
    CourseDict[2]=Course(2,"Advanced Mathematics",5,2)
    CourseDict[3]=Course(3,"Python",3,3)
    CourseDict[4]=Course(4,"College English",4,4)
    CourseDict[5]=Course(5,"Linear Algebra",3,5)



#<程序：建立班级信息>
def setupClass (StudentDict):    #输入一个空列表
    NameList = ["Aaron","Abraham","Andy","Benson","Bill","Brent","Chris","Daniel",
    "Edward","Evan","Francis","Howard","James","Kenneth","Norma","Ophelia","Pearl",
    "Phoenix","Prima","XiaoMing"] 
    stuid = 1
    for name in NameList:
        StudentDict [stuid]=student(name,stuid)     #student对象的字典
        stuid = stuid + 1


#+++++++++++++++++++++++++++++++++++++++++
#4.7.4 Python实例功能模拟
#+++++++++++++++++++++++++++++++++++++++++
        
#<程序：模拟选课>
def SelectCourse (StudentList, CourseList):
    for stu in StudentList:		#每一个学生修几门课
        CourseNum = random.randint(3,len(CourseList))		#修CourseNum数量的课
        #随机选，返回列表
        CourseIndex = random.sample(range(len(CourseList)), CourseNum)
        for index in CourseIndex:
            stu.selectCourse(CourseList[index].courseName,CourseList[index].Credit)
            CourseList[index].SelectThisCourse(stu.StuID)



#<程序：模拟考试>
def ExamSimulation (StudentList, CourseList):
    for day in range(1,6):	#Simulate the date
        for cour in CourseList:
            if(cour.ExamDate==day):	# Hold the exam of course on that day
                for stuID in cour.studentID:
                    for stu in StudentList:
                        if(stu.StuID == stuID):	#student stuID selected this course
                            stu.TakeExam(cour.courseID)



#<程序：主程序>
import random
CourseDict={}
StudentDict={}
setupCourse(CourseDict)
setupClass(StudentDict)
SelectCourse(list(StudentDict.values()),list(CourseDict.values()))
ExamSimulation(list(StudentDict.values()),list(CourseDict.values()))
for sid,stu in StudentDict.items():
	stu.getInfo()


#==================================================================================================

#=========================================
#4.8 有趣的小乌龟——Python之绘图
#=========================================

#+++++++++++++++++++++++++++++++++++++++++
#4.8.2 小乌龟绘制基础图形绘制
#+++++++++++++++++++++++++++++++++++++++++

#<程序：绘出三条不同的平行线>
from turtle import *
def jumpto(x,y):		#移动小乌龟不绘图
        up(); goto(x,y); down()
reset()			#置小乌龟到原点处
colorlist = ['red','green','yellow']
for i in range(3):
        jumpto(-50,50-i*50);width(5*(i+1));
        color(colorlist[i])   #设置小乌龟属性
        forward(100)	#绘图
s = Screen(); s.exitonclick()



#<程序：绘出边长为50的正方形>
from turtle import *
def jumpto(x,y):
	up(); goto(x,y); down()
reset()
jumpto(-25,-25)
k=4
for i in range(k):
	forward(50)
	left(360/k)
s = Screen(); s.exitonclick()


#解法1

#<程序：绘出半径为50的圆>
from turtle import *
import math
def jumpto(x,y):
    up(); goto(x,y); down()
def getStep(r,k):
	rad = math.radians(90*(1-2/k))
	return ((2*r)/math.tan(rad))
def drawCircle(x,y,r,k):
	S=getStep(r,k)
	speed(10); jumpto(x,y)	
	for i in range(k):
		forward(S)
		left(360/k)
reset()
drawCircle(0,0,50,20)
s = Screen(); s.exitonclick()


#解法1

#<程序：绘出半径为50的圆>
from turtle import *
circle(50)
s = Screen(); s.exitonclick()



#+++++++++++++++++++++++++++++++++++++++++
#4.8.3 小乌龟绘制迷宫
#+++++++++++++++++++++++++++++++++++++++++

#<程序：迷宫输入>
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



#<程序：迷宫中的墙与通道绘制>
from turtle import *
def jumpto(x,y):
    up(); goto(x,y); down()
def Access(x,y):
	jumpto(x,y)
	for i in range(4):
		forward(size/6); up(); forward(size/6*4); down();
		forward(size/6); right(90)
def Wall(x,y,size):
	color("red"); jumpto(x,y);
	for i in range(4):
		forward(size)
		right(90)
	goto(x+size,y-size); jumpto(x,y-size); goto(x+size,y)



#<程序：小乌龟画迷宫>
reset(); speed('fast')
size=40; startX = -len(m)/2*size; startY = len(m)/2*size
for i in range(0,len(m)):
	for j in range(0,len(m[i])):
		if m[i][j]==0:
			Access(startX+j*size, startY-i*size)
		else:
			Wall(startX+j*size, startY-i*size,size)
s = Screen(); s.exitonclick()   



#程序练习题4.8.2

#<程序：多个圆形的美丽聚合>
from turtle import *
reset()
speed('fast')
IN_TIMES = 40
TIMES = 20
for i in range(TIMES):
    right(360/TIMES)
    forward(200/TIMES)  #这一步是做什么用的？
    for j in range(IN_TIMES):
        right(360/IN_TIMES)
        forward (400/IN_TIMES)
write(" Click me to exit", font = ("Courier", 12, "bold") )
s = Screen()
s.exitonclick()
