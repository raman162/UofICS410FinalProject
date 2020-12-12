import numpy as np
import sys
import pandas as pd
import collections
import nltk
import codecs
from pylab import random
from nltk.stem import WordNetLemmatizer
#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
#from ..classifier import classifier as gm

import re
nltk.download('wordnet')
nltk.download('stopwords')

class TelehealthMiner(object):
    def __init__(self, input_arg_list):
        """
        This is init function
        """
        print('This is init function')
        self.data_file_path = input_arg_list[0];
        self.no_of_topics = input_arg_list[1]
        self.no_of_iterations = input_arg_list[2]
        self.threshold = input_arg_list[3]
        self.no_of_topic_words_dist = input_arg_list[4]
        self.stop_words_repo = []
        self.no_of_docs = 0
        self.topic_prob = None
        self.notes_clean = []
        self.notes_raw = []
        self.map_word_to_id = {} 
        self.map_id_to_word = {}
        self.word_frequencies = []
        self.word_count = {}
        self.vocabulary = []
        self.vocabulary_size = 0
        self.number_of_notes = 0
        self.term_doc_matrix = []
        self.total_doc_matrix = None
        self.document_topic_prob = None
        self.topic_word_prob = None

    def clean_data(self):
        clean_docs = []
        stemmer = WordNetLemmatizer()
        for dirty_doc in self.notes_raw:
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
        self.clean_notes = self.clean_data()
        #print(self.clean_notes)

       # print(self.pos_notes[0])

    def build_vocabulary (self):
        current_id = 0;
        for line in self.clean_notes:
            lineSplit = line.split(' ')
            word_count = {}
            #lineSplit = np.unique(lineSplit)
            for word in lineSplit:
                if (word not in self.stop_words_repo and len(word) > 2 and not word.isnumeric()):
                    #result_vocabulary.append(word) 
                    if word not in self.map_word_to_id.keys():     
                        self.map_word_to_id[word] = current_id;   
                        self.map_id_to_word[current_id] = word;    
                        current_id += 1;                            
                    if word in word_count:                    
                        word_count[word] += 1
                    else:
                        word_count[word] = 1                   
            self.word_frequencies.append(word_count)  
        self.vocabulary = list(self.map_word_to_id.keys())
        self.vocabulary_size = len(self.vocabulary)
        #print(self.word_frequencies)
        #print(self.vocabulary)
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
        documents = pd.read_csv(self.data_file_path, sep=',', header='infer', encoding = 'utf-8')
        self.notes_raw = documents.iloc[:,[False,False,False,False,True]].values.tolist()
        self.no_of_docs = len(self.notes_raw)
        print(self.no_of_docs)
        
    def build_stop_words_repo(self, file_path):
        """
        This function is to extract notes from the encounters CSV file
        :return:
        """
        stop_words_file = open(file_path)
        stop_words = stop_words_file.readlines()
        for word in stop_words:
            word = word.strip()
            self.stop_words_repo.append(word)
        stop_words_file.close()
        return(self.stop_words_repo)

    def build_term_doc_matrix(self):
#        n = self.no_of_docs
#        m = len(self.vocabulary)
#        #self.pos_term_doc_matrix = np.zeros([n, m], dtype=np.int)
#        #self.no_pos_term_doc_matrix = np.zeros([n, m], dtype=np.int)
#        self.total_doc_matrix = np.zeros([n, m], dtype=np.int)
#        for i in range(n):
#            for j in range(m):
#                #self.pos_term_doc_matrix[i][j] = self.pos_notes[i].count(self.vocabulary[j])
#                #self.no_pos_term_doc_matrix[i][j] = self.no_pos_notes[i].count(self.vocabulary[j])
#                self.total_doc_matrix[i][j] = self.total_notes[i].count(self.vocabulary[j])
        
         self.term_doc_matrix = np.zeros([self.no_of_docs, self.vocabulary_size], dtype=np.int8)
         for word in self.vocabulary:
             j = self.map_word_to_id[word]
             for i in range(0, self.no_of_docs):
                 if word in self.word_frequencies[i]:
                     self.term_doc_matrix[i, j] = self.word_frequencies[i][word];  
         #print(self.term_doc_matrix)
                
    def initialize(self):
        self.topic_prob = np.zeros([self.no_of_docs, self.vocabulary_size, self.no_of_topics], dtype=np.float)
        #self.document_topic_prob = normalize(np.random.random_sample((self.no_of_docs, self.no_of_topics)))
        #self.topic_word_prob = normalize(np.random.random_sample((self.no_of_topics, self.vocabulary_size)))
        self.document_topic_prob = random((self.no_of_docs, self.no_of_topics))
        #self.document_topic_prob = normalize(self.document_topic_prob)
        self.topic_word_prob = random((self.no_of_topics, self.vocabulary_size))
        #self.topic_word_prob = normalize(self.topic_word_prob)
    
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
        
    def e_step(self):
        for i in range(self.no_of_docs):
            for j in range(self.vocabulary_size):
                denominator = 0;
                for k in range(0, self.no_of_topics):
                    self.topic_prob[i, j, k] = self.topic_word_prob[k, j] * self.document_topic_prob[i, k];
                    denominator += self.topic_prob[i, j, k];
                if denominator == 0:
                    for k in range(0, self.no_of_topics):
                        self.topic_prob[i, j, k] = 0;
                else:
                    for k in range(0, self.no_of_topics):
                        self.topic_prob[i, j, k] /= denominator;
        
        
    def m_step(self):
#        print("M step:")
#        print("building topic_word_prob matrix in M step ...")
#        for w in range(self.vocabulary_size):
#            for d in range(self.no_of_docs):
#                for z in range(self.no_of_topics):
#                    self.topic_word_prob[z][w] += self.total_doc_matrix[d][w] * self.topic_prob[d][z][w]
#        self.topic_word_prob = normalize(self.topic_word_prob)
#        #print("1st Matrix in M - topic_word_prob is built")
#        #print("Topic_word_prob matrix is {}".format(self.topic_word_prob))
#        for d in range(self.no_of_docs):
#            for w in range(self.vocabulary_size):
#                for z in range(self.no_of_topics):
#                    self.document_topic_prob[d][z] += self.total_doc_matrix[d][w] * self.topic_prob[d][z][w]
#        self.document_topic_prob = normalize(self.document_topic_prob)
#        #print("2nd Matrix in M - document_topic_prob is built")
#        #print("Document_topic_prob is {}".format(self.document_topic_prob))
        
        for k in range(self.no_of_topics):
            denominator = 0
            for j in range(self.vocabulary_size):
                self.topic_word_prob[k, j] = 0
                for i in range(self.no_of_docs):
                    self.topic_word_prob[k, j] += self.term_doc_matrix[i, j] * self.topic_prob[i, j, k]
                denominator += self.topic_word_prob[k, j]
            if denominator == 0:
                for j in range(self.vocabulary_size):
                    self.topic_word_prob[k, j] = 1.0 / self.vocabulary_size
            else:
                for j in range(self.vocabulary_size):
                    self.topic_word_prob[k, j] /= denominator

        for i in range(self.no_of_docs):
            for k in range(self.no_of_topics):
               self.document_topic_prob[i, k] = 0
               denominator = 0
               for j in range(self.vocabulary_size):
                   self.document_topic_prob[i, k] += self.term_doc_matrix[i, j] * self.topic_prob[i, j, k]
                   denominator += self.term_doc_matrix[i, j];
               if denominator == 0:
                   self.document_topic_prob[i, k] = 1.0 / self.no_of_topics
               else:
                   self.document_topic_prob[i, k] /= denominator
       # print("1st Matrix in M - topic_word_prob is built")
       # print("Topic_word_prob matrix is {}".format(self.topic_word_prob))
       # print("2nd Matrix in M - document_topic_prob is built")
       # print("Document_topic_prob is {}".format(self.document_topic_prob))
        
    def calculate_likelihood(self):
#        print("Calculating the Likelihood")
#        likelihood_matrix = np.zeros([self.no_of_docs, self.vocabulary_size], dtype=np.float)
#        x = np.matmul(self.document_topic_prob, self.topic_word_prob)
#        doc_term_matrix = np.log(x)
#        for d in range(self.no_of_docs):
#            for w in range(self.vocabulary_size):
#                likelihood_matrix[d][w] = self.total_doc_matrix[d][w] * doc_term_matrix[d][w]
#        word_vocab = np.zeros([self.no_of_docs, 1], dtype=np.float)
#        for d in range(self.no_of_docs):
#            for w in range(self.vocabulary_size):
#                word_vocab[d] += likelihood_matrix[d][w]
#        likelihood = 0.0
#        for d in range(self.no_of_docs):
#            likelihood += word_vocab[d]
#        print("likelihood is: {}".format(likelihood))
#        return likelihood
        likelihood = 0
        for i in range(0, self.no_of_docs):
            for j in range(0, self.vocabulary_size):
                tmp = 0
                for k in range(0, self.no_of_topics):
                    tmp += self.topic_word_prob[k, j] * self.document_topic_prob[i, k]
                if tmp > 0:
                    likelihood += self.term_doc_matrix[i, j] * np.log(tmp)
        return likelihood
    
    def plsa(self):
        print ("EM iteration begins...")
        current_likelihood = 1.0
        prev_likelihood = 1.0
       # prev_likelihood = current_likelihood
        for iteration in range(self.no_of_iterations):
            print("Iteration #" + str(iteration + 1) + "...")
            self.e_step()
            self.m_step()
            current_likelihood = self.calculate_likelihood()
            print("likelihood is: {}".format(current_likelihood))
            print("previous likelihood is: {}".format(prev_likelihood))
            if abs(prev_likelihood - current_likelihood) < self.threshold:
                print("Topic Word Prob is : {}".format(self.topic_word_prob))
                print("Document Topic Prob is : {}".format(self.document_topic_prob))
                break
            else:
                prev_likelihood = current_likelihood
               
        
        
    def normalize(self):
        for i in range(self.no_of_docs):
            normalization = sum(self.document_topic_prob[i, :])
            for j in range(self.no_of_topics):
                self.document_topic_prob[i, j] /= normalization;
                
        for i in range(self.no_of_topics):
            normalization = sum(self.topic_word_prob[i, :])
            for j in range(self.vocabulary_size):
                self.topic_word_prob[i, j] /= normalization;
                
                
    def print_files(self, topic_doc_fname, topic_word_fname, vocabulary_fname, topic_fname):
    # document-topic distribution
        file = codecs.open(topic_doc_fname,'w','utf-8')
        for i in range(self.no_of_docs):
            tmp = ''
            for j in range(self.no_of_topics):
                tmp += str(self.document_topic_prob[i, j]) + ' '
            file.write(tmp + '\n')
        file.close()
    
        # topic-word distribution
        file = codecs.open(topic_word_fname,'w','utf-8')
        for i in range(self.no_of_topics):
            tmp = ''
            for j in range(0, self.vocabulary_size):
                tmp += str(self.topic_word_prob[i, j]) + ' '
            file.write(tmp + '\n')
        file.close()
    
        # dictionary
        file = codecs.open(vocabulary_fname,'w','utf-8')
        for i in range(self.vocabulary_size):
            file.write(self.map_id_to_word[i] + '\n')
        file.close()
    
        # top words of each topic
        file = codecs.open(topic_fname,'w','utf-8')
        for i in range(self.no_of_topics):
            topicword = []
            ids = self.topic_word_prob[i, :].argsort()
            for j in ids:
                topicword.insert(0, self.map_id_to_word[j])
            tmp = ''
            for word in topicword[0:min(self.no_of_topic_words_dist, len(topicword))]:
                tmp += word + ' '
            file.write(tmp + '\n')
        file.close()

        

        

def main():
    """
    This is the main function
    :return:
    """
    file_path = '../patient_data/'

    
    # Write the main code here
    if(len(sys.argv) == 11):
        file_name = sys.argv[1]
        stop_words_file_name = sys.argv[2]
        no_of_topics = int(sys.argv[3])
        max_iterations = int(sys.argv[4])
        epsilon = float(sys.argv[5])
        # no of words in Topic distribution
        no_of_topic_words = int(sys.argv[6])
        # topic distrubition for each document as output
        topic_doc_distribution = sys.argv[7]
        # topic word distribution as output
        topic_word_distribition = sys.argv[8]
        # vocabulary created as output
        vocabulary_out = sys.argv[9]
        # topics distribution as output
        topics_out = sys.argv[10]
    
    data_file_path = file_path + file_name
    stop_words_file_path = file_path + stop_words_file_name
    input_arg_list = []
    input_arg_list.append(data_file_path)
    input_arg_list.append(no_of_topics)
    input_arg_list.append(max_iterations)
    input_arg_list.append(epsilon)
    input_arg_list.append(no_of_topic_words)
    
    miner = TelehealthMiner(input_arg_list)
    miner.extract_purpose_notes()
    miner.build_stop_words_repo(stop_words_file_path)
    miner.clean_notes()
    miner.build_vocabulary()
    miner.build_term_doc_matrix()
    miner.initialize()
    miner.normalize()
    miner.plsa()
    miner.print_files(topic_doc_distribution,topic_word_distribition,vocabulary_out,topics_out)
   # miner.plsa(max_iteration,epsilon)
    
if __name__ == '__main__':
    main()
