import numpy as np
#import math
import pandas as pd
import nltk
import csv
from csv import DictReader
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
#from ..classifier import classifier as gm

import re
nltk.download('wordnet')
nltk.download('stopwords')

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
        self.stop_words = stopwords.words('english')

    def clean_data(self,flag):
        #if flag == 0:
         #   docs = self.pos_notes
        #else:
         #   docs = self.no_pos_notes
        clean_docs = []
        dirty_docs = []
        stemmer = WordNetLemmatizer()
        if (flag == 'pos') : 
            dirty_docs = self.pos_notes_raw
        else:
            dirty_docs = self.no_pos_notes_raw
        for dirty_doc in dirty_docs:
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
        self.pos_notes = self.clean_data('pos')
        self.no_pos_notes = self.clean_data('no_pos')

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
        self.pos_notes, self.number_of_pos_notes = self.corpus_builder(0)
        self.no_pos_notes, self.number_of_no_pos_notes = self.corpus_builder(1)

    def vocabulary_builder(self, flag):
        result_vocabulary = []
        if (flag =='pos'):
            lines = self.pos_notes
        else:
            lines = self.no_pos_notes
            
        for line in lines:
            lineSplit = line.split(' ')
            np.unique(lineSplit)
            for word in lineSplit:
                if (word not in self.stop_words):
                    result_vocabulary.append(word)
                    
        return result_vocabulary
    
    def build_vocabulary(self):
        pos_vocabulary = self.vocabulary_builder('pos')
        no_pos_vocabulary = self.vocabulary_builder('no_pos')
        
        print(pos_vocabulary)
        print(no_pos_vocabulary)
        
        
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
        pos_encounters = pd.read_csv(self.pos_en_path, sep=',', header='infer')
        no_pos_encounters = pd.read_csv(self.no_pos_en_path, sep=',', header='infer')
        
        self.pos_notes_raw = pos_encounters.iloc[:,[False,False,False,False,True]].values.tolist()
        self.no_pos_notes_raw = no_pos_encounters.iloc[:,[False,False,False,False,True]].values.tolist()


def main():
    """
    This is the main function
    :return:
    """
    data_path = '../patient_data/'
    # Write the main code here
    miner = TelehealthMiner(data_path)
    miner.extract_purpose_notes()
    #miner.build_corpus()
    miner.clean_notes()
    miner.build_vocabulary()
    ##miner.topic_miner()


if __name__ == '__main__':
    main()
