# Topic Analysis

This script performs an analysis on the result of the topic miner. It attempts
to:
1. Identify which topics are related to positive outcomes and which topics are
   related to non-positive outcomes
2. Pull the top words from the positive outcome topics and non-positive outcome
   topics
3. Highlight which top words from positive and non-positive intersect/overlap
   with each other versus which words are unique to their own topics

__Requirements:__
- Python 3.x

## Usage
- Run the topic miner on a concatenated positive and non-positive encounters
  CSV file. DO NOT randomize the entries, keep positive and non-positive
  separated
- update the paths for the coverage file path and the topic word file path
  by changing the COVERAGE_FILE_PATH and TOPIC_WORD_FILE_PATH constants
  respectively
- update the POSITIVE_RANGE and NON_POSITIVE_RANGE to indicate which series of
  notes/documents are positive versus non-positive.
- run `python topic_analysis.py`


## Results

Top Positive Words:
```
['birth', 'med', 'denies', 'wheel', 'wife', 'sooner', 'today', 'tomorrow',
'schedule', 'blood', 'pill', 'concern', 'information', 'someone', 'visit',
'staff', 'state', 'center', 'training', 'emr', 'follow', 'shoulder',
'permission', 'supply', 'cell', 'pound', 'encounter', 'request', 'nurse',
'area', 'activity', 'report', 'program', 'gap', 'number', 'couple',....]
```

Top Non-Positive Words:
```
['allergy', 'pain', 'denies', 'pack', 'today', 'weather', 'tomorrow', 'basis',
'awv', 'conversation', 'blood', 'concern', 'information', 'intervention',
'visit', 'state', 'center', 'bike', 'emr', 'follow', 'hour', 'rescue',
'sample', 'everything', 'supply', 'share', 'potassium', 'son', 'mammogram',
'encounter', 'end', 'tank', 'team', 'department', 'agreement', 'arm', 'note',
'manager', 'mucinex', 'diabetes', 'injection', ....]
```

Overlapping Positive and Non-Positive Words:
```
['pcp', 'spoke', 'plan', 'denies', 'home', 'week', 'today', 'assistance',
'tomorrow', 'etc', 'change', 'month', 'blood', 'insurance', 'foot', 'concern',
'information', 'call', 'visit', 'date', 'state', 'center', 'question',
'health', 'emr', 'time', 'follow', 'supply', 'issue', 'phone', 'morning',
'office', 'need', 'beginning', 'medication', 'result', 'day', 'encounter',
'lot', 'message', 'service', 'ncm', 'minute', 'food', 'provider', 'treatment',
'yesterday', 'statement', 'appointment', 'care', 'pharmacy', 'gap', 'refill',
'number', 'couple', 'chart', 'hospitalization']
```

Top Unique Positive Words:
```
['birth', 'med', 'wheel', 'wife', 'sooner', 'schedule', 'pill', 'someone',
'staff', 'training', 'shoulder', 'permission', 'cell', 'pound', 'request',
'nurse', 'area', 'activity', 'report', 'program', 'amlodipine', 'quality',
'grandson', 'price', 'desk', 'leg', 'planning', 'front', 'weakness', 'purpose',
'practice', 'trip', 'voicemail', 'difficulty', 'letter', 'husband', 'lab',
'cardiology', 'machine', 'referral', 'place', 'carb', 'living', 'thing',
'nothing', 'coverage', 'insulin', 'anxiety', 'appetite', 'tremor', 'appt'...]
```

Top Unique Non-Positive Words:
```
['allergy', 'pain', 'pack', 'weather', 'basis', 'awv', 'conversation',
'intervention', 'bike', 'hour', 'rescue', 'sample', 'everything', 'share',
'potassium', 'son', 'mammogram', 'end', 'tank', 'team', 'department',
'agreement', 'arm', 'note', 'manager', 'mucinex', 'diabetes', 'injection',
'ophthalmologist', 'treadmill', 'mention', 'inhaler', 'stress', 'cataract',
'hipaa', 'offer', 'craving', 'sugar', 'hyperlipidemia', 'management',
'shortness', 'problem', 'cane', 'kidney', 'podiatrist', 'disease', 'regimen',
'psychiatrist', 'barrier', '....]
```
