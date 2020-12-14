import sys

COVERAGE_FILE_PATH = sys.argv[1]
TOPIC_WORD_FILE_PATH = sys.argv[2]

# Read file
doc_topic_cov_file = open(COVERAGE_FILE_PATH, 'r')
content = doc_topic_cov_file.read()
lines = content.splitlines()
doc_topic_cov_file.close()

# get number of topics
NUMBER_OF_TOPICS = len(lines[0].split())

# get number of positive docs
NUM_POSITIVE_DOCS = len(lines)/2

# compute average topic distribution of positive versus non-positive
pos_topic_sums = [0] * NUMBER_OF_TOPICS
non_pos_topic_sums = [0] * NUMBER_OF_TOPICS
index = 0
for line in lines:
    dist = list(map(lambda x: float(x), line.split()))
    for i in range(len(dist)):
        if index < NUM_POSITIVE_DOCS:
            pos_topic_sums[i] += dist[i]
        else:
            non_pos_topic_sums[i] += dist[i]
    index += 1
pos_topic_averages = list(map(lambda x: (x/500.0)*100.0, pos_topic_sums))
print('#######################')
print('pos_topic_averages: ', pos_topic_averages)
print('######################\n')
non_pos_topic_averages = list(map(lambda x: (x/500.0)*100.0, non_pos_topic_sums))
print('#######################')
print('non_pos_topic_averages: ', non_pos_topic_averages)
print('######################\n')



# compute top 2 topics positive versus non-positive
pos_non_pos_topic_average_diff = [None] * NUMBER_OF_TOPICS
for i in range(NUMBER_OF_TOPICS):
    pos_non_pos_topic_average_diff[i] = pos_topic_averages[i] - non_pos_topic_averages[i]
print('######################')
print('pos_non_pos_topic_average_diff: ', pos_non_pos_topic_average_diff)
print('######################\n')


sorted_diffs = sorted(range(len(pos_non_pos_topic_average_diff)), key=lambda i: pos_non_pos_topic_average_diff[i])
num_topics_to_select = int(min(NUMBER_OF_TOPICS/2, 2) * -1)
top_pos_topics = sorted_diffs[num_topics_to_select:]
print('#######################')
print('top_pos_topics: ', list(map(lambda x: x + 1, top_pos_topics)))
print('######################\n')
sorted_diffs.reverse()
top_non_pos_topics = sorted_diffs[num_topics_to_select:]
print('#######################')
print('top_non_pos_topics: ', list(map(lambda x: x + 1, top_non_pos_topics)))
print('######################\n')


# get top 20 words for each topic
topic_words_file = open(TOPIC_WORD_FILE_PATH)
topic_words = topic_words_file.read()
topic_words_file.close()
topics = topic_words.splitlines()

# retrieve pos topic words
top_pos_words = []
for topic in top_pos_topics:
    top_pos_words += topics[topic].split()[:20]
top_pos_words =  list(set(top_pos_words))
print('#######################')
print('top_pos_words: ', top_pos_words)
print('######################\n')

# retrieve pos topic words
top_non_pos_words = []
for topic in top_non_pos_topics:
    top_non_pos_words += topics[topic].split()[:20]
top_non_pos_words = list(set(top_non_pos_words))
print('#######################')
print('top_non_pos_words: ', top_non_pos_words)
print('######################\n')

# intersection of top words from pos and non_pos topics
intersection = list(set(top_pos_words) & set(top_non_pos_words))
print('#######################')
print('pos non_pos intersection: ', intersection)
print('######################\n')

unique_pos_words = list(set(top_pos_words) - set(top_non_pos_words))
print('#######################')
print('unique_pos_words: ', unique_pos_words)
print('######################\n')
unique_non_pos_words = list(set(top_non_pos_words) - set(top_pos_words))
print('#######################')
print('unique_non_pos_words: ', unique_non_pos_words)
print('######################\n')

# write files
pos_no_pos_topic_cov_file_path = TOPIC_WORD_FILE_PATH + '.pos-non-pos-topics.txt'
print('writing top pos and non pos topics to: ', pos_no_pos_topic_cov_file_path)
pos_no_pos_topic_cov_file = open(pos_no_pos_topic_cov_file_path, 'w')
pos_no_pos_topic_cov_file.write('top_pos_topics: ' + str(map(lambda x: x + 1, top_pos_topics)) + '\n')
pos_no_pos_topic_cov_file.write('top_non_pos_topics: ' + str(map(lambda x: x +1, top_non_pos_topics)))
pos_no_pos_topic_cov_file.close()

top_pos_words_file_path = TOPIC_WORD_FILE_PATH + '.top-pos-words.txt'
print('wrting top pos words to: ', top_pos_words_file_path)
top_pos_words_file = open(top_pos_words_file_path, 'w')
top_pos_words_file.write(' '.join(top_pos_words))
top_pos_words_file.close()

top_non_pos_words_file_path = TOPIC_WORD_FILE_PATH + '.top-non-pos-words.txt'
print('wrting top non pos words to: ', top_non_pos_words_file_path)
top_non_pos_words_file = open(top_non_pos_words_file_path, 'w')
top_non_pos_words_file.write(' '.join(top_non_pos_words))
top_pos_words_file.close()
