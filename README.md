# CS 410 - Final Project: Topic Mining Healthcare Data & Classification

## Team Members

Raman Walwyn-Venugopal - [rsw2@illinois.edu](rsw2@illinois.edu)
Srikanth Bharadwaz Samudrala - [sbs7@illinois.edu](sbs7@illinois.edu)
Satish Reddy Asi - [sasi2@illinois.edu](sasi2@illinois.edu)

## Quick Links
- [Proposal PDF](proposal.pdf)
- [Progress Report PDF](progress_report.pdf)

## Overview

The goal of this project is to perform topic mining and classification on
telehealth encounter nursing notes for notes that documented a positive outcome
for the patient form the telehealth services. To accomplish this there were
three primary steps that had to be completed, curating the dataset, building a
topic miner and building a classifier.

### Curating Dataset

__Requirements:__
- [ruby 2.X](https://www.ruby-lang.org/en/libraries/)
- [perl 5.X](https://www.perl.org/)

_Note: This code was ran on ubuntu 18.04 and ubuntu 20.04_

#### Exporting Raw Dataset

The source of the data is from [TimeDocHealth](https://timedochealth.com/) that
has a care team that focuses on providing telehealth services to patients with
multiple chronic diseases.  Two CSV files, each containing 10,000 records was
exported from the TimeDoc system. One file named `positive_encounters.csv`
contained only notes that were labelled as a positive outcome due to the
telehealth services while another file named `no_positive_encounters.csv` only
contained notes that weren't labelled as a positive outcome for the patient.
The format of the exported CSV files are as follows:
`<note_id>,<patient_id>,<purpose>,<duration>,<note>` The `<purpose>` is an
array of attributes of the telehealth encounter, it is selected from a
pre-defined list and can provide insights to the actions of the telehealth
encounter. The  `<duration>` is the total amount of time the telehealth
encounter took, and `<note>` is the free-text nursing note summarizing the
encounter that we will be performing topic mining on.

#### Automating De-Identification of Protected Health Information (PHI)

To ensure we're adhering to HIPPA [HIPPA Privacy
Guidelines](https://www.physionet.org/content/deid/1.1/) we have to redact
Protected Health Information (PHI). This was redacted using the
De-Identification (DEID) Software Package [De-Identification Software Package](
https://www.physionet.org/content/deid/1.1/). For the DEID to be effective,
it required creating separate files of patient names and identifiers
`pid_patientname.txt`, doctor first names `doctor_first_names.txt`, doctor last
names `doctor_last_names.txt`, locations `local_places.txt`, and company names
`company_names.txt`. The `pid_patientname.txt` was created by referencing all
the patients from the two exported CSV lists and curating a file formatted with
each line as `<PATIENT_ID>||||<PATIENT_FIRST_NAME>||||<PATIENT_LAST_NAME>`. The
`doctor_first_names.txt` and the `doctor_last_names.txt` files were created by
referencing exporting each care team member such as their Primary Care
Physician (PCP), Radiologist, etc. and writing each name to a new line. Both
files were scrubbed for duplicates and invalid data. The `local_places.txt` was
created by taking each address related for the patient and writing the city to
a town to each line. The `company_names.txt` file was created by listing out
the pharmacies and local healthcare organizations that the patient utilizes and
writing each to a new line.

For the DEID to perform the redaction of PHI, it required to be fed the notes
in a particular format. So the exported CSV file had to be transformed to the
following format:

```
START_OF_RECORD=<PATIENT_ID>||||<DOCUMENT_ID>||||
<DOCUMENT_CONTENT>
||||END_OF_RECORD
```

We accomplished this transformation for both of the CSV exported files using a
ruby script located at `deid/convert_csv_to_text.rb` and ran the
following commands:

```
# convert csv files to deid text format
ruby deid/convert_csv_to_text.rb demo_data/positive_encounters.csv
ruby deid/convert_csv_to_text.rb demo_data/no_positive_encounters.csv
```

The output produced two files named `positive_encounters.text` and
`no_positive_encounters.text` respectively. Afterwards the new text files were
copied into the DEID directory and  we ran the DEID perl script to
remove the PHI using the following commands:

```
# enter deid directory
cd deid

# redact PHI from text files
perl deid.pl ../demo_data/positive_encounters deid-output.config
perl deid.pl ../demo_data/no_positive_encounters deid-output.config
```

The output produced two PHI redacted files named `positive_encounters.res` and
`no_positive_encounters.res`. To convert the files back into the CSV format, we
used the following script located at `deid/convert_res_to_csv.rb` and
ran the following commands:

```
# convert redacted res files to csv
ruby deid/convert_res_to_csv.rb \
  demo_data/positive_encounters.res \
  demo_data/positive_encounters.csv
ruby deid/convert_res_to_csv.rb \
  demo_data/no_positive_encounters.res \
  demo_data/no_positive_encounters.csv
```

The output produced two files named `positive_encounters.res.csv` and
`no_positive_encounters.res.csv`.

_Note: Since the DEID is an automated too, we have to account for the
possibility of not redacting all PHI data. To minimize actual PHI distributed
50 samples were taken form both the `positive_encounters.res` and
`no_positive_encounters.res` file and manually verified to not contain PHI.
This sampled may be provided upon request by emailing
[rsw2@illinois.edu](rsw2@illinois.edu)_

### Topic Mining and Analysis on Dataset

TODO


### Classifier

__Requirements:__
- [Python 3.X][0]
- Python Virtual Environment Package (Included in Python standard library)

#### Overview of Functionality

The text classifier is responsible for reviewing the notes of the telehealth
encounters and classifying the note as positive versus non-positive. The
`classifier` module has the following features:
- Load positive and non-positive CSV files generated from the
  PHI De-identification process
- Clean data by removing PHI redaction sections, non-alphanumeric characters,
  extra white space, lemmatization, and stop words
- Generate a classifier using the
  [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) from sklearn
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

#### Setup

```
# change directory to classifier
cd classifier

# initlize python virtual evnrionment
python -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

#### Usage

Be sure to update the following constants `POSITIVE_CSV_FILE` and
`NO_POSITIVE_CSV_FILE` to the true file paths of the redacted data produced
from the De-Identification process. Also update the `CLASSIFIER_FILE` for where
you want to store the classifier.


The `classifier` module can be run as a script to quickly generate a classifier
with the pre-optimized defaults determined from testing.

```
python classifier.py
```

This will load the data, clean the data, generate a classifier, print out the
evaluation metrics and store it to the path defined in the `CLASSIFIER_FILE`
constant. An example of the classifier evaluation is shown below.

```
              precision    recall  f1-score   support

non-positive       0.71      1.00      0.83        10
    positive       1.00      0.60      0.75        10

    accuracy                           0.80        20
   macro avg       0.86      0.80      0.79        20
weighted avg       0.86      0.80      0.79        20

Accuracy:  0.8
```

The classifier can be loaded for usage in scripts by doing the following
```
import classifier.py

text_classifier = classifier.load(classifier.CLASSIFIER_FILE)
docs = ['Scheduled transportation for patient appointment on Thursday', 'discussed personal goals with patient']
prepped_docs = classifier.prepare_data(docs)
predictions = text_classifier.predict(prepped_docs)
print(predictions)
```

#### Optimizations

The classification accuracy score was optimized by varying the number of
features and estimators (decision trees) used in the algorithm. This was a
simple iterative algorithm that calculated the accuracy for each
feature/estimator combination and then returned the optimal score and the
combination used to accomplish.

The classifier module has an `optimize_score` function that accepts the
following arguments:
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

It outputs a dictionary that contains the following keys:
```
feature_steps - varying features used
estimator_steps - varying estimators used
scores - 2-dimension numpy array containing all scores generated. Shape is feature stpes length x estimator steps length
optimal_score - The highest accuracy result from the iterations
optimal_num_features - The number of features used to generate optimal score
optimal_num_estimators - The number of estimators used to generate optimal score
```

The optimal number of features used was determined to be 1500 while the optimal
number of estimators was determined to be 750.
