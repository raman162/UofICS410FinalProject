# Topic Analysis

This script performs analysis on the results of the topic miner. It attempts
to:
1. Identify which topics are related to positive outcomes and which topics are
   related to non-positive outcomes
2. Pull the top words from the positive outcome topics and non-positive outcome
   topics
3. Highlight which top words from positive and non-positive overlap
   with each other versus which words are unique to their own topics
4. generates 4 files: `pos-non-pos-topics.txt`, `top-pos-words.txt` and
   `top-non-pos-words.txt`

__Requirements:__
- Python 3.x

## Usage

_Note: Run the topic miner on a concatenated positive and non-positive encounters CSV
file. DO NOT randomize the entries, join positive and non-positive entries
sequentially_

```
# python topic_analysis.py <path_to_doc_topic_cov_file> <path_to_topic_word_file>
python topic_analysis.py \
  ../patient_data/all_encounters.res.csv.10-doc-topic-cov.txt \
  ../patient_data/all_encounters.res.csv.10-topics.txt
```


## Results

Top 20 Positive Words:
```
['someone', 'pharmacy', 'month', 'refill', 'transportation', 'chart',
'voicemail', 'information', 'date', 'shower', 'pill', 'difficulty',
'insurance', 'name', 'phone', 'appointment', 'meal', 'number', 'office',
'message', 'contact', 'desk', 'wheel', 'prescription', 'assistance', 'call',
'care', 'activity', 'machine', 'birth', 'appt', 'hospitalization', 'ccma',
'visit', 'ncm', 'living']
```

Top 20 Non-Positive Words:
```
['encounter', 'change', 'medication', 'emr', 'colonoscopy', 'update',
'treatment', 'agreement', 'information', 'date', 'goal', 'week', 'gap',
'breathing', 'phone', 'health', 'appointment', 'spoke', 'eye', 'conversation',
'knee', 'etc', 'year', 'question', 'state', 'oxygen', 'office', 'inhaler',
'service', 'reconciliation', 'wellness', 'rate', 'exercise', 'exam', 'lot',
'doctor', 'day', 'plan']
```

Overlapping Positive and Non-Positive Words:
```
['information', 'date', 'phone', 'office', 'appointment']
```

Top 20 Unique Positive Words:
```
['someone', 'pharmacy', 'month', 'refill', 'transportation', 'chart',
'voicemail', 'shower', 'pill', 'difficulty', 'insurance', 'name', 'meal',
'number', 'message', 'contact', 'wheel', 'desk', 'prescription', 'assistance',
'call', 'care', 'activity', 'machine', 'birth', 'appt', 'hospitalization',
'ccma', 'visit', 'ncm', 'living']
```

Top 20 Unique Non-Positive Words:
```
['encounter', 'change', 'medication', 'emr', 'colonoscopy', 'update',
'treatment', 'agreement', 'goal', 'week', 'gap', 'breathing', 'health',
'spoke', 'eye', 'conversation', 'knee', 'etc', 'year', 'question', 'state',
'oxygen', 'inhaler', 'service', 'reconciliation', 'wellness', 'rate',
'exercise', 'exam', 'lot', 'doctor', 'day', 'plan']
```
