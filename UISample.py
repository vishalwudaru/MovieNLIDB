# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 19:03:46 2018

@author: VISHAL-PC
"""

import tkinter as tkr
import Testing as nlp

def clicked():
    strr = 'Question : ' + inputField.get("1.0","end-1c") + '\n\n\n'
    sql = nlp.englishToSQL(inputField.get("1.0","end-1c"))
    inputField.delete("1.0","end-1c")
    sqltext.delete("1.0","end-1c")
    restext.delete("1.0","end-1c")
    sqltext.insert('end', sql[0])
    keys = []
    for j in sql[1]:
        keys.append(j)
    for j in range (len(sql[1][keys[0]])):
        for k in range(len(keys)):
            strr += keys[k]+" : "+str(sql[1][keys[k]][j])+'\n'
        strr += '\n'
    strr += str(len(sql[1][keys[0]]))+' rows fetched\n'
    restext.insert('end', strr)

def on_closing():
    nlp.stopnlp()
    print("NLP Closed")
    root.destroy()

nlp.startnlp()

#To remove delay after app opening
nlp.englishToSQL('movie')


root = tkr.Tk()
root.title('Movie Q&A')


frame1 = tkr.Frame(root)
frame1.pack()

inputField = tkr.Text(frame1, width = 145, height = 1)
inputField.pack(side = 'left')

button = tkr.Button(frame1, text = 'Enter', width = 10, command = clicked)
button.pack(side = 'left')


frame2 = tkr.Frame(root)
frame2.pack()

frame3 = tkr.Frame(frame2)
frame3.pack(side = 'left')

s1 = tkr.Scrollbar(frame3)
s1.pack(side='right', fill='y')
sqltext =  tkr.Text(frame3, width = 75, height = 30)
sqltext.pack(side = 'left')
s1.config(command=sqltext.yview)
sqltext.config(yscrollcommand=s1.set)


frame4 = tkr.Frame(frame2)
frame4.pack(side = 'left')

s2 = tkr.Scrollbar(frame4)
s2.pack(side='right', fill='y')
restext =  tkr.Text(frame4, width = 75, height = 30)
restext.pack(side = 'left')
s2.config(command=sqltext.yview)
restext.config(yscrollcommand=s2.set)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()