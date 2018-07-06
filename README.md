# MovieNLIDB

#Problem Statement
Ultimate Goal of the project is to build a Chatbot which can detect and also respond to user sarcasm. In the 1st phase of the project, the goal is to build a chatbot which can respond to user queries non-sarcastically. These user queries are restricted under a  closed domain of Movie Database.
#Introduction
To extract information from a database based system one need to have an expertise in SQL commands. In these conditions a simple conversation system which can convert Natural Language query into a Database query will be a boon to industry. Natural Language Interface to Database systems (NLIDB) helps us to convert Natural Language queries into SQL commands. This project demonstrates a NLIDB system for Movie Database, where an user can ask anything regarding movies in Natural Language and the system will convert it into SQL Query and give results to user.
#Literature Review
Arjun R. Akula, Rajeev Sangal, Radhika Mamidi (2013) have presented an approach which identifies how the contextual information is utilized in the interactions between the user and the system implemented in the natural Language interface to Database (NLiDB).They have used three models namely (Linear Disjoint Model, Linear Coincident Model and NonLinear Model) for utilizing the contextual information in the interactions.

Saikrishna Srirampur, Ravi Chandibhamar, Ashish Palakurthi, Radhika Mamidi (2014) captures the concepts of the Natural Language query using Concepts Identification technique. They have identified the concepts of their own and making it a Named Entity Recognition(NER) problem and having restricted the domain to the Course management Domain. They have used a machine learning approach and the algorithm used is Conditional Random Field.

Manju Mony ,Jyothi M. Rao ,Manish M. Potey (2014) made a report stating various methodologies and approaches to build NLiDB systems along with their advantages and disadvantages and their application areas.They have also implemented an Natural Language Interface in Airline reservation domain.The report mentions the earlier frameworks such as Pattern matching, Syntax based systems , Semantic based systems and intermediate based representation languages and modern based techniques such as machine learning approaches,Intermediate query generation,Ontology based approaches and other techniques.The paper implements a flight reservation system which uses Intermediate based approach and syntax based approach.Syntax Analysis performs syntactic processing and breaks the input sentence into its constituent parts and identifies the relations between the
concepts. Intermediate Query approach allows to easily perform the mapping of concepts to an intermediate representation.
#Methodology
This section discusses the methodology used to build this NLIDB System of Movie Database.
Database Creation
We used a IMDB Dataset found on Github (Link). It consists of 28 attributes out of which we used 12 prime attributes. We divided the dataset among 5 tables Genre, Members, Movie, Movie_Genre and Movie_Members.
Genre: Universal set of Genres available in our dataset.
Members: Consists of all the Directors and Main cast of movies.
Movie: Table consisting different attributes regarding movies.
Movie_Genre: Maps a movie with different types of Genres it has.
Movie_Members: Maps a movie with members who acted or directed it.
fFig 1: ER Diagram

Fig 2: Class Diagram

Integrating NLIDB System 
NLIDB System is responsible for converting user’s NL query into SQL statement. The given NL query is passed into a Tokenizer, then we POS tag the tokenized words and then we parsed it using Stanford Dependency Parser. Dependency parsing helps us in knowing the relation between words. For example, if the user’s query is “What are the top movies rated above 8 which are released before 2015”. In this example, the dependency parser helps us to know that ‘above’ corresponds to rating and ‘before’ corresponds to year. 
	Based on these Dependencies and POS tags, we generated an SQL query which is used to extract corresponding data from Database.

Fig 3: Data flow Diagram

#Results
We tested the chatbot over wide range of Natural Language queries. The following are the questions which were verified to work correctly using our chatbot. These Questions are categorized further for better readability.

Movies:
1.	Search using genre
i.	Top 10 action movies.
ii.	Best adventure movie.
iii.	Which is the best animation movie
iv.	Suggest some movies of drama
v.	What is the best Sci-Fi movie
vi.	Name some action and not adventure movies
2.	Search using members
i.	Name some movies of James Cameron
ii.	Movies of Tom Hardy
iii.	Best movie of Christopher Nolan
iv.	What movies are directed by James Wan
v.	In which movies did Vin Diesel act
vi.	Movies of Christopher Nolan and James Cameron
vii.	Best movies of Vin Diesel and Tom Hardy
3.	Search using year
i.	Movies after 2010
ii.	What movies released before 2011
iii.	Name the best movie in 2012
iv.	Which movies released after 2009 and before 2015
4.	Search using rating
i.	Movies rating above 8
ii.	Name same movies rated 9
iii.	Which movies are below 6
iv.	Movies rated below 9 and above 8
5.	Search using duration
i.	Movies less than 2 hrs
ii.	Movies more than 150 mins
iii.	Name best movies greater than 2 hours
iv.	top movie less than 150 mintue
v.	Movies longer than 2 hrs
6.	Search using country
i.	Movies from USA
ii.	Best movies in New Zealand
iii.	Best movie from UK
iv.	Some movies in Canada and Australia
7.	Search using language
i.	English movies
ii.	Best English movie
iii.	Movies in English
8.	Combined search
i.	Top 5 action movies of USA after 1980, greater than 100 mins and rating above 5 of Tom Hardy and James Cameron in English
ii.	movies from New Zealand, Australia, Canada, UK and USA in English of Tom Hardy
iii.	movies from USA in English and rating above 7 and less than 2 hours
Members:
9.	Search using genre
i.	Names of action directors
ii.	Best action hero and director
iii.	Get all sport directors
iv.	Who is best action hero
v.	Directors of drama and thriller movies
vi.	Directors of action and not adventure movies
10.	Search using movie
i.	Director of Titanic
ii.	Cast of Avatar
iii.	Cast and crew of John Carter
iv.	Actors of Avatar
11.	Search using year
i.	Directors after 2010
ii.	Actors before 2007
iii.	Name the best actor in 2012
iv.	Who are directors after 2009 and before 2015
12.	Search using country
i.	Directors from USA
ii.	Best actor in New Zealand
iii.	Best director from UK
iv.	Top actors in Canada and Australia
13.	Search using language
i.	English directors
ii.	Best English actor
14.	Combines search
i.	Best director in UK before 2013
ii.	Adventure movie directors from Canada
iii.	Top English action actors in New Zealand before 2010
Fields:
15.	Name 
i.	Name top ten action movies
ii.	Drama movie names
iii.	Best actors name
iv.	action directors
v.	Names of sport actors
16.	Rating
i.	rating of adventure movies
ii.	Highest rated movie
iii.	Best action movie rating
iv.	rating of Titanic
v.	Top thriller movie score
17.	IMDB Link
i.	Link of Avatar
ii.	links for animation movies
iii.	imdb link for Avatar
18.	Language
i.	Language of Titanic
ii.	In which language is Avatar available
iii.	What is the language of John Carter
19.	Duration
i.	duration of Avatar
ii.	length of Avatar
iii.	run time of Titanic
iv.	What is duration of Avatar
20.	Year
i.	In which year did Avatar release
ii.	release date of Avatar
iii.	When did Titanic release
21.	Country
i.	Which country Avatar belongs to
ii.	Where did Titanic release
iii.	Place of Avatar
iv.	city in which Titanic release
Others:
22.	Count
i.	How many action directors are there
ii.	Count of drama movies
iii.	Number of action actors
23.	Where
i.	Where did Avatar release
ii.	Where did best action movie released
24.	When
i.	When did John Carter release
ii.	When did best action movie release



#Future Work
Convert Database result into NL response.

#Related Links
Github:
Sarcastic Chatbot: https://github.com/arunreddy079/sarcastic_chatbot
NLIDB System:  https://github.com/VishalReddy-Wudaru/MovieNLIDB

Dataset: 

#Manual
Prerequisites
Python 3.6
Java 1.8+
Stanford CoreNLP 3.9.1 (https://stanfordnlp.github.io/CoreNLP/history.html)

Installation
pip install stanfordcorenlp
pip install nltk
pip install sqlite3
Pip install word2number
Pip install python3-tk
 
Steps
Setup path of Stanford CoreNLP Folder in Testing.py
nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27') 
Setup path of Database in Testing.py
conn = sqlite3.connect('Data/MovieDB.db') 
Run UISample.py

