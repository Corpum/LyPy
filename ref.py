from bs4 import BeautifulSoup
import urllib
import re
import time
import nltk
from nltk.stem.lancaster import LancasterStemmer as ls
class Lyrics:
    
    def __init__(self, songlink):
        
        self.loadlyrics(songlink)
        self.sortlyrics(self.lyrics)
        
    
    def loadlyrics(self, songlink):
        """Load song lyrics into a list"""
        # Open Lyrics page
        ulink = urllib.urlopen(songlink).read()
        soup = BeautifulSoup(ulink, 'lxml')
        # Loads lyrics into one long string
        for lines in soup.find_all('div', class_='lyricbox'):
            string = lines.text
            
        # Use regex to break long lyric string into seperate lines
        self.lyrics = []
        startpoint = 0
        self.regex = r"(([a-z]|[\'!0,\.-])([0-9]|[A-Z]))"
        for lines in re.finditer(self.regex, string):
            endpoint = lines.end()-1
            self.lyrics.append(string[startpoint:endpoint])
            startpoint = endpoint
            
    def sortlyrics(self, lyrics):     
        """ Finds the last used nouns of each line"""
        self.keywords = []
        for lines in lyrics:
            string = nltk.word_tokenize(lines)
            string = nltk.pos_tag(string)
            for entries in string:
                if 'NN' in entries[1]:
                    self.keywords.append(ls.stem(entries[0]))
            

        