from PyQt5 import QtCore, QtGui, QtWidgets
from view import *
from scramble import SCRAMBLE
from PyQt5.QtWidgets import *
import time, sys
from db import DB
import enchant

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
 
class Controller(QMainWindow, Ui_MainWindow):
    #####   Class Variables #####
    spelling_list=[]
    correct_word=""
    entries=[]
    label_entries=[]
    temp_list=[]
    x=-1
    dbResults = []
    ###############################
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.setupUi(self)
        self.d = enchant.Dict("en_US")
        self.bad_words = []
        self.week = ""
        self.btn_speak.clicked.connect(lambda: SCRAMBLE.play_mp3(Controller.correct_word))
        self.btn_validate.clicked.connect(lambda: self.validate(Controller.correct_word))
        self.WordWindow = QtWidgets.QMainWindow()
        self.ui = Ui_WordWindow()
        self.ui.setupUi(self.WordWindow)
        self.ui.btn_use.clicked.connect(lambda: self.finish_gui(Controller.dbResults))
        self.ui.btn_edit.clicked.connect(lambda: self.editWords())
        self.WordWindow.show()
        self.msg_box = QMessageBox()
        self.add_words()

        
    
    def finish_gui(self, all_results) -> None:
        '''
        Function finishes the setup process. Adds words to the list and creates stacked widgets for errors. Calls next word to begin scrammble game.
        :param results: Tuple of the words selected 
        '''  
        results = list(all_results[0])
        if len(results) > 0:
            self.show()
            for word in results:
                if len(word) <= 0:
                    results.remove(word)
                else:
                    Controller.temp_list.append(word.lower())
                    Controller.spelling_list.append(word.lower())
                           
            SCRAMBLE(Controller.temp_list)
            self.WordWindow.deleteLater()
            self.create_stacked()
            Controller.temp_list.clear()
            self.next_word()
        else:
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("There are no words in this list")
            self.msg_box.setWindowTitle("No Words")
            self.msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            self.msg_box.exec_()
            self.add_words()

    def prompt_bad_words(self):
        if len(self.bad_words) > 0:
                self.msg_box.setText(f"The words: {self.bad_words} were not found in the English Dictionary")
                self.setWindowTitle("Words Not Found")
                self.msg_box.setStandardButtons(QMessageBox.Ok)
                self.msg_box.exec_()
                
    def disable_wordEdit(self) -> None:
        '''
        Function to disable editing the words until you hit the edit button. Also disables the save button
        '''
        self.ui.lineEdit_word1.setEnabled(False)
        self.ui.lineEdit_word2.setEnabled(False)
        self.ui.lineEdit_word3.setEnabled(False)
        self.ui.lineEdit_word4.setEnabled(False)
        self.ui.lineEdit_word5.setEnabled(False)
        self.ui.lineEdit_word6.setEnabled(False)
        self.ui.lineEdit_word7.setEnabled(False)
        self.ui.lineEdit_word8.setEnabled(False)
        self.ui.lineEdit_word9.setEnabled(False)
        self.ui.lineEdit_word10.setEnabled(False)
        self.ui.btn_save.setEnabled(False)
        self.ui.btn_use.setEnabled(True)
        self.ui.Start_stackedWidget.setCurrentIndex(0)
        self.add_words()

    def saveWords(self) -> None:
        '''
        Function to save all the words to the database and calls to disable editing after
        '''
        all_words = []
        all_words.append(self.ui.label_week.text())
        all_words.append(self.ui.lineEdit_word1.text())
        all_words.append(self.ui.lineEdit_word2.text())
        all_words.append(self.ui.lineEdit_word3.text())
        all_words.append(self.ui.lineEdit_word4.text())
        all_words.append(self.ui.lineEdit_word5.text())
        all_words.append(self.ui.lineEdit_word6.text())
        all_words.append(self.ui.lineEdit_word7.text())
        all_words.append(self.ui.lineEdit_word8.text())
        all_words.append(self.ui.lineEdit_word9.text())
        all_words.append(self.ui.lineEdit_word10.text())
        ans = (all(word == "" for word in all_words[1:]))
        if ans:
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("Empty List")
            self.msg_box.setWindowTitle("No words to save")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.exec_()
        else:
            for x,word in enumerate(all_words[1:]):
                if word != "":
                    if self.d.check(word) == False:
                        self.bad_words.append(word)
                        all_words[x + 1] = ""
            self.wordsdb.save_words(all_words)
            self.prompt_bad_words()
            self.disable_wordEdit()

    def editWords(self) -> None:
        self.ui.lineEdit_word1.setEnabled(True)
        self.ui.lineEdit_word2.setEnabled(True)
        self.ui.lineEdit_word3.setEnabled(True)
        self.ui.lineEdit_word4.setEnabled(True)
        self.ui.lineEdit_word5.setEnabled(True)
        self.ui.lineEdit_word6.setEnabled(True)
        self.ui.lineEdit_word7.setEnabled(True)
        self.ui.lineEdit_word8.setEnabled(True)
        self.ui.lineEdit_word9.setEnabled(True)
        self.ui.lineEdit_word10.setEnabled(True)
        self.ui.btn_save.setEnabled(True)
        self.ui.btn_use.setEnabled(False)

    def openWordsWindow(self, week) -> None:
        '''
        Function to display words in the database if any. This window allows editing, saving, and an option to use the words provided.
        :param week: Provides the week number picked on the Start Screen
        '''
        self.wordsdb = DB()
        self.week = week
        results = self.wordsdb.get_week_words(week)
        Controller.dbResults = results
        self.ui.Start_stackedWidget.setCurrentIndex(1)
        if len(results) == 0:
            self.ui.btn_use.setEnabled(False)
            self.editWords()
            self.msg_box.setText("Please add words and hit save!")
            self.msg_box.setWindowTitle("Add Words to Begin")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.exec_()
        else:
            self.ui.btn_use.setEnabled(True)
            
        self.ui.btn_save.clicked.connect(lambda: self.saveWords())
        try:
            self.ui.lineEdit_word1.setText(results[0][0])
        except:
            pass
        try:
            self.ui.lineEdit_word2.setText(results[0][1])
        except:
            pass
        try:
            self.ui.lineEdit_word3.setText(results[0][2])
        except:
            pass
        try:
            self.ui.lineEdit_word4.setText(results[0][3])
        except:
            pass
        try:
            self.ui.lineEdit_word5.setText(results[0][4])
        except:
            pass
        try:
            self.ui.lineEdit_word6.setText(results[0][5])
        except:
            pass
        try:
            self.ui.lineEdit_word7.setText(results[0][6])
        except:
            pass
        try:
            self.ui.lineEdit_word8.setText(results[0][7])
        except:
            pass
        try:
            self.ui.lineEdit_word9.setText(results[0][8])
        except:
            pass
        try:
            self.ui.lineEdit_word10.setText(results[0][9])
        except:
            pass
        try:
            self.ui.label_week.setText(week)
        except:
            pass

    def add_words(self) -> None:
        '''
        Function to display the Start Screen. Adds functionality to the buttons
        '''
        self.ui.btn_week1.clicked.connect(lambda: self.openWordsWindow('Week1'))
        self.ui.btn_week2.clicked.connect(lambda: self.openWordsWindow('Week2'))
        self.ui.btn_week3.clicked.connect(lambda: self.openWordsWindow('Week3'))
        self.ui.btn_week4.clicked.connect(lambda: self.openWordsWindow('Week4'))
        self.ui.btn_week5.clicked.connect(lambda: self.openWordsWindow('Week5'))
        self.ui.btn_week6.clicked.connect(lambda: self.openWordsWindow('Week6'))
        self.ui.btn_week7.clicked.connect(lambda: self.openWordsWindow('Week7'))
        self.ui.btn_week8.clicked.connect(lambda: self.openWordsWindow('Week8'))
        self.ui.btn_week9.clicked.connect(lambda: self.openWordsWindow('Week9'))
        self.ui.btn_week10.clicked.connect(lambda: self.openWordsWindow('Week10'))
        
    def exit_program(self) -> int:
        '''
        Function asks user if they want to start over.
        '''
        #self.msg_box.setIcon(QMessageBox.question)
        self.msg_box.setWindowTitle("Restart")
        self.msg_box.setText("Do you want to start over?")
        self.msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = self.msg_box.exec_()
        return reply
                
                
    def create_stacked(self) -> None:
        """
        Function to create stacked widgets in the range of the length of the spelling list
        """
        if len(Controller.temp_list) > 0:
            for i,word in enumerate(Controller.temp_list):
                e = QtWidgets.QWidget()
                e.setObjectName(word)
                e.setLayout(QtWidgets.QHBoxLayout())
                self.stackedWidget.addWidget(e)
                Controller.entries.append(e)
                
                all_labels=[]
                for letter in word:
                    label = QtWidgets.QLabel()
                    label.setObjectName(letter)
                    label.setFont(QtGui.QFont('Arial', 18))
                    Controller.entries[i].layout().addWidget(label)
                    all_labels.append(label)
                Controller.label_entries.append(all_labels)
            
    def reset_labels(self) -> None:
        '''
        Function to reset the labels to default
        '''
        for x,entry in enumerate(Controller.spelling_list):
            correct_word = entry
            for i,letter in enumerate(correct_word):
                label = Controller.label_entries[x][i]
                label.setText("")
                label.setStyleSheet("")
                
    def validate(self,correct_word) -> None:
        """
        Function to validate the users response. It takes the users phrase and creates color coded labels for correct/wrong letters
        :param correct_word: correct word to validate with
        :return: return None if errors
        """
        if correct_word != "":
            phrase = self.lineEdit_scramble.text()  # users response
            phrase = phrase.strip().lower()
            
            ########## Exception Handling  ###############
            if phrase == "":
                self.msg_box.setWindowTitle("Cannot validate")
                self.msg_box.setText("Enter a word!!")
                self.msg_box.setStandardButtons(QMessageBox.Ok)
                self.msg_box.exec_()
                return
            """ if len(phrase) < len(correct_word) :
                alert = pymsgbox.alert("Not enough letters!")   FOR FUTURE USE
                return """
            if len(phrase) > len(correct_word):
                self.msg_box.setWindowTitle("Cannot validate")
                self.msg_box.setText("Too many letters!!")
                self.msg_box.setStandardButtons(QMessageBox.Ok)
                self.msg_box.exec_()
                return
            ##############################################
            
            if phrase == correct_word:  # correct response      
                SCRAMBLE.play_mp3("AnsRight")
                time.sleep(3)
                Controller.spelling_list.pop(0)
                self.next_word()
            else:                       # Incorrect response
                for i,letter in enumerate(correct_word):
                    
                    try:
                        if letter == phrase[i]:  # colors letters green if correct
                            label = Controller.label_entries[Controller.x][i]
                            label.setText(phrase[i])
                            label.setStyleSheet("background-color: lightgreen")
                            
                        else:                     # colors letters pink if incorrect
                            label = Controller.label_entries[Controller.x][i]
                            label.setText(phrase[i])
                            label.setStyleSheet("background-color: pink")
                    except:
                        label = Controller.label_entries[Controller.x][i]
                        label.setText("_")
                        label.setStyleSheet("background-color: pink")

                SCRAMBLE.play_mp3("wrong") 
        else:
            self.msg_box.setWindowTitle("No words")
            self.msg_box.setText("There are no words in this list!")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.exec_()
    
    def next_word(self) -> None:
        """
        Function used to go to the next word
        uses stacked widgets
        
        """
        self.lineEdit_scramble.setText("")  # clear user text
        Controller.x += 1  # set index value
        self.stackedWidget.setCurrentIndex(Controller.x)
        try:
            if len(Controller.spelling_list) > 0:
                Controller.correct_word,scrambled_word = SCRAMBLE.scramble(Controller.spelling_list)
        except Exception as e:
            pass
        if len(Controller.spelling_list) == 0:
            Controller.spelling_list=SCRAMBLE.all_words
            SCRAMBLE.all_words=[]
            ans=self.exit_program()
            if ans== 16384:
                Controller.correct_word,scrambled_word = SCRAMBLE.scramble(Controller.spelling_list)
                self.lineEdit_scramble.setText("")
                Controller.x = 0
                self.stackedWidget.setCurrentIndex(Controller.x)
                self.reset_labels()
            else:
                sys.exit()
        try:
            self.label_scramble.setText(scrambled_word)
        except:
            pass