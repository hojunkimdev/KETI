#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 20:59:57 2018

@author: root
"""
#!/usr/bin/env python -W ignore::DeprecationWarning

import sys
import os
reload(sys)

sys.path.insert(0,os.getcwd()+"/LexRank")
sys.path.insert(0,os.getcwd()+"/KW_lib")
sys.setdefaultencoding('utf-8')

from lexrankr import LexRank
import pymysql.cursors
def getsentence(table):
    
    conn = pymysql.connect(host='localhost',
                           user='user', 
                           password='((user))',
                           db='KETI',
                           use_unicode=True,
                           charset='utf8') 
    lexrank = LexRank()
    curs = conn.cursor()
        
    #sql = "SELECT id,raw,sentence_cnt FROM "+ table +" where id>179460;"
    sql = "select count(*)*0.1 from "+ table +";"
    curs.execute(sql)
    rows = curs.fetchone()
    percentile = int(rows[0])
    
    sql = "SELECT id,raw,sentence_cnt FROM "+ table +" order by sentence_cnt desc;"
    curs.execute(sql)
    rows = curs.fetchall()
    
    i=0
    
    for row in rows:
       i = i+1
       if i == percentile : 
           percentile_cnt = row[2]
           break;
     
    sql = "SELECT avg(sentence_cnt) FROM "+ table +" where sentence_cnt <="+str(percentile_cnt) +";"
    curs.execute(sql)
    rows = curs.fetchone()
    percentile_avg = int(rows[0])
        
    print i, percentile_cnt, percentile_avg
    ''' 
    check_id = []
    for row in rows:
        text="".join(row[1])
        sc = lexrank.factory.text2sentences(text)
        sentence_num = int(len(sc))
        print("insert sentence_cnt to id="+str(row[0]))
        print("sc="+str(sentence_num)+"\n")
        check_id.append(int(row[0]))
        #if sentence_num > 3 and sentence_num < 7 : check_id.append(int(row[0]))
        #curs.execute("UPDATE "+ table +" SET sentence_cnt=%s WHERE id=%s;",(str(len(sc)),str(row[0])))
        #conn.commit()

    conn.close()
    '''

if __name__=='__main__':
    #table = sys.argv[1]
    table = 'social'
    getsentence('KETI.'+table+'_news')
    table = 'it'
    getsentence('KETI.'+table+'_news')
    table = 'economy'
    getsentence('KETI.'+table+'_news')
    

    

