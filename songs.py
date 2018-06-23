import re
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import random


class choir():
    
    def __init__(self):
        self.url = 'http://lyricsera.com/{art}-p{page}-lyrics.html'
 
       
    def learn_old_songs(self, artists: list=['queen'], pages: int = 2)  -> pd.DataFrame:
        print("Analyzing old songs...")
        songs = dict(title=[], lyrics=[])

        for artist in artists:
            print(artist)
            
            for page in range(1,pages+1):
                print("Page: {page}".format(page=page))
                url = 'http://lyricsera.com/{art}-p{page}-lyrics.html'.format(art = artist.lower().replace(" ","-"),page=page)
                request = urllib.request.urlopen(url)
                soup = BeautifulSoup(request, 'lxml')
                for link in self.extract_links(soup):
                    request_link = urllib.request.urlopen(link.get('href'))
                    soup_link = BeautifulSoup(request_link.read(), 'lxml')
                    song_text = self.preprocess_lyrics(str(soup_link.tt).lower())
                    songs['title'].append(link.get('title'))
                    songs['lyrics'].append(song_text)
        
        self.songs_db = pd.DataFrame.from_dict(songs)                    
    
    
    @staticmethod    
    def extract_links(soup):
            links = []
            for link in soup.find_all('a'):
                try:
                    if re.search(r"/[0-9]",link.get('href')):
                        links.append(link)
                except Exception as e:
                    print(e.args + ('failed for {link}'.format(link=link),))
            return links

    @staticmethod
    def preprocess_lyrics(lyrics):
        try:
            song_text = re.sub(r"[\[=,.!?()\"]", " ", lyrics)
            song_text = re.sub(r"<[a-z/]+>", " ", song_text)
            song_text = re.sub(r"\s+", " ", song_text)
            song_text = song_text.replace("chorus", " ").replace(" ' "," ")
            return song_text
        except Exception as e:
            print(e.args + ('preprocessing failed.',))
            return lyrics    

        
    def learn_to_sing(self, n: int = 2):
        
        if hasattr(self, 'songs_db') == False:
            print('Need to learn old songs first...')
            self.learn_old_songs()
        
        print("Learning how to sing...")
        self.n = n
        count = 1.0
        words, words_model = list(), dict()
        for lyrics in self.songs_db['lyrics']:
            words.extend(lyrics.split())
            for i in range(len(words)-n):
                song_part = ' '.join(words[i:i+n])
                if song_part not in words_model.keys():
                    words_model[song_part]=[]
                words_model[song_part].append(words[i+n])
                
            if round(10*count/len(self.songs_db['lyrics']))>round(10*(count-1)/len(self.songs_db['lyrics'])):
                print(round(100*count/len(self.songs_db['lyrics'])), '% done')
            count += 1
        
        self.model = words_model

        
    def sing_song(self, song_start: str = '', steps: int = 30):
       
        if hasattr(self, 'model') == False:
            print("Have to learn how to sing first")
            self.learn_to_sing()
        
        if song_start=='':
            r = random.randrange(len(self.model.keys()))
            song_start = list(self.model.keys())[r]
            
        if song_start in self.model.keys():
            song = list()
            words = song_start
            song.append(words)
            for _ in range(steps):
                possibilities = self.model[words]
                next_item = possibilities[random.randrange(len(possibilities))]
                song.append(next_item)
                words = ' '.join(song[-self.n:])
                words = ' '.join(words.split()[-self.n:])
            return ' '.join(song)
        else: print("Cannot start with those words. Please try a different beginning.")
        