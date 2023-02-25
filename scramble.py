import pygame
from os.path import exists
from gtts import gTTS
from pygame.locals import *
import pymsgbox, string_utils

class SCRAMBLE:
    all_words=[]  # Class Variable
    def __init__(self,spelling_words) -> None:
        """
        Initial function to create mp3 from spelling list if it does not already exist
        :param spelling_words:  spelling list        
        """
        self.spelling_words = spelling_words
        for word in self.spelling_words:
            if exists(f'{word}.mp3')==True:
                pass
            else:
                try:
                    if exists('AnsRight.mp3') == False:
                        tts = gTTS(text="That's right", lang='en')
                        tts.save('AnsRight.mp3')
                except:
                    pass
                try:
                    if exists('wrong.mp3') == False:
                        tts = gTTS(text="That's wrong", lang='en')
                        tts.save('wrong.mp3')
                except:
                    pass
                try:                      
                    tts = gTTS(text=word, lang='en')
                    tts.save(f'{word}.mp3')
                    if exists(f'{word}.mp3') == True: # For some reason the code will not perform correctly without this line
                        pass
                except Exception as e:
                    pass
        
    def play_mp3(word) -> None:
        """
        Function to play the saved mp3 file that matches the word
        :param word: the word that wants to be played
        """
        try:
            if word != "":
                pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(f'{word}.mp3')
                pygame.mixer.music.play()
                return
        except:
            pymsgbox.alert("Could not play mp3")   
            return 
    
    def scramble(spelling_words) -> tuple:
        """
        Function to scramble each word in the spelling list.
        :param spelling_words: spelling list
        :return: return the correct word and the scramble word        
        """
        for word in spelling_words:    
            if word == "":
                pass  
            if word in SCRAMBLE.all_words:
                pass
            else:
                random_word=(string_utils.shuffle(word))
                SCRAMBLE.all_words.append(word)
            return word,random_word