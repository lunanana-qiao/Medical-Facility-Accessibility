import json
from time import sleep

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as py
import math
import eve_data
import os
import xml.etree.ElementTree as ET

# 高德 Web 服务 API Key —— 从环境变量读取，勿硬编码
AMAP_KEY = os.environ.get("AMAP_KEY", "")


def gaode_dist():#高德获取两地距离
    key = AMAP_KEY
    # with open('C:\\Users\\HP\Desktop\毕设\数据\第二次最终数据\医疗\医疗坐标表.csv', 'rb') as f:
    #     result = chardet.detect(f.read())  # 读取一定量的数据进行编码检测
    # print(result)
    data = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\社区卫生服务中心.xls")#GB18030
    data2 = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\社区中心.xls")
    medical_place = data["名称"].tolist()

    medical_jing = data["经度"].tolist()
    medical_wei = data["纬度"].tolist()
    medical_door = data["年门诊"].tolist()
    medical_people = data["床位数"].tolist()
    medical_bed = data["卫生技"].tolist()
    medical_area = data["总建筑"].tolist()

    social_place = data2["Name"].tolist()
    social_people = data2["Total_popu"].tolist()
    social_people1 = data2["F0_14"].tolist()
    social_people2 = data2["F15_59"].tolist()
    social_people3 = data2["F60_and_ab"].tolist()
    social_people4 = data2["F65_and_ab"].tolist()
    social_people5 = data2["Local_rd"].tolist()
    social_jing = data2["Lng_WGS84"].tolist()
    social_wei= data2["Lat_WGS84"].tolist()
    with (open("两地距离.csv", "w", encoding="utf8")) as f:
        f.write("社区,社区经度,社区纬度,Total_popu,F0_14,F15_59,F60_and_ab,F65_and_ab,Local_rd,卫生服务中心,卫生服务中心经度,卫生服务中心纬度,建筑面积,门诊,卫生技,床位,距离,时间\n")
        for i in range(0, len(medical_place)):
            for j in range(0, len(social_place)):
                URL="https://restapi.amap.com/v3/direction/walking?origin=" \
                + str(social_jing[j]) + ',' + str(social_wei[j])\
                +"&destination="\
                +str(medical_jing[i])+','+str(medical_wei[i])+"&key="+key
                response = requests.get(url=URL)
                html_doc = response.text
                print(html_doc)
                    # 解析HTML文档
                decodejson = json.loads(html_doc)
                    # 提取数据
                result = decodejson.get('route').get('paths')[0]

                dis = result.get('distance')
                time_s = result.get('duration')
                re=(str(social_place[j]) + "," + str(social_jing[j]) + ',' + \
                        str(social_wei[j])  +","+ str(social_people[j])+','+ \
                    str(social_people1[j]) + ',' + \
                    str(social_people2[j]) + ',' + \
                    str(social_people3[j]) + ',' \
                    + str(social_people4[j]) + ',' \
                    + str(social_people5[j]) + ',' + \
                    str(medical_place[i])+','+str(medical_jing[i])+','+\
                        str(medical_wei[i])+','+str(medical_area[i])+','+ \
                    str(medical_door[i]) + ',' + str(medical_people[i]) + ',' + \
                    str(medical_bed[i]) + ',' +\
                    str(dis)+','+time_s+','+"\n")
                print(re)
                f.write(re)
                sleep(0.5)

#公平性计算
def gongping():
    py.rcParams['font.sans-serif'] = ['SimHei']
    py.rcParams['axes.unicode_minus'] = False

    data1 = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\\骑行街道到中心.xls")
    data2 = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\\骑行社区到中心.xls")
    data3 = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\公平性.xls")

    jiedao = eve_data.model(data1["求和项:people"].tolist(),data1["求和项:old_people"].tolist(),data1["求和项:s"].tolist())
    shequ = eve_data.model(data2["求和项:people"].tolist(),data2["求和项:old_people"].tolist(),data2["求和项:s"].tolist())
    pianqu = eve_data.model(data3["求和项:求和项:people"].tolist(), data3["求和项:求和项:old_people"].tolist(), data3["求和项:求和项:s"].tolist())

    eve=[jiedao,shequ,pianqu]
    for now in eve:
        for i in range(len(now.old_people)):
            now.sum_peo+=now.total_people[i]
            now.sum_old_peo+=now.old_people[i]
            now.SUM_S+=now.S[i]

    py.Figure()
    label_name=["居住社区生活圈公平性","居住社区生活圈老年群体公平性","基层社区生活圈公平性","基层社区生活圈老年群体公平性","片区社区生活圈公平性","片区社区生活圈老年群体公平性"]
    j=0
    for now_data in eve:
        S=now_data.S
        sumA=now_data.SUM_S
        peo=now_data.sum_peo
        now=0.
        x=0.
        X=0.
        z=[0]
        z2=[0]
        Y=0.
        for i in range(len(S)):
            new=S[i]/sumA
            now+=new
            x+=now_data.total_people[i]/peo
            Y+=now

            X+=x-now
            z.append(now)
            z2.append(x)

        gini=X/(X+Y)
        print(gini)

        py.title('可达性洛伦兹曲线')
        py.xlabel('人口占比')
        py.ylabel('医疗资源占比')
        if j==0:
            py.plot(z2, z2,'--',label='公平')
        py.plot(z2,z,label=label_name[j])

        py.legend()
        j+=1

#老年人口
        S = now_data.S
        sumA = now_data.SUM_S
        peo = now_data.sum_old_peo
        now = 0.
        x = 0.
        X = 0.
        z = [0]
        z2 = [0]
        Y = 0.
        for i in range(len(S)):
            new = S[i] / sumA
            now += new
            x += now_data.old_people[i] / peo
            Y += now
            X += x - now
            z.append(now)
            z2.append(x)

        gini = X / (X + Y)
        print(gini)

        py.title('可达性洛伦兹曲线')
        py.xlabel('人口占比')
        py.ylabel('医疗资源占比')
        py.plot(z2, z, label=label_name[j])
        j+=1
        py.legend()
    py.show()

def filter():
    key = AMAP_KEY
    data = pd.read_excel("C:\\Users\\HP\Desktop\候选点\优化选址.xls")  # GB18030
    infid = data["核心选址_GenerateNearTable.IN_FID"].tolist()
    nearfid = data["核心选址_GenerateNearTable.NEAR_FID"].tolist()
    name = data["核心选址.位置"].tolist()
    inx = data["核心选址.x"].tolist()
    iny = data["核心选址.y"].tolist()

    people = data["人口.grid_code"].tolist()

    lng = data["人口.x"].tolist()
    lat = data["人口.y"].tolist()
    with (open("筛选2.csv", "w", encoding="utf8")) as f:
        f.write(
            "IN_FID,NEAR_FID,起点,人口,时间\n")
        for j in range(0, len(infid)):
            URL = "https://restapi.amap.com/v3/direction/walking?origin=" \
                  + str(inx[j]) + ',' + str(iny[j]) \
                  + "&destination=" \
                  + str(lng[j]) + ',' + str(lat[j]) + "&key=" + key
            response = requests.get(url=URL)
            html_doc = response.text

            # 解析HTML文档
            decodejson = json.loads(html_doc)
            print(decodejson)
            # 提取数据
            if(decodejson!=None):
                result = decodejson.get('route').get('paths')[0]

                time_s = result.get('duration')
                if(int(time_s)<=900):
                    re = (str(infid[j]) + "," + str(nearfid[j]) + ',' + str(name[j]) + ',' +  str(people[j]) + ',' +str(time_s)+"\n")

                    f.write(re)
            sleep(1)

#社区卫生服务站
def filter2():
    key = AMAP_KEY

    data = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\服务站近邻表.xls")  # GB18030
    infid = data["IN_FID"].tolist()
    nearfid = data["NEAR_FID"].tolist()
    inx = data["社区卫生站.经度_WGS"].tolist()
    iny = data["社区卫生站.纬度_WGS"].tolist()
    lng = data["最终200渔网.Lng"].tolist()
    lat = data["最终200渔网.lat"].tolist()
    adj2020 = data["最终200渔网.adj_2020"].tolist()

    with (open("服务站筛选2.csv", "w", encoding="utf8")) as f:
        f.write(
            "IN_FID,NEAR_FID,中心城区社区医疗坐标点X,中心城区社区医疗坐标点Y,渔网Lng,渔网lat,adj_2020,距离,时间\n")
        for j in range(0, len(infid)):
            URL = "https://restapi.amap.com/v3/direction/walking?origin=" \
                  + str(inx[j]) + ',' + str(iny[j]) \
                  + "&destination=" \
                  + str(lng[j]) + ',' + str(lat[j]) + "&key=" + key
            response = requests.get(url=URL)
            html_doc = response.text

            # 解析HTML文档
            decodejson = json.loads(html_doc)
            # 提取数据
            result = decodejson.get('route').get('paths')[0]
            print(result)
            dis = result.get('distance')
            time_s = result.get('duration')
            re = (str(infid[j]) + "," + str(nearfid[j]) + ',' + \
                  str(inx[j]) + ',' + \
                  str(iny[j]) + ',' + \
          str(lng[j]) + ',' + str(lat[j])+','+\
                  str(adj2020[j])+','+
                  str(dis)+','+str(time_s)+"\n")

            f.write(re)
            sleep(0.5)

def gaosi_shequ():
    data = pd.read_excel("C:\\Users\HP\Desktop\要跑的\社区到中心.xls")  # GB18030
    infid = data["终点名称"].tolist()
    number = len(infid)
    #nearfid = data["NEAR_FID"].tolist()
    # inx = data["社区卫生站.经度_WGS"].tolist()
    # iny = data["社区卫生站.纬度_WGS"].tolist()
    # lng = data["最终200渔网.Lng"].tolist()
    # lat = data["最终200渔网.lat"].tolist()

    adj = data["people"].tolist()
    oldadj = data["old_people"].tolist()
    dist = data["耗时_秒_"].tolist()
   # bed =data["床位数"].tolist()
    people = data["s"].tolist()
    #door = data["年门诊"].tolist()
    #area= data["建筑面积"].tolist()
    print("---------数据加载完成-----------")
    G=[]
    GR=[]
    oGR = []
    yuzhi = 900.
    #计算GR
    for i in range(number) :
        tem = ((math.exp(-0.5 * (dist[i] / yuzhi)* (dist[i] / yuzhi)) - math.exp(-0.5)) / (1 - math.exp(-0.5)))
        G.append(tem)
        GR.append(tem*adj[i])
        oGR.append(tem*oldadj[i])
    print("---------GR计算完成-----------")
    dict={}
    for i in range(number):
        if(dict.get(infid[i])==None):
            dict[infid[i]]=eve_data.Eve_medical_data(infid[i],people[i])
            dict[infid[i]].SUM_GR+=GR[i]
            dict[infid[i]].oSUM_GR+=oGR[i]
        else:
            dict[infid[i]].SUM_GR += GR[i]
            dict[infid[i]].oSUM_GR += oGR[i]

    for i in dict.values():

        i.A_people=i.S_people/i.SUM_GR
        i.oA_people = i.S_people / i.oSUM_GR

    #    # print(i.A_bed)】

    print("---------供需比计算完成-----------")
    data2 = pd.read_excel("C:\\Users\HP\Desktop\要跑的\社区到中心.xls") # GB18030
    nearfid2 = data2["起点名称"].tolist()

    infid2 = data2["终点名称"].tolist()
    number2 = len(infid2)
    dist2 = data2["耗时_秒_"].tolist()
    G2 = []
    # 计算GR
    for i in range(number2):
        tem = ((math.exp(-0.5 * (dist2[i] / yuzhi) * (dist2[i] / yuzhi)) - math.exp(-0.5)) / (1 - math.exp(-0.5)))
        G2.append(tem)
    dict2={}
    for i in range(number2):
        if (dict2.get(nearfid2[i]) == None):
            dict2[nearfid2[i]] = eve_data.Eve_social_data(nearfid2[i])

            dict2[nearfid2[i]].SUM_GR_people += G2[i] * dict[infid2[i]].A_people
            dict2[nearfid2[i]].oSUM_GR_people += G2[i] * dict[infid2[i]].oA_people

        else:

            dict2[nearfid2[i]].SUM_GR_people += G2[i] * dict[infid2[i]].A_people
            dict2[nearfid2[i]].oSUM_GR_people += G2[i] * dict[infid2[i]].oA_people


    print("---------可达性计算完成-----------")
    with (open("高斯计算结果社区——质心.csv", "w", encoding="utf8")) as f:
        f.write(
            "FID,people,old_people\n")
        for j in dict2.values():
            re = (str(j.social_id) + ","+
                  str(j.SUM_GR_people) +","+
                  str(j.oSUM_GR_people) +  "\n")
            f.write(re)
            print(re)
def gaosi_jiedao():
    data = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\街道到中心.xls")  # GB18030
    infid = data["终点名称"].tolist()
    number = len(infid)
    #nearfid = data["NEAR_FID"].tolist()
    # inx = data["社区卫生站.经度_WGS"].tolist()
    # iny = data["社区卫生站.纬度_WGS"].tolist()
    # lng = data["最终200渔网.Lng"].tolist()
    # lat = data["最终200渔网.lat"].tolist()

    adj = data["people"].tolist()
    oldadj = data["old_people"].tolist()
    dist = data["耗时_秒_"].tolist()
   # bed =data["床位数"].tolist()
    people = data["s"].tolist()
    #door = data["年门诊"].tolist()
    #area= data["建筑面积"].tolist()
    print("---------数据加载完成-----------")
    G=[]
    GR=[]
    oGR = []
    yuzhi = 900.
    #计算GR
    for i in range(number) :
        tem = ((math.exp(-0.5 * (dist[i] / yuzhi)* (dist[i] / yuzhi)) - math.exp(-0.5)) / (1 - math.exp(-0.5)))
        G.append(tem)
        GR.append(tem*adj[i])
        oGR.append(tem*oldadj[i])
    print("---------GR计算完成-----------")
    dict={}
    for i in range(number):
        if(dict.get(infid[i])==None):
            dict[infid[i]]=eve_data.Eve_medical_data(infid[i],people[i])
            dict[infid[i]].SUM_GR+=GR[i]
            dict[infid[i]].oSUM_GR+=oGR[i]
        else:
            dict[infid[i]].SUM_GR += GR[i]
            dict[infid[i]].oSUM_GR += oGR[i]

    for i in dict.values():

        i.A_people=i.S_people/i.SUM_GR
        i.oA_people = i.S_people / i.oSUM_GR

    print("---------供需比计算完成-----------")
    data2 = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\街道到中心.xls") # GB18030
    nearfid2 = data2["起点名称"].tolist()

    infid2 = data2["终点名称"].tolist()
    number2 = len(infid2)
    dist2 = data2["耗时_秒_"].tolist()
    G2 = []
    # 计算GR
    for i in range(number2):
        tem = ((math.exp(-0.5 * (dist2[i] / yuzhi) * (dist2[i] / yuzhi)) - math.exp(-0.5)) / (1 - math.exp(-0.5)))
        G2.append(tem)
    dict2={}
    for i in range(number2):
        if (dict2.get(nearfid2[i]) == None):
            dict2[nearfid2[i]] = eve_data.Eve_social_data(nearfid2[i])

            dict2[nearfid2[i]].SUM_GR_people += G2[i] * dict[infid2[i]].A_people
            dict2[nearfid2[i]].oSUM_GR_people += G2[i] * dict[infid2[i]].oA_people

        else:

            dict2[nearfid2[i]].SUM_GR_people += G2[i] * dict[infid2[i]].A_people
            dict2[nearfid2[i]].oSUM_GR_people += G2[i] * dict[infid2[i]].oA_people


    print("---------可达性计算完成-----------")
    with (open("高斯计算结果街道——质心.csv", "w", encoding="utf8")) as f:
        f.write(
            "FID,people,old_people\n")
        for j in dict2.values():
            re = (str(j.social_id) + ","+
                  str(j.SUM_GR_people) +","+
                  str(j.oSUM_GR_people) +  "\n")
            f.write(re)
            print(re)
def gaosi_qixing_shequ():
    data = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\骑行社区到中心.xls")  # GB18030
    infid = data["终点名称"].tolist()
    number = len(infid)
    #nearfid = data["NEAR_FID"].tolist()
    # inx = data["社区卫生站.经度_WGS"].tolist()
    # iny = data["社区卫生站.纬度_WGS"].tolist()
    # lng = data["最终200渔网.Lng"].tolist()
    # lat = data["最终200渔网.lat"].tolist()

    adj = data["people"].tolist()
    oldadj = data["old_people"].tolist()
    dist = data["耗时_秒_"].tolist()
   # bed =data["床位数"].tolist()
    people = data["s"].tolist()
    #door = data["年门诊"].tolist()
    #area= data["建筑面积"].tolist()
    print("---------数据加载完成-----------")
    G=[]
    GR=[]
    oGR = []
    yuzhi = 900.
    #计算GR
    for i in range(number) :
        tem = ((math.exp(-0.5 * (dist[i] / yuzhi)* (dist[i] / yuzhi)) - math.exp(-0.5)) / (1 - math.exp(-0.5)))
        G.append(tem)
        GR.append(tem*adj[i])
        oGR.append(tem*oldadj[i])
    print("---------GR计算完成-----------")
    dict={}
    for i in range(number):
        if(dict.get(infid[i])==None):
            dict[infid[i]]=eve_data.Eve_medical_data(infid[i],people[i])
            dict[infid[i]].SUM_GR+=GR[i]
            dict[infid[i]].oSUM_GR+=oGR[i]
        else:
            dict[infid[i]].SUM_GR += GR[i]
            dict[infid[i]].oSUM_GR += oGR[i]

    for i in dict.values():

        i.A_people=i.S_people/i.SUM_GR
        i.oA_people = i.S_people / i.oSUM_GR


    print("---------供需比计算完成-----------")
    data2 = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\骑行社区到中心.xls") # GB18030
    nearfid2 = data2["起点名称"].tolist()

    infid2 = data2["终点名称"].tolist()
    number2 = len(infid2)
    dist2 = data2["耗时_秒_"].tolist()
    G2 = []
    # 计算GR
    for i in range(number2):
        tem = ((math.exp(-0.5 * (dist2[i] / yuzhi) * (dist2[i] / yuzhi)) - math.exp(-0.5)) / (1 - math.exp(-0.5)))
        G2.append(tem)
    dict2={}
    for i in range(number2):
        if (dict2.get(nearfid2[i]) == None):
            dict2[nearfid2[i]] = eve_data.Eve_social_data(nearfid2[i])

            dict2[nearfid2[i]].SUM_GR_people += G2[i] * dict[infid2[i]].A_people
            dict2[nearfid2[i]].oSUM_GR_people += G2[i] * dict[infid2[i]].oA_people

        else:

            dict2[nearfid2[i]].SUM_GR_people += G2[i] * dict[infid2[i]].A_people
            dict2[nearfid2[i]].oSUM_GR_people += G2[i] * dict[infid2[i]].oA_people


    print("---------可达性计算完成-----------")
    with (open("高斯计算结果社区骑行.csv", "w", encoding="utf8")) as f:
        f.write(
            "FID,people,old_people\n")
        for j in dict2.values():
            re = (str(j.social_id) + ","+
                  str(j.SUM_GR_people) +","+
                  str(j.oSUM_GR_people) +  "\n")
            f.write(re)
            print(re)
def gaosi_qixing_jiedao():
    data = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\骑行街道到中心.xls")  # GB18030
    infid = data["终点名称"].tolist()
    number = len(infid)

    adj = data["people"].tolist()
    oldadj = data["old_people"].tolist()
    dist = data["耗时_秒_"].tolist()
   # bed =data["床位数"].tolist()
    people = data["s"].tolist()
    #door = data["年门诊"].tolist()
    #area= data["建筑面积"].tolist()
    print("---------数据加载完成-----------")
    G=[]
    GR=[]
    oGR = []
    yuzhi = 900.
    #计算GR
    for i in range(number) :
        tem = ((math.exp(-0.5 * (dist[i] / yuzhi)* (dist[i] / yuzhi)) - math.exp(-0.5)) / (1 - math.exp(-0.5)))
        G.append(tem)
        GR.append(tem*adj[i])
        oGR.append(tem*oldadj[i])
    print("---------GR计算完成-----------")
    dict={}
    for i in range(number):
        if(dict.get(infid[i])==None):
            dict[infid[i]]=eve_data.Eve_medical_data(infid[i],people[i])
            dict[infid[i]].SUM_GR+=GR[i]
            dict[infid[i]].oSUM_GR+=oGR[i]
        else:
            dict[infid[i]].SUM_GR += GR[i]
            dict[infid[i]].oSUM_GR += oGR[i]

    for i in dict.values():

        i.A_people=i.S_people/i.SUM_GR
        i.oA_people = i.S_people / i.oSUM_GR

    print("---------供需比计算完成-----------")
    data2 = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\骑行街道到中心.xls") # GB18030
    nearfid2 = data2["起点名称"].tolist()

    infid2 = data2["终点名称"].tolist()
    number2 = len(infid2)
    dist2 = data2["耗时_秒_"].tolist()
    G2 = []
    # 计算GR
    for i in range(number2):
        tem = ((math.exp(-0.5 * (dist2[i] / yuzhi) * (dist2[i] / yuzhi)) - math.exp(-0.5)) / (1 - math.exp(-0.5)))
        G2.append(tem)
    dict2={}
    for i in range(number2):
        if (dict2.get(nearfid2[i]) == None):
            dict2[nearfid2[i]] = eve_data.Eve_social_data(nearfid2[i])

            dict2[nearfid2[i]].SUM_GR_people += G2[i] * dict[infid2[i]].A_people
            dict2[nearfid2[i]].oSUM_GR_people += G2[i] * dict[infid2[i]].oA_people

        else:

            dict2[nearfid2[i]].SUM_GR_people += G2[i] * dict[infid2[i]].A_people
            dict2[nearfid2[i]].oSUM_GR_people += G2[i] * dict[infid2[i]].oA_people


    print("---------可达性计算完成-----------")
    with (open("高斯计算结果街道骑行.csv", "w", encoding="utf8")) as f:
        f.write(
            "FID,people,old_people\n")
        for j in dict2.values():
            re = (str(j.social_id) + ","+
                  str(j.SUM_GR_people) +","+
                  str(j.oSUM_GR_people) +  "\n")
            f.write(re)
            print(re)

def serve_people():
    # region 初始化
    data = pd.read_excel("C:\\Users\HP\Desktop\要跑的\基本表\片区人口.xlsx")  # GB18030
    pianqu = data["name"].tolist()
    number = len(pianqu)
    adj = data["grid_code人数"].tolist()
    old_adj = data["old_people"].tolist()
    pointid = data["pointid"].tolist()

    data = pd.read_excel("C:\\Users\HP\Desktop\要跑的\基本表\人口.xlsx")  # GB18030
    jiedao = data["街道名"].tolist()
    shequ = data["社区名"].tolist()
    number_zong = len(jiedao)
    adj_zong = data["grid_code人数"].tolist()
    old_adj_zong = (data["old_people"].tolist())
    pointid_zong = data["pointid"].tolist()

    center = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\serve\中心等时圈.xls")
    center_adj = center["grid_code人数"].tolist()
    center_old_adj = center["old_people"].tolist()
    number_center = len(center_adj)
    center_pointid = center["pointid"].tolist()
    center_jiedao = center["街道名"].tolist()
    center_shequ = center["社区名"].tolist()
    center_time = center["耗时_秒_"].tolist()

    zhan = pd.read_excel("C:\\Users\\HP\Desktop\要跑的\serve\站等时圈.xls")
    zhan_adj = zhan["grid_code人数"].tolist()
    zhan_old_adj= zhan["old_people"].tolist()
    number_zhan = len(zhan_adj)
    zhan_pointid = zhan["pointid"].tolist()
    zhan_jiedao = zhan["街道名"].tolist()
    zhan_shequ = zhan["社区名"].tolist()
    zhan_time = zhan["耗时_秒_"].tolist()

    dict_pianqu={}
    dict_jiedao={}
    dict_shequ={}

    aready_point_center_15=set()
    aready_point_zhan_15 = set()
    aready_point_center_10 = set()
    aready_point_zhan_10 = set()
    aready_point_center_5 = set()
    aready_point_zhan_5 = set()
    # endregion
    print("----------加载完毕-----------")
    # region 中心的计算
    for i in range(number_center):

        if not (center_shequ[i] in dict_shequ):
            dict_shequ[center_shequ[i]]=eve_data.shequ(center_shequ[i])
            if center_time[i]<=300:
                dict_shequ[center_shequ[i]].serve_people_center_5+=center_adj[i]
                dict_shequ[center_shequ[i]].serve_old_people_center_5 += center_old_adj[i]

            if center_time[i]<=600:
                dict_shequ[center_shequ[i]].serve_people_center_10 += center_adj[i]
                dict_shequ[center_shequ[i]].serve_old_people_center_10 += center_old_adj[i]
            dict_shequ[center_shequ[i]].serve_people_center_15 += center_adj[i]
            dict_shequ[center_shequ[i]].serve_old_people_center_15 += center_old_adj[i]
        else:
            if center_time[i] <= 300:
                dict_shequ[center_shequ[i]].serve_people_center_5 += center_adj[i]
                dict_shequ[center_shequ[i]].serve_old_people_center_5 += center_old_adj[i]

            if center_time[i] <= 600:
                dict_shequ[center_shequ[i]].serve_people_center_10 += center_adj[i]
                dict_shequ[center_shequ[i]].serve_old_people_center_10 += center_old_adj[i]
            dict_shequ[center_shequ[i]].serve_people_center_15 += center_adj[i]
            dict_shequ[center_shequ[i]].serve_old_people_center_15 += center_old_adj[i]

        if not (center_jiedao[i] in dict_jiedao):
            dict_jiedao[center_jiedao[i]]=eve_data.jiedao(center_jiedao[i])
            if center_time[i] <= 300:
                dict_jiedao[center_jiedao[i]].serve_people_center_5 += center_adj[i]
                dict_jiedao[center_jiedao[i]].serve_old_people_center_5 += center_old_adj[i]
            if center_time[i] <= 600:
                dict_jiedao[center_jiedao[i]].serve_people_center_10 += center_adj[i]
                dict_jiedao[center_jiedao[i]].serve_old_people_center_10 += center_old_adj[i]
            dict_jiedao[center_jiedao[i]].serve_people_center_15 += center_adj[i]
            dict_jiedao[center_jiedao[i]].serve_old_people_center_15 += center_old_adj[i]

        else:
            if center_time[i] <= 300:
                dict_jiedao[center_jiedao[i]].serve_people_center_5 += center_adj[i]
                dict_jiedao[center_jiedao[i]].serve_old_people_center_5 += center_old_adj[i]
            if center_time[i] <= 600:
                dict_jiedao[center_jiedao[i]].serve_people_center_10 += center_adj[i]
                dict_jiedao[center_jiedao[i]].serve_old_people_center_10 += center_old_adj[i]
            dict_jiedao[center_jiedao[i]].serve_people_center_15 += center_adj[i]
            dict_jiedao[center_jiedao[i]].serve_old_people_center_15 += center_old_adj[i]

        #set
        if center_time[i] <= 300:
            aready_point_center_5.add(center_pointid[i])
        if center_time[i] <= 600:
            aready_point_center_10.add(center_pointid[i])
        aready_point_center_15.add(center_pointid[i])
    # endregion
    print("----------中心计算完毕-----------")
    #region 站计算
    for i in range(number_zhan):
        if not (zhan_shequ[i] in dict_shequ):
            dict_shequ[zhan_shequ[i]] = eve_data.shequ(zhan_shequ[i])
            if zhan_time[i] <= 300:
                dict_shequ[zhan_shequ[i]].serve_people_zhan_5 += zhan_adj[i]
                dict_shequ[zhan_shequ[i]].serve_old_people_zhan_5 += zhan_old_adj[i]
            if zhan_time[i] <= 600:
                dict_shequ[zhan_shequ[i]].serve_people_zhan_10 += zhan_adj[i]
                dict_shequ[zhan_shequ[i]].serve_old_people_zhan_10 += zhan_old_adj[i]
            dict_shequ[zhan_shequ[i]].serve_people_zhan_15 += zhan_adj[i]
            dict_shequ[zhan_shequ[i]].serve_old_people_zhan_15 += zhan_old_adj[i]
        else:
            if zhan_time[i] <= 300:
                dict_shequ[zhan_shequ[i]].serve_people_zhan_5 += zhan_adj[i]
                dict_shequ[zhan_shequ[i]].serve_old_people_zhan_5 += zhan_old_adj[i]
            if zhan_time[i] <= 600:
                dict_shequ[zhan_shequ[i]].serve_people_zhan_10 += zhan_adj[i]
                dict_shequ[zhan_shequ[i]].serve_old_people_zhan_10 += zhan_old_adj[i]
            dict_shequ[zhan_shequ[i]].serve_people_zhan_15 += zhan_adj[i]
            dict_shequ[zhan_shequ[i]].serve_old_people_zhan_15 += zhan_old_adj[i]

        if not (zhan_jiedao[i] in dict_jiedao):
            dict_jiedao[zhan_jiedao[i]] = eve_data.jiedao(zhan_jiedao[i])
            if zhan_time[i] <= 300:
                dict_jiedao[zhan_jiedao[i]].serve_people_zhan_5 += zhan_adj[i]
                dict_jiedao[zhan_jiedao[i]].serve_old_people_zhan_5 += zhan_old_adj[i]
            if zhan_time[i] <= 600:
                dict_jiedao[zhan_jiedao[i]].serve_people_zhan_10 += zhan_adj[i]
                dict_jiedao[zhan_jiedao[i]].serve_old_people_zhan_10 += zhan_old_adj[i]
            dict_jiedao[zhan_jiedao[i]].serve_people_zhan_15 += zhan_adj[i]
            dict_jiedao[zhan_jiedao[i]].serve_old_people_zhan_15 += zhan_old_adj[i]

        else:
            if zhan_time[i] <= 300:
                dict_jiedao[zhan_jiedao[i]].serve_people_zhan_5 += zhan_adj[i]
                dict_jiedao[zhan_jiedao[i]].serve_old_people_zhan_5 += zhan_old_adj[i]
            if zhan_time[i] <= 600:
                dict_jiedao[zhan_jiedao[i]].serve_people_zhan_10 += zhan_adj[i]
                dict_jiedao[zhan_jiedao[i]].serve_old_people_zhan_10 += zhan_old_adj[i]
            dict_jiedao[zhan_jiedao[i]].serve_people_zhan_15 += zhan_adj[i]
            dict_jiedao[zhan_jiedao[i]].serve_old_people_zhan_15 += zhan_old_adj[i]
            # set
        if zhan_time[i] <= 300:
            aready_point_zhan_5.add(zhan_pointid[i])
        if zhan_time[i] <= 600:
            aready_point_zhan_10.add(zhan_pointid[i])
        aready_point_zhan_15.add(zhan_pointid[i])


              # endregion
    print("----------站计算完毕-----------")
    # region 片区计算
    for i in range(number):
        if pointid[i] in aready_point_center_5:
            if (dict_pianqu.get(pianqu[i]) == None):
                dict_pianqu[pianqu[i]] = eve_data.pianqu(pianqu[i])
                dict_pianqu[pianqu[i]].serve_people_center_5 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_center_5 += old_adj[i]
            else:
                dict_pianqu[pianqu[i]].serve_people_center_5 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_center_5 += old_adj[i]

        if pointid[i] in aready_point_center_10:
            if (dict_pianqu.get(pianqu[i]) == None):
                dict_pianqu[pianqu[i]] = eve_data.pianqu(pianqu[i])
                dict_pianqu[pianqu[i]].serve_people_center_10 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_center_10 += old_adj[i]

            else:
                dict_pianqu[pianqu[i]].serve_people_center_10 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_center_10 += old_adj[i]

        if pointid[i] in aready_point_center_15:
            if (dict_pianqu.get(pianqu[i]) == None):
                dict_pianqu[pianqu[i]] = eve_data.pianqu(pianqu[i])

                dict_pianqu[pianqu[i]].serve_people_center_15+=adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_center_15 += old_adj[i]
            else:
                dict_pianqu[pianqu[i]].serve_people_center_15 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_center_15 += old_adj[i]
        if pointid[i] in aready_point_zhan_5:
            if (dict_pianqu.get(pianqu[i]) == None):
                dict_pianqu[pianqu[i]] = eve_data.pianqu(pianqu[i])
                dict_pianqu[pianqu[i]].serve_people_zhan_5 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_zhan_5 += old_adj[i]
            else:
                dict_pianqu[pianqu[i]].serve_people_zhan_5 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_zhan_5 += old_adj[i]
        if pointid[i] in aready_point_zhan_10:
            if (dict_pianqu.get(pianqu[i]) == None):
                dict_pianqu[pianqu[i]] = eve_data.pianqu(pianqu[i])
                dict_pianqu[pianqu[i]].serve_people_zhan_10 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_zhan_10 += old_adj[i]
            else:
                dict_pianqu[pianqu[i]].serve_people_zhan_10 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_zhan_10 += old_adj[i]
        if pointid[i] in aready_point_zhan_15:
            if (dict_pianqu.get(pianqu[i]) == None):
                dict_pianqu[pianqu[i]] = eve_data.pianqu(pianqu[i])
                dict_pianqu[pianqu[i]].serve_people_zhan_15 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_zhan_15 += old_adj[i]
            else:
                dict_pianqu[pianqu[i]].serve_people_zhan_15 += adj[i]
                dict_pianqu[pianqu[i]].serve_old_people_zhan_15 += old_adj[i]

#总人口
        if pianqu[i] in dict_pianqu:
            dict_pianqu[pianqu[i]].sum_people += adj[i]
            dict_pianqu[pianqu[i]].sum_old_people += old_adj[i]
        else:
            dict_pianqu[pianqu[i]] = eve_data.pianqu(pianqu[i])
            dict_pianqu[pianqu[i]].sum_people += adj[i]
            dict_pianqu[pianqu[i]].sum_old_people += old_adj[i]
#联合服务
        if (pointid[i] in aready_point_center_15) or (pointid[i] in aready_point_zhan_15):
            dict_pianqu[pianqu[i]].serve_people_15 += adj[i]
            dict_pianqu[pianqu[i]].serve_old_people_15 += old_adj[i]
        if (pointid[i] in aready_point_center_10) or (pointid[i] in aready_point_zhan_10):
            dict_pianqu[pianqu[i]].serve_people_10 += adj[i]
            dict_pianqu[pianqu[i]].serve_old_people_10 += old_adj[i]
        if (pointid[i] in aready_point_center_5) or (pointid[i] in aready_point_zhan_5):
            dict_pianqu[pianqu[i]].serve_people_5 += adj[i]
            dict_pianqu[pianqu[i]].serve_old_people_5 += old_adj[i]
    with (open("片区服务率5.csv", "w", encoding="utf8")) as f:
        f.write(
            "name,总人数,总老年人数,总服务人数5,总服务人数10,总服务人数15,卫生中心服务人数5,卫生中心服务人数10,卫生中心服务人数15,卫生服务站服务人数5,卫生服务站服务人数10,卫生服务站服务人数15,总服务老年人数5,总服务老年人数10,总服务老年人数15,卫生中心服务老年人数5,卫生中心服务老年人数10,卫生中心服务老年人数15,卫生服务站服务老年人数5,卫生服务站服务老年人数10,卫生服务站服务老年人数15,总服务人数5服务率,总服务人数10服务率,总服务人数15服务率,卫生中心服务人数5服务率,卫生中心服务人数10服务率,卫生中心服务人数15服务率,卫生服务站服务人数5服务率,卫生服务站服务人数10服务率,卫生服务站服务人数15服务率,总服务老年人数5服务率,总服务老年人数10服务率,总服务老年人数15服务率,卫生中心服务老年人数5服务率,卫生中心服务老年人数10服务率,卫生中心服务老年人数15服务率,卫生服务站服务老年人数5服务率,卫生服务站服务老年人数10服务率,卫生服务站服务老年人数15服务率\n")
        for j in dict_pianqu.values():
            re = (str(j.name) + ","+
                  str(j.sum_people) +","+str(j.sum_old_people) +","+
                  str(j.serve_people_5) +","+ str(j.serve_people_10) +","+str(j.serve_people_15) +","+
            str(j.serve_people_center_5) +","+str(j.serve_people_center_10) +","+str(j.serve_people_center_15) +","+
                  str(j.serve_people_zhan_5) +","+str(j.serve_people_zhan_10) +","+str(j.serve_people_zhan_15) +","+
                  str(j.serve_old_people_5) +","+ str(j.serve_old_people_10) +","+str(j.serve_old_people_15) +","+
            str(j.serve_old_people_center_5) +","+str(j.serve_old_people_center_10) +","+str(j.serve_old_people_center_15) +","+
                  str(j.serve_old_people_zhan_5) +","+str(j.serve_old_people_zhan_10) +","+str(j.serve_old_people_zhan_15) +","+

                  str(j.serve_people_5/j.sum_people) +","+ str(j.serve_people_10/j.sum_people) +","+str(j.serve_people_15/j.sum_people) +","+
            str(j.serve_people_center_5/j.sum_people) +","+str(j.serve_people_center_10/j.sum_people) +","+str(j.serve_people_center_15/j.sum_people) +","+
                  str(j.serve_people_zhan_5/j.sum_people) +","+str(j.serve_people_zhan_10/j.sum_people) +","+str(j.serve_people_zhan_15/j.sum_people) +","+
                  str(j.serve_old_people_5/j.sum_old_people) +","+ str(j.serve_old_people_10/j.sum_old_people) +","+str(j.serve_old_people_15/j.sum_old_people) +","+
            str(j.serve_old_people_center_5/j.sum_old_people) +","+str(j.serve_old_people_center_10/j.sum_old_people) +","+str(j.serve_old_people_center_15/j.sum_old_people) +","+
                  str(j.serve_old_people_zhan_5/j.sum_old_people) +","+str(j.serve_old_people_zhan_10/j.sum_old_people) +","+str(j.serve_old_people_zhan_15/j.sum_old_people) +"\n")
            f.write(re)
    print("----------pianqu计算完毕-----------")
    # endregion

    # region 总人数计算
    for i in range(number_zong):

        # region总人口
        if shequ[i] in dict_shequ:
            if not (dict_shequ.get(shequ[i]) == None):
                dict_shequ[shequ[i]].sum_people += adj_zong[i]
                dict_shequ[shequ[i]].sum_old_people += old_adj_zong[i]
            else:
                dict_shequ[shequ[i]] = eve_data.shequ(shequ[i])
                dict_shequ[shequ[i]].sum_people += adj_zong[i]
                dict_shequ[shequ[i]].sum_old_people += old_adj_zong[i]
        # 联合服务
        if (pointid_zong[i] in aready_point_center_15) or (pointid_zong[i] in aready_point_zhan_15):
            dict_shequ[shequ[i]].serve_people_15 += adj_zong[i]
            dict_shequ[shequ[i]].serve_old_people_15 += old_adj_zong[i]
        if (pointid_zong[i] in aready_point_center_10) or (pointid_zong[i] in aready_point_zhan_10):
            dict_shequ[shequ[i]].serve_people_10 += adj_zong[i]
            dict_shequ[shequ[i]].serve_old_people_10 += old_adj_zong[i]
        if (pointid_zong[i] in aready_point_center_5) or (pointid_zong[i] in aready_point_zhan_5):
            dict_shequ[shequ[i]].serve_people_5 += adj_zong[i]
            dict_shequ[shequ[i]].serve_old_people_5 += old_adj_zong[i]

        if jiedao[i] in dict_jiedao:
            if not (dict_jiedao.get(jiedao[i]) == None):
                dict_jiedao[jiedao[i]].sum_people += adj_zong[i]
                dict_jiedao[jiedao[i]].sum_old_people += old_adj_zong[i]
            else:
                dict_jiedao[jiedao[i]] = eve_data.jiedao(jiedao[i])
                dict_jiedao[jiedao[i]].sum_people += adj_zong[i]
                dict_jiedao[jiedao[i]].sum_old_people += old_adj_zong[i]
        if (pointid_zong[i] in aready_point_center_15) or (pointid_zong[i] in aready_point_zhan_15):
            dict_jiedao[jiedao[i]].serve_people_15 += adj_zong[i]
            dict_jiedao[jiedao[i]].serve_old_people_15 += old_adj_zong[i]
        if (pointid_zong[i] in aready_point_center_10) or (pointid_zong[i] in aready_point_zhan_10):
            dict_jiedao[jiedao[i]].serve_people_10 += adj_zong[i]
            dict_jiedao[jiedao[i]].serve_old_people_10 += old_adj_zong[i]
        if (pointid_zong[i] in aready_point_center_5) or (pointid_zong[i] in aready_point_zhan_5):
            dict_jiedao[jiedao[i]].serve_people_5 += adj_zong[i]
            dict_jiedao[jiedao[i]].serve_old_people_5 += old_adj_zong[i]

        # endregion
    with (open("街道服务率5.csv", "w", encoding="utf8")) as f:
        f.write(
            "name,总人数,总老年人数,总服务人数5,总服务人数10,总服务人数15,卫生中心服务人数5,卫生中心服务人数10,卫生中心服务人数15,卫生服务站服务人数5,卫生服务站服务人数10,卫生服务站服务人数15,总服务老年人数5,总服务老年人数10,总服务老年人数15,卫生中心服务老年人数5,卫生中心服务老年人数10,卫生中心服务老年人数15,卫生服务站服务老年人数5,卫生服务站服务老年人数10,卫生服务站服务老年人数15,总服务人数5服务率,总服务人数10服务率,总服务人数15服务率,卫生中心服务人数5服务率,卫生中心服务人数10服务率,卫生中心服务人数15服务率,卫生服务站服务人数5服务率,卫生服务站服务人数10服务率,卫生服务站服务人数15服务率,总服务老年人数5服务率,总服务老年人数10服务率,总服务老年人数15服务率,卫生中心服务老年人数5服务率,卫生中心服务老年人数10服务率,卫生中心服务老年人数15服务率,卫生服务站服务老年人数5服务率,卫生服务站服务老年人数10服务率,卫生服务站服务老年人数15服务率\n")
        for j in dict_jiedao.values():
            if(j.sum_people==0 or j.sum_old_people==0):
                re = (str(j.name) + "," + "," + "," +
                      str(j.serve_people_5) + "," + str(j.serve_people_10) + "," + str(j.serve_people_15) + "," +
                      str(j.serve_people_center_5) + "," + str(j.serve_people_center_10) + "," + str(
                            j.serve_people_center_15) + "," +
                      str(j.serve_people_zhan_5) + "," + str(j.serve_people_zhan_10) + "," + str(
                            j.serve_people_zhan_15) +","+
                      str(j.serve_old_people_5) + "," + str(j.serve_old_people_10) + "," + str(
                            j.serve_old_people_15) + "," +
                      str(j.serve_old_people_center_5) + "," + str(j.serve_old_people_center_10) + "," + str(
                            j.serve_old_people_center_15) + "," +
                      str(j.serve_old_people_zhan_5) + "," + str(j.serve_old_people_zhan_10) + "," + str(
                            j.serve_old_people_zhan_15) + "\n")
            else:
                re = (str(j.name) + "," +
                      str(j.sum_people) + "," + str(j.sum_old_people) + "," +
                      str(j.serve_people_5) + "," + str(j.serve_people_10) + "," + str(j.serve_people_15) + "," +
                      str(j.serve_people_center_5) + "," + str(j.serve_people_center_10) + "," + str(
                            j.serve_people_center_15) + "," +
                      str(j.serve_people_zhan_5) + "," + str(j.serve_people_zhan_10) + "," + str(
                            j.serve_people_zhan_15) + "," +
                      str(j.serve_old_people_5) + "," + str(j.serve_old_people_10) + "," + str(
                            j.serve_old_people_15) + "," +
                      str(j.serve_old_people_center_5) + "," + str(j.serve_old_people_center_10) + "," + str(
                            j.serve_old_people_center_15) + "," +
                      str(j.serve_old_people_zhan_5) + "," + str(j.serve_old_people_zhan_10) + "," + str(
                            j.serve_old_people_zhan_15) + "," +

                      str(j.serve_people_5 / j.sum_people) + "," + str(j.serve_people_10 / j.sum_people) + "," + str(
                            j.serve_people_15 / j.sum_people) + "," +
                      str(j.serve_people_center_5 / j.sum_people) + "," + str(
                            j.serve_people_center_10 / j.sum_people) + "," + str(
                            j.serve_people_center_15 / j.sum_people) + "," +
                      str(j.serve_people_zhan_5 / j.sum_people) + "," + str(
                            j.serve_people_zhan_10 / j.sum_people) + "," + str(
                            j.serve_people_zhan_15 / j.sum_people) + "," +
                      str(j.serve_old_people_5 / j.sum_old_people) + "," + str(
                            j.serve_old_people_10 / j.sum_old_people) + "," + str(
                            j.serve_old_people_15 / j.sum_old_people) + "," +
                      str(j.serve_old_people_center_5 / j.sum_old_people) + "," + str(
                            j.serve_old_people_center_10 / j.sum_old_people) + "," + str(
                            j.serve_old_people_center_15 / j.sum_old_people) + "," +
                      str(j.serve_old_people_zhan_5 / j.sum_old_people) + "," + str(
                            j.serve_old_people_zhan_10 / j.sum_old_people) + "," + str(
                            j.serve_old_people_zhan_15 / j.sum_old_people) + "\n")
            f.write(re)
    with (open("社区服务率5.csv", "w", encoding="utf8")) as f:
        f.write("name,总人数,总老年人数,总服务人数5,总服务人数10,总服务人数15,卫生中心服务人数5,卫生中心服务人数10,卫生中心服务人数15,卫生服务站服务人数5,卫生服务站服务人数10,卫生服务站服务人数15,总服务老年人数5,总服务老年人数10,总服务老年人数15,卫生中心服务老年人数5,卫生中心服务老年人数10,卫生中心服务老年人数15,卫生服务站服务老年人数5,卫生服务站服务老年人数10,卫生服务站服务老年人数15,总服务人数5服务率,总服务人数10服务率,总服务人数15服务率,卫生中心服务人数5服务率,卫生中心服务人数10服务率,卫生中心服务人数15服务率,卫生服务站服务人数5服务率,卫生服务站服务人数10服务率,卫生服务站服务人数15服务率,总服务老年人数5服务率,总服务老年人数10服务率,总服务老年人数15服务率,卫生中心服务老年人数5服务率,卫生中心服务老年人数10服务率,卫生中心服务老年人数15服务率,卫生服务站服务老年人数5服务率,卫生服务站服务老年人数10服务率,卫生服务站服务老年人数15服务率\n")
        for j in dict_shequ.values():
                re = (str(j.name) + "," +
                      str(j.sum_people) + "," + str(j.sum_old_people) + "," +
                      str(j.serve_people_5) + "," + str(j.serve_people_10) + "," + str(j.serve_people_15) + "," +
                      str(j.serve_people_center_5) + "," + str(j.serve_people_center_10) + "," + str(
                            j.serve_people_center_15) + "," +
                      str(j.serve_people_zhan_5) + "," + str(j.serve_people_zhan_10) + "," + str(
                            j.serve_people_zhan_15) + "," +
                      str(j.serve_old_people_5) + "," + str(j.serve_old_people_10) + "," + str(
                            j.serve_old_people_15) + "," +
                      str(j.serve_old_people_center_5) + "," + str(j.serve_old_people_center_10) + "," + str(
                            j.serve_old_people_center_15) + "," +
                      str(j.serve_old_people_zhan_5) + "," + str(j.serve_old_people_zhan_10) + "," + str(
                            j.serve_old_people_zhan_15) + "," +

                      str(j.serve_people_5 / j.sum_people) + "," + str(j.serve_people_10 / j.sum_people) + "," + str(
                            j.serve_people_15 / j.sum_people) + "," +
                      str(j.serve_people_center_5 / j.sum_people) + "," + str(
                            j.serve_people_center_10 / j.sum_people) + "," + str(
                            j.serve_people_center_15 / j.sum_people) + "," +
                      str(j.serve_people_zhan_5 / j.sum_people) + "," + str(
                            j.serve_people_zhan_10 / j.sum_people) + "," + str(
                            j.serve_people_zhan_15 / j.sum_people) + "," +
                      str(j.serve_old_people_5 / j.sum_old_people) + "," + str(
                            j.serve_old_people_10 / j.sum_old_people) + "," + str(
                            j.serve_old_people_15 / j.sum_old_people) + "," +
                      str(j.serve_old_people_center_5 / j.sum_old_people) + "," + str(
                            j.serve_old_people_center_10 / j.sum_old_people) + "," + str(
                            j.serve_old_people_center_15 / j.sum_old_people) + "," +
                      str(j.serve_old_people_zhan_5 / j.sum_old_people) + "," + str(
                            j.serve_old_people_zhan_10 / j.sum_old_people) + "," + str(
                            j.serve_old_people_zhan_15 / j.sum_old_people) + "\n")
                f.write(re)
# gaosi_shequ()
# gaosi_jiedao()
# gaosi_qixing_shequ()
# gaosi_qixing_jiedao()
serve_people()
#gongping()
#filter()