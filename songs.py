
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
import random
    
#soup = BeautifulSoup(urllib.request.urlopen('http://lyricsera.com/queen-lyrics.html').read(), "lxml")
#print(soup.prettify())

def text_job(song_text):
    song_text = re.sub(r"[=,.!?()\"]"," ",song_text)
    song_text = re.sub(r"<[a-z/]+>"," ",song_text)
    song_text = re.sub(r"\s+"," ",song_text)
    song_text=song_text.replace("chorus"," ").replace(" ' "," ")
    return song_text

songs_queen = pd.DataFrame(columns=["title", "lyrics"])
songs_jayz  = pd.DataFrame(columns=["title", "lyrics"])

for k in range(0,4):
#linki do piosenek
    print(k)
    soup_queen = BeautifulSoup(urllib.request.urlopen('http://lyricsera.com/queen-p'+ str(k) +'-lyrics.html').read(), "lxml")
    soup_jayz  = BeautifulSoup(urllib.request.urlopen('http://lyricsera.com/jay-z-p'+ str(k) +'-lyrics.html').read(), "lxml")
    linki_queen = [link for link in soup_queen.find_all('a') if re.search(r"/[0-9]",link.get('href'))]
    linki_jayz  = [link for link in  soup_jayz.find_all('a') if re.search(r"/[0-9]",link.get('href'))]
    
#teksty do dataframe    
    for link in linki_queen:
        soup_song = BeautifulSoup(urllib.request.urlopen(link.get('href')).read(), "lxml")
        song_text = str(soup_song.tt).lower() 
        song_text = text_job(song_text)
        songs_queen = pd.DataFrame(np.insert(songs_queen.values, 0, values=[link.get('title'),song_text], axis=0), columns=["title", "lyrics"])
    
    for link in linki_jayz:
        soup_song = BeautifulSoup(urllib.request.urlopen(link.get('href')).read(), "lxml")
        song_text = str(soup_song.tt).lower() 
        song_text = text_job(song_text)
        songs_jayz = pd.DataFrame(np.insert(songs_queen.values, 0, values=[link.get('title'),song_text], axis=0), columns=["title", "lyrics"])
    
      
#modele

model_queen = {}
for i in range(len(songs_queen['title'])):
    song_words =  songs_queen.iloc[i,1].split()

    for j in range(len(song_words)-1):
        word = song_words[j:j+1][0]
        if word not in model_queen.keys():
            model_queen[word] = []
        model_queen[word].append(song_words[j+1])

model_jayz = {}
for i in range(len(songs_jayz['title'])):
    song_words =  songs_jayz.iloc[i,1].split()

    for j in range(len(song_words)-1):
        word = song_words[j:j+1][0]
        if word not in model_jayz.keys():
            model_jayz[word] = []
        model_jayz[word].append(song_words[j+1])        

     
def sing_a_song(start_improv, song_length):
    start = start_improv
    result= start
    for i in range(song_length):
        if start not in model_queen.keys():
            break
        possibilities = model_queen[start]
        nextItem = possibilities[random.randrange(len(possibilities))]
        result = result +' ' + nextItem
        start =  nextItem
    res_queen = result
    
    start = start_improv
    result = start
    for i in range(song_length):
        if start not in model_jayz.keys():
            break
        possibilities = model_jayz[start]
        nextItem = possibilities[random.randrange(len(possibilities))]
        result = result +' ' + nextItem
        start =  nextItem  
    res_jayz = result
    print(res_queen)
    print(res_jayz)
    return



sing_a_song("drink", 20)
