# from .data.readDict import *
import jieba
import jieba.posseg as pseg
from pyltp import Postagger
from pyltp import Parser
from py2neo import Graph
import os
import numpy as np
import json
import codecs
import linecache
import re

from main.data.readDict import ReadPropertyWord

LTP_DATA_DIR ='F:\python\LTP\ltp_data'
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型

def JieBa(q):
    print("--JieBa--")
    jieba.load_userdict('A:\\B\\Me\构造模板\\data\\userdict.txt')
    seg_list = list(pseg.cut(q))
    print(seg_list)
    segment = []
    segPos = []
    for i in seg_list:
        segment.append(i.word)
        segPos.append(i.flag)
    print(segment, segPos)
    return segment,segPos


def Recognize(segment,segPos):
    print("--Recognize--")
    # 读取关系属性词
    propertyList, propertyDict = ReadPropertyWord()
    for i in range(0,len(segPos)):
        if segment[i] in propertyList:
            segPos[i]="property"
            continue
        else:
            continue
    return segPos

# 计算编辑距离
def edit_distance(word1, word2):
    len1 = len(word1)
    len2 = len(word2)
    dp = np.zeros((len1 + 1, len2 + 1))
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if word1[i - 1] == word2[j - 1]:
                temp = 0
            else:
                temp = 1
            dp[i][j] = min(dp[i - 1][j - 1] + temp, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
    return dp[len1][len2]



def Drive(q):
    print("--Drive--")
#   jieba分词-LTP找出语法树
    print("jieba:")
    segment, segPos=JieBa(q) #jieba：segment 分好的词 segPos 词性
    segPos=Recognize(segment, segPos)
    print("====主函数=====")
    # print('问句模板：')
    # print(qtem)
    # print('模板填槽内容：（在问句分好的词中的下标）')
    # print(numerial)
    print('问句的句法解析树：')
    print("ltp:")
    poslist = []
    postags = postagger.postag(segment)
    for i in postags:
        poslist.append(str(i))
    arcs = parser.parse(segment, poslist)
    arcshead = []
    arcsrela = []
    for i in arcs:
        arcshead.append(i.head)
        arcsrela.append(i.relation)
    print(segment)
    print(poslist,arcshead, arcsrela)#ltp：poslist 词性 arcshead父节点词的索引ROOT节点的索引是0，第一个词开始的索引依次为1、2、3…  arcsrela 依存弧的关系
    ldfg = ''
    for i in segPos:
        ldfg = ldfg + str(i) + ","
    ldfg += "|"
    for i in arcshead:
        ldfg = ldfg + str(i) + ","
    ldfg += "|"
    for i in arcsrela:
        ldfg = ldfg + str(i) + ","
    ldfg += "|"
    print(ldfg)
    ''' 查看是否有一样的结构'''
    return ldfg,segPos,segment
    # return ldfg

    # sub_sens = []
    # with codecs.open(r'A:\\B\\Me\\构造模板\完美数据\句子结构0','r', 'utf8') as f:
    #     for line in f:
    #         # print(line)
    #         sub_sens.append(line)
    # count = len(sub_sens)
    # print("sub_sens",sub_sens)
    # print(count,'循环开始')
    # za=[]
    # for i in range(count):
    #     res = edit_distance(sub_sens[i], ldfg)
    #     # maxLen = max(len(sub_sens[i]), len(ldfg))
    #     # sim= 1 - res * 1.0 / maxLen
    #     # sim = simility(sub_sens[i], ldfg)
    #     # za.append(sim)
    #     print(i,res)
    #     # print(i)
    #
    # # sort_correct = sorted(enumerate(za), key=lambda x: x[1], reverse=True)
    # z = "ok"
    # return z
    for i in range(5):
        print("======================start======================",i)
        max_index = sort_correct[i][0]
        print(max_index, sort_correct[i][1])
        #     内容在词性上面是否符合
        put_index = linecache.getline(r'A:\\B\\Me - 副本\\构造模板\完美数据\0填槽内容', max_index + 1)
        put_index = put_index.split(',')
        search_nei = []
        bool_nei=True
        print("put_index",put_index,len(put_index))
        for i in range(len(put_index) - 1):
            print(put_index[i])
            this_index = int(put_index[i]) # 下标转换为数字
            if this_index>=len(segPos): #句子就没那么长 有问题
                bool_nei = False
                break
            if(segPos[this_index]not in ["nr","nz","property","nt"]):
                bool_nei =False
                break
            search_nei.append(segment[this_index])
            print(i, segment[this_index])
        if bool_nei==False:
            print("内容在词性上面是否符合 此模板不合适")
            continue#此模板不合适
        # 有property至少两个 看填槽内容合适否
        bool_have=False
        for i in segPos:
            if (i =="property"):
                #有property
                bool_have = True
                break
        if((bool_have==True)and(len(put_index)-1)<2):
            print("看填槽内容合适否 此模板不合适")
            continue  # 此模板不合适
        # 合适 看答案是否存在
        print(linecache.getline(r'A:\\B\\Me - 副本\\构造模板\完美数据\0句子结构', max_index + 1))
        template_index = linecache.getline(r'A:\\B\\Me - 副本\\构造模板\完美数据\0测试问题及答案', max_index + 1)
        print("测试问题及答案", template_index)
        print("填槽内容", put_index)
        print("填槽内容split", put_index, "长度", len(put_index))
        moban = linecache.getline(r'A:\\B\\Me - 副本\\构造模板\完美数据\00问句模板', max_index + 1)
        print("模板", moban)
        propertyList, propertyDict = ReadPropertyWord()
        for i in range(len(search_nei)):
            if search_nei[i] in propertyList:
                search_nei[i] = propertyDict[search_nei[i]]
        print(search_nei)
        if len(search_nei) == 1:
            moba = moban % (search_nei[0])
        elif len(search_nei) == 2:
            moba = moban % (search_nei[0], search_nei[1])
        print(moba)
        #     找答案
        cypher = "MATCH p = " + moba + " RETURN n.name"
        print(cypher)
        run_Result = test_graph.run(cypher).data()
        if run_Result == []:  # 没有路径 肯定分词或识别有问题
            print("无答案""此模板不合适")
            continue
        else:
            return (run_Result[0]["n.name"])
            # print(run_Result[0])
            # break













# if __name__=='__main__':
#     str1 = input("输入问句：")
#     Drive(str1)
#

#     Q = ['宜宾五粮液股份有限公司现地址是在哪里的呢？']
#     A = ['四川省宜宾市翠屏区岷江西路150号']宜宾五粮液股份有限公司位置是在哪儿啊？
#     Drive(Q[0], A[0])
# 成功
# 宜宾五粮液股份有限公司现地址是在哪里的呢？
# 宜宾五粮液股份有限公司位置是在哪儿啊？
# 宜宾五粮液股份有限公司邮箱是啥
# 宜宾五粮液股份有限公司领导都有谁  