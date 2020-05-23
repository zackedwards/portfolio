#author: Zack Edwards
#Title: NYT headline analysis 

import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import nltk
import pandas as pd
import string
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

page = requests.get("https://www.nytimes.com/")

soup = BeautifulSoup(page.content, 'html.parser')

word_list = []
temp_list = []
#print(soup.prettify())

#This loop reads the data from the website into a readable 'soup' by focusing on the headlines denoted 
#by the code: css-1ez5fsm esl82me1
for story_heading in soup.find_all(class_="css-1ez5fsm esl82me1"): 
    story_title = story_heading.text.replace("\n", " ").strip()
    new_story_title = story_title.encode('utf-8')
    word_list.append(story_title)
print("The following is the first 15 entries in a list of headlines taken from NY Times")
print(word_list[:15])
    
for i in word_list: #This loops gets ride of the punctuation
    l = nltk.word_tokenize(i)
    ll = [x for x in l if not re.fullmatch('[' + string.punctuation + ']+', x)]
    ll = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in ll]).strip()
    temp_list.append(str(ll))
word_list = temp_list
temp_list = []

stop = open('stopwords_en.txt', 'r')
stops = [] #initializing and cleaning the list of stopwords
stop_list = stop.readlines()
for i in stop_list:
    stops.append(i[:-1])
stop_list = stops

for i in word_list: #This loops eliminates stop words from the data
    for x in i.split():
        if x not in stops:
            if "‘" in x:
                continue
            else:
                temp_list.append(x)
word_list = temp_list
temp_list = [] 

for i in word_list:
    if i.isdigit() == False:
        if "’" in i:
            continue
        else:
            temp_list.append(i)
word_list = temp_list 

#This is our final list of words for the headlines
print('\nThe following is the first 20 cleaned words from the headlines')
print(word_list[:20])

temp_bigrm = []
bigrm = list(nltk.bigrams(word_list))
for i in bigrm:
    for x in i:
        if "‘" in x:
            continue
        else:
            temp_bigrm.append(x)
bigrm = temp_bigrm
print("\nThe following is the first 20 bigrams from the headlines")
print(bigrm[:20])

#Combining the bigrams and original list of words
temp_list = word_list
for i in bigrm:
    for x in i:
        temp_list.append(x)
#print('\n', temp_list)    

# Save a lower-case version of each word to a list
words_list = []
for i in word_list: 
    words_list.append(i.lower())

# Eliminate non alpha elements
text_list = [word.lower() for word in words_list if word.isalpha()]

# Transforming the list into a string for displaying
text_str = ' '.join(text_list)

# Crating and updating the stopword list
stpwords = set(STOPWORDS)
stpwords.add('will')
stpwords.add('said')
stpwords.add('trump')
stpwords.add('biden')


# Defining the wordcloud parameters
wc = WordCloud(background_color="white", max_words=2000, width=800, height=800,
               stopwords=stpwords)

# Generate word cloud
wc.generate(text_str)

# Store to file
wc.to_file('nytwordcloud.png')


print('\nThis is the wordcloud for the NY Times headlines')
# Show the cloud
plt.imshow(wc)
plt.axis('off')
plt.show()
