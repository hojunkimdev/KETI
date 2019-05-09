#-*-encoding:utf-8-*-

#!/usr/bin/env python -W ignore::DeprecationWarning

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0,os.getcwd()+"/LexRank")
sys.path.insert(0,os.getcwd()+"/KW_lib")

import pymysql.cursors
import tensorflow as tf
from lexrankr import LexRank
from kw_summa import KW_SUMMA
from kw_db import KW_DB

import tensorflow as tf
def main():    
    
        
    conn = pymysql.connect(host='localhost',
                           user='user', 
                           password='((user))',
                           db='KETI', 
                           use_unicode=True,
                           charset='utf8')   
    
    KD = KW_DB(conn,"economy_news")
    KD.insertSumma()
    
    
    # TAG 1
    #main_idx=[12426,12448,12524,16790,17181,17221,17222,17904,18229,19995,20025,20026,20030,20033,20121,20123,20138,20139,20141,20143,20150,20495,20563,20600,24206,24352,24387,24531,24566,24570,24608,24752,24758,25905,26199,26234,26241,26247,26298,26301,26367,26389,26634,27662,27684,27758,27762,27767,28807,28879,28951,28960,28981,28987,29048,29181,29192,29238,29242,29243]
    #outlier_idx=[1386,12971,13544,19983,19993,20003,20018,20020,20021,20136,20484,20587,20588,21247,21679,21822,21867,22871,23167,23355,23669,23893,23894,24874,24888,25430,26312,26732,26842,26861,26880,27028,27308,27635,27648,28824,29283,29288]
    #main_idx=[12426,12448,12524,16790,17181]
    #outlier_idx=[1386]
    """"""
    #TAG1,2
    '''
    main_idx=[12426, 12448, 12504, 12524, 12971, 16790]
    outlier_idx=[1386, 13544, 20003, 20020]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    '''
    
    #__init__(self,conn,table,main_idx,outlier_idx,total_event,main_event,summa_count,tag_count):
    
    main_idx=[12426, 12448, 12504, 12524, 12971]
    outlier_idx=[1386, 13544, 20003]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    
    
    
    """
    #s_cnt = 1600 
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144, 75412, 77395, 77396, 77446,77463, 77481, 77516, 77525, 77526, 78123, 78393, 79604, 79622, 79648, 79650, 79652,79656, 79696, 79700, 79705, 79709, 79713, 79725, 79730, 80223, 80267, 80428, 81413, 81853, 81877, 81948, 81972, 82023, 82136, 82185, 82951, 82963, 82993, 83008, 83009,83010]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063, 85316, 85748, 87211, 87655, 88322, 88503, 88521, 88599, 88673,88710, 88711,1386,12971,13544,19983,19993,20003,20018]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()    
    """
    """"""
    #main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096]
    #outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512]
    
    
    #s_cnt = 2000
    '''
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144, 75412, 77395, 77396, 77446,77463, 77481, 77516, 77525, 77526, 78123, 78393, 79604, 79622, 79648, 79650, 79652,79656, 79696, 79700, 79705, 79709, 79713, 79725, 79730, 80223, 80267, 80428, 81413, 81853, 81877, 81948, 81972, 82023, 82136, 82185, 82951, 82963, 82993, 83008, 83009,83010, 83616, 83640, 83645, 83701, 84020, 84038, 84134, 84163, 84164, 86403, 86532, 86646, 87281, 87787, 88053, 88158, 88356, 88375, 88392, 88434, 88442, 88475, 88512,88536, 88571, 88575, 88596, 88603, 88691, 88694, 88701, 88703, 88704, 88706, 88713,88714, 88720, 88735]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063, 85316, 85748, 87211, 87655, 88322, 88503, 88521, 88599, 88673,88710, 88711,1386,12971,13544,19983,19993,20003,20018,20020,20021,20136,20484,20587,20588,21247,21679]
    #main_idx=[292, 339, 447, 5350, 5597, 5728, 10591]
    #outlier_idx=[14255, 38565, 71591, 750125]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    
    
    conn.close()
    '''
    
    
    #Speed Test
    #s_cnt = 200
    
    '''
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591]
    outlier_idx=[14255, 38565]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    
    #s_cnt = 400
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    
    #s_cnt = 600
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
 
    
    #s_cnt = 800
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144, 75412, 77395, 77396, 77446,77463, 77481, 77516, 77525, 77526, 78123, 78393, 79604]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063, 85316, 85748, 87211, 87655, 88322, 88503, 88521, 88599, 88673]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    
    #s_cnt = 1000
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144, 75412, 77395, 77396, 77446,77463, 77481, 77516, 77525, 77526, 78123, 78393, 79604, 79622, 79648, 79650, 79652,79656, 79696, 79700, 79705]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063, 85316, 85748, 87211, 87655, 88322, 88503, 88521, 88599, 88673,88710, 88711,1386,12971,13544,19983,19993,20003]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()

    #s_cnt = 1200 
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144, 75412, 77395, 77396, 77446,77463, 77481, 77516, 77525, 77526, 78123, 78393, 79604, 79622, 79648, 79650, 79652,79656, 79696, 79700, 79705, 79709, 79713, 79725, 79730, 80223, 80267]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063, 85316, 85748, 87211, 87655, 88322, 88503, 88521, 88599, 88673,88710, 88711,1386,12971,13544,19983,19993,20003,20018,20020,20021,20136,20484,20587,20588,21247,21679]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    
    #s_cnt = 1400 
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144, 75412, 77395, 77396, 77446,77463, 77481, 77516, 77525, 77526, 78123, 78393, 79604, 79622, 79648, 79650, 79652,79656, 79696, 79700, 79705, 79709, 79713, 79725, 79730, 80223, 80267, 80428, 81413, 81853, 81877, 81948, 81972, 82023, 82136, 82185, 82951, 82963, 82993, 83008, 83009,83010, 83616, 83640]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063, 85316, 85748, 87211, 87655, 88322, 88503, 88521, 88599, 88673,88710, 88711,1386,12971,13544,19983,19993,20003,20018,20020,20021,20136,20484,20587,20588,21247,21679]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    
    #s_cnt = 1600 
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144, 75412, 77395, 77396, 77446,77463, 77481, 77516, 77525, 77526, 78123, 78393, 79604, 79622, 79648, 79650, 79652,79656, 79696, 79700, 79705, 79709, 79713, 79725, 79730, 80223, 80267, 80428, 81413, 81853, 81877, 81948, 81972, 82023, 82136, 82185, 82951, 82963, 82993, 83008, 83009,83010, 83616, 83640, 83645, 83701, 84020, 84038, 84134, 84163, 84164, 86403, 86532, 86646, 87281, 87787, 88053, 88158, 88356]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063, 85316, 85748, 87211, 87655, 88322, 88503, 88521, 88599, 88673,88710, 88711,1386,12971,13544,19983,19993,20003,20018,20020,20021,20136,20484,20587,20588,21247,21679]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    
    #s_cnt = 1800
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144, 75412, 77395, 77396, 77446,77463, 77481, 77516, 77525, 77526, 78123, 78393, 79604, 79622, 79648, 79650, 79652,79656, 79696, 79700, 79705, 79709, 79713, 79725, 79730, 80223, 80267, 80428, 81413, 81853, 81877, 81948, 81972, 82023, 82136, 82185, 82951, 82963, 82993, 83008, 83009,83010, 83616, 83640, 83645, 83701, 84020, 84038, 84134, 84163, 84164, 86403, 86532, 86646, 87281, 87787, 88053, 88158, 88356, 88375, 88392, 88434, 88442, 88475, 88512,88536, 88571, 88575, 88596, 88603]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063, 85316, 85748, 87211, 87655, 88322, 88503, 88521, 88599, 88673,88710, 88711,1386,12971,13544,19983,19993,20003,20018,20020,20021,20136,20484,20587,20588,21247,21679]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()

    #s_cnt = 2000    
    main_idx=[292, 339, 447, 5350, 5597, 5728, 10591, 44741, 44985, 45096, 45176, 45179, 45182,45216, 45228, 45623, 45710, 61893, 65890, 67909, 70144, 75412, 77395, 77396, 77446,77463, 77481, 77516, 77525, 77526, 78123, 78393, 79604, 79622, 79648, 79650, 79652,79656, 79696, 79700, 79705, 79709, 79713, 79725, 79730, 80223, 80267, 80428, 81413, 81853, 81877, 81948, 81972, 82023, 82136, 82185, 82951, 82963, 82993, 83008, 83009,83010, 83616, 83640, 83645, 83701, 84020, 84038, 84134, 84163, 84164, 86403, 86532, 86646, 87281, 87787, 88053, 88158, 88356, 88375, 88392, 88434, 88442, 88475, 88512,88536, 88571, 88575, 88596, 88603, 88691, 88694, 88701, 88703, 88704, 88706, 88713,88714, 88720, 88735]
    outlier_idx=[14255, 38565, 71591, 750125, 77461, 77462, 77512, 77521, 77865, 77954, 79646, 79703,79722, 81990, 82063, 85316, 85748, 87211, 87655, 88322, 88503, 88521, 88599, 88673,88710, 88711,1386,12971,13544,19983,19993,20003,20018,20020,20021,20136,20484,20587,20588,21247,21679]
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    '''
    
    conn.close()
    '''
    '''#Get sentence and id'''
    """
    main_idx = []
    outlier_idx = []
    
    #get main_id
    main_sql = "SELECT id,sentence_cnt FROM KETI.movie_news WHERE date BETWEEN '2017-01-01' and '2017-07-30'"
    curs = conn.cursor()
    curs.execute(main_sql)
    main_raws = curs.fetchall()
    sum_sent = 0
    for row in main_raws :
        main_idx.append(row[0])
        sum_sent += int(row[1])
        if sum_sent > 200:
            break;
    
    
    #get outlier_id
    outlier_sql = "SELECT id,sentence_cnt FROM KETI.movie_news WHERE date BETWEEN '2017-08-01' and '2017-09-30'"
    curs = conn.cursor()
    curs.execute(outlier_sql)
    outlier_raws = curs.fetchall()
    sum_sent = 0
    for row in outlier_raws :
        outlier_idx.append(row[0])
        sum_sent += int(row[1])
        if sum_sent > 100:
            break;
    
    
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    KS.createJSON()
    conn.close()
    """
    """ # TEST
   main_sql = "select id,raw,summa,title,date from KETI.movie_news where sentence_cnt = 3 limit 100;"
    
    lexrank=LexRank()
    curs=conn.cursor()    
    curs.execute(main_sql)
    rows = curs.fetchall()
    for row in rows:
        raw = row[1]
        print(raw)
        lexrank.summarize(raw)
        summaries=lexrank.probe(2)
        for summa in summaries:
            print(str(summa)+". ")
      
    printf("s")
    """
 
    """
    outlier_sql = "SELECT id,raw,summa,title,date FROM KETI.politics_news WHERE id in("
    
    for i in range(outlier_size):
       if(i!=(outlier_size-1)):
           outlier_sql+=str(outlier[i])+","
       else:
           outlier_sql+=str(outlier[i])+")"
    
    outlier_summa+="[ Outlier ]\n"+ str(t-n) + " summas\n" + "SQL = " +outlier_sql+"\n\n"
    
    curs.execute(outlier_sql)
    rows = curs.fetchall()
    for row in rows:
        if(row[2] is None):
            outlier_text+="".join(row[1])
        else:
            outlier_text+="".join(row[2])
    
    lexrank.summarize(outlier_text)
    summaries=lexrank.probe(t-n)
    for summa in summaries:
        for row in rows:
            if(row[2] is None):
                temp="".join(row[1])
                if(temp.find("".join(summa))!=-1):
                    outlier_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
            else:
                temp="".join(row[2])
                if(temp.find("".join(summa))!=-1):
                    outlier_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
        outlier_summa+="<summa>: " +summa +".\n\n"
    
    
    main_outlier += main_summa +outlier_summa
    print(main_outlier)
    """
    
    """
    #Full SQL Main, Outlier TEST
    main_sql = "select id,raw,summa,title,date from KETI.politics_news where date BETWEEN '2017-01-01' and '2017-01-30' and match(title,tag) against('\"박근혜 탄핵\"' in boolean mode)"
    main_summa+="[ Main Media ]\n"+ str(n) + " summas\n" + "SQL = " +main_sql+"\n\n"
    
    curs.execute(main_sql)
    rows = curs.fetchall()
    for row in rows:
        if(row[2] is None):
            main_text+="".join(row[1])
        else:
            main_text+="".join(row[2])
    
    lexrank.summarize(main_text)
    summaries=lexrank.probe(n)
    for summa in summaries:
        for row in rows:
            if(row[2] is None):
                temp="".join(row[1])
                if(temp.find("".join(summa))!=-1):
                    main_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
            else:
                temp="".join(row[2])
                if(temp.find("".join(summa))!=-1):
                    main_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
        main_summa+="<summa>: " +summa +".\n\n"
    
       
    outlier_sql = "select id,raw,summa,title,date from KETI.politics_news where date BETWEEN '2017-01-01' and '2017-01-30' and match(title,tag) against('\"박근혜 미국\"' in boolean mode)"
    outlier_summa+="[ Outlier ]\n"+ str(t-n) + " summas\n" + "SQL = " +outlier_sql+"\n\n"
    
    curs.execute(outlier_sql)
    rows = curs.fetchall()
    for row in rows:
        if(row[2] is None):
            outlier_text+="".join(row[1])
        else:
            outlier_text+="".join(row[2])
    
    lexrank.summarize(outlier_text)
    summaries=lexrank.probe(t-n)
    for summa in summaries:
        for row in rows:
            if(row[2] is None):
                temp="".join(row[1])
                if(temp.find("".join(summa))!=-1):
                    outlier_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
            else:
                temp="".join(row[2])
                if(temp.find("".join(summa))!=-1):
                    outlier_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
        outlier_summa+="<summa>: " +summa +".\n\n"
    
    
    main_outlier += main_summa +outlier_summa
   
    """
    
    
   
    
    
    
    """
    #index
    main_sql = "SELECT id,raw,summa FROM KETI.politics_news WHERE id in("
    for i in range(main_size):
        if(i!=(main_size-1)):
            main_sql+=str(main[i])+","
        else:
            main_sql+=str(main[i])+")"
            
    curs.execute(main_sql)
    rows = curs.fetchall()
    for row in rows:
        if(row[2] is None):
            main_text+="".join(row[1])
        else:
            main_text+="".join(row[2])
    
    lexrank.summarize(main_text)
    summaries=lexrank.probe(n)
    for summa in summaries:
        main_summa+="".join(summa)
        main_summa+=". "
    print(main_summa)
    
    
    outlier_sql = "SELECT id,raw,summa FROM KETI.politics_news WHERE id in("
    for i in range(outlier_size):
        if(i!=(outlier_size-1)):
            outlier_sql+=str(outlier[i])+","
        else:
            outlier_sql+=str(outlier[i])+")"
            
    curs.execute(outlier_sql)
    rows = curs.fetchall()
    for row in rows:
        if(row[2] is None):
            outlier_text+="".join(row[1])
        else:
            outlier_text+="".join(row[2])
    
    lexrank.summarize(outlier_text)
    summaries=lexrank.probe(t-n)
    for summa in summaries:
        outlier_summa+="".join(summa)
        outlier_summa+=". "
    print(outlier_summa)
            
    main_outlier += main_summa +outlier_summa
    print(main_outlier)
    """
    
    
    
    
    """
    #insert summa
    
    #POLITICS
    summa_total=""
    sql = "SELECT id,raw,sentence_cnt FROM KETI.politics_news ORDER BY id ASC;"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        print("id="+str(row[0]))
        text="".join(row[1])
        if(lexrank.summarize(text)==0):
            continue
            
        if(row[2]<=20):
            summaries=lexrank.probe(5)
        else:
            summaries=lexrank.probe(10)
        for summa in summaries:
            summa_total+="".join(summa)
            summa_total+=". "
        print(summa_total)
        curs.execute("UPDATE politics_news SET summa=%s WHERE id=%s;",(summa_total,row[0]))
        conn.commit()
        summa_total=""

    #MOVIES
    summa_total=""
    sql = "SELECT id,raw,sentence_cnt FROM KETI.movie_news ORDER BY id ASC;"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        print("movie_news summa")
        print("id="+str(row[0]))
        text="".join(row[1])
        if(lexrank.summarize(text)==0):
            continue            
        if(row[2]<=20):
            summaries=lexrank.probe(5)
        else:
            summaries=lexrank.probe(10)
        for summa in summaries:
            summa_total+="".join(summa)
            summa_total+=". "
        print(summa_total)
        curs.execute("UPDATE movie_news SET summa=%s WHERE id=%s;",(summa_total,row[0]))
        conn.commit()
        summa_total=""
    
    """
    
   
   
    
    """
    #update movie_news Tag from updated KETI Data
    sql = "SELECT o.id,n.tag FROM KETI.movie_news o,KETI.movie_temp n where o.id=n.id ORDER BY o.id;"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        print("id="+str(row[0]))
        curs.execute("UPDATE KETI.movie_news SET tag=%s WHERE id=%s;",(row[1],row[0]))
        conn.commit()
    """
    
    """
    #insert sentence_cnt to DB by using lexrank.factory.text2sentences(text)
    sql = "SELECT id,raw FROM KETI.politics_news WHERE id>134245 ORDER BY id;"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        text="".join(row[1])
        sc = lexrank.factory.text2sentences(text)
        print("politics_news")
        print("id="+str(row[0]))
        print("sc="+str(len(sc)))
        curs.execute("UPDATE politics_news SET sentence_cnt=%s WHERE id=%s;",(str(len(sc)),str(row[0])))
        conn.commit()

    sql = "SELECT id,raw FROM KETI.movie_news ORDER BY id;"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        text="".join(row[1])
        sc = lexrank.factory.text2sentences(text)
        print("movie_news")
        print("id="+str(row[0]))
        print("sc="+str(len(sc)))
        curs.execute("UPDATE movie_news SET sentence_cnt=%s WHERE id=%s;",(str(len(sc)),str(row[0])))
        conn.commit()
    """
        
    """
    #insert sentence_cnt to DB by using count('.')
    sql = "SELECT id,raw FROM KETI.politics_news;"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        text="".join(row[1])
        s_count=text.count('.')
        if s_count!=0:
            curs.execute("UPDATE politics_news SET sentence_cnt="+str(s_count)+" WHERE id="+str(row[0])+";")
    
    
    sql = "SELECT id,raw FROM KETI.movie_news;"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        text="".join(row[1])
        s_count=text.count('.')
        if s_count!=0:
            curs.execute("UPDATE movie_news SET sentence_cnt="+str(s_count)+" WHERE id="+str(row[0])+";")  
           
    conn.commit()
    """
    
    """
    # Find the min,max,mean,median,std of sentences in each article and show histogram
    sentenceCount=[]
    sql = "SELECT id,sentence_cnt FROM KETI.politics_news WHERE sentence_cnt>20;"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        sentenceCount.append(row[1])

    sql = "SELECT id,sentence_cnt FROM KETI.movie_news WHERE sentence_cnt>20;"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        sentenceCount.append(row[1])
        
    sc_min=min(sentenceCount)
    sc_max=max(sentenceCount)
    sc_mean=numpy.mean(sentenceCount)
    sc_median=numpy.median(sentenceCount)
    sc_std=numpy.std(sentenceCount)    
    

    plt.hist(sentenceCount)
    plt.show()
    """
    


     
    """
    # Where Tag, 1 Day, Politics
    in_file_tag=codecs.open("/home/user/spyder_workspace/rankTest/tag_in.txt",'w',encoding="utf-8")
    out_file_tag=open("/home/user/spyder_workspace/rankTest/tag_out.txt",'w')
    for m in range(1,13):
        for i in range(1,31):
            sql = "SELECT raw FROM KETI.politics_news where (date = '2017-"+str(m)+"-"+str(i)+"') and tag like '%박근혜%' limit 10;"
            out_file_tag.write(sql+"\n")
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                text+="".join(row)
                text+="\n"
            in_file_tag.write(sql+"\n\n"+text+"\n\n")
            start=time.time()   
            lexrank.summarize(text)
            end=time.time()-start
            out_file_tag.write("Time to summarize = "+str(end)+"s\n\n")
            for i in range(1,6):
                summaries=lexrank.probe(i)
                out_file_tag.write("lexrank.probe("+str(i)+")\n")
                for summa in summaries:            
                    out_file_tag.write(summa+".\n")
                out_file_tag.write("\n")
            text=""
        
    in_file_tag.close()
    out_file_tag.close()
    """
    
    
    """
    # Where Title and Tag, 1 Day, Politics
    in_file_Politics=codecs.open("/home/user/spyder_workspace/rankTest/Politics_in.txt",'w',encoding="utf-8")
    out_file_Politics=open("/home/user/spyder_workspace/rankTest/Politics_out.txt",'w')
    for m in range(1,10):
        for i in range(1,32):
            sql = "SELECT raw FROM KETI.politics_news where (date = '2017-"+str(m)+"-"+str(i)+"') and title like '%박근혜%' and tag like '%박근혜%' limit 10;"
            out_file_Politics.write(sql+"\n")
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                text+="".join(row)
                text+="\n"
            if text == "":
                continue
            in_file_Politics.write(sql+"\n\n"+text+"\n\n")
            start=time.time()   
            lexrank.summarize(text)
            end=time.time()-start
            out_file_Politics.write("Time to summarize = "+str(end)+"s\n\n")
            for i in range(1,6):
                summaries=lexrank.probe(i)
                out_file_Politics.write("lexrank.probe("+str(i)+")\n")
                for summa in summaries:            
                    out_file_Politics.write(summa+".\n")
                out_file_Politics.write("\n")
            text=""
        
    in_file_Politics.close()
    out_file_Politics.close()
    """
    
    """
    # Where Title and Tag, 1 Day, Movies
    in_file_Movies=codecs.open("/home/user/spyder_workspace/rankTest/Movies_in.txt",'w',encoding="utf-8")
#    out_file_Movies=open("/home/user/spyder_workspace/rankTest/Movies_out.txt",'w')
    for m in range(1,10):
        for i in range(1,32):
            sql = "SELECT raw FROM KETI.movie_news where (date = '2017-"+str(m)+"-"+str(i)+"') and title like '%이병헌%' and tag like '%이병헌%' limit 10;"
            out_file_Movies.write(sql+"\n")
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                text+="".join(row)
                text+="\n"
            if text == "":
                continue
            in_file_Movies.write(sql+"\n\n"+text+"\n\n")
            start=time.time()   
            lexrank.summarize(text)
            end=time.time()-start
            out_file_Movies.write("Time to summarize = "+str(end)+"s\n\n")
            for i in range(1,6):
                summaries=lexrank.probe(i)
                out_file_Movies.write("lexrank.probe("+str(i)+")\n")
                for summa in summaries:            
                    out_file_Movies.write(summa+".\n")
                out_file_Movies.write("\n")
            text=""
        
    in_file_Movies.close()
    out_file_Movies.close()
    """
    
    """
    # Where Title and Tag, N Day, Each Text Summarization -> Merge
    in_file_titleTag_eachSumma=codecs.open("/home/user/spyder_workspace/rankTest/titleTag_eachSumma_in.txt",'w',encoding="utf-8")
    out_file_titleTag_eachSumma=open("/home/user/spyder_workspace/rankTest/titleTag_eachSumma_out.txt",'w')
    
 
    eachSumma=""
    
    start=time.time()  
    for i in range(1,8):
        sql = "SELECT raw FROM KETI.politics_news where (date = '2017-02-0"+str(i)+"') and title like '%박근혜%' and tag like '%박근혜%' limit 10;"
        out_file_titleTag_eachSumma.write("SQL = "+sql+"\n")
        curs.execute(sql)
        rows = curs.fetchall()
        for row in rows:
            text+="".join(row)
            text+="\n"
        lexrank.summarize(text)
        text=""
        in_file_titleTag_eachSumma.write(sql+"\nSummarization\n")
        summaries=lexrank.probe(10)
        for summa in summaries:
            in_file_titleTag_eachSumma.write(summa+".\n")
            eachSumma += summa+".\n"
        in_file_titleTag_eachSumma.write("\n")
        
        
  
    lexrank.summarize(eachSumma)
    end=time.time()-start
    
    out_file_titleTag_eachSumma.write("Time to summarize = "+str(end)+"s\n\n")
    for i in range(1,6):
        summaries=lexrank.probe(i)
        out_file_titleTag_eachSumma.write("lexrank.probe("+str(i)+")\n")
        for summa in summaries:            
            out_file_titleTag_eachSumma.write(summa+".\n")
            print(summa+"\n")
        out_file_titleTag_eachSumma.write("\n")
        
    in_file_titleTag_eachSumma.close()
    out_file_titleTag_eachSumma.close()
  
    
    # Where Title and Tag, N Day, Once Text Summarization 
    in_file_titleTag_onceSumma=codecs.open("/home/user/spyder_workspace/rankTest/titleTag_onceSumma_in.txt",'w',encoding="utf-8")
    out_file_titleTag_onceSumma=open("/home/user/spyder_workspace/rankTest/titleTag_onceSumma_out.txt",'w')
    for i in range(1,8):
        sql = "SELECT raw FROM KETI.politics_news where (date = '2017-02-0"+str(i)+"') and title like '%박근혜%' and tag like '%박근혜%' limit 10;"
        out_file_titleTag_onceSumma.write("SQL = "+sql+"\n")
        curs.execute(sql)
        rows = curs.fetchall()
        for row in rows:
            text+="".join(row)
            text+="\n"
        in_file_titleTag_onceSumma.write(sql+"\n\n"+text+"\n\n")
        
        
    start=time.time()   
    lexrank.summarize(text)
    end=time.time()-start
    out_file_titleTag_onceSumma.write("Time to summarize = "+str(end)+"s\n\n")
    for i in range(1,6):
        summaries=lexrank.probe(i)
        out_file_titleTag_onceSumma.write("lexrank.probe("+str(i)+")\n")
        for summa in summaries:            
            out_file_titleTag_onceSumma.write(summa+".\n")
        out_file_titleTag_onceSumma.write("\n")
    text=""
    
    in_file_titleTag_onceSumma.close()
#    out_file_titleTag_onceSumma.close()
    """
    
    
    
    
    
    

    
if __name__ == "__main__":
     main()
