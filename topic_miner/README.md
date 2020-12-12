# Probabilistic Latent Semantic Analysis and Topic Miner
The Topic Miner module is implementation of PLSA and mine topics from Documents

### Sub-Modules
- [ ] stopwords

        This sub module is to generate Stop words. The file generated (stopwords.txt) will be used as stop words.
- [ ] topic_miner

        This is the module implementing PLSA and generating Vocabular/Dictionary, top words of topics and coverage probabilities
        
### Usage
##### stopwords
        python stopwords.py
##### topic_miner
        python topic_miner.py data_file.csv stopwords.txt <num_topics> <num_iterations> <epsilon> <num_topic-words> <output-doc_topic_coverage-file> <output-topic_word_coverage> <output-vocabulary-file> <output-topic_words-file>
        
        Example:
        python topic_miner.py encounters.res-sample-50.res.csv stopwords.txt 10 50 3.0 1000 ../doctopic.txt ../topicword.txt ../dictionary.dic ../topics.txt

#### Usage guidelines
- [ ] The input is present in a folder "patient_data" as a child folder under root of the project i.e.
- [ ] Make sure stopwords.txt generated from stopwords sub-module is copied to 

####Arguments Explanation
| Argument | Description |
|:-------- |:-----------|
| data_file.csv  | Teledoc data in CSV file      |
| stopwords.txt     | stop words file with path       |
| num_topics   | Number of Topics |
| num_iterations | Number of Maximum Iterations |
| epsilon | Threshold for Likelihood difference for convergence |
| num_topic_words | Number of Words in the Topic |
| output-doc_topic_coverage-file | Document Topic Coverage probabilities - output file |
| output-topic_word_coverage | Topic Word Coverage probabilities - output file |
| output-vocabulary-file | Dictionary or Vocabulary file - output file |
| output-topic_words-file | Words of Topics - output file |