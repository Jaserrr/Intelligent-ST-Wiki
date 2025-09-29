#=============================
#6.6 文件系统（File System）
#=============================

#+++++++++++++++++++++++++++++
#6.6.3 Python中的文件操作
#+++++++++++++++++++++++++++++

#<程序：读取文件os.py>
f = open("./Task1.txt",'r'); fls = f.readlines()
for line in fls:
    line = line.strip(); print (line)
f.close()



#<程序：读取文件os.py，计算并写回>
f = open("./Task1.txt",'r+'); fls = f.readlines()
for line in fls:
    line = line.strip(); lstr = line.split()
    if lstr[0] == '3':
        res = 0
        for e in lstr[1:]:
            res+=int(e)
f.write('\n4 '+str(res)); f.close()


#+++++++++++++++++++++++++++++
#6.6.4 学生实例4.6.3扩展
#+++++++++++++++++++++++++++++

#<程序：存储考试结果到class1.txt文件>
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

class Course:
	def __init__ (self,cid,mname,CourseCredit,FinalDate):
		self.courseID = cid
		self.courseName = mname
		self.studentID = []
		self.Credit = CourseCredit
		self.ExamDate = FinalDate
	def SelectThisCourse(self,stuID):	#记录谁修了这门课，在studentID列表里
		self.studentID.append(stuID)

def setupCourse (CourseDict):	#建立CourseList: list of Course objects
    CourseDict[1]=Course(1,"Introducation to Computer Science",4,1)
    CourseDict[2]=Course(2,"Advanced Mathematics",5,2)
    CourseDict[3]=Course(3,"Python",3,3)
    CourseDict[4]=Course(4,"College English",4,4)
    CourseDict[5]=Course(5,"Linear Algebra",3,5)

def setupClass (StudentDict):    #输入一个空列表
    NameList = ["Aaron","Abraham","Andy","Benson","Bill","Brent","Chris","Daniel",
    "Edward","Evan","Francis","Howard","James","Kenneth","Norma","Ophelia","Pearl",
    "Phoenix","Prima","XiaoMing"] 
    stuid = 1
    for name in NameList:
        StudentDict [stuid]=student(name,stuid)     #student对象的字典
        stuid = stuid + 1

def SelectCourse (StudentList, CourseList):
    for stu in StudentList:		#每一个学生修几门课
        CourseNum = random.randint(3,len(CourseList))		#修CourseNum数量的课
        #随机选，返回列表
        CourseIndex = random.sample(range(len(CourseList)), CourseNum)
        for index in CourseIndex:
            stu.selectCourse(CourseList[index].courseName,CourseList[index].Credit)
            CourseList[index].SelectThisCourse(stu.StuID)

def ExamSimulation (StudentList, CourseList):
    for day in range(1,6):	#Simulate the date
        for cour in CourseList:
            if(cour.ExamDate==day):	# Hold the exam of course on that day
                for stuID in cour.studentID:
                    for stu in StudentList:
                        if(stu.StuID == stuID):	#student stuID selected this course
                            stu.TakeExam(cour.courseID)

import random
CourseDict={}
StudentDict={}
setupCourse(CourseDict)
setupClass(StudentDict)
SelectCourse(list(StudentDict.values()),list(CourseDict.values()))
ExamSimulation(list(StudentDict.values()),list(CourseDict.values()))

SaveToFile = ["ID"," ","Name"," ","Credit"," ","GPA","\n"]
for stu in StudentDict.values():
                SaveToFile.append(str(stu.StuID))
                SaveToFile.append(" ")
                SaveToFile.append(str(stu.name))
                SaveToFile.append(" ")
                SaveToFile.append(str(stu.Credit))
                SaveToFile.append(" ")
                SaveToFile.append(str(stu.GPA))
                SaveToFile.append("\n")
f = open("class1.txt","w")
f.writelines(SaveToFile)
f.close()




#<程序：查询文件class1.txt中满足某条件的学生信息>
def select(path,col,op,val):
	f = open(path,"r")
	colNum = 0
	if col == "ID": colNum = 0
	elif col == "Name": colNum = 1
	elif col == "Credit": colNum = 2
	elif col == "GPA": colNum = 3
	f.readline()
	Info = f.readlines()
	res = []
	for e in Info:
		e = e.strip()
		eList = e.split()
		if colNum != 1:
			exp = eList[colNum] + op + val
		else:
			exp = "'" + eList[colNum] + "'" + op + "'" + val + "'"
		if eval(exp):
			res.append(e)
	f.close()
	return res
for e in select("class1.txt","Credit",">=","15"):
    print (e)



#<程序：对文件class1.txt中学生进行排序>
def sort(path,col,direct):	
#direct表示排序方向，">"为从大到小排序，"<"相反。
	colNum = 0
	if col == "Credit": colNum = 2
	elif col == "GPA": colNum = 3
	ifrev = False
	if direct == ">":ifrev = True
	f = open(path,"r")
	f.readline()
	Info = f.readlines()
	res = []
	for e in Info:
		eList = e.split()
		res.append(eList)
	res =sorted(res, key=lambda res: res[colNum],reverse=ifrev) 
#第三个参数为排序方向
	f.close()
	return res
L = [('b',2),('a',1),('c',3),('d',4)]
print (sorted(L, key=lambda x:x[1]))
