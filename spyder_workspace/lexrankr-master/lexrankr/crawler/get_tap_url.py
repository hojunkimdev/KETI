# -*- coding: utf-8 -*-
import urllib2
import sys
import os
import time
from bs4 import BeautifulSoup
from httplib import IncompleteRead
import httplib
reload(sys)
sys.setdefaultencoding('utf-8')

def loop_for(address, tap_ori ):
    main_dir = os.getcwd()

    
    dir_address = make_directory(main_dir, tap_ori, Year, Month)	#make directory
    os.chdir(dir_address)	                                        #move OS's working directory
        
    page_num = 1
    while True:            

        address_test = address +'%d'%(page_num)            
        address_max = '%s' % (address_test)
        print address_max
        
        dir_day = Year+Month+Day
        
        get_url(address_max, tap_ori, dir_day)  #get url using beautiful soup
        
        page_num = page_num+1
        
        #you can change maximum page number
        if page_num == 50:
            break;   
    
    
    os.chdir(main_dir)   # go home directory
    
    '''end Loop of page'''


#make_directory function
def make_directory(cur_dir, tap, dir_year, dir_month):
	
	os.chdir(cur_dir)		#change working directory
	address = os.getcwd()
	
	if not os.path.isdir(tap):
		os.mkdir(tap)
	address = address+'/' + tap
	os.chdir(address)
	
	return address


def get_url(address, tap, date, maxbuf = 104857600):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(address, headers=hdr)
    try:
        res = urllib2.urlopen(req)
    except:
        time.sleep(10)
        res = urllib2.urlopen(req)
        print 'fail'
    else:
        try:
            html = res.read(maxbuf)
            res.close()
        except httplib.IncompleteRead as e:
            html = e.partial
            res.close()
            
        soup = BeautifulSoup(html,"lxml")
        
        
        f = open('%s_%s.txt' %( tap, date), 'a')    #file open - save url obtained 
            
        url_list = []
        photo_class = soup.find_all('dt', attrs={'class':'photo'}) #in photo class
        for photo in photo_class:
            photo_link =  photo.a               #in a tag
            url = photo_link.get('href')        #get href attribute
            url_list.append(url)
            f.write(url+'\n')

		
if __name__ == '__main__':
	parent_address = os.getcwd()
	os.chdir(parent_address)
	address = os.getcwd()
    
try:
	Year=sys.argv[1]   
	Month=sys.argv[2]
	Day=sys.argv[3]
	sid1=sys.argv[4]
	sid2=sys.argv[5]
	
except Exception:
    print 'get_tap_url.py [Year] [Month] [day] [SID] [SID2]'
    print 'ex : python get_tap_url.py 2018 10 30 100 269'


else:
    #naver news base url
    address = 'https://news.naver.com/main/list.nhn?mode=LS2D&sid2='+sid2+'&sid1='+sid1+'&mid=shm&date='+Year+Month+Day+'&page='
    loop_for(address, sid1)
	

