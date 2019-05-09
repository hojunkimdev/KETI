# -*- coding: utf-8 -*-

lexrank = LexRank()  # can init with various settings


    

    
        # MySQL Connection 연결
    conn = pymysql.connect(host='localhost',
                           user='user', 
                           password='((user))',
                           db='KETI', 
                           use_unicode=True,
                           charset='utf8')
 
    curs = conn.cursor()
    text=""
    
     
    t=5
    n=4
    
    #main_idx=[1,2,3,4,19584,19485,19486,19487,19488,19489,19490,38596,38597,38598,38599,38600]
    main_idx=[12426,12448,12524,16790,17181,17221,17222,17904,18229,19995,20025,20026,20030,20033,20121,20123,20138,20139,20141,20143,20150,20495,20563,20600,24206,24352,24387,24531,24566,24570,24608,24752,24758,25905,26199,26234,26241,26247,26298,26301,26367,26389,26634,27662,27684,27758,27762,27767,28807,28879,28951,28960,28981,28987,29048,29181,29192,29238,29242,29243]
    #main_idx=[12426,12448,12524,16790]
    main_idx_size=len(main_idx)
    #outlier_idx=[5,6,7,8,19491,19492,19493,19494,19495,19496,19497,3859,38601,38602,38603,38604]
    outlier_idx=[1386,12971,13544,19983,19993,20003,20018,20020,20021,20136,20484,20587,20588,21247,21679,21822,21867,22871,23167,23355,23669,23893,23894,24874,24888,25430,26312,26732,26842,26861,26880,27028,27308,27635,27648,28824,29283,29288]
    #outlier_idx=[1386,12971,13544,19983]
    outlier_idx_size=len(outlier_idx)
    
    
     
    tag=""
    main_text=""
    main_summa=""
                
    outlier_text=""
    outlier_summa=""
        
    main_outlier_summa=""
        
    
    
    main_sql = "SELECT id,raw,summa,title,date,tag FROM KETI.movie_news WHERE id in("
        
    for i in range(main_idx_size):
        if(i!=(main_idx_size-1)):
            main_sql+=str(main_idx[i])+","
        else:
            main_sql+=str(main_idx[i])+");"
             
    
                               
    curs.execute(main_sql)
    rows = curs.fetchall()
    for row in rows:
        tag+="".join(row[5])
        if(row[2] is None):
            main_text+="".join(row[1])
        else:
            main_text+="".join(row[2])
        
    lexrank.summarize(main_text)
    summaries=lexrank.probe(n)
   
    for summa in summaries:
        main_summa+="".join(summa)
        main_summa+=". "
    
    
    
        
   
    
    outlier_sql = "SELECT id,raw,summa,title,date,tag FROM KETI.movie_news WHERE id in("
        
    for i in range(outlier_idx_size):
        if(i!=(outlier_idx_size-1)):
            outlier_sql+=str(outlier_idx[i])+","
        else:
            outlier_sql+=str(outlier_idx[i])+");"
             
                                  
    curs.execute(outlier_sql)
    rows = curs.fetchall()
    for row in rows:
        tag+="".join(row[5])
        if(row[2] is None):
            outlier_text+="".join(row[1])
        else:
            outlier_text+="".join(row[2])
        
    lexrank.summarize(outlier_text)
    summaries=lexrank.probe(t-n)
    
    outlier_summa ="[ OUTLIER ] "
    for summa in summaries:
        outlier_summa+="".join(summa)
        outlier_summa+=". "
               
    main_outlier_summa += main_summa +outlier_summa
    
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
    main_outlier_tag=""
    for tag in sorted_tag_list:
        main_outlier_tag+=tag+" "
        if(i==5):
            break
        i+=1
        
    
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
    
    for m in range (1,9):
        
        
                        
        main_text=""
        main_summa=""
                
        outlier_text=""
        outlier_summa=""
        
        main_outlier_summa=""
        
        main_sql = "SELECT id,raw,summa,title,date FROM KETI.movie_news WHERE id in("
        
        for i in range(main_idx_size):
            if(i!=(main_idx_size-1)):
                main_sql+=str(main_idx[i])+","
            else:
                main_sql+=str(main_idx[i])+") and date BETWEEN '2017-"+str(m)+"-01' and '2017-"+str(m)+"-31';"
             
        main_summa+="[ Main Media ]\n"+ str(n) + " summas\n" + "SQL = " +main_sql+"\n\n"
                               
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
        summaries=lexrank.probe(n)
       
        
        
        item_idx=1
        text={}
        for summa in summaries:
            eq=False
            for row in rows:
                if(row[2] is None):
                    temp="".join(row[1])
                    if(temp.find("".join(summa))!=-1):
                        main_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
                        for checkDupIdx in range(1,item_idx):
                            if(text["headline"+str(checkDupIdx)] == row[3]):
                                text["text"+str(checkDupIdx)] += summa+". "
                                eq=True
                                break
                        
                        if(eq==False):
                            text["headline"+str(item_idx)]=row[3]
                            text["text"+str(item_idx)]=summa+". "
                            item_idx+=1
                        break
                else:
                    temp="".join(row[2])
                    if(temp.find("".join(summa))!=-1):
                        main_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
                        for checkDupIdx in range(1,item_idx):
                            if(text["headline"+str(checkDupIdx)] == row[3]):
                                text["text"+str(checkDupIdx)] += summa+". "
                                eq=True
                                break
                        
                        if(eq==False):
                            text["headline"+str(item_idx)]=row[3]
                            text["text"+str(item_idx)]=summa+". "
                            item_idx+=1
                        break
            main_summa+="<summa>: " +summa +".\n\n"
            
            
        outlier_sql = "SELECT id,raw,summa,title,date FROM KETI.movie_news WHERE id in("
        
        for i in range(outlier_idx_size):
            if(i!=(outlier_idx_size-1)):
                outlier_sql+=str(outlier_idx[i])+","
            else:
                outlier_sql+=str(outlier_idx[i])+") and date BETWEEN '2017-"+str(m)+"-01' and '2017-"+str(m)+"-31';"
             
        outlier_summa+="[ Main Media ]\n"+ str(n) + " summas\n" + "SQL = " +outlier_sql+"\n\n"
                               
        curs.execute(outlier_sql)
        rows = curs.fetchall()
        for row in rows:
            if(row[2] is None):
                outlier_text+="".join(row[1])
            else:
                outlier_text+="".join(row[2])
        
        lexrank.summarize(outlier_text)
        
        
        
        summaries=lexrank.probe(n)
            
        find=0
        for summa in summaries:
            eq=False
            for row in rows:
                if(row[2] is None):
                    temp="".join(row[1])
                    if(temp.find("".join(summa))!=-1):
                        find+=1
                        outlier_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
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
                        outlier_summa+="<id>: " +str(row[0]) + "\n<title>: " + row[3] +"\n<date>: "+str(row[4]) +"\n"
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
            if(find==(t-n)):
                break
            outlier_summa+="<summa>: " +summa +".\n\n"    
        
        
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
    

    
    # Print JSON
    print(json.dumps(total_data, ensure_ascii=False, indent=4, sort_keys=False) )