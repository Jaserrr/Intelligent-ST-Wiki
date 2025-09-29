import csv
import matplotlib.pyplot as plt
with open("score.csv",'r') as f:
# with open语句确保在处理完文件后，文件被正确关闭
    dic=csv.DictReader(f) # 将文件的内容转换成字典格式
    stu=[line for line in dic] # 列表推导式，将dic每一行数据以字典形式依次添加到列表stu中
m,fm,a,b,c,d,e=0,0,0,0,0,0,0 # 分别表示男生、女生、五个等级的人数
for s in stu:
    if s["性别"]=="男":
        m+=1
    elif s["性别"]=="女":
        fm+=1
    s=int(s["成绩"])
    if s>=90:
        a+=1
    elif s>=80:
        b+=1
    elif s>=70:
        c+=1
    elif s>=60:
        d+=1
    else:
        e+=1
mrate=m/len(stu)
fmrate=fm/len(stu)
print('男生比例：{:.2%}'.format(mrate))
print('女生比例：{:.2%}'.format(fmrate))
print('优秀：{}人'.format(a))
print('良好：{}人'.format(b))
print('中等：{}人'.format(c))
print('及格：{}人'.format(d))
print('不及格：{}人'.format(e))
plt.rcParams['font.family']='Microsoft YaHei'
# 字体设置为“微软雅黑”，确保在生成的图表中，中文文本能够正常显示
labels=['优秀','良好','中等','及格','不及格']
sizes=[a,b,c,d,e]
plt.pie(sizes,labels=labels)
plt.title('学生成绩统计饼状图')
plt.legend(loc='upper right') # 设置标签位置为窗口右上角
plt.show()
stu.sort(key=lambda x:int(x['成绩']),reverse=True)
# sort为升序排序，使用reverse=True方法反转为降序排序
with open('sorted.csv','w',newline='') as file:
    writer=csv.writer(file) # 创建一个CSV文件写入器，用来将数据写入到指定文件中
    writer.writerow(['学号','姓名','性别','成绩'])
    for s in stu:
        writer.writerow([s['学号'],s['姓名'],s['性别'],s['成绩']]) # 将一行数据写入CSV文件

# import pandas as pd
# import matplotlib.pyplot as plt
# df=pd.read_csv("score.csv")  # 使用pandas的read_csv函数读取CSV文件数据
# df['成绩'] = pd.to_numeric(df['成绩'], errors='coerce')
# m,f,a,b,c,d,e=0,0,0,0,0,0,0  # 分别统计男生、女生、五个等级的学生数量
# for s in df['性别']:
#     if s=="男":
#         m+=1
#     elif s=="女":
#         f+=1
# for s in df['成绩']:
#     if s>=90:
#         a+=1
#     elif s>=80:
#         b+=1
#     elif s>=70:
#         c+=1
#     elif s>=60:
#         d+=1
#     else:
#         e+=1
# m_rate=m/len(df)
# f_rate=f/len(df)
# print('男生比例：{:.2%}'.format(m_rate))
# print('女生比例：{:.2%}'.format(f_rate))
# print('优秀：{}人'.format(a))
# print('良好：{}人'.format(b))
# print('中等：{}人'.format(c))
# print('及格：{}人'.format(d))
# print('不及格：{}人'.format(e))
# plt.rcParams['font.family']='Microsoft YaHei'
# # 字体设置为“微软雅黑”，确保在生成的图表中，中文文本能够正常显示
# labels=['优秀','良好','中等','及格','不及格']
# sizes=[a,b,c,d,e]
# plt.pie(sizes,labels=labels)
# plt.title('学生成绩统计饼状图')
# plt.legend()
# plt.show()
# sorted_df=df.sort_values(by='成绩',ascending=False)  # 按成绩降序排序
# sorted_df.to_csv('sorted.csv',index=False)  # 将排序后的结果写入到新的CSV文件中


