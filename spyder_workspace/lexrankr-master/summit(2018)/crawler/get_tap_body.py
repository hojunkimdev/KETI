# -*- coding: utf-8 -*-
import urllib2
import sys
import os
import time
from bs4 import BeautifulSoup
from httplib import IncompleteRead
import pymysql.cursors
reload(sys)
sys.setdefaultencoding('utf-8')

def remove_strange(article): # remove strange word
    f = open(article, 'r')
    while True:
        text = f.readline()
        
def get_title(main_dir, day_articles, Keyword, Year, Month, day, maxbuf = 10485760):
    conn = pymysql.connect(host='localhost',
                           user='user', 
                           password='((user))',
                           db='KETI', 
                           use_unicode=True,
                           charset='utf8') 
     
    f = open(day_articles, 'r')
    rep = ["\n","\t","영상 뉴스","'"]
    
    dir_address = main_dir + '/%s_body'%(Keyword)
    if not os.path.isdir(dir_address):
	os.mkdir(dir_address)
    os.chdir(dir_address)
    
    print os.getcwd()
   
    index = 1
    while True:
        url = f.readline()
        if not url: break
        url = url.replace('\n', '')  # get rid of '\n' -> ''
               
        try:
            res = urllib2.urlopen(url)
        except:
            time.sleep(20)
            res = urllib2.urlopen(url)
        try:
            html = res.read(maxbuf)
            res.close()
        except httplib.IncompleteRead as e:
            html = e.partial
            res.close()

        soup = BeautifulSoup(html,'lxml')
        body = soup.find('div', attrs={'id':'articleBodyContents'})
        
        body_file = open('%s_%s_body.txt' %( Keyword, Year+Month+day), 'a')
        body_file.write('#%s\n'%(index))
        
        for t_title in soup.title:
            title = '%s\n'%(t_title)

        try : 
            sel = body.select("script")#extract 'script' tag
        except :
            continue;
        
        #eliminate unnecessary characters
        for s in sel:
            s.extract()
            
        sel2 = body.select("a") #extract 'a' tag 
        for s in sel2:
            s.extract()
        
        body_text = '%s\n'%(body.text)
        
        
        #conbvert to string type
        url = str(url).strip()
        title = str(title).strip()
        body_text = str(body_text).strip()
        date = Year+'-'+Month+'-'+Day
        
        for re in rep:
            title = title.replace(re,"")
            body_text = body_text.replace(re,"")
        
        #print console
        print title
        print body_text
        
        #print text file
        body_file.write(title)
        body_file.write(body_text)
        
        '''
        #            insert news into database 
        # you should change DB table name and domain as you need
        #           ex. movie_news, social_news
        '''
        table = 'it_news'
        domain = 'it'
        main_sql = "insert into KETI."+table+" values(id,'"+title+"','"+domain+"' , '"+date+"', NULL, '"+ body_text+ "', NULL, '" + url+"',NULL, NULL);"
        curs = conn.cursor()
        curs.execute(main_sql)
        conn.commit()
        
        
        time.sleep(1) 
        index = index + 1
        
        
    os.chdir(main_dir)
    f.close()
    body_file.close()
    conn.close()
      
			
if __name__ == '__main__':
	parent_address = os.getcwd()
	os.chdir(parent_address)
	address = os.getcwd()

try:
	Year=sys.argv[1]
	Month=sys.argv[2]
	Day=sys.argv[3]
	Keyword=sys.argv[4]

	
except Exception:
	 print 'get_tap_url.py [Year] [Month] [day] [SID]'
	 print 'ex : python get_tap_body.py 2018 10 30 100'

else:	

	main_dir = os.getcwd()
	address = main_dir + '/' + Keyword
	os.chdir(address)
	print address
	sid1_dir = os.getcwd()
    
	#get an already existing url file
	day_articles = '%s_%s.txt' %(Keyword, Year+Month+Day)
    
	address = address + '/'+ day_articles
	print address

	get_title(main_dir, day_articles, Keyword,  Year, Month, Day)
	os.chdir(address)
    
	print "finish saving news body"
