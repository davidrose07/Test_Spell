import sqlite3
from os import mkdir

class DB:
    spell_list = []
    def __init__(self) -> None:
        '''
        Create Database if not exists
        '''
        try:
            self.con = sqlite3.connect('Spelling.db')
        except sqlite3.OperationalError:
            mkdir('Spelling.db')
        finally:
            self.con = sqlite3.connect('Spelling.db')
            #### Create Table is not exists  #####    
            self.con.execute("CREATE TABLE IF NOT EXISTS Week1(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")
            self.con.execute("CREATE TABLE IF NOT EXISTS Week2(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")     
            self.con.execute("CREATE TABLE IF NOT EXISTS Week3(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")
            self.con.execute("CREATE TABLE IF NOT EXISTS Week4(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")
            self.con.execute("CREATE TABLE IF NOT EXISTS Week5(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")
            self.con.execute("CREATE TABLE IF NOT EXISTS Week6(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")
            self.con.execute("CREATE TABLE IF NOT EXISTS Week7(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")
            self.con.execute("CREATE TABLE IF NOT EXISTS Week8(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")
            self.con.execute("CREATE TABLE IF NOT EXISTS Week9(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")
            self.con.execute("CREATE TABLE IF NOT EXISTS Week10(id integer PRIMARY KEY, word1 text, word2 text, word3 text, word4 text, word5 text, word6 text, word7 text, word8 text, word9 text, word10 text)")         

            self.con.commit()
            self.con.close()

    def get_week_words(self, week) -> list:
        '''
        Function to retrieve all words in table
        :param week:  table name
        :return: returns a list of tuples 
        '''
        self.con =  sqlite3.connect('Spelling.db')
        cursor = self.con.cursor()
        cursor.execute("SELECT word1,word2,word3,word4,word5,word6,word7,word8,word9,word10 FROM " + week)
        rows = cursor.fetchall()
        self.con.close()
        return rows
            
    def save_words(self, all_words) -> None:
        '''
        Function to save edited words to the database
        :param all_words: list of words to save that includes the table name
        '''
        self.con = sqlite3.connect('Spelling.db')
        self.con.execute("REPLACE INTO " + all_words[0] + " VALUES(1,?,?,?,?,?,?,?,?,?,?)", all_words[1:])
        self.con.commit()
        self.con.close()

    def remove_words(self, week, bad_words):
        '''
        Function to remove words from database
        :param bad_words:  list of words to remove
        '''
        self.con = sqlite3.connect('Spelling.db')
    
        self.con.execute("DELETE FROM " + week + " WHERE word1= '%" + bad_words +"%' OR word2= '%" + bad_words +"%' OR word3= '%" + bad_words +"%' OR word4= '%" + bad_words +"%' OR word5= '%" + bad_words +"%' OR word6= '%" + bad_words +"%' OR word7= '%" + bad_words +"%' OR word8= '%" + bad_words +"%' OR word9= '%" + bad_words +"%' OR word10= '%" + bad_words +"%'")
        
        self.con.commit()
        self.con.close()
