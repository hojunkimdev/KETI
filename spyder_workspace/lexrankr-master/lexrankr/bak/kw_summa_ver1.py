# -*- coding: utf-8 -*-

#-*-encoding:utf-8-*-

#!/usr/bin/env python -W ignore::DeprecationWarning


from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from lexrankr import LexRank
import codecs
import json 
from collections import OrderedDict

class KW_SUMMA(object):
    
    def __init__(self,conn,table,main_idx,outlier_idx,t_sc,m_sc,tag_count):
        self.conn = conn
        self.table = table
        self.main_idx = main_idx
        self.outlier_idx = outlier_idx
        self.t_sc = t_sc
        self.m_sc = m_sc
        self.tag_count = tag_count
    
    def selectTag(self,tag):
        tag_list=tag.split(' ')
        tag_dict={}
        for tag in tag_list:
            if tag in tag_dict:
                tag_dict[tag]+=1
            else:
                if len(tag)>=2:
                    tag_dict[tag]=1
        
        sorted_tag_list = sorted(tag_dict,key=lambda k : tag_dict[k],reverse=True)
        
        i=1
        selected_tag=""
        for tag in sorted_tag_list:
            selected_tag+=tag+" "
            if(i==self.tag_count):
                break
            i+=1
        return selected_tag
            
            
    def deleteNoise(self,row):
        row = row.split('기자]')[1]
        if(row[0]==' ' or row[0]=='는'):
            row = "".join(row[1:])
        return row
    
    def day(self):
        lexrank = LexRank()  # can init with various settings
        curs = self.conn.cursor()
    
        tag=""
        main_outlier_text=""
                
        main_outlier_idx = self.main_idx + self.outlier_idx
        main_outlier_sql = "SELECT id,raw,summa,title,date,tag FROM "+self.table+" WHERE id in("
        
        main_outlier_idx_size = len(main_outlier_idx)
        
        for i in range(main_outlier_idx_size):
            if(i!=(main_outlier_idx_size-1)):
                main_outlier_sql+=str(main_outlier_idx[i])+","
            else:
                main_outlier_sql+=str(main_outlier_idx[i])+");"
        
        curs.execute(main_outlier_sql)
        rows = curs.fetchall()
             
        events=[]
      
        
        for row in rows:
            tag+="".join(row[5])
            text={}
                        
            row1=str(row[1])
            row2=str(row[2])
            row3=str(row[3])
            if(row1.find("기자]")!=-1):
                row1 = self.deleteNoise(row1)
            if(row2.find("기자]")!=-1):
                row2 = self.deleteNoise(row2)                        
            if(row3.find("기자]")!=-1):
                row3 = self.deleteNoise(row3)
            
            if(row[2] is None):
                main_outlier_text+="".join(row[1])
                text["headline"]=row3
                text["text1"]=row1
            else:
                main_outlier_text+="".join(row[2])
                text["headline"]=row3
                text["text1"]=row1
                text["text2"]=row2
            event={
                    "start_date": {
                    "year":		str(row[4]).split('-')[0],
                    "month":	     str(row[4]).split('-')[1],
                    "day": 		str(row[4]).split('-')[2],
                    "hour": 		"",
                    "minute": 		"",
                    "second": 		"",
                    "millisecond": 	"",
                    "format": 		""
                    },
    		          "group": "",
                    "media": {
                    "caption": "",
                    "credit": "",
                    "url": "",
                    "thumb": 	""
                    }
            }
                           
            event["text"]=text
            events.append(event)
        
        
        
        main_outlier_tag=self.selectTag(tag)
                   
        lexrank.summarize(main_outlier_text)
            
        # If there is an exception to the input value, you can not find the article in the summary statement.
        # Therefore, we allocate summaires to t_sc and search for summary aricles from the beginning.
        # if any are found (Because we decided to include only one outlier), end the loop
        summaries=lexrank.probe(self.t_sc)
            
        
        find=0
        main_outlier_summa=""
        for summa in summaries:
            
            summa=str(summa)
            if(summa.find("기자]")!=-1):
                summa = self.deleteNoise(summa)
            
            for row in rows:
                if(row[2] is None):
                    temp="".join(row[1])
                    if(temp.find("".join(summa))!=-1):
                        find+=1                        
                        main_outlier_summa += summa+". "
                else:
                    temp="".join(row[2])
                    if(temp.find("".join(summa))!=-1):
                        find+=1
                        main_outlier_summa += summa+". "                 
                                   
            if(find==(1)):
                break
                           
        total_data = OrderedDict()
        
        total_data["scale"] = ""
                        total_data["title"] =  {
                    		        "media": {
                    		            "caption": "",
                    		            "credit": "",
                    		            "url": "",
                    		            "thumb": 	""
                    		        },
                    	            "text": {
                    	                "headline": main_outlier_tag,
                    	                "text": main_outlier_summa
                    	            }
                    	    }
                                    
        total_data["events"]=events
        
        with codecs.open('day.json','w',encoding="utf-8") as make_file:
            json.dump(total_data, make_file, ensure_ascii=False, indent=4, sort_keys=False)
        
        
        print(json.dumps(total_data, ensure_ascii=False, indent=4, sort_keys=False) )
        
        
        
         
        
    def month(self):
        lexrank = LexRank()  # can init with various settings       
        curs = self.conn.cursor()
                                       
        main_idx_size=len(self.main_idx)
        outlier_idx_size=len(self.outlier_idx)
                 
        tag=""
        main_text=""
        outlier_text=""
            
                      
        """
        #main text + outlier text 
        main_sql = "SELECT id,raw,summa,title,date,tag FROM "+self.table+" WHERE id in("
        for i in range(main_idx_size):
            if(i!=(main_idx_size-1)):
                main_sql+=str(self.main_idx[i])+","
            else:
                main_sql+=str(self.main_idx[i])+");"
                                         
        curs.execute(main_sql)
        rows = curs.fetchall()
        for row in rows:
            tag+="".join(row[5])
            if(row[2] is None):
                main_text+="".join(row[1])
            else:
                main_text+="".join(row[2])
            
        lexrank.summarize(main_text)
        summaries=lexrank.probe(self.m_sc)
       
        for summa in summaries:
            main_summa+="".join(summa)
            main_summa+=". "
        
        outlier_sql = "SELECT id,raw,summa,title,date,tag FROM "+self.table+" WHERE id in("
            
        for i in range(outlier_idx_size):
            if(i!=(outlier_idx_size-1)):
                outlier_sql+=str(self.outlier_idx[i])+","
            else:
                outlier_sql+=str(self.outlier_idx[i])+");"
                 
        curs.execute(outlier_sql)
        rows = curs.fetchall()
        for row in rows:
            tag+="".join(row[5])
            if(row[2] is None):
                outlier_text+="".join(row[1])
            else:
                outlier_text+="".join(row[2])
            
        lexrank.summarize(outlier_text)
        summaries=lexrank.probe(self.t_sc-self.m_sc)
        
        outlier_summa ="[ OUTLIER ] "
        for summa in summaries:
            outlier_summa+="".join(summa)
            outlier_summa+=". "
                   
        main_outlier_summa += main_summa +outlier_summa
        main_outlier_tag=self.selectTag(tag)
          
        if(main_outlier_summa.find("기자]")!=-1):
            main_outlier_summa = self.deleteNoise(main_outlier_summa)
        """
        main_outlier_text=""
                
        main_outlier_idx = self.main_idx + self.outlier_idx
        main_outlier_sql = "SELECT id,raw,summa,title,date,tag FROM "+self.table+" WHERE id in("
        
        main_outlier_idx_size = len(main_outlier_idx)
        
        for i in range(main_outlier_idx_size):
            if(i!=(main_outlier_idx_size-1)):
                main_outlier_sql+=str(main_outlier_idx[i])+","
            else:
                main_outlier_sql+=str(main_outlier_idx[i])+");"
        
        curs.execute(main_outlier_sql)
        rows = curs.fetchall()
             
     
        for row in rows:
            tag+="".join(row[5])                       
            if(row[2] is None):
                main_outlier_text+="".join(row[1])             
            else:
                main_outlier_text+="".join(row[2])
        main_outlier_tag=self.selectTag(tag)
        
        
        lexrank.summarize(main_outlier_text)
        # If there is an exception to the input value, you can not find the article in the summary statement.
        # Therefore, we allocate summaires to t_sc and search for summary aricles from the beginning.
        # if any are found (Because we decided to include only one outlier), end the loop
        summaries=lexrank.probe(self.t_sc)
            
        find=0
        main_outlier_summa=""
        for summa in summaries:
            
            summa=str(summa)
            if(summa.find("기자]")!=-1):
                summa = self.deleteNoise(summa)
            
            for row in rows:
                if(row[2] is None):
                    temp="".join(row[1])
                    if(temp.find("".join(summa))!=-1):
                        find+=1                        
                        main_outlier_summa += summa+". "
                else:
                    temp="".join(row[2])
                    if(temp.find("".join(summa))!=-1):
                        find+=1
                        main_outlier_summa += summa+". "                 
                                   
            if(find==(1)):
                break
        
        
        total_data = OrderedDict()
        
        total_data["scale"] = ""
        total_data["title"] =  {
    		        "media": {
    		            "caption": "",
    		            "credit": "",
    		            "url": "",
    		            "thumb": 	""
    		        },
    	            "text": {
    	                "headline": main_outlier_tag,
    	                "text": main_outlier_summa
    	            }
    	    }
      
        
        events=[]      
        for m in range (1,12):
                           
            main_text=""
            outlier_text=""
           
            main_sql = "SELECT id,raw,summa,title,date,tag FROM "+self.table+" WHERE id in("
            
            for i in range(main_idx_size):
                if(i!=(main_idx_size-1)):
                    main_sql+=str(self.main_idx[i])+","
                else:
                    main_sql+=str(self.main_idx[i])+") and date BETWEEN '2017-"+str(m)+"-01' and '2017-"+str(m)+"-31';"
                 
                                           
            curs.execute(main_sql)
            rows = curs.fetchall()
            if(len(rows) ==0):
                continue
            
            for row in rows:
                if(row[2] is None):
                    main_text+="".join(row[1])
                else:
                    main_text+="".join(row[2])
            
            lexrank.summarize(main_text)
            summaries=lexrank.probe(self.m_sc)
               
            
            item_idx=1
            text={}
            for summa in summaries:
                
                summa=str(summa)
                if(summa.find("기자]")!=-1):
                    summa = self.deleteNoise(summa)
                
                eq=False
                               
                for row in rows:
                                        
                    row3=str(row[3])
                    if(row3.find("기자]")!=-1):
                            row3 = self.deleteNoise(row3)
                    
                    if(row[2] is None):
                        temp="".join(row[1])
                        if(temp.find("".join(summa))!=-1):
                            for checkDupIdx in range(1,item_idx):
                                if(text["headline"+str(checkDupIdx)] == row[3]):
                                    text["text"+str(checkDupIdx)] += summa+". "
                                    eq=True
                                    break
                            
                            if(eq==False):
                                text["headline"+str(item_idx)]=row3
                                text["text"+str(item_idx)]=summa+". "
                                item_idx+=1
                            break
                    else:
                        temp="".join(row[2])
                        if(temp.find("".join(summa))!=-1):
                            for checkDupIdx in range(1,item_idx):
                                if(text["headline"+str(checkDupIdx)] == row[3]):
                                    text["text"+str(checkDupIdx)] += summa+". "
                                    eq=True
                                    break
                            
                            if(eq==False):
                                text["headline"+str(item_idx)]=row3
                                text["text"+str(item_idx)]=summa+". "
                                item_idx+=1
                            break
             
            outlier_sql = "SELECT id,raw,summa,title,date,tag FROM KETI.movie_news WHERE id in("
            
            for i in range(outlier_idx_size):
                if(i!=(outlier_idx_size-1)):
                    outlier_sql+=str(self.outlier_idx[i])+","
                else:
                    outlier_sql+=str(self.outlier_idx[i])+") and date BETWEEN '2017-"+str(m)+"-01' and '2017-"+str(m)+"-31';"
                                             
            curs.execute(outlier_sql)
            rows = curs.fetchall()
            for row in rows:
                if(row[2] is None):
                    outlier_text+="".join(row[1])
                else:
                    outlier_text+="".join(row[2])
            
            lexrank.summarize(outlier_text)
            
            # If there is an exception to the input value, you can not find the article in the summary statement.
            # Therefore, we allocate summaires to t_sc and search for summary aricles from the beginning.
            # if any are found (Because we decided to include only one outlier), end the loop
            summaries=lexrank.probe(self.t_sc)
            find=0
            for summa in summaries:
                
                summa=str(summa)
                if(summa.find("기자]")!=-1):
                    summa = self.deleteNoide(summa)
                
                eq=False
                for row in rows:
                    
                    row3=str(row[3])
                    if(row3.find("기자]")!=-1):
                            row3 = self.deleteNoide(row3)
    
                    if(row[2] is None):
                        temp="".join(row[1])
                        if(temp.find("".join(summa))!=-1):
                            find+=1
                            for checkDupIdx in range(1,item_idx):
                                if(text["headline"+str(checkDupIdx)] == row[3]):
                                    text["text"+str(checkDupIdx)] += "[OUTLIER] "+summa+". "
                                    eq=True
                                    break
                            
                            if(eq==False):
                                text["headline"+str(item_idx)]="[OUTLIER] "+row[3]
                                text["text"+str(item_idx)]="[OUTLIER] "+summa+". "
                                item_idx+=1
                            break
                    else:
                        temp="".join(row[2])
                        if(temp.find("".join(summa))!=-1):
                            find+=1
                            for checkDupIdx in range(1,item_idx):
                                if(text["headline"+str(checkDupIdx)] == row[3]):
                                    text["text"+str(checkDupIdx)] += "[OUTLIER] "+summa+". "
                                    eq=True
                                    break
                            
                            if(eq==False):
                                text["headline"+str(item_idx)]="[OUTLIER] "+row[3]
                                text["text"+str(item_idx)]="[OUTLIER] "+summa+". "
                                item_idx+=1
                            break
                if(find==(self.t_sc-self.m_sc)):
                    break
           
            event={
                            "start_date": {
                                "year":		2017,
                                "month":	m,
                                "day": 		"",
                                "hour": 		"",
                                "minute": 		"",
                                "second": 		"",
                                "millisecond": 	"",
                                "format": 		""
                            },
                		    "group": "",
                            "media": {
                                "caption": "",
                                "credit": "",
                                "url": "",
                                "thumb": 	""
                            }
                }
                            
            event["text"]=text
            events.append(event)
             
        total_data["events"]=events
        
        with codecs.open('month.json','w',encoding="utf-8") as make_file:
            json.dump(total_data, make_file, ensure_ascii=False, indent=4, sort_keys=False)
        
        
        print(json.dumps(total_data, ensure_ascii=False, indent=4, sort_keys=False) )
        

