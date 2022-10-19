
def CV():
    with open('所有产品实体.txt', 'r', encoding='utf8')as f:
        lines=f.read().split('\n')
    for i in range(0,len(lines)):
        lines[i]+=' nz\n'
    print(lines)
    with open('userdict.txt', 'a+', encoding='utf8') as f:
        f.writelines(lines)
def AV():
    with open('所有人物实体.txt', 'r', encoding='utf8')as f:
        lines=f.read().split('\n')
    for i in range(0,len(lines)):
        lines[i]+=' nr\n'
    print(lines)
    with open('userdict.txt', 'a+', encoding='utf8') as f:
        f.writelines(lines)
def BV():
    with open('所有公司实体.txt', 'r', encoding='utf8')as f:
        lines=f.read().split('\n')
    for i in range(0,len(lines)):
        # 没有判断是否有空行
        lines[i]+=' nt\n'
    print(lines)
    with open('userdict.txt', 'a+', encoding='utf8') as f:
        f.writelines(lines)

if __name__ == '__main__':
    AV()
    BV()
    CV()
    # string ='邮箱 邮箱号 邮箱号码 电子邮箱'
    # print(string.replace(' ','\n'))
    # with open("a","r",encoding="gbk")as f:
    #     z=f.read().split("\n")
    #     for i in z:
    #         m=i.split(" ")
    #         zzz=m[0]+' 5 '+m[1]
    #         with open("aa",'a+',encoding='utf8')as fuke:
    #             fuke.writelines(zzz+'\n')
    #         print(zzz)

    # s='1,2,'
    # print(s.strip().split(','))
