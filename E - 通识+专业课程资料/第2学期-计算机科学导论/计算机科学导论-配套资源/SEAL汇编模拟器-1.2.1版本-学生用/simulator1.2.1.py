import turtle
import copy
import sys
import os

op = ["load", "move", "add", "sub", "shiftl", "shiftr", "store", "slt", "sle", "beqz", "goto", "and", "or", "xor", "call", "ret", "clz", "push",
      "pop", "_pr","div","mul","_data","mov"]  # 指令序列
Memory_size=10000
Reg_size=16
Ins_operator = []  # 操作码，即上述列表op中的某个值，如move
Ins_operand = []  # 操作数，存放指令对应的操作数
Ins_op = [] #保存当前读到的完整指令，'#'后面的注释除外，它包含Ins_operator和Ins_operand两个部分，即完整指令
Reg = [0] * Reg_size # 寄存器    # 等价于[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Reg1 = [0] * Reg_size  # 寄存器副本  等价于[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Memory = [0] * Memory_size  # data  内存解释同上，均为list类型
label = {}  # 用来记录label的标签，字典类型
line_count = -1  # 记录文件读取的行数
pc = 0  # pc寄存器，指令寄存器
sp = Memory_size  # sp寄存器，堆栈寄存器，stack pointer
list_flag = []  # 标记指令的模式，每条指令都对应一个list_flag位，可取的值有-1，0,1
list_pc = []  # 用来记录pc值


def removeBom(file):
    '''移除UTF-8文件的BOM字节'''
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s == BOM else False
    f = open(file, 'rb')  # 以二进制读模式打开
    if existBom(f.read(3)):
        fbody = f.read()
        # f.close()
        with open(file, 'wb') as f:
            f.write(fbody)


def read(filename):  # 读文件
    removeBom(filename)
    file = open(filename, 'r', encoding='utf-8',errors="ignore")
    for line in file:
        global line_count
        # line = line.strip('\n')
        line = line.strip()   # 删除每行前后的空白字符
        if len(line) != 0:   # 所有空白行都排除，不做任何操作
            if line[0] != '#' and line != "_pause":   #说明不是注释，同时也不是调试状态，忽略它们
                line_count = line_count + 1
                #flag, op, oper = judge_Ins(line)
                try:
                    #print("aaa")
                    flag, op, oper = judge_Ins(line)
                except:
                    raise IndexError(line,"Err:寄存器数目超过",len(Reg),"个")
                else:
                    if flag == -1:  # 返回值flag==-1表示指令格式不正确，此时应该输出错误，并结束执行
                        raise BaseException("Err:格式错误", line)   # 2018.4.24修改，将错误自定义抛出
                    elif flag == 1:
                        Ins_operator.append(op)
                        Ins_operand.append(oper)
                        line_str=""
                        for i in line:
                            if i=='#':
                                break
                            line_str+=i
                        Ins_op.append(line_str)
    file.close()  #关闭文件


def debug_read(filename):  # 读文件
    file = open(filename, 'r', encoding='utf-8',errors="ignore")
    for line in file:
        global line_count
        # line = line.strip('\n')
        line = line.strip()
        if len(line) != 0:
            if line[0] != '#':    # 忽略注释行
                line_count = line_count + 1
                if line == '_pause':
                    Ins_operator.append(line)
                    Ins_operand.append(" ")  #起到占位的作用，这样会使得每条指令操作op的位置和操作的位置一样
                    list_flag.append(-1)
                    Ins_op.append(line)
                else:
                    try:
                        flag, op, oper = judge_Ins(line)
                    except:
                        raise IndexError(line, "Err:寄存器数目超过", len(Reg), "个")
                    else:
                        if flag == -1:    # 返回值flag==-1表示指令格式不正确，此时应该输出错误，并结束执行
                            raise BaseException("Err:格式错误", line)  # 2018.4.24修改，将错误自定义抛出
                        elif flag == 1:
                            Ins_operator.append(op)
                            Ins_operand.append(oper)
                            line_str = ""
                            for i in line:
                                if i == '#':
                                    break
                                line_str += i
                            Ins_op.append(line_str)
    file.close()  # 关闭文件

def hex16(x):
    return{
        '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,
        '6':6,'7':7,'8':8,'9':9,'a':10,'b':11,
        'c':12,'d':13,'e':14,'f':15,'A':10,'B':11,
        'C':12,'D':13,'E':14,'F':15,
    }.get(x)

def to10(str, to):
    sum = 0
    flag=0
    if str[0]=='-':
        flag=1
    str=str.strip('-')
    if(to==16):
        for i in range(len(str)):
            sum += int(hex16(str[len(str) - 1 - i])) * (to ** i)
    else:
        for i in range(len(str)):
            sum += int(str[len(str) - 1 - i]) * (to ** i)
    if flag==1:
        sum=-sum
    return sum

def cover(str):
    str = str.strip()
    if (str[-1] == 'H' or str[-1] == 'h'):
        str = str.strip('H')
        str = str.strip('h')
        return to10(str, 16)
    elif (str[-1] == 'B' or str[-1] == 'b'):
        str = str.strip('B')
        str = str.strip('b')
        return to10(str, 2)
    elif (str[-1] == 'O' or str[-1] == 'o'):
        str = str.strip('O')
        str = str.strip('o')
        return to10(str, 8)
    else:
        return int(str)

def judge_Ins(op_Ins):  # 判断指令格式是否正确
    list_operand = []  # 操作数
    global label, line_count
    Str_Ins = ""
    for i in range(len(op_Ins)):  # 判断操作码是否正确
        if op_Ins[i] == " " and op_Ins[0] != 'L':  # 判断操作码是否存在或者格式是否正确，判断空格主要是因为每个操作之后都会跟一个空格
            flag = 0
            for j in op:   # op中存放了所有本实验允许使用的操作符
                if Str_Ins == j:
                    flag = 1
                    break
            if flag == 0:   # 如果标志位为0，说明该条指令在本实验中不支持
                return -1, 0, 0
            break
        Str_Ins = Str_Ins + op_Ins[i]  #  获取到op_Ins中的指令名称，如move
    Str_Ins = Str_Ins.strip()
    op_num = i
    for i in range(op_num, len(op_Ins)):   # 获取到操作数的最后位置，碰到#或者超过这一行最大长度时结束
        if op_Ins[i] == '#':
            end_num = i
            break
        else:
            end_num = len(op_Ins)
    if Str_Ins[0] == "L":   # 判断操作符是否以L开头
        list_flag.append(-1)
        str_op = ""
        for i in range(len(Str_Ins)):
            if Str_Ins[i] == '#':
                break
            str_op += Str_Ins[i]
        str_op = str_op.strip()
        if str_op[len(str_op) - 1] == ':':
            str_op = str_op.replace(':', '')
            list_operand.append("")
            label[str_op] = line_count
            return 1, str_op, ""
        else:
            return -1, 0, 0
    elif Str_Ins == "load":  # load
        str_op = ""   # 存放操作数
        for i in range(op_num, end_num):
            if op_Ins[i] == ",":
                for j in range(i + 1, end_num):
                    if op_Ins[j] != " ":
                        kuohao = j
                        break
            str_op += op_Ins[i]   # 将所有的操作数存入到str_op中，如load R1,(1000)，此时R1,(1000)被存入到st_op中
        str_op = str_op.strip()  # 去掉两边空格
        if op_Ins[kuohao] == '(':
            # print(str_op)
            str_op = ""
            for i in range(op_num, end_num):
                if op_Ins[i] != " ":
                    if op_Ins[i] == ",":   #插入第一个寄存器的数据
                        if str_op.startswith('R'):  
                            if int(str_op[1:]) >= len(Reg):  
                                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
                            else:
                                list_operand.append(str_op)
                                str_op = ""
                                continue
                        else:
                            list_operand.append(str_op)
                            str_op = ""
                            continue
                    if op_Ins[i] == "(":
                        continue
                    if op_Ins[i] == ")":
                        list_operand.append(str_op)
                        # if op_Ins[i + 1] != "":   #这段代码在访问时存在数组下标越界，早期版本为什么在这里实现这样的逻辑？
                        #     return -1, 0, 0
                        continue
                    str_op += op_Ins[i]
            if len(list_operand) == 2:
                list_operand[1] = cover(list_operand[1])
                list_flag.append(0)
            else:
                return -1, 0, 0
        else:
            str_op = ""
            for i in range(op_num, end_num):
                if op_Ins[i] != " ":
                    if op_Ins[i] == ",": #插入第一个寄存器参数
                        if str_op.startswith('R'):  
                            if int(str_op[1:]) >= len(Reg):  
                                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
                            else:
                                list_operand.append(str_op)
                                str_op = ""
                                continue
                        else:
                            list_operand.append(str_op)
                            str_op = ""
                            continue
                    if op_Ins[i] == "(":   # 插入数字
                        list_operand.append(str_op)
                        str_op = ""
                        continue
                    if op_Ins[i] == ")":  # 插入第二个寄存器参数
                        if str_op.startswith('R'):  
                            if int(str_op[1:]) >= len(Reg):  
                                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
                            else:
                                list_operand.append(str_op)
                                str_op = ""
                                continue
                        else:
                            list_operand.append(str_op)
                            str_op = ""
                            continue
                    str_op += op_Ins[i]
            if len(list_operand) == 3:  # 判断格式
                list_operand[1] = cover(list_operand[1])
                list_flag.append(1)
            else:
                return -1, 0, 0
    elif Str_Ins == "move" or Str_Ins == "mov":  # move
        str_op = ""
        for i in range(op_num, end_num):   # 读取操作数
            if op_Ins[i] != " ":
                if op_Ins[i] == ",":
                    if str_op.startswith('R'):    #
                        if int(str_op[1:]) >= len(Reg):  #
                            Reg(int(str_op[1:]))   # 寄存器数目超过指定个数会产生IndexError
                        else:
                            list_operand.append(str_op)    #将操作数插入到操作数表中
                            str_op = ""    # 接着清空str_op，用于接受另外一个操作数
                            continue
                    else:
                        list_operand.append(str_op)  # 将操作数插入到操作数表中
                        str_op = ""  # 接着清空str_op，用于接受另外一个操作数
                        continue
                str_op += op_Ins[i]
        if str_op.startswith('R'):  
            if int(str_op[1:]) >= len(Reg):  
                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
        list_operand.append(str_op)   #将操作数str_op插入到操作数列表中
        if len(list_operand) != 2:   # 说明命令格式不正确，操作数个数应该为2
            return -1, 0, 0
        if list_operand[1][0] == 'R' or list_operand[1][0] == 's':   # 如果操作数被存在寄存器或者sp寄存器中
            list_flag.append(1)  # move_r
        else:
            list_operand[1]=cover(list_operand[1])
            list_flag.append(0)  # move_c
    elif Str_Ins == "add" or Str_Ins == "sub" or Str_Ins == "shiftl" or Str_Ins == "shiftr" or Str_Ins == "slt" or Str_Ins == "sle" or Str_Ins == "or" or Str_Ins == "and" or Str_Ins == "xor" or Str_Ins == "div" or Str_Ins == "mul":
        str_op = ""
        for i in range(op_num, end_num):
            if op_Ins[i] != " ":
                if op_Ins[i] == ",":
                    if str_op.startswith('R'):    #
                        if int(str_op[1:]) >= len(Reg):  #
                            Reg(int(str_op[1:]))   # 寄存器数目超过指定个数会产生IndexError
                        else:
                            list_operand.append(str_op)
                            str_op = ""
                            continue
                    else:
                        list_operand.append(str_op)
                        str_op = ""
                        continue
                str_op += op_Ins[i]
        if str_op.startswith('R'):  
            if int(str_op[1:]) >= len(Reg):  
                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
        list_operand.append(str_op)
        if len(list_operand) != 3:
            return -1, 0, 0
        if list_operand[2][0] == 'R' or list_operand[2][0] == 's':
            list_flag.append(1)  # 当最后一位操作数为寄存器时
        else:
            list_operand[2] = cover(list_operand[2])
            list_flag.append(0)  # z最后一位操作数为常数
    elif Str_Ins == "store":  # store_r
        flag1 = 0
        flag2 = 0
        str_op = ""
        for i in range(op_num, end_num):
            str_op += op_Ins[i]
        str_op = str_op.strip()
        if str_op[0][0] != '(':
            str_op = ""
            for i in range(op_num, end_num):
                if op_Ins[i] != " ":
                    if op_Ins[i] == "(":   #插入寄存器前面的数字
                        list_operand.append(str_op)
                        str_op = ""
                        continue
                    if op_Ins[i] == ")": # 插入第一个寄存器
                        if str_op.startswith('R'):  
                            if int(str_op[1:]) >= len(Reg):  
                                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
                            else:
                                list_operand.append(str_op)
                                str_op = ""
                                continue
                        else:
                            list_operand.append(str_op)
                            str_op = ""
                            continue
                    if op_Ins[i] == ",":
                        continue
                    str_op += op_Ins[i]
            if str_op.startswith('R'):  
                if int(str_op[1:]) >= len(Reg):  
                    Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
            list_operand.append(str_op)
            if len(list_operand) == 3:
                list_operand[0] = cover(list_operand[0])
                list_flag.append(1)
            else:
                return -1, 0, 0
        else:
            str_op = ""
            for i in range(op_num, end_num):
                if op_Ins[i] != " ":
                    if op_Ins[i] == "(" or op_Ins[i] == ',':
                        str_op = ""
                        continue
                    if op_Ins[i] == ")":
                        list_operand.append(str_op)
                        str_op = ""
                        continue
                    str_op += op_Ins[i]
            if str_op.startswith('R'):  
                if int(str_op[1:]) >= len(Reg):  
                    Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
            list_operand.append(str_op)
            if len(list_operand) == 2:
                list_flag.append(0)
                list_operand[0] = cover(list_operand[0])
            else:
                return -1, 0, 0
    elif Str_Ins == "beqz":
        str_op = ""
        for i in range(op_num, end_num):
            if op_Ins[i] != " ":
                if op_Ins[i] == ",":   #插入寄存器的值
                    if str_op.startswith('R'):  
                        if int(str_op[1:]) >= len(Reg):  
                            Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
                        else:
                            list_operand.append(str_op)
                            str_op = ""
                            continue
                    else:
                        list_operand.append(str_op)
                        str_op = ""
                        continue
                str_op += op_Ins[i]
        list_operand.append(str_op)   #插入beqz指令中的Label值
        list_flag.append(-1)
        if len(list_operand) != 2:
            return -1, 0, 0
    elif Str_Ins == "goto":
        str_op = ""
        for i in range(op_num, end_num):
            if op_Ins[i] != " ":
                str_op += op_Ins[i]
        list_operand.append(str_op)
        list_flag.append(-1)
        if len(list_operand) != 1:
            return -1, 0, 0
    elif Str_Ins == "call":
        str_op = ""
        for i in range(op_num, end_num):
            if op_Ins[i] != " ":
                str_op += op_Ins[i]
        list_operand.append(str_op)
        list_flag.append(-1)
        if len(list_operand) != 1:
            return -1, 0, 0
    elif Str_Ins == "ret":
        str_op = ""
        for i in range(op_num +1, end_num):
            # if op_Ins[op_num] != " ":
            #    return  -1,0,0
            str_op += op_Ins[i]
        str_op=str_op.strip()
        list_flag.append(-1)
        list_operand.append("ret")
        if len(str_op) != 0:
            return -1, 0, 0
    elif Str_Ins == "clz":
        str_op = ""
        for i in range(op_num, end_num):
            if op_Ins[i] != " ":
                if op_Ins[i] == ",":   #插入第一个寄存器
                    if str_op.startswith('R'):  
                        if int(str_op[1:]) >= len(Reg):  
                            Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
                        else:
                            list_operand.append(str_op)
                            str_op = ""
                            continue
                    else:
                        list_operand.append(str_op)
                        str_op = ""
                        continue
                str_op += op_Ins[i]
        if str_op.startswith('R'):  
            if int(str_op[1:]) >= len(Reg):  
                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
        list_operand.append(str_op)   #插入第二个寄存器
        list_flag.append(-1)
        if len(list_operand) != 2:
            return -1, 0, 0
    elif Str_Ins == "push":
        str_op = ""
        for i in range(op_num, end_num):
            if op_Ins[i] != " ":
                str_op += op_Ins[i]
        if str_op.startswith('R'):  
            if int(str_op[1:]) >= len(Reg):  
                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
        list_operand.append(str_op)
        list_flag.append(-1)
        if len(list_operand) != 1:
            return -1, 0, 0
    elif Str_Ins == "pop":
        str_op = ""
        for i in range(op_num, end_num):
            if op_Ins[i] != " ":
                str_op += op_Ins[i]
        if str_op.startswith('R'):  
            if int(str_op[1:]) >= len(Reg):  
                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
        list_operand.append(str_op)
        list_flag.append(-1)
        if len(list_operand) != 1:
            return -1, 0, 0
    elif Str_Ins == "_pr":
        str_op = ""
        for i in range(op_num, end_num):
            if op_Ins[i] != " ":
                if op_Ins[i] == ",":  #除最后一个值以外，所有的值全部在此处插入
                    if str_op.startswith('R'):  
                        if int(str_op[1:]) >= len(Reg):  
                            Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
                        else:
                            list_operand.append(str_op)
                            str_op = ""
                            continue
                    else:
                        list_operand.append(str_op)
                        str_op = ""
                        continue
                str_op += op_Ins[i]
        if str_op.startswith('R'):  
            if int(str_op[1:]) >= len(Reg):  
                Reg(int(str_op[1:]))  # 寄存器数目超过指定个数会产生IndexError
        list_operand.append(str_op)   #插入最后一个寄存器的值
        list_flag.append(-1)
    elif Str_Ins=="_data":
        global Memory_size
        str_op=""
        list_tmp=[]
        for i in range(op_num,end_num):
            if op_Ins[i]!=" ":
                if op_Ins[i]==",":
                    if int(cover(str_op))>Memory_size or int(cover(str_op))<0:
                        print("起始地址越界")
                        return -1,0,0
                    else:
                        list_operand.append(cover(str_op))
                        str_op=""
                        continue
                if op_Ins[i]=="[":
                    tmp_i=i
                    while op_Ins[i]!=']':
                        i+=1
                    str_op=op_Ins[tmp_i+1:i]
                    list_operand.append(list(str_op.strip(',').split(',')))
                    break
                str_op+=op_Ins[i]
        list_flag.append(-1)
        for i in range(len(list_operand[1])):
            list_operand[1][i] = cover(list_operand[1][i])
        if len(list_operand)!=2:
            return -1,0,0
    else:
        return -1, 0, 0
    return 1, Str_Ins, list_operand   # 返回值1表示指令格式正确，返回值Str_Ins存储当前指令如move、add等，list_operand存储当前指令的操作数


def run():  # 指令执行
    global pc,Reg,sp
    i = 0
    while i < len(Ins_operator):   #遍历Ins_operator，将取出其中的操作码，如move、add等
        Reg1 = Reg
        op = Ins_operator[i]
        if op[0] == "L":
            i += 1
            continue
        elif op == "load":
            if list_flag[i] == 0:
                load_m(Ins_operand[i])
            else:
                load_r(Ins_operand[i])
        elif op == "move" or op == "mov":
            if list_flag[i] == 0:
                move_c(Ins_operand[i])
            else:
                move_r(Ins_operand[i])
        elif op == "add":
            if list_flag[i] == 0:
                add_c(Ins_operand[i])
            else:
                add_r(Ins_operand[i])
        elif op == "sub":
            if list_flag[i] == 0:
                sub_c(Ins_operand[i])
            else:
                sub_r(Ins_operand[i])
        elif op == "shiftl":
            if list_flag[i] == 0:
                shiftl_c(Ins_operand[i])
            else:
                shiftl_r(Ins_operand[i])
        elif op == "shiftr":
            if list_flag[i] == 0:
                shiftr_c(Ins_operand[i])
            else:
                shiftr_r(Ins_operand[i])
        elif op == "store":
            if list_flag[i] == 0:
                store_m(Ins_operand[i])
            else:
                store_r(Ins_operand[i])
        elif op == "slt":
            if list_flag[i] == 0:
                slt_c(Ins_operand[i])
            else:
                slt_r(Ins_operand[i])
        elif op == "sle":
            if list_flag[i] == 0:
                sle_c(Ins_operand[i])
            else:
                sle_r(Ins_operand[i])
        elif op == "beqz":
            tmp = beqz(Ins_operand[i])
            if tmp != -1:
                i = tmp
                continue
        elif op == "goto":
            i = goto(Ins_operand[i])
        elif op == "and":
            if list_flag[i] == 0:
                and_c(Ins_operand[i])
            else:
                and_r(Ins_operand[i])
        elif op == "or":
            if list_flag[i] == 0:
                or_c(Ins_operand[i])
            else:
                or_r(Ins_operand[i])
        elif op == "xor":
            if list_flag[i] == 0:
                xor_c(Ins_operand[i])
            else:
                xor_r(Ins_operand[i])
        elif op == "call":
            tmp = i
            i = call(Ins_operand[i])
            if i == -1:
                print("Err:第", tmp + 1, "行,没有设置栈空间")
                return
        elif op == "ret":
            i = ret()
        elif op == "clz":
            clz(Ins_operand[i])
        elif op == "push":
            # print("sp的值为:", sp)
            if push(Ins_operand[i]) == -1:
                print("Err:第", i + 1, "行,没有设置栈空间")
                return -1
        elif op == "pop":
            if pop(Ins_operand[i]) == -1:
                print("Err:第", i + 1, "行,栈为空")
                return -1
        elif op == '_pr':
            _pr(Ins_operand[i])
        elif op=='div':
            if list_flag[i] == 0:
                div_c(Ins_operand[i])
            else:
                div_r(Ins_operand[i])
        elif op=="mul":
            if list_flag[i] == 0:
                mul_c(Ins_operand[i])
            else:
                mul_r(Ins_operand[i])
        elif op=="_data":
            _data(Ins_operand[i])
        else:
            return -1
        for num in range(Reg_size):   # 读取并查看16个寄存器的值
            if Reg[num] > (2**63-1) or Reg[num] < (-(2**63)):
                print("Err:溢出，超出位数限制 第", pc + 1, "行 ", Ins_op[pc])
                return -1
        if sp > 10000:
            print("Err:内存溢出 第", pc + 1, "行 ", Ins_op[pc])
            return -1
        i += 1
        pc = i
    print("完成！！！")
    return 1

def debug_run(i):  # 指令逐行去调试
    global pc, Reg1, Reg
    Reg1 = copy.deepcopy(Reg)
    if i < len(Ins_operator):
        op = Ins_operator[i]
        if op[0] == "L":
            i = i
        elif op == "load":
            if list_flag[i] == 0:
                load_m(Ins_operand[i])
            else:
                load_r(Ins_operand[i])
        elif op == "move" or op == "mov":
            if list_flag[i] == 0:
                move_c(Ins_operand[i])
            else:
                move_r(Ins_operand[i])
        elif op == "add":
            if list_flag[i] == 0:
                add_c(Ins_operand[i])
            else:
                add_r(Ins_operand[i])
        elif op == "sub":
            if list_flag[i] == 0:
                sub_c(Ins_operand[i])
            else:
                sub_r(Ins_operand[i])
        elif op == "shiftl":
            if list_flag[i] == 0:
                shiftl_c(Ins_operand[i])
            else:
                shiftl_r(Ins_operand[i])
        elif op == "shiftr":
            if list_flag[i] == 0:
                shiftr_c(Ins_operand[i])
            else:
                shiftr_r(Ins_operand[i])
        elif op == "store":
            if list_flag[i] == 0:
                store_m(Ins_operand[i])
            else:
                store_r(Ins_operand[i])
        elif op == "slt":
            if list_flag[i] == 0:
                slt_c(Ins_operand[i])
            else:
                slt_r(Ins_operand[i])
        elif op == "sle":
            if list_flag[i] == 0:
                sle_c(Ins_operand[i])
            else:
                sle_r(Ins_operand[i])
        elif op == "beqz":
            tmp = beqz(Ins_operand[i])
            if tmp != -1:
                i = tmp
                # continue
        elif op == "goto":
            i = goto(Ins_operand[i])
        elif op == "and":
            if list_flag[i] == 0:
                and_c(Ins_operand[i])
            else:
                and_r(Ins_operand[i])
        elif op == "or":
            if list_flag[i] == 0:
                or_c(Ins_operand[i])
            else:
                or_r(Ins_operand[i])
        elif op == "xor":
            if list_flag[i] == 0:
                xor_c(Ins_operand[i])
            else:
                xor_r(Ins_operand[i])
        elif op == "call":
            tmp = i
            i = call(Ins_operand[i])
            if i == -1:
                print("Err:第", tmp + 1, "行,没有设置栈空间")
                return -1
        elif op == "ret":
            i = ret()
        elif op == "clz":
            clz(Ins_operand[i])
        elif op == "push":
            if push(Ins_operand[i]) == -1:
                print("Err:第", i + 1, "行,没有设置栈空间")
                return -1
        elif op == "pop":
            if pop(Ins_operand[i]) == -1:
                print("Err:第", i + 1, "行,栈为空")
                return -1
        elif op == '_pause':
            i = i
        elif op == '_pr':
            _pr(Ins_operand[i])
        elif op == 'div':
            if list_flag[i] == 0:
                div_c(Ins_operand[i])
            else:
                div_r(Ins_operand[i])
        elif op == "mul":
            if list_flag[i] == 0:
                mul_c(Ins_operand[i])
            else:
                mul_r(Ins_operand[i])
        elif op=="_data":
            _data(Ins_operand[i])
        else:
            return -1
        for num in range(Reg_size):   # 读取并查看16个寄存器的值
            if Reg[num] > (2**63-1) or Reg[num] < (-(2**63)):
                print("Err:溢出，超出位数限制 第", pc + 1, "行 ", Ins_op[pc])
                return -1
        if sp > 10000:
            print("Err:内存溢出 第", pc + 1, "行 ", Ins_op[pc])
            return -1
        i += 1
        pc = i
        return 1
    else:
        return 0
       # win32api.PostQuitMessage()
    return 1


def debug2_run():  # 在断点处停止
    i = 0
    global pc, Reg1, Reg
    window = turtle.Screen()  # 开启小乌龟
    while i < len(Ins_operator):
        op = Ins_operator[i]
        if op != "_pause":
            Reg1 = copy.deepcopy(Reg)
        if op[0] == "L":
            i += 1
            continue
        elif op == "load":
            if list_flag[i] == 0:
                load_m(Ins_operand[i])
            else:
                load_r(Ins_operand[i])
        elif op == "move" or op == "mov":
            if list_flag[i] == 0:
                move_c(Ins_operand[i])
            else:
                move_r(Ins_operand[i])
        elif op == "add":
            if list_flag[i] == 0:
                add_c(Ins_operand[i])
            else:
                add_r(Ins_operand[i])
        elif op == "sub":
            if list_flag[i] == 0:
                sub_c(Ins_operand[i])
            else:
                sub_r(Ins_operand[i])
        elif op == "shiftl":
            if list_flag[i] == 0:
                shiftl_c(Ins_operand[i])
            else:
                shiftl_r(Ins_operand[i])
        elif op == "shiftr":
            if list_flag[i] == 0:
                shiftr_c(Ins_operand[i])
            else:
                shiftr_r(Ins_operand[i])
        elif op == "store":
            if list_flag[i] == 0:
                store_m(Ins_operand[i])
            else:
                store_r(Ins_operand[i])
        elif op == "slt":
            if list_flag[i] == 0:
                slt_c(Ins_operand[i])
            else:
                slt_r(Ins_operand[i])
        elif op == "sle":
            if list_flag[i] == 0:
                sle_c(Ins_operand[i])
            else:
                sle_r(Ins_operand[i])
        elif op == "beqz":
            tmp = beqz(Ins_operand[i])
            if tmp != -1:
                i = tmp
                continue
        elif op == "goto":
            i = goto(Ins_operand[i])
        elif op == "and":
            if list_flag[i] == 0:
                and_c(Ins_operand[i])
            else:
                and_r(Ins_operand[i])
        elif op == "or":
            if list_flag[i] == 0:
                or_c(Ins_operand[i])
            else:
                or_r(Ins_operand[i])
        elif op == "xor":
            if list_flag[i] == 0:
                xor_c(Ins_operand[i])
            else:
                xor_r(Ins_operand[i])
        elif op == "call":
            tmp = i
            i = call(Ins_operand[i])
            if i == -1:
                print("Err:第", tmp + 1, "行,没有设置栈空间")
                return 0
        elif op == "ret":
            i = ret()
        elif op == "clz":
            clz(Ins_operand[i])
        elif op == "push":
            if push(Ins_operand[i]) == -1:
                print("Err:第", i + 1, "行,没有设置栈空间")
                return 0
        elif op == "pop":
            if pop(Ins_operand[i]) == -1:
                print("Err:第", i + 1, "行,栈为空")
                return 0
        elif op == '_pause':
            #window = turtle.Screen()  # 开启小乌龟
            P_debug()
            p = input("选择继续的方式（输入“1”进入逐行调试模式/按回车继续断点调试/“exit”退出调试）：")
            p.strip()
            if p.lower() == 'exit':
                print("调试退出！！！(若调试界面没有关闭，请点击界面上任意空白位置)")
                window.exitonclick()
                turtle.TurtleScreen._RUNNING = True
                return 0
            elif p=='1':
                while 1:
                    tmp=debug_run(pc)
                    P_debug()
                    pr = input("选择继续的方式（按回车继续逐行调试/“exit”返回断点调试）：")
                    if tmp==0 or pr.lower() == "exit":   # 修改输入指令，使得用户的输入忽略大小写
                        break              
                i = pc
                continue
        elif op == '_pr':
            _pr(Ins_operand[i])
        elif op == 'div':
            if list_flag[i] == 0:
                div_c(Ins_operand[i])
            else:
                div_r(Ins_operand[i])
        elif op == "mul":
            if list_flag[i] == 0:
                mul_c(Ins_operand[i])
            else:
                mul_r(Ins_operand[i])
        elif op=="_data":
            _data(Ins_operand[i])
        else:
            return 0
        for num in range(Reg_size):   # 读取并查看16个寄存器的值
            if Reg[num] > (2**63-1) or Reg[num] < (-(2**63)):
                print("Err:溢出，超出位数限制 第", pc + 1, "行 ", Ins_op[pc])
                return -1
        if sp > 10000:
            print("Err:内存溢出 第", pc + 1, "行 ", Ins_op[pc])
            return -1
        i += 1
        pc = i
    #win32api.PostQuitMessage()
    print("完成！！！(若调试界面没有关闭，请点击界面上任意空白位置)")
    window.exitonclick()
    turtle.TurtleScreen._RUNNING = True
    return 1


def com(x):
    if x > (1 << 64):
        return -1
    return 1


def R_SP(str):  # 判断寄存器的类型
    global sp, pc
    if str == "sp":
        return sp
    elif str == "pc":
        return pc
    elif str[0] == '(':
        str = str.strip('(')
        str = str.strip(')')
        return Memory[int(str)]
    elif str[0] == "'" or str[0] == '"':
        str = str.strip("'")
        str = str.strip('"')
        return str
    else:
        return Reg[int(str.strip('R'))]


def _pr_R_SP(str):  # 判断寄存器的类型
    global sp, pc
    if str == "sp":
        return sp,1
    elif str == "pc":
        return pc,1
    elif str[0] == "'" or str[0] == '"':
        str = str.strip("'")
        str = str.strip('"')
        return str,1
    elif str[0]=="R" or str[0]=="r":
        return Reg[int(str.strip('R'))],1
    elif str[-1]==")":
        op_str=""
        ins=[]
        t=2
        for i in range(0,len(str)):
            if str[i]== "(":
                if op_str=="":
                    op_str="0"
                ins.append(int(cover(op_str)))
                op_str=""
                continue
            elif str[i]==")":
                if(op_str[0]=='R'or op_str[0]=='r'):
                    ins.append(int(op_str.strip('R').strip('r')))
                    t=6
                elif(op_str[0]=='s'):
                    t=7
                else:
                    ins.append(int(cover(op_str)))
                op_str=""
                continue
            op_str+=str[i]
        return ins,t
    else:
        t=3
        op_str = ""
        ins = []
        for i in range(0, len(str)):
            if str[i] == "(":
                if op_str == "":
                    op_str = "0"
                ins.append(int(cover(op_str)))
                op_str = ""
                continue
            elif str[i] == ")":
                ins.append(int(cover(op_str)))
                op_str = ""
                continue
            elif str[i]=="%":
                op_str=""
                continue
            elif(str[i]=='R'or str[i]=='r'):
                t=4
                op_str=""
                continue
            elif(str[i]=='s' or str[i]=='p'):
                t=5
                op_str="0"
                continue
            op_str += str[i]
        ins.append(int(cover(op_str)))
        return ins, t


def strip_R(str):
    str = str.strip('R')
    str = str.strip('r')
    return str


############指令函数###################

def load_m(op_str):  # load_m
    global sp
    op_mem = int(op_str[1])
    if op_str[0] == "sp":
        sp = Memory[op_mem]
    else:
        op_res = int(strip_R(op_str[0]))
        Reg[op_res] = Memory[op_mem]
    return


def load_r(op_str):  # load_r
    global sp
    op_mem = int(op_str[1])
    op_res2= R_SP(op_str[2])
    if op_str[0] == "sp":
        sp = Memory[op_mem + op_res2]
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = Memory[op_mem + op_res2]
    return


def move_c(op_str): # move指令的第二个操作数为常数
    global sp
    op_con = int(op_str[1])    #取出第二个操作数，将其类型从字符型转到int型
    # if op_con > (1 << 64):
    #     print("大于64位")    # 删除该部分代码，没有作用，因为在else中已经将op_con的值返回到对应的寄存器中，在run函数中有处理这种情况，并返回错误
    if op_str[0] == "sp":
        sp = op_con
    else:
        op_res = int(strip_R(op_str[0]))
        Reg[op_res] = op_con
    return


def move_r(op_str): # move指令的第二个操作存放在寄存器中
    global sp
    op_res2= R_SP(op_str[1])
    if op_str[0] == "sp":
        sp = op_res2
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2
    return


def add_c(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_con = int(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 + op_con
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 + op_con
    return


def add_r(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_res3= R_SP(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 + op_res3
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 + op_res3
    return


def sub_c(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_con = int(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 - op_con
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 - op_con
    return


def sub_r(op_str):
    global sp
    op_res2= R_SP(op_str[1])
    op_res3 = R_SP(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 - op_res3
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 - op_res3
    return

def mul_c(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_con = int(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 * op_con
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 * op_con
    return


def mul_r(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_res3 = R_SP(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 * op_res3
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 * op_res3
    return

def div_c(op_str):
    global sp
    op_res2= R_SP(op_str[1])
    op_con = int(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 // op_con
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 // op_con
    return

def div_r(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_res3 = R_SP(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 // op_res3
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 // op_res3
    return


def shiftl_c(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_con = int(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 << op_con
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 << op_con
    return


def shiftl_r(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_res3 = R_SP(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 << op_res3
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 << op_res3
    return


def shiftr_c(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_con = int(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 >> op_con
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 >> op_con
    return


def shiftr_r(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_res3 = R_SP(op_str[2])
    if op_str[0] == "sp":
        sp = op_res2 >> op_res3
    else:
        op_res1 = int(strip_R(op_str[0]))
        Reg[op_res1] = op_res2 >> op_res3
    return


def store_m(op_str):  # store_m
    global sp
    op_mem = int(op_str[0])
    op_res = R_SP(op_str[1])
    Memory[op_mem] = op_res
    return


def store_r(op_str):  # store_r
    global sp
    op_res2 = R_SP(op_str[2])
    op_mem = int(op_str[0])
    if op_str[1] == "sp":
        Memory[sp + op_mem] = op_res2
    else:
        op_res1 = int(strip_R(op_str[1]))
        Memory[op_mem + Reg[op_res1]] = op_res2
    return


def slt_c(op_str):
    global sp
    op_res2 = R_SP(strip_R(op_str[1]))
    op_con = int(op_str[2])
    if op_str[0] == "sp":
        if op_res2 < op_con:
            sp = 1
        else:
            sp = 0
    else:
        op_res1 = int(strip_R(op_str[0]))
        if op_res2 < op_con:
            Reg[op_res1] = 1
        else:
            Reg[op_res1] = 0
    return


def slt_r(op_str):
    global sp
    op_res2= R_SP(op_str[1])
    op_res3 = R_SP(op_str[2])
    if op_str[0] == "sp":
        if op_res2 < op_res3:
            sp = 1
        else:
            sp = 0
    else:
        op_res1 = int(strip_R(op_str[0]))
        if op_res2 < op_res3:
            Reg[op_res1] = 1
        else:
            Reg[op_res1] = 0
    return


def sle_c(op_str):
    global sp
    op_res2= R_SP(strip_R(op_str[1]))
    op_con = int(op_str[2])
    if op_str[0] == "sp":
        if op_res2 <= op_con:
            sp = 1
        else:
            sp = 0
    else:
        op_res1 = int(strip_R(op_str[0]))
        if op_res2 <= op_con:
            Reg[op_res1] = 1
        else:
            Reg[op_res1] = 0
    return


def sle_r(op_str):
    global sp
    op_res2 = R_SP(op_str[1])
    op_res3 = R_SP(op_str[2])
    if op_str[0] == "sp":
        if op_res2 <= op_res3:
            sp = 1
        else:
            sp = 0
    else:
        op_res1 = int(strip_R(op_str[0]))
        if op_res2 <= op_res3:
            Reg[op_res1] = 1
        else:
            Reg[op_res1] = 0
    return


def beqz(op_str):
    op_res1 = int(strip_R(op_str[0]))
    if Reg[op_res1] == 0:
        return label[op_str[1]]
    else:
        return -1


def goto(op_str):
    return label[op_str[0]]


def or_r(op_str):
    op_res1 = int(strip_R(op_str[0]))
    op_res2 = int(strip_R(op_str[1]))
    op_res3 = int(strip_R(op_str[2]))
    Reg[op_res1] = Reg[op_res2] | Reg[op_res3]
    return


def and_r(op_str):
    op_res1 = int(strip_R(op_str[0]))
    op_res2 = int(strip_R(op_str[1]))
    op_res3 = int(strip_R(op_str[2]))
    Reg[op_res1] = Reg[op_res2] & Reg[op_res3]
    return


def xor_r(op_str):
    op_res1 = int(strip_R(op_str[0]))
    op_res2 = int(strip_R(op_str[1]))
    op_res3 = int(strip_R(op_str[2]))
    Reg[op_res1] = Reg[op_res2] ^ Reg[op_res3]
    return

def or_c(op_str):
    op_res1 = int(strip_R(op_str[0]))
    op_res2 = int(strip_R(op_str[1]))
    op_con = int(op_str[2])
    Reg[op_res1] = Reg[op_res2] | op_con
    return

def and_c(op_str):
    op_res1 = int(strip_R(op_str[0]))
    op_res2 = int(strip_R(op_str[1]))
    op_con = int(op_str[2])
    Reg[op_res1] = Reg[op_res2] & op_con
    return

def xor_c(op_str):
    op_res1 = int(strip_R(op_str[0]))
    op_res2 = int(strip_R(op_str[1]))
    op_con = int(op_str[2])
    Reg[op_res1] = Reg[op_res2] ^ op_con
    return

def call(op_str):
    global list_pc, pc, sp
    list_pc.append(pc)
    if sp < 0:
        return -1
    else:
        sp = sp - 1
        Memory[sp] = pc
        pc = label[op_str[0]]
        return pc

def ret():
    global sp
    tmp = Memory[sp]
    sp = sp + 1
    return tmp

def clz(op_str):
    op_res1 = int(strip_R(op_str[0]))
    op_res2 = int(strip_R(op_str[1]))
    Reg[op_res1] = 64 - len(bin(Reg[op_res2])) + 2

def push(op_str):
    global sp
    op_res = R_SP(op_str[0])
    if sp < 0:
        return -1
    else:
        sp = sp - 1
        Memory[sp] = op_res
    return

def pop(op_str):
    global sp
    op_res = int(strip_R(op_str[0]))
    if sp < 0:
        return -1
    else:
        Reg[op_res] = Memory[sp]
        sp = sp + 1
    return

def _pr(op_str):  # _pr打印多个值和字符串
    for i in range(len(op_str)):
        data,flag=_pr_R_SP(op_str[i])
        if flag==1:
            print(data,end=" ")
        elif flag==2:
            print(Memory[data[0]+data[1]],end=" ")
        elif flag==4:
            if len(data)!=3:
                return -1
            mem_s=data[0]+Reg[data[1]]
            for i in range(0,data[2]):
                print(mem_s+i,":",Memory[mem_s+i],end=",")
        elif flag==3:
            if len(data)!=3:
                return -1
            mem_s=data[0]+data[1]
            for i in range(0,data[2]):
                print(mem_s+i,":",Memory[mem_s+i],end=",")
        elif flag==5:
            if len(data)!=3:
                return -1
            mem_s=data[0]+sp
            for i in range(0,data[2]):
                print(mem_s+i,":",Memory[mem_s+i],end=",")
        elif flag==6:
            print(Memory[data[0]+Reg[data[1]]],end=" ")
        elif flag==7:
            print(Memory[data[0] + sp], end=" ")
    print()
    return

def _data(op_str):
    global sp
    tmp=int(op_str[0])
    for i in range(len(op_str[1])):
        Memory[tmp+i]=int(op_str[1][i])
    return

"""""""""
def _P(str):  # 打印寄存器或者memory的值
    str = str.strip()
    op_str = ""
    for i in range(len(str)):
        if str[i] == " ":
            num = i
            break
        op_str += str[i]
    if op_str != "_P" and op_str != '_p':
        return -1
    else:
        op_str = ""
        for j in range(num, len(str)):
            op_str += str[j]
    op_str = op_str.strip()
    if op_str[0] == 'R':
        print(Reg[int(op_str.strip('R'))])
    elif op_str[0] == '(':
        op_str = op_str.strip('(')
        op_str = op_str.strip(')')
        print(Memory[int(op_str)])
    return True
"""""""""

"""""""""
class KeyboardMgr:
    def on_key_pressed(self, event):
        if str(event.Key) == 'Q':
            win32api.PostQuitMessage()
        elif str(event.Key) == 'Space':
            debug_run(pc)
            P_debug()
        return True
"""""""""

"""""""""
def keypress():  # 开启键盘监控
    keyMgr = KeyboardMgr()
    hookMgr = pyHook.HookManager()
    hookMgr.KeyDown = keyMgr.on_key_pressed
    hookMgr.HookKeyboard()
    pythoncom.PumpMessages()
"""""""""

def P_debug():  # 将值在新窗口给出
    turtle.clear()
    turtle.hideturtle()
    turtle.Turtle().screen.delay(0)
    turtle.pencolor("red")
    turtle.speed(10)
    turtle.penup()
    turtle.goto(-300, 300)
    str_pc = "pc:  " + str(pc)    #在屏幕上显示当前pc的值
    turtle.write(str_pc, font=("Arial", 16, "normal"))
    turtle.goto(-200, 300)
    turtle.write(Ins_op[pc - 1], font=("Arial", 16, "normal"))
    setx = -300
    sety = 200
    turtle.penup()
    k = 0
    for i in range(4):
        turtle.pencolor("black")
        r = "R" + str(k)
        turtle.goto(setx, sety)
        turtle.write(r, font=("Arial", 16, "normal"))
        setx += 150
        for j in range(4):
            turtle.goto(setx, sety)
            if Reg1[k] != Reg[k]:
                turtle.pencolor("red")
                s = str(Reg1[k]) + "-->" + str(Reg[k])
                turtle.write(s, font=("Arial", 16, "normal"))
            else:
                turtle.pencolor("black")
                turtle.write(Reg[k], font=("Arial", 16, "normal"))
            setx += 150
            k += 1
        setx = -300
        sety -= 100
        turtle.pencolor("black")
    turtle.goto(-300, -200)
    str_sp = "sp:  " + str(sp)
    turtle.write(str_sp, font=("Arial", 16, "normal"))
    #turtle.bye()
    return True

if __name__ == '__main__':

    while 1:
        Ins_operator = []  # 操作码
        Ins_operand = []  # 操作数
        Ins_op = []  # 完整指令
        Reg = [0] * Reg_size  # 寄存器
        Reg1 = [0] * Reg_size  # 寄存器副本
        Memory = [0] * Memory_size # data
        label = {}  # 用来记录label的标签
        line_count = -1  # 记录文件读取的行数
        pc = 0  # pc寄存器
        sp = Memory_size  # sp寄存器
        list_flag = []  # 标记指令的模式
        list_pc = []  # 用来记录pc值
        flag_p = 1
        p = ""
        p_op = ""
        p = input("请输入文件名(不在同目录下请输入完整路径)/输入“exit”退出：")   # 读入文件
        p = p.strip()   # 删除空白符，主要目的是防止用户在输入路径或者文件名时，在整个字符串前后增加空白字符。只能删除整个字符串前后的字符，字符串中空白字符不会被删除
        if p.lower() == "exit":    # 当用户输入“exit”时，此时正确的状态为退出
            break

        while os.path.isfile(p) == False: #检查文件是否存在，如果不存在，提示用户继续输入在，直到正确为止，如果您的目录下某个文件夹命名为xxx.txt，此时也会报文件不存在错误，因为这里的输入只允许文件，不允许文件夹
            #说明文件不存在，此时应该提醒用户，并重新输入
            p = input("文件不存在，请您输入正确的文件名(不在同目录下请输入完整路径)/输入“exit”退出：")  # 读入文件
            p = p.strip()   #删除输入两端存在的空白字符
            if p.lower() == "exit":  # 当用户输入“exit”时，此时正确的状态为退出
                break
            if os.path.isfile(p) == True:
                break
            else:
                continue
        if p.lower() == "exit":    # 当用户输入“exit”时，此时正确的状态为退出
            break
        p_op = input('请选择模式（输入“normal”进入普通模式/“debug”进入调试模式/“exit退出调试”）：')
        p_op = p_op.strip()  # 默认删除空白符
        instruction_content = ["normal","exit","debug"]
        if p_op.lower() not in instruction_content:  
            # print("指令不存在")  # 当输入的指令不存在时，应该要求用户再次输入指令，而不是跳转到输入文件处
            while True:
                p_op = input('输入指令错误,请重新选择模式（输入“normal”进入普通模式/“debug”进入调试模式/“exit退出调试”）：')
                p_op.strip()
                if p_op.lower() in instruction_content:
                    break
        if p_op.lower() == "normal":
            #read(p)
            #run()
            try:
                read(p)
                
            except IOError:
                print("Err: 找不到该文件")
            except IndexError as e:
                error_type, error_value, trace_back = sys.exc_info()
                print(error_value)
                # print(str(e))     #打印寄存器数目超过指定个数限制
            except BaseException as e:
                error_type, error_value, trace_back = sys.exc_info()
                print(error_value)
                # print(format(e))   #处理格式错误异常
            else:    # 修改逻辑，增加else字句，当上面读文件没有错误时，执行run函数，完成输出
                #run()
                try:
                    run()
                except:
                    print("Err : 第", pc + 1, "行", Ins_op[pc])
        elif p_op.lower() == "debug":
            try:
                debug_read(p)
            except IOError:
                print("Err: 找不到该文件")
            except IndexError as e:
                error_type, error_value, trace_back = sys.exc_info()
                print(error_value)
                # print(str(e))     #打印寄存器数目超过指定个数限制
            except BaseException as e:
                error_type, error_value, trace_back = sys.exc_info()
                print(error_value)
            else:   # 在debug模式下，如果能够找到指定的文件，则启动“小乌龟”，并按照指定方式显示，如果找不到指定文件，不启动“小乌龟”，
                # x = debug2_run()
                try:
                    x = debug2_run()
                except:
                    print("Err : 第", pc + 1, "行", Ins_op[pc])
        else:
            break

        while flag_p == 1:
            p2 = input("请输入指令(输入“exit”退出/输入“again”可以再次输入文件):")
            p2 = p2.strip()
            if p2.lower() == "exit":
                flag_p = -1
                break
            elif p2.lower() == "again":
                flag_p = 0
            else:
                print("该指令不存在，请重新输入")
        if flag_p == -1:
            break
