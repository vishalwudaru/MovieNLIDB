# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:48:11 2018

@author: VISHAL-PC
"""
from nltk.stem import WordNetLemmatizer

from stanfordcorenlp import StanfordCoreNLP
from word2number import w2n
import sqlite3

nlp = StanfordCoreNLP(r'D:\IIIT\stanford-corenlp-full-2018-02-27')

sentence = 'list top ten action, adventure and not comedy movies'
#sentence = 'directors and actors of action movies'
#sentence = 'top action and not comdey movies'
pos = nlp.pos_tag(sentence)
tok = nlp.word_tokenize(sentence)
#ner = nlp.ner(sentence)
#cparse = nlp.parse(sentence)
dparse = nlp.dependency_parse(sentence)
parsedict = {}
for line in dparse:
    print(line[0]+" "+tok[line[1]-1]+" "+tok[line[2]-1])
    if line[0] not in parsedict:
        parsedict[line[0]] = [[tok[line[1]-1],tok[line[2]-1]]]
    else:
        parsedict[line[0]].append([tok[line[1]-1],tok[line[2]-1]])
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

#To find variables to be printed
attr1 = []
attr2 = []
if 'nsubj' in parsedict:
    att=parsedict['nsubj'][0][1]
elif 'dep' in parsedict:
    att=parsedict['dep'][0][1]
elif 'appos' in parsedict:
    att=parsedict['appos'][0][1]
else:
    att=parsedict['ROOT'][0][1]
attr1.append(att)
attr2.append('')
for i in range(len(dparse)):
    if((dparse[i][0]=='cc' or dparse[i][0]=='punct') and tok[dparse[i][1]-1]==att):
        if(dparse[i][0]=='punct'):
            strr ="or"
        else:
            strr= tok[dparse[i][2]-1]
        attr1.append(tok[dparse[i+1][2]-1])
        attr2.append(strr)

genrelist=['action', 'adventure', 'fantasy', 'sci-fi', 'thriller', 
           'romance', 'animation', 'comedy', 'family', 'musical', 
           'mystery', 'western', 'drama', 'history', 'sport', 'crime', 'horror']
#To find genre
gen1 =[]
gen2 =[]
if 'NN' in pos_tags:
    for d in pos_tags['NN']:
        if d in genrelist:
            gen1.append(d)
            strr =''
            for i in range(len(dparse)):
                if((dparse[i][0]=='compound' or dparse[i][0]=='conj') and tok[dparse[i][2]-1]==d):
                    #print(d)
                    if(dparse[i-1][0]=='neg'):
                        strr = ' not'+strr
                        i -=1
                    if(dparse[i-1][0]=='cc'):
                        strr = tok[dparse[i-1][2]-1]+strr
                        break
                    if(dparse[i-1][0]=='punct'):
                        strr = 'or'+strr
                        break
            gen2.append(strr)

#To get proper nouns(members)
ppn = []

actor = ['actor','hero','heroine']
director = ['director']

mem1=[]
mem2=[]

mov1=[]
mov2=[]                  
wordnet_lemmatizer = WordNetLemmatizer()
for i in range(len(attr1)):
    d = wordnet_lemmatizer.lemmatize(attr1[i])
    if d in actor:
        mem1.append('actor')
        mem2.append(attr2[i])
    elif d in director:
        mem1.append('director')
        mem2.append(attr2[i])
    else:
        mov1.append(d)
        mov2.append(attr2[i])

num = 0
if('CD' in pos_tags):
    num = w2n.word_to_num(pos_tags['CD'][0])
elif 'NNS' not in pos_tags:
    num = 1

order = 'desc'
if('JJ' in pos_tags):
    if(pos_tags['JJ'][0]=='bottom'):
        order = 'asc'

genre = ''
if(len(gen1)>0):
    genre = 'where'
    for i in range(len(gen1)):
        genre  = genre +' '+gen2[i] +' lower(g.NAME)="'+gen1[i]+'"'

command  = 'select distinct m.* from MOVIE m \
            left join MOVIE_GENRE mg on mg.MOVIE_ID = m.ID \
            left join GENRE g on g.ID = mg.GENRE_ID '+genre+'\
            order by RATING '+order

if(num>0):
    command = 'select t.NAME from('+command+')t limit '+str(num)

print(command)

conn = sqlite3.connect('Data/MovieDB.db')
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
