COVERAGE_FILE_PATH = '../patient_data/all_encounters.res.csv.10-doc-topic-cov.txt'
TOPIC_WORD_FILE_PATH = '../patient_data/all_encounters.res.csv.10-topics.txt'

POSITIVE_RANGE = [0, 499]
NON_POSITIVE_RANGE = [500, 999]

# Read file
f = open(COVERAGE_FILE_PATH, 'r')
content = f.read()
lines = content.splitlines()
f.close()

# get number of topics
NUMBER_OF_TOPICS = len(lines[0].split())

# compute average topic distribution of positive versus non-positive
pos_topic_sums = [0] * NUMBER_OF_TOPICS
non_pos_topic_sums = [0] * NUMBER_OF_TOPICS
index = 0
for line in content.splitlines():
    dist = list(map(lambda x: float(x), line.split()))
    for i in range(len(dist)):
        if index <= POSITIVE_RANGE[1]:
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

sorted_diffs = sorted(range(len(pos_non_pos_topic_average_diff)), key=lambda i: pos_non_pos_topic_average_diff[i])
top_pos_topics = sorted_diffs[-2:]
print('#######################')
print('top_pos_topics: ', top_pos_topics)
print('######################\n')
sorted_diffs.reverse()
top_non_pos_topics = sorted_diffs[-2:]
print('#######################')
print('top_non_pos_topics: ', top_non_pos_topics)
print('######################\n')

# get top 50 words for each topic
topic_words_file = open(TOPIC_WORD_FILE_PATH)
topic_words = topic_words_file.read()
topic_words_file.close()
topics = topic_words.splitlines()

# retrieve pos topic words
top_pos_words = []
for topic in top_pos_topics:
    top_pos_words += topics[topic].split()[:50]
top_pos_words =  list(set(top_pos_words))
print('#######################')
print('top_pos_words: ', top_pos_words)
print('######################\n')

# retrieve pos topic words
top_non_pos_words = []
for topic in top_non_pos_topics:
    top_non_pos_words += topics[topic].split()[:50]
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
