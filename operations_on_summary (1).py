
# coding: utf-8

# In[1]:


import nltk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
import csv
titles = [line.rstrip() for line in open(r'C:\Users\Aravind\Downloads\Udemy,NLP\machine_learning_examples-master\machine_learning_examples-master\nlp_class\all_book_titles.txt')]
titles1 = []
file =  open(r'C:\Users\Aravind\Downloads\moviesummaries1.csv',"r")
reader = csv.reader(file)
for line in reader:
    titles1.append(line)
titles1 = np.array(titles1)
titlesx = titles1[:,1]
titles = titlesx


# In[2]:


def my_tokenizer(s):
    s = s.lower() # downcase
    tokens = nltk.tokenize.word_tokenize(s) # split string into words (tokens)
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords
    return tokens


# In[3]:


titles2 =[]
for title in titles:
    title = my_tokenizer(title)
    fre = nltk.FreqDist(title)
    temp =fre.most_common(5)
    titles2.append(temp)
x = []
for titlex in titles2:
    words = "" 
    for word,tag in titlex:
      words = " ".join((words, word))
    x.append(words)
titles = x   
titles[1]


# In[4]:



stopwords = set(w.rstrip() for w in open(r'C:\Users\Aravind\Downloads\Udemy,NLP\machine_learning_examples-master\machine_learning_examples-master\nlp_class\stopwords.txt'))


# In[5]:


def my_tokenizer(s):
    s = s.lower() # downcase
    tokens = nltk.tokenize.word_tokenize(s) # split string into words (tokens)
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords
    return tokens


# In[6]:


word_index_map = {}
current_index = 0
all_tokens = []
all_titles = []
index_word_map = []
error_count = 0
for title in titles:
    try:
        title = title.encode('ascii', 'ignore').decode('utf-8') # this will throw exception if bad characters
        all_titles.append(title)
        tokens = my_tokenizer(title)
        all_tokens.append(tokens)
        for token in tokens:
            if token not in word_index_map:
                word_index_map[token] = current_index
                current_index += 1
                index_word_map.append(token)
    except Exception as e:
        print(e)
        print(title)
        error_count += 1
        
all_tokens




   


# In[7]:


nltk.download('averaged_perceptron_tagger')  


# In[ ]:





# In[8]:


nltk.download('maxent_ne_chunker')


# In[9]:


nltk.download('words')


# In[10]:


print("Number of errors parsing file:", error_count, "number of lines in file:", len(titles))
if error_count == len(titles):
    print("There is no data to do anything with! Quitting...")
    exit()
        





# In[ ]:





# In[283]:


def tokens_to_vector(tokens):
    x = np.zeros(len(word_index_map))
    for t in tokens:
        i = word_index_map[t]
        x[i] = 1
    return x


# In[284]:



N = len(all_tokens)
D = len(word_index_map)
X = np.zeros((D, N)) # terms will go along rows, documents along columns
i = 0
for tokens in all_tokens:
    X[:,i] = tokens_to_vector(tokens)
    i += 1


# In[285]:


def main():
    svd = TruncatedSVD()
    Z = svd.fit_transform(X)
    plt.scatter(Z[:,0], Z[:,1])
    for i in range(D):
        plt.annotate(s=index_word_map[i], xy=(Z[i,0], Z[i,1]))
    plt.savefig("latent.eps",dsi = 1000)

if __name__ == '__main__':
    main()


# In[286]:


import csv
with open(r'C:\Users\Aravind\Downloads\keyowords.csv','w',newline = '') as f:
    writer = csv.writer(f)
    for i in range(0,45):
        writer.writerow([titles1[i,3],titles[i]])


# In[ ]:





# In[ ]:




