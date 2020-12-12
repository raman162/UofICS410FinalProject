import numpy as np
#import math
import pandas as pd
import collections
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
        self.no_of_docs = 100
        self.no_of_topics = 10
        self.topic_prob = None
        self.data_path = data_path
        self.pos_notes = []
        self.no_pos_notes = []
        self.pos_notes_raw = []
        self.no_pos_notes_raw = []
        self.total_notes =[]
        self.vocabulary = []
        self.vocabulary_size = 0
        self.number_of_pos_notes = 0
        self.number_of_no_pos_notes = 0
        self.pos_vocabulary =[]
        self.no_pos_vocabulary = []
        #self.pos_term_doc_matrix = None
        #self.no_pos_term_doc_matrix = None
        self.total_doc_matrix = None
        self.pos_en_path = data_path + 'positive_encounters.res-sample-50.res.csv'
        self.no_pos_en_path = data_path + 'no_positive_encounters.res-sample-50.res.csv'

        self.pos_note_path = data_path + 'positive_notes.txt'
        self.no_pos_note_path = data_path + 'no_positive_notes.txt'

        self.pos_purpose_path = data_path + 'positive_purpose.txt'
        self.no_pos_purpose_path = data_path + 'no_positive_purpose.txt'
        self.stop_words = stopwords.words('english')
        self.document_topic_prob = None
        self.topic_word_prob = None

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
            
            # remove 
            clean_doc = re.sub(r'\^[0-9]\s+', ' ', clean_doc)

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
        #print(clean_docs)

        return clean_docs

    def clean_notes(self):
        print("####*** Inside cleaning the notes ***###")
        #print(self.pos_notes[0])
       # self.pos_notes = clean_data(self.pos_notes)
       # self.no_pos_notes = gm.clean_data(self.no_pos_notes)
        self.pos_notes = self.clean_data('pos')
        self.no_pos_notes = self.clean_data('no_pos')
        self.total_notes = self.pos_notes
        for note in self.no_pos_notes:
            self.total_notes.append(note)

       # print(self.pos_notes[0])

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
            lineSplit = np.unique(lineSplit)
            for word in lineSplit:
                if (word not in self.stop_words and len(word) > 2 and not word.isnumeric()):
                    result_vocabulary.append(word) 
        return result_vocabulary
    
    def build_vocabulary(self):
       self.pos_vocabulary = self.vocabulary_builder('pos')
       self.no_pos_vocabulary = self.vocabulary_builder('no_pos')
       for word in self.pos_vocabulary:
           self.vocabulary.append(word)
       for word in self.no_pos_vocabulary:
            self.vocabulary.append(word)
       self.vocabulary = np.unique(self.vocabulary)
       #print(self.vocabulary)
       self.vocabulary_size = len(self.vocabulary)
       #print(self.vocabulary_size)
        
        
    def get_word_frequency(self):
        #for i in range(0, len(self.vocabulary)): 
         #   print('Word Frequency [{}]: {}'.format(self.vocabulary[i], self.vocabulary.count(self.vocabulary[i])))
         word_frequencies_no_pos = collections.Counter(self.no_pos_vocabulary)
         top_word_frequencies_no_pos = word_frequencies_no_pos.most_common(50)
     #    print(top_word_frequencies_no_pos)
         word_frequencies_pos = collections.Counter(self.pos_vocabulary)
         top_word_frequencies_pos = word_frequencies_pos.most_common(50)
       #  print(top_word_frequencies_pos)
         word_frequencies = collections.Counter(self.vocabulary)
         top_word_frequencies = word_frequencies.most_common()
         print(top_word_frequencies)
        
        
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
        print(self.pos_en_path)
        pos_encounters = pd.read_csv(self.pos_en_path, sep=',', header='infer')
        no_pos_encounters = pd.read_csv(self.no_pos_en_path, sep=',', header='infer')
        
        self.pos_notes_raw = pos_encounters.iloc[:,[False,False,False,False,True]].values.tolist()
        self.no_pos_notes_raw = no_pos_encounters.iloc[:,[False,False,False,False,True]].values.tolist()
        
    def build_term_doc_matrix(self):
        n = self.no_of_docs
        m = len(self.vocabulary)
        #self.pos_term_doc_matrix = np.zeros([n, m], dtype=np.int)
        #self.no_pos_term_doc_matrix = np.zeros([n, m], dtype=np.int)
        self.total_doc_matrix = np.zeros([n, m], dtype=np.int)
        for i in range(n):
            for j in range(m):
                #self.pos_term_doc_matrix[i][j] = self.pos_notes[i].count(self.vocabulary[j])
                #self.no_pos_term_doc_matrix[i][j] = self.no_pos_notes[i].count(self.vocabulary[j])
                self.total_doc_matrix[i][j] = self.total_notes[i].count(self.vocabulary[j])
                
    def initialize(self):
        self.topic_prob = np.zeros([self.no_of_docs, self.no_of_topics, self.vocabulary_size], dtype=np.float)
        #self.document_topic_prob = normalize(np.random.random_sample((self.no_of_docs, self.no_of_topics)))
        #self.topic_word_prob = normalize(np.random.random_sample((self.no_of_topics, self.vocabulary_size)))
        self.document_topic_prob = np.ones((self.no_of_docs, self.no_of_topics))
        self.document_topic_prob = normalize(self.document_topic_prob)
        self.topic_word_prob = np.ones((self.no_of_topics, self.vocabulary_size))
        self.topic_word_prob = normalize(self.topic_word_prob)
        
        
    def expectation_step(self):
        print("E step:")
        #self.topic_prob = normalize(np.matmul(self.document_topic_prob, self.topic_word_prob))
        for d in range(self.no_of_docs):
            for z in range(self.no_of_topics):
                for w in range(self.vocabulary_size):
                    self.topic_prob[d][z][w] = self.document_topic_prob[d][z] * self.topic_word_prob[z][w]
                    # normalizing the values with column total
        for d in range(self.no_of_docs):
            for w in range(self.vocabulary_size):
                column_total = 0
                for z in range(self.no_of_topics):
                    column_total += self.topic_prob[d][z][w]
                    #print(column_total)
                for z in range(self.no_of_topics):
                    self.topic_prob[d][z][w] = (self.topic_prob[d][z][w] / column_total)
       # print("topic_prob is: {}".format(self.topic_prob))
        #print("shape of topic_prob is: {}".format(self.topic_prob.shape))
        
        
    def maximization_step(self):
        print("M step:")
        print("building topic_word_prob matrix in M step ...")
        for w in range(self.vocabulary_size):
            for d in range(self.no_of_docs):
                for z in range(self.no_of_topics):
                    self.topic_word_prob[z][w] += self.total_doc_matrix[d][w] * self.topic_prob[d][z][w]
        self.topic_word_prob = normalize(self.topic_word_prob)
        #print("1st Matrix in M - topic_word_prob is built")
        #print("Topic_word_prob matrix is {}".format(self.topic_word_prob))
        for d in range(self.no_of_docs):
            for w in range(self.vocabulary_size):
                for z in range(self.no_of_topics):
                    self.document_topic_prob[d][z] += self.total_doc_matrix[d][w] * self.topic_prob[d][z][w]
        self.document_topic_prob = normalize(self.document_topic_prob)
        #print("2nd Matrix in M - document_topic_prob is built")
        #print("Document_topic_prob is {}".format(self.document_topic_prob))
        
    def calculate_likelihood(self):
        print("Calculating the Likelihood")
        likelihood_matrix = np.zeros([self.no_of_docs, self.vocabulary_size], dtype=np.float)
        x = np.matmul(self.document_topic_prob, self.topic_word_prob)
        doc_term_matrix = np.log(x)
        for d in range(self.no_of_docs):
            for w in range(self.vocabulary_size):
                likelihood_matrix[d][w] = self.total_doc_matrix[d][w] * doc_term_matrix[d][w]
        word_vocab = np.zeros([self.no_of_docs, 1], dtype=np.float)
        for d in range(self.no_of_docs):
            for w in range(self.vocabulary_size):
                word_vocab[d] += likelihood_matrix[d][w]
        likelihood = 0.0
        for d in range(self.no_of_docs):
            likelihood += word_vocab[d]
        print("likelihood is: {}".format(likelihood))
        return likelihood
    
    def plsa(self, max_iter, epsilon):
        print ("EM iteration begins...")
        current_likelihood = 0.0
        prev_likelihood = current_likelihood
        for iteration in range(max_iter):
            print("Iteration #" + str(iteration + 1) + "...")
            self.expectation_step()
            self.maximization_step()
            current_likelihood = self.calculate_likelihood()
            print("likelihood is: {}".format(current_likelihood))
            print("previous likelihood is: {}".format(prev_likelihood))
            if abs(prev_likelihood - current_likelihood) < epsilon:
                print("Topic Word Prob is : {}".format(self.topic_word_prob))
                print("Document Topic Prob is : {}".format(self.document_topic_prob))
                break
            else:
                prev_likelihood = current_likelihood
               
        
        
def normalize(input_matrix):
    row_sums = input_matrix.sum(axis=1)
    try:
        assert (np.count_nonzero(row_sums)==np.shape(row_sums)[0]) # no row should sum to zero
    except Exception:
        raise Exception("Error while normalizing. Row(s) sum to zero")
    new_matrix = input_matrix / row_sums[:, np.newaxis]
    #print(new_matrix)
    return new_matrix
        

        

def main():
    """
    This is the main function
    :return:
    """
    data_path = '../patient_data/'
    # Write the main code here
    max_iteration = 50
    epsilon = 0.001
    miner = TelehealthMiner(data_path)
    miner.extract_purpose_notes()
    #miner.build_corpus()
    miner.clean_notes()
    miner.build_vocabulary()
    ##miner.topic_miner()
    #miner.get_word_frequency()
    miner.build_term_doc_matrix()
    miner.initialize()
#    miner.expectation_step()
#    miner.maximization_step()
#    miner.calculate_likelihood()
#    miner.expectation_step()
#    miner.maximization_step()
#    miner.calculate_likelihood()
#    miner.expectation_step()
#    miner.maximization_step()
#    miner.calculate_likelihood()
    miner.plsa(max_iteration,epsilon)
    
if __name__ == '__main__':
    main()
