from bs4 import BeautifulSoup
import urllib
import re
import time
import nltk

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
        self.accepted = ['n.', 'adj.']
        self.blacklisted = [',', 'my', ]
        # Queries words beginning from end of line. If adjective or noun is found, that line is finished.
        for lines in lyrics:
            string = nltk.word_tokenize(lines)
            string.reverse()
            for words in string:
                if words not in self.blacklisted:
                    pos = self.partofspeech(words)
                    if pos in self.accepted:
                        self.keywords.append(words)
                        break
                    else:
                        self.blacklisted.append(words)
        
    def partofspeech(self, word):
        """ Uses wordnik to find part of speech"""
        # Open Wordnik
        wordnik = 'https://www.wordnik.com/words/%s' % word
        ulink = urllib.urlopen(wordnik).read()
        soup = BeautifulSoup(ulink, 'lxml')
        # Get the first defintion of wordnik, locates partofspeech
        defs = soup.select('#define')[0]
        defs = defs.text[:104]
        try:
            regex = "[a-z]+\."
            pattern = re.search(regex, defs)
            start = pattern.start()
            end = pattern.end()
            return defs[start:end]
        
        except AttributeError:
            pass
        
        