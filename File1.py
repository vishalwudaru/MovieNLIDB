# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 15:06:08 2018

@author: VISHAL-PC
"""

from nltk.stem import WordNetLemmatizer

from stanfordcorenlp import StanfordCoreNLP
from word2number import w2n
import sqlite3

nlp = StanfordCoreNLP(r'D:\IIIT\stanford-corenlp-full-2018-02-27')

#sentence = 'ratings of top 2 movies of Tom Hardy and James Cameron'
#sentence = 'best director and actor of action movies'
sentence = 'Top 5 action movies after 1980 and rating below ten and greater than 1 hrs of Tom Hardy and James Cameron'

pos = nlp.pos_tag(sentence)
i = 0
names = []
sentence = ''
while i<len(pos):
    strr = pos[i][0]
    name = strr
    if pos[i][1]=='NNP':
        i += 1
        while((i<len(pos)) and pos[i][1]=='NNP'):
            strr = strr + pos[i][0]
            name = name + ' ' + pos[i][0]
            i += 1
        names.append(name)
        i = i-1
    i += 1
    sentence = sentence + strr + ' '  
tok = nlp.word_tokenize(sentence)
pos = nlp.pos_tag(sentence)
#ner = nlp.ner(sentence)
#cparse = nlp.parse(sentence)
dparse = nlp.dependency_parse(sentence)
print('Completed')
nlp.close()

parsedict = {}
for line in dparse:
    print(line[0]+" "+tok[line[1]-1]+" "+tok[line[2]-1])
    if line[0] not in parsedict:
        parsedict[line[0]] = [[tok[line[1]-1],tok[line[2]-1]]]
    else:
        parsedict[line[0]].append([tok[line[1]-1],tok[line[2]-1]])

pos_tags = {}
for d in pos:
    if d[1] in pos_tags:
        pos_tags[d[1]].append(d[0])
    else:
        pos_tags[d[1]] = [d[0]]

list1 = ['compound', 'conj', 'appos']
list2 = ['cc', 'punct']

def conj(data):
    for i in range(len(dparse)):
        if dparse[i][0] in list1:
            if tok[dparse[i][2]-1] in data:
                k = data.index(tok[dparse[i][2]-1])
                if dparse[i-1][0] == 'neg':
                    data[k] = 'and not ' + data[k]
                if dparse[i-1][0] in list2:
                    data[k] = 'or ' + data[k]
    return data
            

    
#To find person's name
per = []
if 'NNP' in pos_tags:
    per = conj(pos_tags['NNP'])

#To combine NN and NNS and lemmatize
wordnet_lemmatizer = WordNetLemmatizer()
nounslist = []
if 'NN' in pos_tags:
    for d in pos_tags['NN']:
        nounslist.append(wordnet_lemmatizer.lemmatize(d))
if 'NNS' in pos_tags:
    for d in pos_tags['NNS']:
        nounslist.append(wordnet_lemmatizer.lemmatize(d))

#To find genres
genrelist = ['action', 'adventure', 'fantasy', 'sci-fi', 'thriller', 
           'romance', 'animation', 'comedy', 'family', 'musical', 
           'mystery', 'western', 'drama', 'history', 'sport', 'crime', 'horror']

gen = []
for d in nounslist:
    if d in genrelist:
        gen.append(d)

gen = conj(gen)


#To find member table coloums
memlabel = 0
actorlist = ['actor','hero','heroine']
directorlist = ['director'] 

mem = {'actor':0, 'director':0}
bestcount = 0
if len(per) == 0:
    for d in nounslist:
        if d in actorlist:
            if d not in pos_tags['NNS']:
                bestcount = 1
            mem['actor'] = 1
            memlabel = 1
        elif d in directorlist:
            if d not in pos_tags['NNS']:
                bestcount = 1
            mem['director'] = 1
            memlabel = 1


#To find movie table coloums
movielist = ['movie', 'cinema']
ratinglist = ['rating', 'score', 'rated']
durationlist = ['time', 'duration', 'length', 'hour', 'minute', 'hr', 'min']
languagelist = ['language']
yearlist = ['year', 'date']
countrylist = ['country', 'place', 'area']

beforelist = ['before', 'prior', 'early']
afterlist = ['after','follow','later']
inlist = ['in', 'of']
betweenlist = ['between', 'middle', 'later']

lesslist = ['less', 'below', 'before', 'prior', 'early']
greatlist = ['greater', 'above', 'after','follow','later']

hrlist = ['hr', 'hour']
minlist = ['min', 'minute']

if memlabel == 0 and 'CD' in pos_tags:
    #Movie table conditions
    def comp(strr):
        if(strr in greatlist):
            return '> '
        elif(strr in lesslist):
            return '< '
        else:
            return '= '
    
    tokl = []
    for t in tok:
        tokl.append(wordnet_lemmatizer.lemmatize(t))
    
    i = concount = 0
    mcon = ''
    while i < len(dparse):
        fl = 0
        mstr = ''
        if(dparse[i][0] == 'case'):
            if(dparse[i+1][0] == 'nmod'):
                if(dparse[i-1][0] == 'amod' or dparse[i-1][0] == 'conj'):
                    if(tokl[dparse[i-1][1]-1] in ratinglist or tokl[dparse[i-1][2]-1] in ratinglist):
                        if(concount == 0):
                            mstr = 'where t.RATING '
                            concount = 1
                        else:
                            mstr = mstr + ' and t.RATING '
                        if dparse[i-1][0] == 'amod':
                            mstr = mstr + comp(tokl[dparse[i-1][2]-1])
                        else:
                            mstr = mstr + comp(tokl[dparse[i][2]-1])
                        if tokl[dparse[i][1]-1] in pos_tags['CD']:
                            mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1]))
                            fl = 1
                else:
                    if(tokl[dparse[i+1][1]-1] in ratinglist):
                        if(concount == 0):
                            mstr = 'where t.RATING '
                            concount = 1
                        else:
                            mstr = mstr + ' and t.RATING'
                        mstr = mstr + comp(tokl[dparse[i][2]-1])
                        if tokl[dparse[i][1]-1] in pos_tags['CD']:
                            mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1]))
                            fl = 1
                    elif (tokl[dparse[i+1][1]-1] in durationlist):
                        if(concount == 0):
                            mstr = 'where t.DURATION '
                            concount = 1
                        else:
                            mstr = mstr + ' and t.DURATION '
                        mstr = mstr + comp(tokl[dparse[i][2]-1])
                        if tokl[dparse[i][1]-1] in pos_tags['CD']:
                            if tokl[dparse[i+1][1]-1] in minlist:
                                mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1]))
                            else:
                                mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1])*60)
                            fl = 1
                    elif (tokl[dparse[i][1]-1] in pos_tags['CD'] and w2n.word_to_num(tokl[dparse[i][1]-1])>1500):
                        if(concount == 0):
                            mstr = 'where t.YEAR '
                            concount = 1
                        else:
                            mstr = mstr + ' and t.YEAR '
                        mstr = mstr + comp(tokl[dparse[i][2]-1])
                        if tokl[dparse[i][1]-1] in pos_tags['CD']:
                            mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1]))
                            fl = 1
            elif(dparse[i+1][0] == 'nummod'):
                if (tokl[dparse[i+1][1]-1] in durationlist):
                    if(concount == 0):
                        mstr = 'where t.DURATION '
                        concount = 1
                    else:
                        mstr = mstr + ' and t.DURATION '
                    if(dparse[i-1][0] == 'amod' or dparse[i-1][0] == 'conj'):
                        mstr = mstr + comp(tokl[dparse[i-1][2]-1])
                    else:
                        mstr = mstr + comp(tokl[dparse[i][2]-1])
                    if tokl[dparse[i+1][2]-1] in pos_tags['CD']:
                        if tokl[dparse[i+1][1]-1] in minlist:
                            mstr = mstr + str(w2n.word_to_num(tokl[dparse[i+1][2]-1]))
                        else:
                            mstr = mstr + str(w2n.word_to_num(tokl[dparse[i+1][2]-1])*60)
                        fl = 1
        elif (dparse[i][0] == 'mwe' and dparse[i+1][0] == 'nummod'):
            if (tokl[dparse[i+1][1]-1] in durationlist):
                if(concount == 0):
                    mstr = 'where t.DURATION '
                    concount = 1
                else:
                    mstr = mstr + ' and t.DURATION '
                mstr = mstr + comp(tokl[dparse[i+1][2]-1])
                if tokl[dparse[i][1]-1] in pos_tags['CD']:
                    if tokl[dparse[i+1][1]-1] in minlist:
                        mstr = mstr + str(w2n.word_to_num(tokl[dparse[i+1][2]-1]))
                    else:
                        mstr = mstr + str(w2n.word_to_num(tokl[dparse[i+1][2]-1])*60)
                    fl = 1
        if fl == 1:
            mcon = mcon + mstr
        i += 1
                


mov = {'name':0, 'rating':0, 'duration':0, 'language':0, 'year':0, 'country':0}

for d in nounslist:
    if d in movielist:
        mov['name'] = 1
    elif d in ratinglist:
        mov['rating'] = 1
    elif d in durationlist:
        mov['duration'] = 1
    elif d in languagelist:
        mov['language'] = 1
    elif d in yearlist:
        mov['year'] = 1
    elif d in countrylist:
        mov['country'] = 1
          


    
num = 0
i=0
while i < len(dparse):
    if dparse[i][0] == 'nummod' and dparse[i-1][0] != 'case':
        num = w2n.word_to_num(pos_tags['CD'][0])
    i += 1
if 'NNS' not in pos_tags:
    num = 1

order = 'desc'
#==============================================================================
# if('JJ' in pos_tags):
#     if(pos_tags['JJ'][0]=='bottom'):
#         order = 'asc'
#==============================================================================

genre = ''
if(len(gen)>0):
    genre = 'where'
    for i in range(len(gen)):
        ii = gen[i].split()
        for j in range(len(ii)-1):
            genre  = genre +' '+ii[j]
        genre = genre +' lower(g.NAME) = "'+ii[-1].lower()+'"'

memdata = ''
if(len(per)>0):
    memdata = 'where'
    for i in range(len(per)):
        ii = per[i].split()
        for j in range(len(ii)-1):
            memdata  = memdata +' '+ii[j]
        memdata = memdata +' lower(mem.NAME) = "'+names[i].lower()+'"'


column = ''
col = []
for i in mov:
    if mov[i] == 1:
        col.append(i)
        column = column + 't.'+i+', '
column = column[:-2]

if memlabel == 1:
    num = bestcount
    col = ['name','profession']
    column = 'mem.NAME, mem.PROFESSION'
    memdata = 'where mem.PROFESSION = '
    if mem['actor'] == 1 and mem['director'] == 1:
        memdata = memdata + '"director" or mem.PROFESSION = "actor"'
        num = bestcount * 2
    else:
        if mem['actor'] == 1:
            memdata = memdata + '"actor"'
        else:
            memdata = memdata + '"director"'

command = 'select distinct '+column+' from'
command += '(select distinct m.* from MOVIE m '
command += 'left join MOVIE_GENRE mg on mg.MOVIE_ID = m.ID '
command += 'left join GENRE g on g.ID = mg.GENRE_ID '+genre+')t '
command += 'left join MOVIE_MEMBERS mm on mm.MOVIE_ID = t.ID '
command += 'left join MEMBERS mem on mem.ID = mm.MEMBERS_ID '+memdata+' '
if memlabel == 0:
    if memdata != '':
        command = command + 'and' + mcon[5:] + ' '
    else:
        command = command + mcon + ' '
command += 'order by t.RATING '+order


if(num>0):
    command += ' limit '+str(num)



print(command)

conn = sqlite3.connect('MovieDB.db')
print ("Opened database successfully\n")

cursor = conn.execute(command)

rowcount = 0
for row in cursor:
    rowcount += 1
    for i in range(len(col)):
        print( ""+col[i]+":", row[i])
   
print("\n" + str(rowcount) + " rows fetched\n")   

print ("Operation done successfully")
conn.close()
