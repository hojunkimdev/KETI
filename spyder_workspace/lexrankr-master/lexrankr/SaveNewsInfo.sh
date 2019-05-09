#!/bin/bash

TABLE=$1
query="select avg(sentence_cnt) from KETI."$TABLE"_news;"
echo $query
mysql -h localhost -u user -p\(\(user\)\) -D KETI -e "$query" > auto_params.config
 

