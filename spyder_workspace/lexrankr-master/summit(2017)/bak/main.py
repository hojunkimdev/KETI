#-*-encoding:utf-8-*-

#!/usr/bin/env python -W ignore::DeprecationWarning


import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0,os.getcwd()+"/LexRank")
sys.path.insert(0,os.getcwd()+"/KW_lib")

import pymysql.cursors
from lexrankr import LexRank
from kw_summa import KW_SUMMA
from kw_db import KW_DB

def main():    
        
    conn = pymysql.connect(host='localhost',
                           user='your_id', 
                           password='your_password',
                           db='your_db', 
                           use_unicode=True,
                           charset='utf8')   
    
    """
    1. KW_SUMMA(Multi-Document Summarization)

    # Input documents of Main media and Outlier
    main_idx=[12426, 12448, 12504, 12524, 12971, 16790, 17181, 17221, 17222]
    outlier_idx=[1386, 13544, 20003, 20020, 20021, 20025]
    
    # __init__(self,conn,table,main_idx,outlier_idx,total_event,main_event,summa_count,tag_count):
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    
    # The JSON file is stored in the ../JSON folder
    KS.createJSON()
    
    # DB Close
    conn.close()
    
    """
        
    
    """
    2. KW_DB(Database Management)

    # Table settings to update
    KD = KW_DB(conn,"your_table")

    # Update the number of sentences in document to the sentence_cnt column
    KD.insertSentenceCount()
    
    # Update the summary of the document to the summa column
    KD.insertSumma()

    # DB Close
    conn.close()

    """
    
if __name__ == "__main__":
    main()
