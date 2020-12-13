# Text Classifier

The text classifier is responsible for reviewing the notes of the telehealth
encounters and classifying the note as positive versus non-positive. The
`classifier` module has the following features:
- Load positive and non-positive CSV files generated from the
  PHI De-identification process
- Clean data by removing PHI redaction sections, non-alphanumeric characters,
  extra white space, lemmatization, and stop words
- Generate a classifier using the `RandomForestClassifier` from `sklearn`
- Evaluate classifier by collecting Recall, Precision, F1 Score, micro
  averages per category, mean absolute error, mean squared error, root mean
  squared error and the overall classification accuracy
- Store classifier to a file
- Load classifier from a file
- Score optimizer that steps through a combination of number of features and
  estimators for the classifier model and returns the optimal inputs and score

The process of generating the classifier requires the docs to be cleaned and
vectorized into TF-IDF weights. The vectorized version of the corpus was then
split into two sets; 20% for training and 80% for testing. The model used for
training is the `RandomForestClassifier` from `sklearn` which is based on a
Random Forest Algorithm that uses a 'random forest' of numerous decision trees.

The core of the algorithm follows the steps below:
- Pick N random records from the dataset
- Build a decision tree on the randomly selected N records
- Choose the number of trees used in the algorithm and repeat steps 1 and 2

The algorithm is ideal for classification because it is known to reduce
biases with the use of multiple randomly formed decision trees and it performs
well when unknown data points are introduced. Disadvantages of the algorithm is
that the complexity causes it to take longer to train and process due to the
amount of decision trees.

## Requirements

- [Python 3.X][0]
- Python Virtual Environment Package (Included in Python standard library)

## Setup

Initialize python virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

## Usage

Be sure to update the following constants `POSITIVE_CSV_FILE` and
`NO_POSITIVE_CSV_FILE` to the true file paths of the redacted data produced
from the De-Identification process. Also update the `CLASSIFIER_FILE` for where
you want to store the classifier

### Generate Classifier

The `classifier` module can be run as a script to quickly generate a classifier
with the pre-optimized defaults determined from testing.

```
python classifier.py
```

This will load the data, generate a classifier, print out the evaluation
metrics and store it to path defined in the `CLASSIFIER_FILE` constant.

The classifier can be loaded for usage in scripts by doing the following
```
import classifier.py

text_classifier = classifier.load(classifier.CLASSIFIER_FILE)
docs = ['Scheduled transportation for patient appointment on Thursday', 'discussed personal goals with patient']
prepped_docs = classifier.prepare_data(docs)
predictions = text_classifier.predict(prepped_docs)
print(predictions)
```

### Determine Optimal Inputs To Generate Classifier

The `optimize_score` function iteratively calculates the accuracy score for a
classifier based on the varying number of features and estimators used.
The arguments for the score function are:
```
docs (default: to cleaned version of dataset) - complete corpus of documents
labels (default to dataset defined) - labels each document
min_features (default: 1000)- start number of features to use
max_features (default: 5000)- max number of features to use
feature_step (default: 250) - amount to increase number of features by
min_df (default: 10) - minimum document frequency for a feature to be selected
max_df (default: 0.8) - maximum document frequency for a feature to be selected
min_estimators (default: 750) - start number of estimators to use
max_estimators (default: 2500) - max number of estimators to use
estimator_step (default: 250) - amount to increase number of estimators by
```

The output is a dictionary that contains the following keys:
```
feature_steps - varying features used
estimator_steps - varying estimators used
scores - 2-dimension numpy array containing all scores generated. Shape is feature stpes length x estimator steps length
optimal_score - The highest accuracy result from the iterations
optimal_num_features - The number of features used to generate optimal score
optimal_num_estimators - The number of estimators used to generate optimal score
```

The optimizer can be run following the steps below:
```
import classifier

docs, labels = classifier.load_data()

result = classifier.optimize_score(
  docs=docs,
  labels=labels,
  min_features=500,
  feature_step=100,
  max_features=1500,
  min_estimators=500,
  max_estimators=1500,
  estimator_step=100)
print(result)

clean_docs = classifier.clean_data(docs)
text_classifier, train_test_data = classifier.generate(
  clean_docs,
  labels
  n_estimators=result['optimal_num_estimators'],
  max_features=result['optimal_num_features'])
classifier.evaluate(text_classifier, train_test_data)
```

[0]: https://www.python.org/

