# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 15:06:08 2018

@author: VISHAL-PC
"""

from nltk.stem import WordNetLemmatizer

from stanfordcorenlp import StanfordCoreNLP
from word2number import w2n
import sqlite3

def englishToSQL(sentence):

    nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')

    #sentence = 'ratings of top 2 movies of Tom Hardy and James Cameron'
    #sentence = 'best director and actor of action movies'
    #sentence = 'Top 5 action and adventure movies after 1980, greater than 100 mins and rating above 5 of Tom Hardy and James Cameron'
    #sentence = 'movies rated above 8'
    
    
    pos = nlp.pos_tag(sentence)
    i = 0
    names = []
    sentence = ''
    while i<len(pos):
        strr = pos[i][0]
        name = strr
        if pos[i][1]=='NNP':
            i += 1
            while((i<len(pos)) and pos[i][1]=='NNP' ):
                strr = strr + pos[i][0]
                name = name + ' ' + pos[i][0]
                i += 1
            names.append(name)
            i = i-1
        else:
            strr = strr.lower()
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
    
    wordnet_lemmatizer = WordNetLemmatizer()
    tokl = []
    for t in tok:
        tokl.append(wordnet_lemmatizer.lemmatize(t))
    
    list1 = ['compound', 'conj', 'appos', 'amod']
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
                
    countrynames = ['usa', 'uk', 'new zealand', 'canada', 'australia']
    languages = ['english']
        
    
    per = []
    perr = []
    cou = []
    couu = []
    lan = []
    lann = []
    i = 0
    while i < len(names):
        if names[i].lower() in countrynames:
            cou.append(pos_tags['NNP'][i])
            couu.append(names[i])
        elif names[i].lower() in languages:
            lan.append(pos_tags['NNP'][i])
            lann.append(names[i])
        else:
            per.append(pos_tags['NNP'][i])
            perr.append(names[i])
        i += 1
    
    #To find languages
    for t in tokl:
        if t in languages:
            lan.append(t)
            lann.append(t)
    if len(lan) > 0:
        lan = conj(lan)
    
    #To find countries
    if len(cou) > 0:
        cou = conj(cou)
    
    #To find person's name
    if len(per) > 0:
        per = conj(per)
    
    #To combine NN and NNS and lemmatize
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
    for d in tokl:
        if d in genrelist:
            gen.append(d)
    
    gen = conj(gen)
    
    #For handling not
    notflag = 0
    gen1 =[]
    for g in gen:
        gen1.append(g)
    i = 0
    while i < len(gen1):
        ii = gen1[i].split()
        if len(ii) == 2:
            gen1[i] = " and not "+ii[1]
        elif len(ii) == 3:
            gen1[i] = "and "+ii[2]
            notflag = 1
        else:
            gen1[i] = "not " + gen1[i]
        i += 1
    
    
    #To find member table coloums
    memlabel = 0
    actorlist = ['actor','hero','heroine', 'cast']
    directorlist = ['director', 'crew'] 
    
    mem = {'actor':0, 'director':0}
    bestcount = 0
    for d in nounslist:
        if d in actorlist:
            if 'NN' in pos_tags and d in pos_tags['NN']:
                bestcount = 1
            mem['actor'] = 1
            memlabel = 1
        elif d in directorlist:
            if 'NN' in pos_tags and d in pos_tags['NN']:
                bestcount = 1
            mem['director'] = 1
            memlabel = 1
    
    
    #To find movie table coloums
    movielist = ['movie', 'cinema']
    ratinglist = ['rating', 'score', 'rated']
    durationlist = ['time', 'duration', 'length', 'hour', 'minute', 'hr', 'min', 'runtime']
    languagelist = ['language']
    yearlist = ['year', 'date', 'when']
    linklist = ['link', 'url', 'website']
    countrylist = ['country', 'city', 'place', 'area', 'where']
    
    #==============================================================================
    #     beforelist = ['before', 'prior', 'early']
    #     afterlist = ['after','follow','later']
    #     inlist = ['in', 'of']
    #     betweenlist = ['between', 'middle', 'later']
    #==============================================================================
    
    lesslist = ['le', 'below', 'before', 'prior', 'early']
    greatlist = ['greater', 'above', 'after','follow','later', 'more', 'long', 'longer']
    
    #==============================================================================
    #     hrlist = ['hr', 'hour']
    #==============================================================================
    minlist = ['min', 'minute']
    
    
    mcon = ''
    #To get condition on countries
    if(len(cou)>0):
        mcon = 'where ('
        for i in range(len(cou)):
            ii = cou[i].split()
            for j in range(len(ii)-1):
                mcon  = mcon +' '+ii[j]
            mcon = mcon +' lower(t.COUNTRY) = "'+couu[i].lower()+'" '
        mcon += ') '
    
    if(len(lan)>0):
        if mcon == '':
            mcon = 'where ('
        else:
            mcon += 'and ('
        for i in range(len(lan)):
            ii = lan[i].split()
            for j in range(len(ii)-1):
                mcon  = mcon +' '+ii[j]
            mcon = mcon +' lower(t.LANGUAGE) = "'+lann[i].lower()+'" '
        mcon += ') '
    
    if 'CD' in pos_tags:
        #Movie table conditions
        def comp(strr):
            if(strr in greatlist):
                return '> '
            elif(strr in lesslist):
                return '< '
            else:
                return '= '
        
        i = 0
        while i < len(dparse):
            fl = 0
            mstr = ''
            if(dparse[i][0] == 'case'):
                if (tokl[dparse[i][1]-1] in pos_tags['CD'] and w2n.word_to_num(tokl[dparse[i][1]-1])>1500):
                    if(mcon == ''):
                        mstr = 'where t.YEAR '
                    else:
                        mstr = mstr + ' and t.YEAR '
                    mstr = mstr + comp(tokl[dparse[i][2]-1])
                    if tokl[dparse[i][1]-1] in pos_tags['CD']:
                        mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1]))
                        fl = 1
                elif(dparse[i+1][0] == 'nmod'):
                    if(dparse[i-1][0] == 'amod' or (dparse[i-1][0] == 'conj' and tokl[dparse[i-1][2]-1] in ratinglist)):
                        if(tokl[dparse[i-1][1]-1] in ratinglist or tokl[dparse[i-1][2]-1] in ratinglist):
                            if(mcon == ''):
                                mstr = 'where t.RATING '
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
                        print(tokl[dparse[i][1]-1])
                        if(tokl[dparse[i+1][1]-1] in ratinglist):
                            if(mcon == ''):
                                mstr = 'where t.RATING '
                            else:
                                mstr = mstr + ' and t.RATING'
                            mstr = mstr + comp(tokl[dparse[i][2]-1])
                            if tokl[dparse[i][1]-1] in pos_tags['CD']:
                                mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1]))
                            if(i+3 < len(dparse) and dparse[i+2][0] == 'cc' and dparse[i+3][0] == 'case'):
                                mstr = mstr + ' and t.RATING'
                                mstr = mstr + comp(tokl[dparse[i+3][2]-1])
                                if tokl[dparse[i+3][1]-1] in pos_tags['CD']:
                                    mstr = mstr + str(w2n.word_to_num(tokl[dparse[i+3][1]-1]))
                                fl = 1
                        elif (tokl[dparse[i+1][1]-1] in durationlist):
                            if(mcon == ''):
                                mstr = 'where t.DURATION '
                            else:
                                mstr = mstr + ' and t.DURATION '
                            mstr = mstr + comp(tokl[dparse[i][2]-1])
                            if tokl[dparse[i][1]-1] in pos_tags['CD']:
                                if tokl[dparse[i+1][1]-1] in minlist:
                                    mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1]))
                                else:
                                    mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1])*60)
                                fl = 1
                elif(dparse[i+1][0] == 'nummod'):
                    if (tokl[dparse[i+1][1]-1] in durationlist):
                        if(mcon == ''):
                            mstr = 'where t.DURATION '
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
                elif(dparse[i+1][0] == 'dep'):
                    if(dparse[i-1][0] == 'conj'):
                        if(tokl[dparse[i-1][2]-1] in ratinglist):
                            if(mcon == ''):
                                mstr = 'where t.RATING '
                            else:
                                mstr = mstr + ' and t.RATING'
                            mstr = mstr + comp(tokl[dparse[i][2]-1])
                            if tokl[dparse[i+1][2]-1] in pos_tags['CD']:
                                mstr = mstr + str(w2n.word_to_num(tokl[dparse[i+1][2]-1]))
                                fl = 1
            elif (dparse[i][0] == 'advmod' and (i+3 < len(dparse) and (dparse[i+2][0] == 'nummod' or dparse[i+3][0] == 'dep')) ):
                if dparse[i+2][0] == 'nummod':
                    dname = tokl[dparse[i+2][1]-1]
                else:
                    dname = tokl[dparse[i+3][2]-1]
                if (dname in durationlist):
                    if(mcon == ''):
                        mstr = 'where t.DURATION '
                    else:
                        mstr = mstr + ' and t.DURATION '
                    mstr = mstr + comp(tokl[dparse[i][2]-1])
                    if tokl[dparse[i][1]-1] in pos_tags['CD']:
                        if dname in minlist:
                            mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1]))
                        else:
                            mstr = mstr + str(w2n.word_to_num(tokl[dparse[i][1]-1])*60)
                        fl = 1
            if fl == 1:
                mcon = mcon + mstr
            i += 1
                    
    
    
    mov = {'name':0, 'rating':0, 'duration':0, 'language':0, 'year':0, 'country':0, 'link':0}
    
    for d in tokl:
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
        elif d in linklist:
            mov['link'] = 1
              
    
    
        
    num = 0
    i=0
    while i < len(dparse):
        if dparse[i][0] == 'nummod' and (dparse[i-1][0] != 'case' and dparse[i-1][0] != 'mwe'):
            num = w2n.word_to_num(pos_tags['CD'][0])
        i += 1
    if 'NNS' not in pos_tags:
        num = 1
    
    
    order = 'desc'
    if('JJ' in pos_tags):
        if'worst' in tokl: 
            order = 'asc'
    
    genre = ''
    if(len(gen)>0):
        genre = 'where'
        for i in range(len(gen)):
            ii = gen[i].split()
            for j in range(len(ii)-1):
                genre  = genre +' '+ii[j]
            genre = genre +' lower(g.NAME) = "'+ii[-1].lower()+'"'
    
    genre1 = ''
    if(len(gen1)>0):
        genre1 = 'where'
        for i in range(len(gen1)):
            ii = gen1[i].split()
            for j in range(len(ii)-1):
                genre1  = genre1 +' '+ii[j]
            genre1 = genre1 +' lower(g.NAME) = "'+ii[-1].lower()+'"'
    
    memdata = ''
    if len(genre)<1 and len(per)>0 and mov['name'] == 0:
        genre = 'where '
        for i in range(len(per)):
            ii = per[i].split()
            for j in range(len(ii)-1):
                genre  = genre +' '+ii[j]
            genre = genre +' lower(m.NAME) = "'+names[i].lower()+'"'
    else:
        if(len(per)>0):
            memdata = 'where ('
            for i in range(len(per)):
                ii = per[i].split()
                for j in range(len(ii)-1):
                    memdata  = memdata +' '+ii[j]
                memdata = memdata +' lower(mem.NAME) = "'+perr[i].lower()+'"'
    
    
    column = 'distinct '
    col = []
    for i in mov:
        if mov[i] == 1:
            col.append(i)
            column = column + 't.'+i+', '
    if 'genre' in tokl:
        col.append('genre')
        column = column + 't.gname, '
    column = column[:-2]
    
    if memlabel == 1:
        num = bestcount
        col = ['person name','profession']
        column = 'distinct mem.NAME, mem.PROFESSION'
        memdata = 'where (mem.PROFESSION = '
        if mem['actor'] == 1 and mem['director'] == 1:
            memdata = memdata + '"director" or mem.PROFESSION = "actor"'
            num = bestcount * 2
        else:
            if mem['actor'] == 1:
                memdata = memdata + '"actor"'
            else:
                memdata = memdata + '"director"'
    
    #==============================================================================
    # if column == 'distinct ':
    #     column = 't.*'
    #==============================================================================
    
    if ('how' in tokl and 'many' in tokl) or (('number' in tokl or 'count' in tokl) and 'of' in tokl):
        column = 'COUNT(distinct t.name)'
        col = ['Count']
    
    
    cgname = ', g.NAME as gname'
    if notflag == 1:
        cgname = ''
    command = 'select '+column+' from\n'
    command += '(select distinct m.*' + cgname + ' from MOVIE m\n'
    command += 'left join MOVIE_GENRE mg on mg.MOVIE_ID = m.ID\n'
    command += 'left join GENRE g on g.ID = mg.GENRE_ID '+genre+'\n'
    if genre != '' and notflag == 1:
        command += 'except\n'
        command += 'select distinct m.*' + cgname + ' from MOVIE m\n'
        command += 'left join MOVIE_GENRE mg on mg.MOVIE_ID = m.ID\n'
        command += 'left join GENRE g on g.ID = mg.GENRE_ID '+genre1+')t\n'
    else:
        command += ')t\n'
    command += 'left join MOVIE_MEMBERS mm on mm.MOVIE_ID = t.ID\n'
    command += 'left join MEMBERS mem on mem.ID = mm.MEMBERS_ID '+memdata
    if memdata != '':
        command += ')\n'
    if len(mcon) > 0:
        if memdata != '':
            command = command + 'and' + mcon[5:] + '\n'
        else:
            command = command + mcon + '\n'
    command += 'order by t.RATING '+order+'\n'
    
    
    if(num>0):
        command += 'limit '+str(num)
    #==============================================================================
    # else:
    #     command += ' limit '+str(5)
    #==============================================================================
    
    
    
    print(command)
    
    conn = sqlite3.connect('Data/MovieDB.db')
    print ("Opened database successfully\n")
    
    try:
        cursor = conn.execute(command)
    except sqlite3.OperationalError:
        return [command,{}]
    
    rowcount = 0
    result = {}
    for i in col:
        result[i] = []
    for row in cursor:
        rowcount += 1
        for i in range(len(col)):
            result[col[i]].append(row[i])
            print( ""+col[i]+":", row[i])
       
    print("\n" + str(rowcount) + " rows fetched\n")
    
    print ("Operation done successfully")
    conn.close()
    
    return [command,result]
    
#englishToSQL('top adventure movie directors')