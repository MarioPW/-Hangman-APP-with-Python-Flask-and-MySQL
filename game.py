from random import choice
from dataclasses import dataclass
from models import Words

lives = 0
lines = ''
hits = 0
image = 'lives0'
message = None
points = 0
letters = [chr(i) for i in range(65,91)]

def word_to_guess(words):
    words_list = words.split()
    word = choice(words_list)
    cleaned_word = {
        ord(","):None,
        ord("'"):None,
        ord("["):None,
        ord("]"):None,
        ord('"'):None}
    word = word.translate(cleaned_word)
    return word

@dataclass
class Hangman:
    
    word: str
    lives: int
    lines: str
    hits: int
    message: str
    points: int
    
      
    def parameters(category):     
        words_list =  Words.query.filter_by(category=category).first()
        word = word_to_guess(words_list.words)     
        lines = []
        to_hits = 0
        for i in word:
            if i == '_':
                lines.append(' ')
                to_hits += 1
            else:
                lines.append('_')

        return {
            'word_to_guess': word,
            'letters': letters,
            'lines': lines,
            'category': category,
            'to_hits': to_hits}
    
    def progress(self, id):       
        letter = id    
        self.message = None
        uploaded_lines = self.lines              
        if letter in uploaded_lines:
            return {'lines': uploaded_lines,
                    'lives': self.lives,
                    'hits': self.hits,
                    'message': self.message,
                    'points': self.points,
                    'message': 'Letter alredy used...'
                    }    
        elif letter in self.word:                  
            for i in range(len(self.word)):  
                if letter == self.word[i]:                                       
                    uploaded_lines[i] = letter
                    self.hits += 1
                else:
                    continue
            return {'lines': uploaded_lines,
                    'lives': self.lives,
                    'hits': self.hits,
                    'message': self.message,
                    'points': self.points + 10
                    }
        else:         
            return {'lines': uploaded_lines,
                        'lives': self.lives + 1,
                        'hits': self.hits,
                        'message': self.message,
                        'points': self.points
                        }

    def images(index):
        images_urls = f'lives{index}'
        return images_urls
