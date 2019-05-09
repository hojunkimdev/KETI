# -*- coding: utf-8 -*-

#-*-encoding:utf-8-*-

#!/usr/bin/env python -W ignore::DeprecationWarning

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from lexrankr import LexRank
import pymysql.cursors

class KW_DB(object):
    
    def __init__(self,conn,table):
        
        self.conn = conn
        self.table = table
        
    def insertSumma(self):
      
        lexrank = LexRank()
        curs = self.conn.cursor()
        
        #1. get a value of 90 percent
        #you can change the percent value like 80, 70 ..
        percent = 90
        sql = "select count(*)*"+str(1-percent*0.01)+" from "+ self.table +";"
        curs.execute(sql)
        rows = curs.fetchone()
        percentile = int(rows[0])
    
        #2. get a value located at a percetile
        sql = "SELECT id,raw,sentence_cnt FROM "+ self.table +" order by sentence_cnt desc;"
        curs.execute(sql)
        rows = curs.fetchall()
    
        i=0
        for row in rows:
            i = i+1
            if i == percentile : 
                percentile_cnt = row[2]
                break;
     
        #3. get a average value in a percentile
        sql = "SELECT avg(sentence_cnt) FROM "+ self.table +" where sentence_cnt <="+str(percentile_cnt) +";"
        curs.execute(sql)
        rows = curs.fetchone()
        percentile_avg = int(rows[0])
        
        #the minimum average value is 6 
        if percentile_avg < 6 :
            percentile_avg = 6
    
        #4. get the total table row except for less than half of the average
        summa_total=""
        sql = "SELECT id,raw,sentence_cnt FROM KETI."+ self.table +" WHERE sentence_cnt > " + str(int(percentile_avg/2)) + " ORDER BY id ASC;"
        curs.execute(sql)
        rows = curs.fetchall()
        
        #5. we can get raw and sentence count in each row
        # and update summa column using the parameter rule
        
        for row in rows :
            #using the curs as iterator
            raw = row[1]
            sentence_cnt = row[2]
            text="".join(raw)

            if(lexrank.summarize(text)==0):
                continue
                
            if(sentence_cnt<=percentile_cnt):
                summaries=lexrank.probe(int(percentile_avg/2))
            else:
                summaries=lexrank.probe(percentile_avg)
                
            for summa in summaries:
                summa_total+="".join(summa)
                summa_total+=". "
     
                curs.execute("UPDATE "+ self.table + " SET summa=%s WHERE id=%s;",(summa_total,row[0]));
            self.conn.commit()
            
            summa_total=""
            
    
        
    def insertSentenceCount(self):
        
        lexrank = LexRank()
        curs = self.conn.cursor()
        
        sql = "SELECT id,raw FROM "+ self.table +" ORDER BY id ASC;"
        curs.execute(sql)
        rows = curs.fetchall()
        
        for row in rows:
            text="".join(row[1])
            sc = lexrank.factory.text2sentences(text)
            print("insert sentence_cnt to id="+str(row[0]))
            print("sc="+str(len(sc))+"\n")
            curs.execute("UPDATE "+ self.table +" SET sentence_cnt=%s WHERE id=%s;",(str(len(sc)),str(row[0])))
            self.conn.commit()
                            
