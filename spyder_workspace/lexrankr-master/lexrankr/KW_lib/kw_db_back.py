# -*- coding: utf-8 -*-

#-*-encoding:utf-8-*-

#!/usr/bin/env python -W ignore::DeprecationWarning

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from lexrankr import LexRank

class KW_DB(object):
    
    def __init__(self,conn,table):
        
        self.conn = conn
        self.table = table
        
    def insertSumma(self):
      
        lexrank = LexRank()
        curs = self.conn.cursor()
        
        summa_total=""
        sql = "SELECT id,raw,sentence_cnt FROM "+ self.table +" WHERE sentence_cnt > 5  ORDER BY id ASC;"
        curs.execute(sql)
        rows = curs.fetchall()
        
        for row in rows:
            raw = row[1]
            sentence_cnt = row[2]
            text="".join(raw)

            if(lexrank.summarize(text)==0):
                continue
                
            if(sentence_cnt<=20):
                summaries=lexrank.probe(5)
            else:
                summaries=lexrank.probe(10)
                
            for summa in summaries:
                summa_total+="".join(summa)
                summa_total+=". "
            
            curs.execute("UPDATE "+ self.table + " SET summa=%s WHERE id=%s;",(summa_total,row[0]))
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
                            
                    
            
    