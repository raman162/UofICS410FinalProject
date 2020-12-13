import string
import sys
import nltk
from nltk.corpus import stopwords
import codecs
from plsa import Corpus, Pipeline, Visualize
from plsa import preprocessors
from plsa.pipeline import DEFAULT_PIPELINE
from plsa.algorithms import PLSA

nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

pipeline_args = [
    preprocessors.remove_non_ascii,
    preprocessors.to_lower,
    preprocessors.remove_numbers,
    preprocessors.remove_tags('<[^>]*>'),
    preprocessors.remove_tags('\[\*\*.*?\*\*\]+'),
    preprocessors.remove_punctuation(string.punctuation),
    preprocessors.tokenize,
    preprocessors.LemmatizeWords('NN'),
    preprocessors.RemoveStopwords(stopwords.words('english') + ['patient', 'nbsp', 'amp', 'urllink']),
    preprocessors.remove_short_words(3)
]
pipeline = Pipeline(*pipeline_args)
csv_file = sys.argv[1]
n_topics = sys.argv[2]
print('#######################')
print('beginning topic mining!')
print('csv_file: ', csv_file)
print('number of topics: ', n_topics)
print('prepping dataset through pipeline...')
corpus = Corpus.from_csv(csv_file, pipeline, col=4)
plsa = PLSA(corpus, n_topics, True)
print('running plsa...')
result = plsa.fit()
print('finished plsa')


print('writing results...')
topic_word_file_path = csv_file + '.' + n_topics + '-topics.txt'
topic_word_file = codecs.open(topic_word_file_path, 'w', 'utf-8')

topic_word_prob_file_path = csv_file + '.' + n_topics + '-topic-word-probs.txt'
topic_word_prob_file = codecs.open(topic_word_prob_file_path, 'w', 'utf-8')

topic_word_prob_grouped_file_path = csv_file + '.' + n_topics + '-topic-word-probs-grouped.txt'
topic_word_prob_grouped_file = codecs.open(topic_word_prob_grouped_file_path, 'w', 'utf-8')
for topic in result.word_given_topic:
    topic_words = []
    word_probs = []
    topic_word_prob_groups = []
    for word_prob in topic:
        topic_words.append(word_prob[0])
        word_probs.append(str(word_prob[1]))
    words = ' '.join(topic_words)
    probs = ' '.join(word_probs)
    topic_word_file.write(words + '\n')
    topic_word_prob_file.write(probs + '\n')
    topic_word_prob_grouped_file.write(str(topic) + '\n')

print('writing topics to: ', topic_word_file_path)
topic_word_file.close()

print('writing topic word probabilities to: ', topic_word_prob_file_path)
topic_word_prob_file.close()

print('writing topic word probabilities grouped to: ', topic_word_prob_grouped_file_path)
topic_word_prob_grouped_file.close()

doc_topic_cov_file_path = csv_file + '.' + n_topics + '-doc-topic-cov.txt'

print('writing doc topic coverage file: ', doc_topic_cov_file_path)
doc_topic_cov_file = codecs.open(doc_topic_cov_file_path, 'w', 'utf-8')
for doc_topic_cov in result.topic_given_doc:
    probs = ' '.join(list(map(lambda x: str(x), doc_topic_cov)))
    doc_topic_cov_file.write(probs + '\n')
doc_topic_cov_file.close()

vocab_file_path = csv_file + '.vocab'
print('writing vocabulary to: ', vocab_file_path)

vocab_file = codecs.open(vocab_file_path, 'w', 'utf-8')
for word in corpus.vocabulary.values():
    vocab_file.write(word + '\n')
vocab_file.close()

print('finished writing results')
