import numpy as np
import re
import nltk
import pickle
import csv
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

## PATH TO FILES
POSITIVE_CSV_FILE = '../patient_data/positive_encounters.res-sample-50.res.csv'
NO_POSITIVE_CSV_FILE = '../patient_data/no_positive_encounters.res-sample-50.res.csv'

def load_data():
    docs = []
    labels = []

    # Load positive docs
    with open(POSITIVE_CSV_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                docs.append(row[4])
                labels.append('positive')
            line_count += 1

    # Load non-positive docs
    with open(NO_POSITIVE_CSV_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                docs.append(row[4])
                labels.append('non-positive')
            line_count += 1

    return docs, np.array(labels)

def clean_data(docs):
    clean_docs = []
    nltk.download('wordnet')
    stemmer = WordNetLemmatizer()
    for dirty_doc in docs:
        # remove phi redaction brackets
        clean_doc = re.sub(r'\[\*\*.*?\*\*\]+', ' ', dirty_doc)

        # remove special chars
        clean_doc = re.sub(r'\W', ' ', clean_doc)

        # remove all single chars
        clean_doc = re.sub(r'\s+[a-zA-Z]\s+', ' ', clean_doc)

        # remove single chars  from the start
        clean_doc = re.sub(r'\^[a-zA-Z]\s+', ' ', clean_doc)

        # replace multi space with single space
        clean_doc = re.sub(r'\s+', ' ', clean_doc, flags=re.I)

        # removing prefixed with 'b'
        clean_doc = re.sub(r'^b\s+', '', clean_doc)

        # conver to lowercase
        clean_doc = clean_doc.lower()

        # lemmatization
        clean_doc =  clean_doc.split()
        clean_doc = [stemmer.lemmatize(word) for word in clean_doc]
        clean_doc = ' '.join(clean_doc)

        clean_docs.append(clean_doc)

    return clean_docs

def transform_docs_to_numeric(docs, max_features=2000, min_df=10, max_df=0.8):
    nltk.download('stopwords')
    transformer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            stop_words = stopwords.words('english'))
    return transformer.fit_transform(docs).toarray()

def generate_classifier(docs, labels, n_estimators=1000, test_size=0.2, random_state=0):
    train_docs, test_docs, train_labels, test_labels = train_test_split(
        transformed_docs,
        labels,
        test_size=test_size,
        random_state=random_state)
    classifier = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state)
    classifier.fit(train_docs, train_labels)
    train_test_data = {
            'train_docs': train_docs,
            'test_docs': test_docs,
            'train_labels': train_labels,
            'test_labels': test_labels
        }
    return classifier, train_test_data

def evaluate_classifier(classifier, train_test_data):
    test_docs = train_test_data['test_docs']
    test_labels = train_test_data['test_labels']
    predict_labels = classifier.predict(test_docs)
    print(confusion_matrix(test_labels, predict_labels))
    print(classification_report(test_labels, predict_labels))
    print(accuracy_score(test_labels, predict_labels))

if __name__ == '__main__':
    docs, labels = load_data()
    clean_docs = clean_data(docs)
    transformed_docs = transform_docs_to_numeric(clean_docs)
    classifier, train_test_data = generate_classifier(transformed_docs, labels)
    evaluate_classifier(classifier, train_test_data)

"""
docs, labels = generate_model.load_data()
clean_docs = generate_model.clean_data(docs)
transformed_docs = generate_model.transform_docs_to_numeric(clean_docs)
train_docs, test_docs, train_labels, test_labels = train_test_split(
    transformed_docs,
    labels,
    test_size=0.2,
    random_state=0)
"""
