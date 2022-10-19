import subprocess
import chardet
import jieba
import jieba.posseg as posg
import sys
import random
def ReadPropertyWord():#读取属性词
    f = open('A:\\B\\Me\\构造模板\\data\\属性词.txt','r',encoding="utf8")
    lines = f.read().split("\n")
    prolist = []  # 所有中文集合
    prodict = {} #对应字典
    for i in lines:
        units = i.split(" ")
        for j in range(0, len(units)):
            if j==0:
                continue
            units[j] = units[j].replace(" ", "")
            if units[j] != "":
                prolist.append(units[j])
                prodict[units[j]] = units[0]
    print(prolist, prodict )
    return prolist, prodict  # 对应的英文



# 读取问答对
def ReadQA():
    with open('A:\\B\\Me\\构造模板\\data\\问答集合', 'r', encoding='gbk') as f:
        lines=f.read().split('\n')
        # print(lines)
    Q=[]
    A=[]
    for i in range(0,len(lines),2):
        # print(i)
        if i%2==0:#问题
            Q.append(lines[i])
            A.append(lines[i+1])
    print(Q)
    print(A)
    return Q,A

# 读取问答对
def ReadQ2A():
    with open('A:\\B\\Me\\构造模板\\data\\两跳问答', 'r', encoding='gbk') as f:
        lines=f.read().split('\n')
        # print(lines)
    Q=[]
    A=[]
    for i in range(0,len(lines),2):
        # print(i)
        if i%2==0:#问题
            Q.append(lines[i])
            A.append(lines[i+1])
    print(Q)
    print(A)
    return Q,A

def readPeo():
    with open('D:\\工商小能手网站\\main\\data\\pe.txt', 'r', encoding='utf-8') as f:
        lines=f.read().split('\n')
    h=set()
    while(len(h)<10):
        i = random.randint(0,1803)
        h.add(i)

    peo_re=[]
    for i in h:
        peo_re.append(lines[i])
    return peo_re

def readCom():#10哦公司
    with open('D:\\工商小能手网站\\main\\data\\com.txt', 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    h = set()
    while (len(h) < 10):
        i=random.randint(0, 372)
        h.add(i)
    com_re = []
    for i in h:
        com_re.append(lines[i])
    return com_re
if __name__=='__main__':
    # ReadPropertyWord()
    # ReadQ2A()
    print(readPeo())
    # s='生产 开发 开发研制 开发研究制作 发明 研究 制作 研制 产品 成果 作品 专利 软件 著作 东西'
    # print(s.replace(' ','\n'))

