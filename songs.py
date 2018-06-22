import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
import random
from typing import Dict

artists=['Paul Mccartney','Rod Stewart','Johnny Cash','Ray Charles']

def extract_links(soup):
        links = []
        for link in soup.find_all('a'):
            try:
                if re.search(r"/[0-9]",link.get('href')):
                    links.append(link)
            except Exception as e:
                print(e.args + ('failed for {link}'.format(link=link),))
        return links

def preprocess_lyrics(lyrics):
    try:
        song_text = re.sub(r"[=,.!?()\"]", " ", lyrics)
        song_text = re.sub(r"<[a-z/]+>", " ", song_text)
        song_text = re.sub(r"\s+", " ", song_text)
        song_text = song_text.replace("chorus", " ").replace(" ' "," ")
        return song_text
    except Exception as e:
        print(e.args + ('preprocessing failed.',))
        return lyrics    

songs = dict(title=[], lyrics=[])

for artist in artists:
    print(artist)
    art = artist.lower().replace(" ","-")
    
    for page in range(1,5):
        print("Page: {page}".format(page=page))
        url = 'http://lyricsera.com/{art}-p{page}-lyrics.html'.format(art = art,page=page)
        request = urllib.request.urlopen(url)
        soup = BeautifulSoup(request, 'lxml')
        for link in extract_links(soup):
            request_link = urllib.request.urlopen(link.get('href'))
            soup_link = BeautifulSoup(request_link.read(), 'lxml')
            song_text = preprocess_lyrics(str(soup_link.tt).lower())
            songs['title'].append(link.get('title'))
            songs['lyrics'].append(song_text)
      
           
class choir(object):

    def __init__(self, n: int = 1):

        self.n = n
        count = 1.0
        words, words_model = list(), dict()
        for lyrics in songs['lyrics']:
            words.extend(lyrics.split())
            for i in range(len(words)-n):
                song_part = ' '.join(words[i:i+n])
                if song_part not in words_model.keys():
                    words_model[song_part]=[]
                words_model[song_part].append(words[i+n])
            if round(100*count/len(songs['lyrics']))>round(100*(count-1)/len(songs['lyrics'])):
                print(round(100*count/len(songs['lyrics'])), '% done')
            count += 1
        
        self.model = words_model

    def sing_song(self, song_start: str, steps: int):
       
        assert song_start in self.model.keys()
    
        song = list()
        words = song_start
        song.append(words)
        for _ in range(steps):
            possibilities = self.model[words]
            next_item = possibilities[random.randrange(len(possibilities))]
            song.append(next_item)
            words = ' '.join(song[-self.n:])
        return ' '.join(song)


model_1 = choir()
model_2 = choir(2)
model_3 = choir(3)

model_1.sing_song("you", 30)
model_2.sing_song("you myyy", 30)
model_1.sing_song("you are my", 30)
