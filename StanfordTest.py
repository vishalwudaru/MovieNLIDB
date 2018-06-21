# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:48:11 2018

@author: VISHAL-PC
"""
from nltk import pos_tag, word_tokenize, ne_chunk
from nltk.chunk import tree2conlltags

from stanfordcorenlp import StanfordCoreNLP
from word2number import w2n
import sqlite3

nlp = StanfordCoreNLP(r'D:\IIIT\stanford-corenlp-full-2018-02-27')

sentence = 'list top ten action or adventure movies of Tom Cruise and Tom Hardy'

pos = nlp.pos_tag(sentence)
#ner = nlp.ner(sentence)
#cparse = nlp.parse(sentence)
#dparse = nlp.dependency_parse(sentence)
print('Completed')
nlp.close()

pos_tags = {}
pos2=[]
k=1
i=0
while i<len(pos):
    if(pos[i][1]=='NNP' or pos[i][1]=='NNPS'):
        i = i+1
        name  = pos[i-1][0]
        while((i<len(pos)) and (pos[i][1]=='NNP' or pos[i][1]=='NNPS')):
            name += ' '+pos[i][0]
            i = i+1
        if 'NNP' not in pos_tags:
            pos_tags['NNP'] = [name]
        else:
            pos_tags['NNP'].append(name)
        i = i-1
        pos_data = (name,'NNP',k)
    else:
        if pos[i][1] not in pos_tags:
            pos_tags[pos[i][1]] = [pos[i][0]]
        else:
            pos_tags[pos[i][1]].append(pos[i][0])
        pos_data = (pos[i][0],pos[i][1],k)
    pos2.append(pos_data)
    k += 1
    i +=1


num = 5
if('CD' in pos_tags):
    num = w2n.word_to_num(pos_tags['CD'][0])

order = 'desc'
if('JJ' in pos_tags):
    if(pos_tags['JJ'][0]=='bottom'):
        order = 'asc'

genre = ''
if('NN' in pos_tags):
    genre = 'where'
    for d in pos_tags['NN']:
        genre  = genre + ' lower(g.NAME)="'+d+'" or'
    genre = genre[:-3]

command  = 'select t.NAME from(select m.* from MOVIE m \
                            left join MOVIE_GENRE mg on mg.MOVIE_ID = m.ID \
                            left join GENRE g on g.ID = mg.GENRE_ID '+genre+'\
                            order by RATING '+order+')t \
                            limit '+str(num)
print(command)

conn = sqlite3.connect('MovieDB.db')
print ("Opened database successfully")

cursor = conn.execute(command)
for row in cursor:
   print( "NAME = ", row[0])

print ("Operation done successfully")
conn.close()
#==============================================================================
# #print( 'Tokenize:', nlp.word_tokenize(sentence))
# print( 'Part of Speech:', nlp.pos_tag(sentence))
# print( 'Named Entities:', nlp.ner(sentence))
# #print( 'Constituency Parsing:', nlp.parse(sentence))
# #print( 'Dependency Parsing:', nlp.dependency_parse(sentence))
# 
# props={'annotators': 'ner','pipelineLanguage':'en','outputFormat':'text'}
# data =nlp.annotate(sentence, properties=props)
# print(data)
# nlp.close()
# 
# pos = pos_tag(word_tokenize(sentence))
# chunks = ne_chunk(pos)
# iob = tree2conlltags(chunks)
# 
# print(pos)
# print(iob)
#==============================================================================
