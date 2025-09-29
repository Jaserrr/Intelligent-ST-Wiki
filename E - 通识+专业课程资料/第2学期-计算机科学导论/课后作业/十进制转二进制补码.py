def DtoBNR(n):
    if n>=0:
        return format(n,'08b')
    else:
        absn=format(abs(n),'07b')  # 先去掉符号位
        n1=''
        for b in absn:
            n1=n1+str(1-int(b))  # 取反
        c=bin(int(n1,2)+1)[2:]  # 加1
        while len(c)<7:
            c='0'+c
        return '1'+c   # 再补回符号位

x=int(input("输入一个-128~127的十进制整数："))
print(DtoBNR(x))