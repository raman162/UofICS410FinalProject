# Topic Miner V2

## Installation Instructions

Create new virtual environment
```
python -m venv venv
```

Activate virtual environment
```
source venv/bin/activate
```

Install required packages
```
pip install -r requirements.txt
```

## Usage

```
# python topic_miner.py <path/to/encounters.res.csv> <number_of_topics>

python topic_miner.py ../demo_data/positive_encounters.res.csv 10
```

Output would be:

```
# topic coverage of topic probability per document in corpus
positive_encounters.res.csv.10-doc-topic-cov.txt

#grouping of words and probabilities of topic per line
positive_encounters.res.csv.10-topic-word-probs-grouped.txt

#all the probabilities for each topic per line
positive_encounters.res.csv.10-topic-word-probs.txt

#all the words for each topic per line
positive_encounters.res.csv.10-topics.txt

#vocabulary of corpus
positive_encounters.res.csv.vocab
```
