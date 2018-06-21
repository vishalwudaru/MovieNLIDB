# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 13:42:53 2018

@author: VISHAL-PC
"""

import sqlite3

with open('MovieData.csv') as f:
    lines = f.read().split('\n')
f.close()

df = []
for line in lines:
    fields =  line.split(',')
    df.append(fields)

l = 50


genre = {}
members = {}
i=1
j=1
k=1
while(i<=l):
    gen = df[i][10].split('|')
    for g in gen:
        if g in genre:
            genre[g][0] +=1
        else:
            genre[g] = [1,j]
            j += 1
    if df[i][11] not in members:
        members[df[i][11]]=['director',df[i][12],k]
        k += 1
    if df[i][13] not in members:
        members[df[i][13]]=['actor',df[i][14],k]
        k += 1
    if df[i][15] not in members:
        members[df[i][15]]=['actor',df[i][16],k]
        k += 1
    if df[i][17] not in members:
        members[df[i][17]]=['actor',df[i][18],k]
        k += 1
    i=i+1

conn = sqlite3.connect('MovieDB.db')

print ("Opened database successfully");

#==============================================================================
# conn.execute('''CREATE TABLE MOVIE
#          (ID INT PRIMARY KEY     NOT NULL,
#          NAME           CHAR(100)    NOT NULL,
#          RATING         REAL     NOT NULL,
#          VOTES          INT      NOT NULL,
#          LIKES          INT     NOT NULL,
#          DURATION       INT    NOT NULL,
#          LINK          TEXT    NOT NULL,
#          LANGUAGE      CHAR(20)    NOT NULL,
#          CONTENT       CHAR(20) NOT NULL,
#          COUNTRY       CHAR(50) NOT NULL,
#          YEAR         INT NOT NULL);''')
# print( "Table created successfully");
# 
# i=1
# while(i<=l):
#     
#     command = "INSERT INTO MOVIE VALUES ("+str(i)+", \""+df[i][0][:-1]+"\", "+df[i][1]+", "+df[i][2]+", "+df[i][3]+","+df[i][4]+", '"+df[i][5]+"', '"+df[i][6]+"', '"+df[i][7]+"',  '"+df[i][8]+"', "+df[i][9]+")"
#     print(command)
#     i=i+1
#     conn.execute(command)
#     
# conn.commit()
#==============================================================================

#==============================================================================
# conn.execute('''CREATE TABLE GENRE
#          (ID INT PRIMARY KEY     NOT NULL,
#          NAME           CHAR(100)    NOT NULL);''')
# print( "Table created successfully");
# 
# i = 1
# for key in genre.keys():
#     command = "INSERT INTO GENRE VALUES ("+str(i)+", \""+key+"\")"
#     print(command)
#     i=i+1
#     conn.execute(command)
#     
# conn.commit()
# 
#==============================================================================

#==============================================================================
# conn.execute('''CREATE TABLE MEMBERS
#          (ID INT PRIMARY KEY     NOT NULL,
#          NAME           CHAR(100)    NOT NULL,
#          PROFESSION   CHAR(100)  NOT NULL,
#          LIKES      INT   NOT NULL);''')
# print( "Table created successfully");
# 
# i = 1
# for key in members.keys():
#     command = "INSERT INTO MEMBERS VALUES ("+str(i)+", \""+key+"\", '"+members[key][0]+"', "+members[key][1]+")"
#     print(command)
#     i=i+1
#     conn.execute(command)
#     
# conn.commit()
#==============================================================================

#==============================================================================
# conn.execute('''CREATE TABLE MOVIE_GENRE
#          (ID INT PRIMARY KEY     NOT NULL,
#          MOVIE_ID    INT    NOT NULL,
#          GENRE_ID    INT    NOT NULL,
#          FOREIGN KEY(MOVIE_ID) REFERENCES MOVIE(ID),
#          FOREIGN KEY(GENRE_ID) REFERENCES GENRE(ID));''')
# print( "Table created successfully");
# 
# i = 1
# k=1
# while(i<=l):
#     mid=i
#     gen = df[i][10].split('|')
#     for g in gen:
#         command = "INSERT INTO MOVIE_GENRE VALUES ("+str(k)+", "+str(i)+", "+str(genre[g][1])+")"
#         k += 1
#         #print(command)
#         conn.execute(command)
#     i += 1
#     
# conn.commit()
#==============================================================================

#==============================================================================
# conn.execute('''CREATE TABLE MOVIE_MEMBERS
#          (ID INT PRIMARY KEY     NOT NULL,
#          MOVIE_ID    INT    NOT NULL,
#          MEMBERS_ID    INT    NOT NULL,
#          FOREIGN KEY(MOVIE_ID) REFERENCES MOVIE(ID),
#          FOREIGN KEY(MEMBERS_ID) REFERENCES MEMBERS(ID));''')
# print( "Table created successfully");
# 
# i = 1
# k=1
# while(i<=l):
#     mid=i
#     command = "INSERT INTO MOVIE_MEMBERS VALUES ("+str(k)+", "+str(i)+", "+str(members[df[i][11]][2])+")"
#     k += 1
#     conn.execute(command)
#     command = "INSERT INTO MOVIE_MEMBERS VALUES ("+str(k)+", "+str(i)+", "+str(members[df[i][13]][2])+")"
#     k += 1
#     conn.execute(command)
#     command = "INSERT INTO MOVIE_MEMBERS VALUES ("+str(k)+", "+str(i)+", "+str(members[df[i][15]][2])+")"
#     k += 1
#     conn.execute(command)
#     command = "INSERT INTO MOVIE_MEMBERS VALUES ("+str(k)+", "+str(i)+", "+str(members[df[i][17]][2])+")"
#     k += 1
#     conn.execute(command)
#     i += 1
#     
# conn.commit()
#==============================================================================


conn.close()
