#-*-encoding:utf-8-*-
#!/usr/bin/env python -W ignore::DeprecationWarning

"""
KW_SUMMA(Multi-Document Summarization) 

Copyright (c) 2017 Data Science Laboratory

E-mail: kihoonlee@kw.ac.kr, timetopray@naver.com  
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from lexrankr import LexRank
import codecs
import time
import json 
from collections import OrderedDict

class KW_SUMMA(object):
    
    def __init__(self,conn,table,main_idx,outlier_idx,total_event,main_event,summa_count,tag_count):
        
        self.conn = conn
        self.table = table
        self.main_idx = main_idx
        self.outlier_idx = outlier_idx
        self.total_event = total_event
        self.main_event = main_event
        self.summa_count = summa_count
        self.tag_count = tag_count
               
    # Total System Management
    def createJSON(self):
        
        start_time_createJSON=time.time()
        if(self.main_event > len(self.main_idx)):
            sys.exit("main_event must be smaller than main_idx")
        elif((self.total_event-self.main_event) > len(self.outlier_idx)):
            sys.exit("total_event-main_event must be smaller than outlier_idx")

               
        lexrank = LexRank()  # can init with various settings
        curs = self.conn.cursor()
        
        ############################################################################## 
        # MAKE TITLE #        
        ##############################################################################        
        main_outlier_text=""
        
        main_outlier_idx = self.main_idx + self.outlier_idx
        main_outlier_idx_size = len(main_outlier_idx)
        
        tag=""
        main_outlier_sentence_cnt=0        
        
        main_outlier_sql = "SELECT id,raw,summa,title,date,tag,sentence_cnt,link FROM "+self.table+" WHERE id in("
        
        for i in range(main_outlier_idx_size):
            if(i!=(main_outlier_idx_size-1)):
                main_outlier_sql+=str(main_outlier_idx[i])+","
            else:
                main_outlier_sql+=str(main_outlier_idx[i])+");"
        
        curs.execute(main_outlier_sql)
        main_outlier_rows = curs.fetchall()
             
     
        for row in main_outlier_rows:
            tag+="".join(row[5])     
            main_outlier_sentence_cnt += row[6]                  
            if(row[2] is None):
                main_outlier_text+="".join(row[1])             
            else:
                main_outlier_text+="".join(row[2])
        main_outlier_tag=self.selectTag(tag)       
        
        
        print("===============================================================")
        print("====================== START CREATE_JSON ======================")
        print("===============================================================\n")
        
        print("[MAIN+OUTLIER Sentence Count] = "+str(main_outlier_sentence_cnt))
        
        start_time = time.time()
        print("<START> [MAIN + OUTLIER] Create Title(main+outlier) Summa")
        lexrank.summarize(main_outlier_text)
        print("     [TOTAL]: %.02f sec" % (time.time() - start_time))
        print("<END>   [MAIN + OUTLIER] Create Title(main+outlier) Summa\n")
        
        
        summaries=lexrank.probe(self.total_event)

        
        find=0
        db_link=""
        main_outlier_summa=""
        for summa in summaries:
            
            summa=str(summa)
            if(summa.find("기자]")!=-1):
                summa = self.deleteNoise(summa)
   
            for row in main_outlier_rows:
                if(row[2] is None):
                    temp="".join(row[1])
                    if(temp.find("".join(summa))!=-1):
                        db_link = str(row[7])
                        find+=1                        
                        main_outlier_summa += summa+". "
                        break;
                else:
                    temp="".join(row[2])
                    if(temp.find("".join(summa))!=-1):
                        db_link = str(row[7])
                        find+=1
                        main_outlier_summa += summa+". "                 
                        break;
                                   
            if(find==(1)):
                break
                           
            
        total_data = OrderedDict()
        
        total_data["scale"] = ""
        total_data["title"] =  {
    		        "media": {
    		            "caption": "",
    		            "credit": "",
    		            "url": db_link,
    		            "thumb": 	""
    		        },
    	            "text": {
    	                "headline": main_outlier_tag,
    	                "text": main_outlier_summa
    	            }
    	    }
        ##############################################################################                                     
                # MAKE TITLE # END
        ##############################################################################         

        ##############################################################################      
                # MAKE EVENTS # START
        ##############################################################################        
        events = []
        
        main_idx_size=len(self.main_idx)
        main_text=""
        
        outlier_idx_size=len(self.outlier_idx) 
        outlier_text=""
        
        main_sql = "SELECT id,raw,summa,title,date,tag,sentence_cnt,link FROM "+self.table+" WHERE id in("
        for i in range(main_idx_size):
            if(i!=(main_idx_size-1)):
                main_sql+=str(self.main_idx[i])+","
            else:
                main_sql+=str(self.main_idx[i])+");"
                                         
        curs.execute(main_sql)
        main_rows = curs.fetchall()
        for row in main_rows:
            if(row[2] is None):
                main_text+="".join(row[1])
            else:
                main_text+="".join(row[2])
        
        start_time=time.time()
        print("<START> [MAIN] Create main summa")
        lexrank.summarize(main_text)
        print("     [TOTAL]: %.02f sec" % (time.time() - start_time))
        print("<END>   [MAIN] Create main summa\n")
        
        start_time=time.time()
        print("<START> [MAIN] Get distinct article summaries")
        summaries=self.getDistinctArticleSummaries(lexrank,main_rows,self.main_event)
        print("     [TOTAL]: %.02f sec" % (time.time() - start_time))
        print("<END>   [MAIN] Get distinct article summaries\n")
        
        start_time=time.time()
        print("<START> [MAIN] Create main events")
        events += self.makeEvents(summaries,main_rows,self.main_event)
        print("     [TOTAL]: %.02f sec" % (time.time() - start_time))
        print("<END>   [MAIN] Create main events\n")
        
        outlier_sql = "SELECT id,raw,summa,title,date,tag,sentence_cnt,link FROM "+self.table+" WHERE id in("
        for i in range(outlier_idx_size):
            if(i!=(outlier_idx_size-1)):
                outlier_sql+=str(self.outlier_idx[i])+","
            else:
                outlier_sql+=str(self.outlier_idx[i])+");"
                 
        curs.execute(outlier_sql)
        outlier_rows = curs.fetchall()
        for row in outlier_rows:
            if(row[2] is None):
                outlier_text+="".join(row[1])
            else:
                outlier_text+="".join(row[2])

        start_time=time.time()
        print("<START> [OUTLIER] Create outlier summa")
        lexrank.summarize(outlier_text)
        print("     [TOTAL]: %.02f sec" % (time.time() - start_time))
        print("<END>   [OUTLIER] Create outlier summa\n")
        
        start_time=time.time()
        print("<START> [OUTLIER] get Distinct Article Summaries")
        summaries=self.getDistinctArticleSummaries(lexrank,outlier_rows,self.total_event-self.main_event)
        print("     [TOTAL]: %.02f sec" % (time.time() - start_time))
        print("<END>   [OUTLIER] get Distinct Article Summaries\n")
        
        start_time=time.time()
        print("<START> [OUTLIER] Create outlier events")
        events += self.makeEvents(summaries,outlier_rows,self.total_event-self.main_event)
        print("     [TOTAL]: %.02f sec" % (time.time() - start_time))
        print("<END>   [OUTLIER] Create outlier events\n")
        
        total_data["events"]=events
        ##############################################################################      
                # MAKE EVENTS # END
        ##############################################################################         
        
        numTag=3
        fileTag=""
        for i in range(0,numTag):
            fileTag+="".join(main_outlier_tag.split(' ')[i])
            if(i!=numTag-1):
                fileTag+="-"
        
        file_path="JSON/"+fileTag+"_"+str(self.total_event)+".json"
        with codecs.open(file_path,'w',encoding="utf-8") as make_file:
            json.dump(total_data, make_file, ensure_ascii=False, indent=4, 
                      sort_keys=False)
        
        print("\n<<< TOTAL createJSON >>> : %.02f sec\n\n" % (time.time() - start_time_createJSON))
    
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
    
    
    def getDistinctArticleSummaries(self,lexrank,rows,x_event):
        
        final_distArticle_summmaries = []
        probe_n = x_event
        
        while True:
            dupCount=0
            summaries=lexrank.probe(probe_n)
            distArticle_summmaries=[]
            distArticle_titles=[]
            distArticle_size=0
            for summa in summaries:
                
                dupCheck=False
                for row in rows:
                    
                    # When Summa value is None
                    if(row[2] is None):
                        temp="".join(row[1])
                        if(temp.find("".join(summa))!=-1):
                            db_title=str(row[3])
                           
                            if(distArticle_size>0):
                                for i in range(0,distArticle_size):
                                    if(distArticle_titles[i]==db_title):
                                        dupCheck=True
                                        dupCount+=1
                                        break
                            
                            if(dupCheck==False):
                                distArticle_summmaries.append(summa)
                                distArticle_titles.append(db_title)
                                distArticle_size += 1
                            
                            break
                        
                    # When Summa value isn't None
                    else:
                        temp="".join(row[2])
                        if(temp.find("".join(summa))!=-1):
                            db_title=str(row[3])
                            
                            if(distArticle_size>0):
                                for i in range(0,distArticle_size):
                                    if(distArticle_titles[i]==db_title):
                                        dupCheck=True
                                        dupCount+=1
                                        break
                            
                            if(dupCheck==False):
                                distArticle_summmaries.append(summa)
                                distArticle_titles.append(db_title)
                                distArticle_size += 1
                            
                            break
                
                if(distArticle_size==x_event):
                    break
                
            # <SUCCESS>, Summas of x_event removed duplicates
            if(distArticle_size==x_event):
                final_distArticle_summmaries = distArticle_summmaries
                break
            elif(distArticle_size!=x_event):
                
                # <FAIL>, If the find() does not find an article in the summary sentence
                if(dupCount==0):
                    probe_n += 1                    
                # <FAIL>, If x_event's summa can not be created because of duplicate articles
                else:
                    probe_n += dupCount
                      
            
        return final_distArticle_summmaries

        
    def makeEvents(self,summaries,rows,x_event):
        
        lexrank = LexRank()
        events=[]
        events_size=0
        for summa in summaries:
            
            find=False
            text={}
            summa=str(summa)
            db_date=""
            if(summa.find("기자]")!=-1):
                summa = self.deleteNoise(summa)    
            
            for row in rows:
                
                # When Summa value is none
                if(row[2] is None):
                    temp="".join(row[1])
                    if(temp.find("".join(summa))!=-1):
                        find=True
                        
                        db_raw=str(row[1])
                        db_summa=str(row[2])
                        db_title=str(row[3])
                        db_date=str(row[4])
                        db_sentenceCnt=str(row[6])
                        db_link = str(row[7])
                        
                        if(db_raw.find("기자]")!=-1):
                            db_raw = self.deleteNoise(db_raw)
                        if(db_summa.find("기자]")!=-1):
                            db_summa = self.deleteNoise(db_summa)                        
                        if(db_title.find("기자]")!=-1):
                            db_title = self.deleteNoise(db_title)
                        
                        text["headline"]=db_title
                        text["text"]=db_raw
                        text["text2"]=db_raw
                        if(db_sentenceCnt>self.summa_count):
                            raw="".join(row[1])
                            lexrank.summarize(raw)
                            raw_summaries=lexrank.probe(self.summa_count)
                            text3_summa=""
                            
                            for raw_summa in raw_summaries:
                                text3_summa += str(raw_summa)+". "
                            
                            if(text3_summa.find("기자]")!=-1):
                                text3_summa = self.deleteNoise(text3_summa)                        
                            text["text3"]=text3_summa
                        else:
                            text["text3"]=""
                        break;
                        
                # When Summa value isn't none
                else:
                    temp="".join(row[2])
                    if(temp.find("".join(summa))!=-1):
                        find=True
                        
                        db_raw=str(row[1])
                        db_summa=str(row[2])
                        db_title=str(row[3])
                        db_date=str(row[4])
                        db_sentenceCnt=str(row[6])
                        db_link = str(row[7])
                        
                        if(db_raw.find("기자]")!=-1):
                            db_raw = self.deleteNoise(db_raw)
                        if(db_summa.find("기자]")!=-1):
                            db_summa = self.deleteNoise(db_summa)                        
                        if(db_title.find("기자]")!=-1):
                            db_title = self.deleteNoise(db_title)
                        
                        text["headline"]=db_title
                        text["text"]=db_raw
                        text["text2"]=db_summa
                        
                        if(db_sentenceCnt>self.summa_count):
                            raw="".join(row[1])
                            lexrank.summarize(raw)
                            raw_summaries=lexrank.probe(self.summa_count)
                            text3_summa=""
                            
                            for raw_summa in raw_summaries:
                                text3_summa += str(raw_summa)+". "
                            
                            if(text3_summa.find("기자]")!=-1):
                                text3_summa = self.deleteNoise(text3_summa)                        
                            text["text3"]=text3_summa
                        else:
                            text["text3"]=""
                        break;
                    
            if(find==True):
                event={
                        "start_date": {
                        "year":		db_date.split('-')[0],
                        "month":	     db_date.split('-')[1],
                        "day": 		db_date.split('-')[2],
                        "hour": 		"",
                        "minute": 		"",
                        "second": 		"",
                        "millisecond": 	"",
                        "format": 		""
                        },
    		              "group":        db_date.split('-')[1],
                        "media": {
                        "caption": "",
                        "credit": "",
                        "url":          db_link,
                        "thumb": 	""
                        }
                }                           
                event["text"]=text
                events.append(event)
                events_size += 1
                
            if(events_size == x_event):
                break
            
        return events
    


        
        
        
        
        
         
        
  


      
