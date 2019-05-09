=======================================
Kwangwoon University Text Summarization
=======================================

Description:
-----------

 1. KW_SUMMA(Multi-Document Summarization)

  - Create a JSON file with morphological analysis of document, graph clustering, elimination of
    duplicate sentences, calculation of cosine similarity and text summarization. 
 
 2. KW_DB(Database Management)

  - Update the number of sentences in the document and the summary of the document in the database.
 
Usage:
-----
   
 1. KW_SUMMA(Multi-Document Summarization)


    ``````````````````````````````````````
    import pymysql.cursors
    from lexrankr import LexRank
    from kw_summa import KW_SUMMA
    
 
    # DB Connection
    conn = pymysql.connect(host='localhost',
                           user='your_id', 
                           password='your_password',
                           db='your_db', 
                           use_unicode=True,
                           charset='utf8')   

    # Input documents
    main_idx=[12426, 12448, 12504, 12524, 12971, 16790, 17181, 17221, 17222]
    outlier_idx=[1386, 13544, 20003, 20020, 20021, 20025]
    
    # __init__(self,conn,table,main_idx,outlier_idx,total_event,main_event,summa_count,tag_count):
    KS = KW_SUMMA(conn,"movie_news",main_idx,outlier_idx,5,4,2,2)
    
    # The JSON file is stored in the ../JSON folder
    KS.createJSON()
    
    # DB Close
    conn.close()

    ``````````````````````````````````````
 
 2. KW_DB(Database Management)


    ``````````````````````````````````````
    import pymysql.cursors
    from lexrankr import LexRank
    from kw_db import KW_DB
    
 
    # DB Connection
    conn = pymysql.connect(host='localhost',
                           user='your_id', 
                           password='your_password',
                           db='your_db', 
                           use_unicode=True,
                           charset='utf8')   
  
    # Table settings to update
    KD = KW_DB(conn,"your_table")

    # Update the number of sentences in document to the sentence_cnt column
    KD.insertSentenceCount()
    
    # Update the summary of the document to the summa column
    KD.insertSumma()

    # DB Close
    conn.close()

    ``````````````````````````````````````

