import numpy as np
#import math
import pandas as pd
import nltk
import csv
from csv import DictReader
#from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
#from ..classifier import generate_model as gm

import re

class TelehealthMiner(object):
    def __init__(self, data_path):
        """
        This is init function
        """
        print('This is init function')
        self.data_path = data_path
        self.pos_notes = []
        self.no_pos_notes = []
        self.pos_notes_raw = []
        self.no_pos_notes_raw = []
        self.vocabulary = []
        self.number_of_pos_notes = 0
        self.number_of_no_pos_notes = 0

        self.pos_en_path = data_path + 'positive_encounters.res-sample-50.res.csv'
        self.no_pos_en_path = data_path + 'no_positive_encounters.res-sample-50.res.csv'

        self.pos_note_path = data_path + 'positive_notes.txt'
        self.no_pos_note_path = data_path + 'no_positive_notes.txt'

        self.pos_purpose_path = data_path + 'positive_purpose.txt'
        self.no_pos_purpose_path = data_path + 'no_positive_purpose.txt'

    def clean_data(self):
        #if flag == 0:
         #   docs = self.pos_notes
        #else:
         #   docs = self.no_pos_notes
        print("I m here")
        clean_docs = []
        nltk.download('wordnet')
        stemmer = WordNetLemmatizer()
        for dirty_doc in self.pos_notes_raw:
            dirty_doc=' '.join(dirty_doc)
            # remove phi redaction brackets
            clean_doc = re.sub(r'\[\*\*.*?\*\*\]+', ' ', dirty_doc)

            # remove special chars
            clean_doc = re.sub(r'\W', ' ', dirty_doc)

            # remove all single chars
            clean_doc = re.sub(r'\s+[a-zA-Z]\s+', ' ', clean_doc)

            # remove single chars  from the start
            clean_doc = re.sub(r'\^[a-zA-Z]\s+', ' ', clean_doc)

            # replace multi space with single space
            clean_doc = re.sub(r'\s+', ' ', clean_doc, flags=re.I)

            # removing prefixed with 'b'
            clean_doc = re.sub(r'^b\s+', '', clean_doc)

            # conver to lowercase
            clean_doc = clean_doc.lower()

            # lemmatization
            clean_doc = clean_doc.split()
            clean_doc = [stemmer.lemmatize(word) for word in clean_doc]
            clean_doc = ' '.join(clean_doc)

            clean_docs.append(clean_doc)
        print(clean_docs)

        return clean_docs

    def clean_notes(self):
        print("####*** Inside cleaning the notes ***###")
        #print(self.pos_notes[0])
       # self.pos_notes = clean_data(self.pos_notes)
       # self.no_pos_notes = gm.clean_data(self.no_pos_notes)
        self.pos_notes = self.clean_data()

        print(self.pos_notes[0])

    def corpus_builder(self, flag):
        if flag == 0:
            doc_path = self.pos_note_path
            note = self.pos_notes
            number = self.number_of_pos_notes
        else:
            doc_path = self.no_pos_note_path
            note = self.no_pos_notes
            number = self.number_of_no_pos_notes

        fh = open(doc_path)
        lines = fh.readlines()
        for line in lines:
            #print("line is: {}".format(line))
            note.append(line.split())
            number += 1
        return note, number


    def build_corpus(self):
        """
        Read document, fill in self.documents, a list of list of word
        self.documents = [["the", "day", "is", "nice", "the", ...], [], []...]

        Update self.number_of_documents
        """
        #self.pos_notes, self.number_of_pos_notes = self.corpus_builder(self.pos_note_path, self.pos_notes, self.number_of_pos_notes)
        self.pos_notes, self.number_of_pos_notes = self.corpus_builder(0)
        #self.no_pos_notes, self.number_of_no_pos_notes = self.corpus_builder(self.no_pos_note_path, self.no_pos_notes, self.number_of_no_pos_notes)
        self.no_pos_notes, self.number_of_no_pos_notes = self.corpus_builder(1)

    def build_vocabulary(self):
        pos_vocabulary = []
        no_pos_vocabulary = []

    def topic_miner(self):
        """
        This is topic miner function
        :return:
        """
        print('This is topic_miner')

    def extract_purpose_notes(self):
        """
        This function is to extract notes from the encounters CSV file
        :return:
        """
        ## This worked ##
        pos_encounters = pd.read_csv(self.pos_en_path, sep=',', header='infer')
        no_pos_encounters = pd.read_csv(self.no_pos_en_path, sep=',', header='infer')
        
        self.pos_notes_raw = pos_encounters.iloc[:,[False,False,False,False,True]].values.tolist()
        #print(self.pos_notes_raw)
        ## This worked End ##
        #with open(self.pos_en_path) as csv_file:
          #  csv_reader = csv.reader(csv_file, delimiter=',')
           # line_count = 0
            #for row in csv_reader:
             #   if line_count > 0:
              #      self.no_pos_notes_raw.append(row[4])
           # line_count += 1
        #print(self.pos_notes_raw)
        
        #with open(self.no_pos_en_path, 'r') as csvFile:
         #   csvReader = DictReader(csvFile)
          #  for row in csvReader:
           #     self.pos_notes_raw.append(row['note'])
      

        ##with open(self.pos_note_path, 'w') as f:
           ## f.write(pos_encounters['note'].str.cat(sep='\n'))

        ##with open(self.no_pos_note_path, 'w') as f:
           ## f.write(no_pos_encounters['note'].str.cat(sep='\n'))

        ##with open(self.pos_purpose_path, 'w') as f:
           ## f.write(pos_encounters['purpose'].str.cat(sep='\n'))

        ##with open(self.no_pos_purpose_path, 'w') as f:
          ##  f.write(no_pos_encounters['purpose'].str.cat(sep='\n'))

def main():
    """
    This is the main function
    :return:
    """
    data_path = '../patient_data/'
    # Write the main code here
    miner = TelehealthMiner(data_path)
    miner.extract_purpose_notes()
     ## miner.build_corpus()
    miner.clean_notes()
    ##miner.topic_miner()


if __name__ == '__main__':
    main()
