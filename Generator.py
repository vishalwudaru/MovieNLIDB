
# coding: utf-8

# In[19]:


import nltk
import numpy as np 
from nltk.corpus import wordnet as wn 


# In[20]:


def indefinite_article(w):
    """Generate an indefinite article for the given phrase: a, an, or empty string"""
    if (len(w) == 0):
        return ""
    if w.lower().startswith("a ") or w.lower().startswith("an ") or w.lower().startswith("the "):
        return ""
    return "an " if w.lower()[0] in list('aeiou') else "a "


# In[21]:


def camel(s):
    """Camel case the given string"""
    return s[0].upper() + s[1:]


# In[22]:


def removeArticle(s):
    """Remove the article in the beginning of the given phrase"""
    if s.startswith("a "):
        return s[2:]
    elif s.startswith("an "):
        return s[3:]
    elif s.startswith("the "):  
        return s[4:]
    return s 


# In[23]:


def NA_joke(d1, d2, w1, w2):
    return "What do you call " + indefinite_article(d1) + d1 + "" +  " that is  " + removeArticle(d2) + "? " +         camel(indefinite_article(w1)) + w1 + " " + w2 + "."


# In[24]:


from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()


# In[25]:


import csv 


# In[26]:


h1 = []
file =  open(r'C:\Users\Aravind\Downloads\J.E.F.F.-master\generator\homophones.csv',"r")
reader = csv.reader(file)
for line in reader:
    h1.append(line)


# In[27]:


def get_part_of_speech(word):
    synsets = wn.synsets(word)
# Get a collection of synsets (synonym sets) for a word
    return (synsets[0].lexname().split(".")[0])
    


# In[28]:


def get_def(word):
    synsets = wn.synsets(word)
    
    


# In[29]:


get_part_of_speech("airy")


# In[ ]:





# '
# # NA JOKE - DONE

# In[30]:


for line in h1:
    if wn.synsets(line[0]) and get_part_of_speech(line[0]) == 'noun':
       for i in range(len(line)) :
        if (wn.synsets(line[i])) and get_part_of_speech(line[i]) == 'adj':
          s1 = wn.synsets(line[0])
          s2 = wn.synsets(line[i])
          print(NA_joke(s1[0].definition(),s2[0].definition(),line[i],line[0])) 
            
          


# # N2A2 DONE

# In[31]:


def N2A2_joke(d1, d2, w1, w2):
    return "What do you call " + indefinite_article(d1) + d1 + " " + removeArticle(d2) + "? " +         camel(indefinite_article(w1)) + w1 + " " + w2 + "."


# In[ ]:





# In[32]:


harr = np.array(h1)
words = []
for item in harr:
    for i in range(len(item)):
        words.append(item[i])
    
words = words[:1000]   


# In[33]:


s = wn.synsets("complacent")     
xa = []
for sa in s:    
    xa.append(sa.lemma_names())
print(xa)           
 
stopwords = set(w.rstrip() for w in open(r'C:\Users\Aravind\Downloads\Udemy,NLP\machine_learning_examples-master\machine_learning_examples-master\nlp_class\stopwords.txt'))    


# In[67]:


wordnet_lemmatizer.lemmatize("cake")


# In[72]:


w11 = "x"
w22 = "x"
syn1 = []
syn2 = []
for word in words:
    
    if wn.synsets(word) and get_part_of_speech(word) == 'noun' and word not in stopwords: 
    
       for i in range(len(words)) :
         
        if (wn.synsets(words[i])) and get_part_of_speech(words[i]) == 'adj' and words[i] not in stopwords:
            s1 = wn.synsets(word) 
            s2 = wn.synsets(words[i]) 
            syn1 = []
            syn2 = []
            
            for s in s1:
                
                syn1.append(s.lemma_names())
                
            for s in s2:
                
                syn2.append(s.lemma_names()) 
                
            for line in syn1:
                for part in line:
                  if (get_part_of_speech(part) == 'noun' and part != word and wordnet_lemmatizer.lemmatize(part) != wordnet_lemmatizer.lemmatize(word)): 
                    w11 = part
                    break   
            for line in syn2:
                for part in line:
                  if (get_part_of_speech(part) == 'adj' and part != words[i] and wordnet_lemmatizer.lemmatize(part) != wordnet_lemmatizer.lemmatize(words[i])):
                    w22 = part
                    break   
            if(len(w11) > 2  and len(w22) > 2):    
              print(N2A2_joke(w22,w11,words[i],wordnet_lemmatizer.lemmatize(word))) 
              w11 = " "
              w22 = " "  
               


# # N2AN DONE

# In[16]:


def N2AN_joke(d1, d2, w1, w2):
    return "When is " + indefinite_article(d1) + d1 + " like " + indefinite_article(d2) + d2 + "? " +            "When it is " + indefinite_article(w1) + w1 + " " + w2 + "."


# In[44]:


w13 = ""
w23 = ""
for line in h1:
    if wn.synsets(line[0]) and get_part_of_speech(line[0]) == 'noun' and line[0] not in stopwords:
       for i in range(len(line)) :
        if (wn.synsets(line[i])) and get_part_of_speech(line[i]) == 'adj' and line[i] not in stopwords:
            s1 = wn.synsets(line[0]) 
            s2 = wn.synsets(line[i]) 
            syn1 = []
            syn2 = []
            
            for s in s1:
                
                syn1.append(s.lemma_names())
                
            for s in s2:
                
                syn2.append(s.lemma_names()) 
                
            for lin in syn1:
                for part in lin:
                  if (get_part_of_speech(part) == 'noun' and part != line[0] and wordnet_lemmatizer.lemmatize(part) != wordnet_lemmatizer.lemmatize(line[0])): 
                    w13 = part
                    break   
            for lin in syn2:
                for part in lin:
                  if (get_part_of_speech(part) == 'adj' and part != line[i] and wordnet_lemmatizer.lemmatize(part) != wordnet_lemmatizer.lemmatize(line[i])):
                    w23 = part
                    break   
            if(len(w13) > 2  and len(w23) > 2):    
              print(N2A2_joke(w23,w13,line[i],line[0])) 
              w13 = " "
              w23 = " "   
 


# In[ ]:



                 


# for line in h1:
#  for i in range(len(line)) :
#           s2 = wn.synsets(line[i])
#           for s in s2:
#                 if (s.lexname().split(".")[0] == 'noun' and s.name().split(".")[0] != line[i] ):
#                     w13 = s.name().split(".")[0]
#                     print(w13 + " " + line[i])
#                     break 

# # N2V2 DONE

# In[61]:


def N2V2_joke(d1, d2, w1, w2):
    return "Why did someone " + d2 + " " + indefinite_article(d1) + d1 + "? " +            "So they could " + w1 + " " + indefinite_article(w1) + w2 + "." 


# In[71]:


for line in h1:
    if wn.synsets(line[0]) and get_part_of_speech(line[0]) == 'noun' and line[0] not in stopwords:
       for i in range(len(line)) :  
        if (wn.synsets(line[i])) and get_part_of_speech(line[i]) == 'verb' and line[i] not in stopwords:
            s1 = wn.synsets(line[0]) 
            s2 = wn.synsets(line[i]) 
            syn1 = []
            syn2 = []
            
            for s in s1:
                
                syn1.append(s.lemma_names())
                
            for s in s2:
                
                syn2.append(s.lemma_names()) 
                
            for lin in syn1:
                for part in lin:
                  if (get_part_of_speech(part) == 'noun' and part != line[0] and wordnet_lemmatizer.lemmatize(part) != wordnet_lemmatizer.lemmatize(line[0])): 
                    w11 = part
                    break   
            for lin in syn2:
                for part in lin:
                  if (get_part_of_speech(part) == 'verb' and part != line[i] and wordnet_lemmatizer.lemmatize(part) != wordnet_lemmatizer.lemmatize(line[i])):
                    w22 = part
                    break   
            if(len(w11) > 2  and len(w22) > 2  ):    
              print(N2V2_joke(wordnet_lemmatizer.lemmatize(w11, 'v'),w22,wordnet_lemmatizer.lemmatize(line[i],'v'),line[0])) 
              w11 = " "
              w22 = " "   
                  


# # N4 DONE

# In[47]:


def N4_joke(d1, d2, w1, w2):
    return "When is " + indefinite_article(d1) + d1 + " like " + indefinite_article(d2) + d2 + "? " +            "When it is " + indefinite_article(w2) + w2 + "." 


# In[87]:


def ishomophoneof(x,y):
    linex = []
    liney = []
    for line in h1:
        if x in line:
            linex = line
        if y in line:
            liney = line
    if linex == liney: 
        return "true"


# In[89]:


w2 = ""
w1 = ""
for line in h1:
    if wn.synsets(line[0]) and get_part_of_speech(line[0]) == 'noun' and line[0] not in stopwords:
       for i in range(len(line)) :
        if (wn.synsets(line[i])) and get_part_of_speech(line[i]) == 'noun' and line[i] not in stopwords:
          s1 = wn.synsets(line[0]) 
          s2 = wn.synsets(line[i]) 
          syn1 = []
          syn2 = []
            
          for s in s1:
                
            syn1.append(s.lemma_names())
                
          for s in s2:
                
            syn2.append(s.lemma_names()) 
                
          for lin in syn1:
            for part in lin:
                if (get_part_of_speech(part) == 'noun' and part != line[0] and wordnet_lemmatizer.lemmatize(part) != wordnet_lemmatizer.lemmatize(line[0])): 
                    w1 = part
                    break   
          for lin in syn2:
            for part in lin:
                if (get_part_of_speech(part) == 'noun' and part != line[i] and part != line[0] and wordnet_lemmatizer.lemmatize(part) != wordnet_lemmatizer.lemmatize(line[i]) and ishomophoneof(part,line[0]) == "true"):
                    w2 = part
                    break  
         
                    
          if(len(w1) > 2  and len(w2) > 2 and w1!= w2):    
              print(N4_joke(w2,w1,line[i],line[0])) 
              w1 = " "
              w2 = " "    
            #w2 must be a homophone of line[0]
          


# # N3A wip

# In[25]:


def N3A_joke(d1, d2, w1, w2):
    return "What do you call " + indefinite_article(d1) + d1 + " " + d2 + "? " +            camel(indefinite_article(w2)) + w2 + "."


# In[ ]:




