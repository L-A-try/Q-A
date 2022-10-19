


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Neo4j
from main.main_drive import *
import json
import sys
from main.data.readDict import ReadPropertyWord,readPeo,readCom




# Create your views here.


def index(request):
    return render(request, 'index.html')


def index_recv_data(request):
    # 接收用户前端传来的问题
    inputQuestion = request.POST.get('inputQuestion')
    course = request.POST.get('course')

    qst_type = {'chinese': '查公司', 'history': "查老板", "question": "知识问答", "tupu": "知识图谱"}
    tupu_type = {'tupu_chinese': '查公司知识图谱', 'tupu_history': "查老板知识图谱"}

    print('问题是：' + inputQuestion)
    print('问题类别：' + qst_type[course])

    ret_info = {
        'baseinfo_type': -1,  # -1代表未定义，0代表公司信息，1代表老板信息，2代表知识问答，3代表知识图谱
        'message_jiben': {},  # 基本信息
        'zhuanli': [],  # 专利
        'message_Crj': [],  # 软件著作权
        'message_Czp': [],  # 作品著作权
        'message_Fkt': [],  # 开庭公告
        'message_Fsf': [],  # 司法风险
        'result': '',  # 基本废弃了
        't1_text': {},
        't2_text': [],
        # 't1_text': {"1": {"name": "数据结构"},
        #             "2": {"name": "二叉树"}},
        # 't2_text': [{"source": 1, "target": 2, "rela": "包含"}],
    }
    entity = Neo4j()
    db = entity.connectDB()
    neo4j_db = db.session()
    print("数据库连接成功")
    if course == 'chinese':  # '查公司'
        print("----查公司----", inputQuestion)
        ret_info['baseinfo_type'] = 0  # 代表是查公司
        # 基本信息 message_jiben
        key_serch=['地址','邮箱','网址','经营范围']
        message_jiben={}
        for i in key_serch:
            cypher1 = "MATCH (n:Company)-[r:"+i+"]-(m) WHERE n.name =~ {comName} RETURN m.name"  # 找 实体
            result1 = neo4j_db.run(cypher1, {"comName": "(?i).*" + inputQuestion + ".*"})
            result1 = result1.data()
            print(result1)
            message_jiben[i]=result1[0]['m.name']
        cypher1 = "MATCH (n:Company) WHERE n.name =~ {comName} RETURN n,keys(n)"  # 找 实体
        result1 = neo4j_db.run(cypher1, {"comName": "(?i).*" + inputQuestion + ".*"})
        result1 = result1.data()
        print(result1)
        for i in result1[0]['keys(n)']:
            message_jiben[i]=result1[0]['n'][i]
        print("message_jiben",message_jiben)
        # message_Czl message_Crj message_Czp message_Fkt message_Fsf
        message_Czl=[]  # 专利
        message_Crj = []  # 软件著作权
        message_Czp = []  # 作品著作权
        message_Fkt = []  # 开庭公告
        message_Fsf = []  # 司法风险
        key_serch = ['产品', '风险']
        for i in key_serch:
            cypher1 = "MATCH (n:Company)-[r:"+i+"]-(m)  WHERE n.name =~ {comName} RETURN r.type,keys(m),m"  # 找实体
            result1 = neo4j_db.run(cypher1, {"comName": "(?i).*" + inputQuestion + ".*"})
            result1 = result1.data()
            for j in result1:#多个产品 一个个看
                zzz = {}
                if j['r.type']=='专利':
                    print('专利',j['keys(m)'])
                    for z in j['keys(m)']:
                        zzz[z]=j['m'][z]
                    message_Czl.append(zzz)
                elif j['r.type']=='软件著作权':
                    print('软件著作权',j['keys(m)'])
                    for z in j['keys(m)']:
                        zzz[z] = j['m'][z]
                    message_Crj.append(zzz)

                elif j['r.type']=='作品著作权':
                    print('作品著作权',j['keys(m)'])
                    for z in j['keys(m)']:
                        zzz[z] = j['m'][z]
                    message_Czp.append(zzz)

                elif j['r.type']=='开庭公告':
                    print('开庭公告',j['keys(m)'])
                    for z in j['keys(m)']:
                        zzz[z] = j['m'][z]
                    message_Fkt.append(zzz)

                elif j['r.type']=='司法风险':
                    print('司法风险',j['keys(m)'])
                    for z in j['keys(m)']:
                        zzz[z] = j['m'][z]
                    message_Fsf.append(zzz)

        print("______________________________")
        print("message_jiben", message_jiben)
        print("______________________________")
        print("message_Czl",message_Czl)
        print("______________________________")
        print("message_Crj",message_Crj)
        print("______________________________")
        print("message_Czp",message_Czp)
        print("______________________________")
        print("message_Fkt",message_Fkt)
        print("______________________________")
        print("message_Fsf",message_Fsf)

        # 公司与人物图谱
        index_i = 1
        cypher1 = "MATCH (n:Company)-[r:任职]-(m)  WHERE n.name =~ {comName} RETURN r.type,m.name,n.name"  # 找 实体
        result1 = neo4j_db.run(cypher1, {"comName": "(?i).*" + inputQuestion + ".*"})
        result1 = result1.data()
        print(result1)
        t1_text = {}
        t2_text = []
        if result1!=[]:
            t1_text = {"1": {"name": result1[0]["n.name"]}}
            t2_text = []
            for i in result1:
                nei = {}
                index_i += 1
                j_count = index_i
                j_count = str(j_count)
                nei["name"] = i["m.name"]
                t1_text[j_count] = nei
                mz = {}
                mz["source"] = "1"
                mz["target"] = j_count
                mz["rela"] = i["r.type"]
                t2_text.append(mz)
        print(t1_text,t2_text)
        string = '问题：' + inputQuestion + '\r\n' + '成立日期"：'  # + t1_text["2"]["name"]# 分块吧 一个块是查询内容 另一个块是

        ret_info['result'] = string
        ret_info['t1_text'] = t1_text
        ret_info['t2_text'] = t2_text
        ret_info['message_jiben'] = message_jiben
        ret_info['zhuanli'] = message_Czl
        ret_info['message_Crj'] = message_Crj
        ret_info['message_Czp'] = message_Czp
        ret_info['message_Fkt'] = message_Fkt
        ret_info['message_Fsf'] = message_Fsf

    elif course == 'history':  # "查老板"
        print("----查老板----", inputQuestion)
        ret_info['baseinfo_type'] = 1  # 代表是查老板

        results2 = neo4j_db.run("MATCH (person:Person) "
                                "WHERE person.name =~ {personName} "
                                "RETURN person.name as personName,person.introduction as personIntro",
                                {"personName": "(?i).*" + inputQuestion + ".*"})
        print(results2)
        t1_text = {}
        t2_text = []
        for record in results2:
            t1_text = {"1": {"name": record["personName"]}, "2": {"name": record["personIntro"]}}
            t2_text = [{"source": "1", "target": "2", "rela": "简介"}]
        print("t1_text ", t1_text)
        print("t2_text ", t2_text)
        string =  '简介：' + t1_text["2"]["name"]
        ret_info['result'] = string
        ret_info['t1_text'] = t1_text
        ret_info['t2_text'] = t2_text
        #---------------------------------------------------------------------------------------------------

    elif course == "question":  # "知识问答"
        print("----知识问答----", inputQuestion)
        ret_info['baseinfo_type'] = 2  # 代表是知识问答
        ldfg ,segPos,segment= Drive(inputQuestion)
        sub_sens = []
        with codecs.open(r'A:\\B\\Me\\构造模板\完美数据\句子结构0','r', 'utf8') as f:
            for line in f:
                sub_sens.append(line)
        count = len(sub_sens)
        print("sub_sens",sub_sens)
        print(count,'循环开始')
        za=[]
        for i in range(count):
            res = edit_distance(sub_sens[i], ldfg)
            maxLen = max(len(sub_sens[i]), len(ldfg))
            sim= 1 - res * 1.0 / maxLen
            za.append(sim)
            print(i,sim)

        sort_correct = sorted(enumerate(za), key=lambda x: x[1], reverse=True)
        for i in range(5):
            print("======================start======================", i)
            max_index = sort_correct[i][0]
            print(max_index, sort_correct[i][1])
            #     内容在词性上面是否符合
            put_index = linecache.getline(r'A:\\B\\Me - 副本\\构造模板\完美数据\0填槽内容', max_index + 1)
            put_index = put_index.split(',')
            search_nei = []
            bool_nei = True
            print("put_index", put_index, len(put_index))
            for i in range(len(put_index) - 1):
                print(put_index[i])
                this_index = int(put_index[i])  # 下标转换为数字
                if this_index >= len(segPos):  # 句子就没那么长 有问题
                    bool_nei = False
                    break
                if (segPos[this_index] not in ["nr", "nz", "property", "nt"]):
                    bool_nei = False
                    break
                search_nei.append(segment[this_index])
                print(i, segment[this_index])
            if bool_nei == False:
                print("内容在词性上面是否符合 此模板不合适")
                continue  # 此模板不合适
            # 有property至少两个 看填槽内容合适否
            bool_have = False
            for i in segPos:
                if (i == "property"):
                    # 有property
                    bool_have = True
                    break
            if ((bool_have == True) and (len(put_index) - 1) < 2):
                print("看填槽内容合适否 此模板不合适")
                continue  # 此模板不合适
            # 合适 看答案是否存在
            print(linecache.getline(r'A:\\B\\Me - 副本\\构造模板\完美数据\0句子结构', max_index + 1))
            print("填槽内容", put_index)
            print("填槽内容split", put_index, "长度", len(put_index))
            moban = linecache.getline(r'A:\\B\\Me - 副本\\构造模板\完美数据\0问句模板', max_index + 1)
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
            run_Result = neo4j_db.run(cypher).data()
            if run_Result == []:  # 没有路径 肯定分词或识别有问题
                print("无答案""此模板不合适")
                continue
            else:
                a=run_Result[0]["n.name"]
                template_index = linecache.getline(r'A:\\B\\Me - 副本\\构造模板\完美数据\0测试问题及答案', max_index + 1)
                template_index.split()
                q_q=template_index[0]
                q_a=template_index[1]
                # search_nei[0]
                # a
                print("测试问题及答案", template_index)
                # print(run_Result[0])
                break
        # a是答案  填写一个槽  答案怎么获得 and 两层问答
        # 图谱展示？？？？1！！！！！！！！！！
        # 匹配模板案例q_q q_a
        # print(type(a))
        print("++++++++++++++++++++++++++")
        print(a, "a")
        # t1_text = {"1": {"name": "数据结构"},
        #            "2": {"name": "二叉树"}
        #            }
        # t2_text = [
        #     {"source": 1, "target": 2, "rela": "包含"}
        # ]
        # ret_info['result'] = '问题：' + inputQuestion + '\n' + a
        ret_info['result'] = "答案："+ a


    elif course == 'tupu':  # "知识图谱"
        tupu_type = {'tupu_chinese': '查公司知识图谱', 'tupu_history': "查老板知识图谱"}
        ret_info['baseinfo_type'] = 3  # 代表是查知识图谱
        cos=request.POST.get('tupu_type')
        print(request.POST.get('tupu_type'))
        # 随机10公司 随机10老板
        if cos=='tupu_chinese':
            com_list = readCom()
            count = 1
            t1_text = {}
            t2_text = []
            for ia in com_list:
                j_count = count
                j_count=str(j_count)
                # t1_text[j_count] = {"name":'"'+ ia+'"'}
                t1_text[j_count] = {"name": ia}
                kep_count = j_count
                count += 1
                # 关系
                key_serch = ['地址', '邮箱', '网址', '经营范围', '任职', '产品', '风险']
                for i in key_serch:
                    cypher1 = "MATCH (n:Company)-[r:" + i + "]-(m) WHERE n.name ='" + ia + "' RETURN m.name"  # 找 实体
                    result1 = neo4j_db.run(cypher1)
                    result1 = result1.data()
                    print(result1)
                    zansh = {}
                    if result1==[]:continue
                    x_count = count
                    x_count = str(x_count)
                    # t1_text[x_count] = {"name":'"'+ result1[0]['m.name']+'"'}
                    t1_text[x_count] = {"name": result1[0]['m.name']}
                    zansh["source"] = kep_count
                    # zansh["source"] = '"'+kep_count+'"'
                    # zansh["target"] ='"'+ x_count+'"'
                    zansh["target"] = x_count
                    zansh["rela"] = i
                    # zansh["rela"] = '"'+i+'"'
                    count += 1
                    t2_text.append(zansh)
                # 属性
                cypher1 = "MATCH (n:Company) WHERE n.name ='" + ia + "' RETURN n,keys(n)"  # 找 实体
                result1 = neo4j_db.run(cypher1)
                result1 = result1.data()
                print(result1)
                for i in result1[0]['keys(n)']:
                    zansh = {}
                    if result1 == []: continue
                    x_count = count
                    x_count = str(x_count)
                    # t1_text[x_count] = {"name": '"'+result1[0]['n'][i]+'"'}
                    t1_text[x_count] = {"name": result1[0]['n'][i]}
                    # zansh["source"] = '"'+kep_count+'"'
                    zansh["source"] = kep_count
                    # zansh["target"] = '"'+x_count+'"'
                    zansh["target"] = x_count
                    # zansh["rela"] = '"'+i+'"'
                    zansh["rela"] = i
                    count += 1
                    t2_text.append(zansh)
            print("ok")
            # t1_text = str(t1_text)
            # t1_text = t1_text.replace("'", '"')
            print(t1_text)

            # t1_text = json.loads(t1_text)
            print(t1_text)
            # t2_text = str(t2_text)
            # t2_text = t2_text.replace("'", '"')

            # t2_text = json.loads(t2_text)
            print("t1_text ", t1_text)
            print("t2_text ", t2_text)
            # string = '问题：'
            # ret_info['result'] = string
            ret_info['t1_text'] = t1_text
            ret_info['t2_text'] = t2_text

        else:
            # peo
            peo_list = readPeo()
            count = 1
            t1_text = {}
            t2_text = []
            for ia in peo_list:
                results2 = neo4j_db.run("MATCH (person:Person) "
                                    "WHERE person.name =~ {personName} "
                                    "RETURN person.name as personName,person.introduction as personIntro",
                                    {"personName": "(?i).*" + ia + ".*"})
                print(results2)
                for record in results2:
                    zansh = {}
                    j_count = count
                    j_count = str(j_count)
                    t1_text[j_count]={"name": record["personName"]}
                    zansh["source"] =j_count
                    count+=1
                    j_count = count
                    j_count = str(j_count)
                    t1_text[j_count]={"name": record["personIntro"]}
                    zansh["target"]=j_count
                    zansh["rela"]="简介"
                    t2_text.append(zansh)
                    count+=1

            print("t1_text ", t1_text)
            print("t2_text ", t2_text)
            # string = '问题：'
            # ret_info['result'] = string
            ret_info['t1_text'] = t1_text
            ret_info['t2_text'] = t2_text

    tmp_value_list = list(ret_info['t1_text'].values())
    tmp_point = 1
    for tmp_key in ret_info["t1_text"].keys():
        if ret_info["t1_text"][tmp_key] in tmp_value_list[tmp_point:]:
            ret_info["t1_text"][tmp_key]['name'] += " " * tmp_point
            tmp_point += 1
    ret_info["t1_text"] = str(ret_info["t1_text"]).replace("'", '"')
    ret_info["t2_text"] = str(ret_info["t2_text"]).replace("'", '"')
    print(ret_info)
    response = JsonResponse(ret_info)
    return response


def show_graph_demo(request):
    # 展示graph demo
    return render(request, 'graph_index.html')


def mytest(request):
    return render(request, 'mytest.html')





# -----------------------------------------------------------------------------------------------------------------


# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# # from main.models import Neo4j
# import json
# import sys
#
#
# # from main.main_drive import *
#
#
# # Create your views here.
#
#
# def index(request):
#     return render(request, 'index.html')
#
#
# def index_recv_data(request):
#     # 接收用户前端传来的问题
#     inputQuestion = request.POST.get('inputQuestion')
#     course = request.POST.get('course')
#
#     qst_type = {'chinese': '查公司', 'history': "查老板", "question": "知识问答", "tupu": "知识图谱"}
#     tupu_type = {'tupu_chinese': '查公司知识图谱', 'tupu_history': "查老板知识图谱"}
#
#     print('问题是：' + inputQuestion)
#     print('问题类别：' + qst_type[course])

    #     ret_info = {
    #         'baseinfo_type': 0,  # -1代表未定义，0代表公司信息，1代表老板信息，2代表知识问答，3代表知识图谱
    #         'message_jiben': {# 基本信息
    #             '成立日期':'2010-03-03',
    #             '经营范围':'技术开发;货物进出口、技术进出口、代理进出口;销售通讯设备、厨房用品、卫生用品(含个人护理用品)、日用杂货、化妆品、医疗器械I类、II类、避孕器具、玩具、体育用品、文化用品、服装鞋帽、钟表眼镜、针纺织品、家用电器、家具(不从事实体店铺经营)、花、草及观赏植物、不再分装的包装种子、照相器材、工艺品、礼品、计算机、软件及辅助设备、珠宝首饰、食用农产品、宠物食品、电子产品、摩托车、电动车、自行车及零部件、智能卡、五金交电(不从事实体店铺经营)、建筑材料(不从事实体店铺经营) ;维修仪器仪表;维修办公设备;承办展览展示活动; 会议服务;筹备、策划、组织大型庆典;设计、制作、代理、发布广告;摄影扩印服务;文艺演出票务代理、体育赛事票务代理、展览会票务代理、博览会票务代理:手机技术开发;手机生产、手机服务(限海淀区永捷北路2号二层经营) ;从事互联网文化活动;出版物零售;出版物批发;销售第三类医疗器械:销售食品:零售药品:广播电视节目制作:经营电信业务。 (企业依法自主选择经营项目，开展经营活动:从事互联网文化活动、出版物批发、出版物零售、销售食品、经营电信业务、广播电视节目制作、零售药品、销售第三类医疗器械以及依法须经批准的项目，经相关部门]批准后依批准的内容开展经营活动;不得从事本市产业政策禁止和限制类项目的经营活动。)',
    #             'name':'小米科技有限责任公司',
    #             '邮箱':'chenchongwei@xiaomi. com',
    #             '纳税人识别号':'91110108551385082Q',
    #             '营业期限':'2010-03-03至2030-03-02',
    #             '人员规模':'100-499人',
    #             '网址':'www. mi. com',
    #             '地址':'北京市海淀区西二旗中路33号院6号楼6层006号',
    #             '统一社会信用代码':'91110108551385082Q',
    #             '注册资本':'185000万人民币'},
    #         'zhuanli': [],
    #         'message_Crj':[], # 软件著作权
    #         'message_Czp':[], # 作品著作权
    #         'message_Fkt':[], # 开庭公告
    #         'message_Fsf':[], # 司法风险
    #         'result': '姓名看看撒娇的饭卡手动阀',
    #         't1_text':
    #             {"1": {"name": "数据结构","type": "学科"},
    # "2": { "name": "二叉树", "type": "知识点"},
    # "3": {"name": "链表","type": "知识点"},
    # "4": {"name": "平衡二叉树","type": "知识点"},
    # "5": {"name": "二叉树的结构讲解","url": "www.mooc.com/15.html",
    # "type": "视频资源"},
    # "6": {"name": "链表的反转",
    # "url": "www.mooc.com/1.ppt",
    # "type": "ppt资源"},
    # "7": {"name": "闲节点","type": "闲"},
    # "8": {"name": "闲节点2","type": "闲"},
    # "9": {"name": "闲节点3","type": "闲"},
    # "10": {"name": "芳芳老师","type": "老师"},
    # "11": {"name": "月老师","type": "老师"},
    # "12":{"name":"月老师1", "type":"老师"},
    # "13":{"name":"月老师2", "type":"老师"},
    # "14": {"name": "芳芳老师","type": "老师"},
    # "15": {"name": "芳芳老师","type": "老师"},
    # "16": {"name": "芳芳老师","type": "老师"},
    # "17": {"name": "芳芳老师","type": "老师"},
    # "18": {"name": "芳芳老师","type": "老师"},
    # "19": {"name": "芳芳老师","type": "老师"},
    # "20": {"name": "芳芳老师","type": "老师"}
    # },
    #         't2_text':
    # [
    # { "source": 1, "target": 2, "rela": "包含", "type": "包含关系" },
    # { "source": 1, "target": 3, "rela": "包含", "type": "包含关系" },
    # { "source": 1, "target": 4, "rela": "包含", "type": "包含关系" },
    # { "source": 2, "target": 5, "rela": "视频课程", "type": "资源" },
    # { "source": 3, "target": 6, "rela": "ppt教程", "type": "资源" },
    # { "source": 3, "target": 7, "rela": "没关系" },
    # { "source": 8, "target": 9, "rela": "没关系" },
    # { "source": 10, "target": 5, "rela": "授课", "type": "行为" },
    # {"source": 11, "target": 5, "rela": "授课", "type": "行为"},
    # { "source": 12, "target": 1, "rela": "授课", "type": "行为" },
    # { "source": 13, "target": 1, "rela": "授课", "type": "行为" },
    # { "source": 14, "target": 1, "rela": "授课", "type": "行为" },
    # { "source": 15, "target": 11, "rela": "授课", "type": "行为" },
    # { "source": 16, "target": 11, "rela": "授课", "type": "行为" },
    # { "source": 17, "target": 1, "rela": "授课", "type": "行为" },
    # { "source": 18, "target": 1, "rela": "授课", "type": "行为" },
    # { "source": 19, "target": 1, "rela": "授课", "type": "行为" },
    # { "source": 20, "target": 1, "rela": "授课", "type": "行为" }
    # ]
    # ,
    #     }

    # ret_info = {
    #     'baseinfo_type': 0,  # -1代表未定义，0代表公司信息，1代表老板信息，2代表知识问答，3代表知识图谱
    #     'message_jiben': {  # 基本信息
    #         '成立日期': '2010-03-03',
    #         '经营范围': '技术开发;货物进出口、技术进出口、代理进出口;销售通讯设备、厨房用品、卫生用品(含个人护理用品)、日用杂货、化妆品、医疗器械I类、II类、避孕器具、玩具、体育用品、文化用品、服装鞋帽、钟表眼镜、针纺织品、家用电器、家具(不从事实体店铺经营)、花、草及观赏植物、不再分装的包装种子、照相器材、工艺品、礼品、计算机、软件及辅助设备、珠宝首饰、食用农产品、宠物食品、电子产品、摩托车、电动车、自行车及零部件、智能卡、五金交电(不从事实体店铺经营)、建筑材料(不从事实体店铺经营) ;维修仪器仪表;维修办公设备;承办展览展示活动; 会议服务;筹备、策划、组织大型庆典;设计、制作、代理、发布广告;摄影扩印服务;文艺演出票务代理、体育赛事票务代理、展览会票务代理、博览会票务代理:手机技术开发;手机生产、手机服务(限海淀区永捷北路2号二层经营) ;从事互联网文化活动;出版物零售;出版物批发;销售第三类医疗器械:销售食品:零售药品:广播电视节目制作:经营电信业务。 (企业依法自主选择经营项目，开展经营活动:从事互联网文化活动、出版物批发、出版物零售、销售食品、经营电信业务、广播电视节目制作、零售药品、销售第三类医疗器械以及依法须经批准的项目，经相关部门]批准后依批准的内容开展经营活动;不得从事本市产业政策禁止和限制类项目的经营活动。)',
    #         'name': '小米科技有限责任公司',
    #         '邮箱': 'chenchongwei@xiaomi. com',
    #         '纳税人识别号': '91110108551385082Q',
    #         '营业期限': '2010-03-03至2030-03-02',
    #         '人员规模': '100-499人',
    #         '网址': 'www. mi. com',
    #         '地址': '北京市海淀区西二旗中路33号院6号楼6层006号',
    #         '统一社会信用代码': '91110108551385082Q',
    #         '注册资本': '185000万人民币'},
    #     'zhuanli': [  # 专利
    #         {'name': '社交网络交互信息处理方法及装置', "专利类型": '发明专利', '申请号': 'CN201510991437.0', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #     ],
    #     'message_Crj': [
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交adf阿斯蒂芬阿斯蒂 撒地方互信息处理方法及装置',
    #          '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #
    #     ],  # 软件著作权
    #     'message_Czp': [],  # 作品著作权
    #     'message_Fkt': [
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #         {"专利类型": '发明专利', '申请号': 'CN201510991437.0', 'name': '社交网络交互信息处理方法及装置', '申请公布号': 'CN105512945B',
    #          ' 申请公布日': '2020-01-10'},
    #
    #     ],  # 开庭公告
    #     'message_Fsf': [],  # 司法风险
    #     'result': '姓名看看撒娇的饭卡手动阀',
    #     "t1_text":
    #         {'1': {'name': '云南省建设投资控股集团有限公司'},
    #          '2': {'name': '云南省昆明市经济技术开发区信息产业基地林溪路188号'},
    #          '3': {'name': 'ycihzhb@163.com'},
    #          '4': {'name': 'www.ynjg.com'},
    #          '5': {'name': '经营授权范围内的国有资产；水利水电、公路、 港口、码头、铁路、轨道交通、市政道路、综合管廊、污水处理、能源、机场等基础设施投资建设和管理；酒店、旅游产业、文化产业的投资建设和管理；向境外派遣各类劳务人员（不含港澳台地区）；国内外工程总承包及发包，房屋建筑工程施工总承包，建筑工程劳务服务，房地产开发及经营，勘察设计，建筑施工及设备施工，商品混凝土、混凝土预制构件、外掺料及其他建筑构件的生产及销售，普通货运及泵送，建筑预构件生产及建筑机械制造，自营和代理除国家组织统一联合经营的16种出口商品和国家实行核定公司经营的12种进出口商品以外的其它商品及技术的进出口业务；对外工程所需设备、材料的出口，建筑科研开发及技术咨询，承办中外合资经营、合作生产业务，开展“三来一补”业务，按国家规定在海外举办各类企业及国内贸易；保险、银行业的投资。（依法须经批准的项目，经相关部门批准后方可开展经营活动）'},
    #          '6': {'name': '王峥'},
    #          '7': {'name': '王建新'},
    #          '8': {'name': '陈文山'},
    #          '9': {'name': '建筑施工外爬架结构支撑体系计算分析软件'},
    #          '10': {'name': 'YCIH海外施工项目风险管理平台'},
    #          '11': {'name': '元蔓高速南沙红河特大桥大体积混凝土水化热监控系统'},
    #          '12': {'name': '基于BIM的铝合金模板配模和虚拟拼装软件'},
    #          '13': {'name': '基于BIM的铝合金模板智能出图软件'},
    #          '14': {'name': '电梯井工具式全钢施工平台施工工法'},
    #          '15': {'name': '一种公路水沟盖板塑料模具脱模装置'},
    #          '16': {'name': '一种适用于水泥土搅拌桩的室内模拟试验装置'},
    #          '17': {'name': '高空施工辅助装置'},
    #          '18': {'name': '一种雨水收集池及其施工方法'},
    #          '19': {'name': '桥梁施工平台'},
    #          '20': {'name': '一种雨季湿软路基填筑施工方法'},
    #          '21': {'name': '预制T梁腹板钢筋绑扎辅助胎架施工工法'},
    #          '22': {'name': '桥梁高空作业吊篮'},
    #          '23': {'name': '一种简易的混凝土浇筑施工中垂直输送管道'},
    #          '24': {'name': '（2019）粤0306民初3274号之二'},
    #          '25': {'name': '（2019）云2528民初1171号'},
    #          '26': {'name': '（2018）云2901民初2050号'},
    #          '27': {'name': '（2019）云29民终378号'},
    #          '28': {'name': '（2019）豫12民终1920号'},
    #          '29': {'name': '（2019）云0721民初214号'},
    #          '30': {'name': '（2019）云0721民初34号'},
    #          '31': {'name': '（2019）云07民终831号'},
    #          '32': {'name': '（2016）云06民初62号'},
    #          '33': {'name': '（2019）赣0721民初2320号'},
    #          '34': {'name': '(2019)赣0721民初2320号'},
    #          '35': {'name': '(2019)云2528民初1098号'},
    #          '36': {'name': '(2019)云0521民初326号'},
    #          '37': {'name': '(2018)云0114民初3616号'},
    #          '38': {'name': '(2019)云3325民初987号'},
    #          '39': {'name': '(2019)云0114民初5298号'},
    #          '40': {'name': '(2019)云0626民初512号'},
    #          '41': {'name': '(2019)云0626民初508号'},
    #          '42': {'name': '(2019)云3401民初908号'},
    #          '43': {'name': '1000-4999人'},
    #          '44': {'name': '91530000MA6K5LYD33'},
    #          '45': {'name': '91530000MA6K5LYD33'},
    #          '46': {'name': '2815775.807万人民币'},
    #          '47': {'name': '云南省建设投资控股集团有限公司'},
    #          '48': {'name': '2016-04-19至无固定期限'},
    #          '49': {'name': '2016-04-19'}},
    #     "t2_text":
    #         [{'target': '2', 'source': '1', 'rela': '地址'}, {'target': '3', 'source': '1', 'rela': '邮箱'},
    #          {'target': '4', 'source': '1', 'rela': '网址'}, {'target': '5', 'source': '1', 'rela': '经营范围'},
    #          {'target': '6', 'source': '1', 'rela': '任职'}, {'target': '7', 'source': '1', 'rela': '任职'},
    #          {'target': '8', 'source': '1', 'rela': '任职'}, {'target': '9', 'source': '1', 'rela': '产品'},
    #          {'target': '10', 'source': '1', 'rela': '产品'}, {'target': '11', 'source': '1', 'rela': '产品'},
    #          {'target': '12', 'source': '1', 'rela': '产品'}, {'target': '13', 'source': '1', 'rela': '产品'},
    #          {'target': '14', 'source': '1', 'rela': '产品'}, {'target': '15', 'source': '1', 'rela': '产品'},
    #          {'target': '16', 'source': '1', 'rela': '产品'}, {'target': '17', 'source': '1', 'rela': '产品'},
    #          {'target': '18', 'source': '1', 'rela': '产品'}, {'target': '19', 'source': '1', 'rela': '产品'},
    #          {'target': '20', 'source': '1', 'rela': '产品'}, {'target': '21', 'source': '1', 'rela': '产品'},
    #          {'target': '22', 'source': '1', 'rela': '产品'}, {'target': '23', 'source': '1', 'rela': '产品'},
    #          {'target': '24', 'source': '1', 'rela': '风险'}, {'target': '25', 'source': '1', 'rela': '风险'},
    #          {'target': '26', 'source': '1', 'rela': '风险'}, {'target': '27', 'source': '1', 'rela': '风险'},
    #          {'target': '28', 'source': '1', 'rela': '风险'}, {'target': '29', 'source': '1', 'rela': '风险'},
    #          {'target': '30', 'source': '1', 'rela': '风险'}, {'target': '31', 'source': '1', 'rela': '风险'},
    #          {'target': '32', 'source': '1', 'rela': '风险'}, {'target': '33', 'source': '1', 'rela': '风险'},
    #          {'target': '34', 'source': '1', 'rela': '风险'}, {'target': '35', 'source': '1', 'rela': '风险'},
    #          {'target': '36', 'source': '1', 'rela': '风险'}, {'target': '37', 'source': '1', 'rela': '风险'},
    #          {'target': '38', 'source': '1', 'rela': '风险'}, {'target': '39', 'source': '1', 'rela': '风险'},
    #          {'target': '40', 'source': '1', 'rela': '风险'}, {'target': '41', 'source': '1', 'rela': '风险'},
    #          {'target': '42', 'source': '1', 'rela': '风险'}, {'target': '43', 'source': '1', 'rela': '人员规模'},
    #          {'target': '44', 'source': '1', 'rela': '统一社会信用代码'},
    #          {'target': '45', 'source': '1', 'rela': '纳税人识别号'},
    #          {'target': '46', 'source': '1', 'rela': '注册资本'},
    #          {'target': '47', 'source': '1', 'rela': 'name'},
    #          {'target': '48', 'source': '1', 'rela': '营业期限'},
    #          {'target': '49', 'source': '1', 'rela': '成立日期'}
    #          ]
    # }
#     tmp_value_list = list(ret_info['t1_text'].values())
#     tmp_point = 1
#     for tmp_key in ret_info["t1_text"].keys():
#         if ret_info["t1_text"][tmp_key] in tmp_value_list[tmp_point:]:
#             ret_info["t1_text"][tmp_key]['name']+=" "*tmp_point
#             tmp_point += 1
#     ret_info["t1_text"] = str(ret_info["t1_text"]).replace("'", '"')
#     ret_info["t2_text"] = str(ret_info["t2_text"]).replace("'", '"')
#
#
#     response = JsonResponse(ret_info)
#     return response
# #
# #
# def show_graph_demo(request):
#     # 展示graph demo
#     return render(request, 'graph_index.html')
#
#
# def mytest(request):
#     return render(request, 'mytest.html')
