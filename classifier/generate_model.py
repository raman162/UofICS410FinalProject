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

nltk.download('wordnet')
nltk.download('stopwords')

## PATH TO FILES
POSITIVE_CSV_FILE = '../patient_data/positive_encounters.res.csv'
NO_POSITIVE_CSV_FILE = '../patient_data/no_positive_encounters.res.csv'
CLASSIFIER_FILE = './text_classifier'

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
    transformer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            stop_words = stopwords.words('english'))
    return transformer.fit_transform(docs).toarray()

def generate_classifier(docs, labels, n_estimators=1000, test_size=0.2, random_state=0):
    train_docs, test_docs, train_labels, test_labels = train_test_split(
        docs,
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

def store_classifier(classifier, file_path):
    with open(file_path, 'wb') as picklefile:
        pickle.dump(classifier, picklefile)

def load_classifier(file_path):
    classifier = None
    with open(file_path, 'rb') as picklefile:
        classifier = pickle.load(picklefile)
    return classifier


def build_optimized_classifier(**kwargs):
    docs, labels = load_data()
    clean_docs = clean_data(docs)
    min_features = kwargs.get('min_features', 1000)
    max_features = kwargs.get('max_features', 5000)
    feature_step = kwargs.get('feature_step', 250)
    min_estimators = kwargs.get('min_estimators', 750)
    max_estimators = kwargs.get('max_estimators', 2500)
    estimator_step = kwargs.get('estimator_step', 250)
    min_df = kwargs.get('min_df', 10)
    max_df = kwargs.get('max_df', 0.8)
    feature_steps = list(range(min_features, max_features + 1, feature_step))
    estimator_steps = list(range(min_estimators, max_estimators + 1, estimator_step))
    scores = np.zeros([len(feature_steps), len(estimator_steps)])
    for feature_index in range(len(feature_steps)):
        num_features = feature_steps[feature_index]
        for estimator_index in range(len(estimator_steps)):
            num_estimators = estimator_steps[estimator_index]
            print("###################")
            print("# Of Features: ", num_features)
            print("# Of Estimators: ", num_estimators)
            transformed_docs = transform_docs_to_numeric(
                    clean_docs,
                    max_features=num_features,
                    min_df=min_df,
                    max_df=max_df)
            classifier, train_test_data = generate_classifier(
                    transformed_docs,
                    labels,
                    n_estimators=num_estimators)
            predict_labels = classifier.predict(train_test_data['test_docs'])
            score = accuracy_score(
                    train_test_data['test_labels'],
                    predict_labels)
            scores[feature_index][estimator_index] = score
            print("Score: ", score)
            print("###################\n\n")

    optimal_feature_index, optimal_estimator_index = np.unravel_index(
            scores.argmax(),
            scores.shape)
    return {
            'feature_steps': feature_steps,
            'estimator_steps': estimator_steps,
            'scores': scores,
            'optimal_score': scores.max(),
            'optimal_num_features': feature_steps[optimal_feature_index],
            'optimal_num_estimators': estimator_steps[optimal_estimator_index]
            }





if __name__ == '__main__':
    docs, labels = load_data()
    clean_docs = clean_data(docs)
    transformed_docs = transform_docs_to_numeric(clean_docs)
    classifier, train_test_data = generate_classifier(transformed_docs, labels)
    evaluate_classifier(classifier, train_test_data)
    store_classifier(classifier, CLASSIFIER_FILE)
