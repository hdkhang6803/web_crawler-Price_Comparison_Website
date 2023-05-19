import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

from DataStructures.GoogleSheet import GoogleSheet

class ProductClassifier:
    test_row = 700
    def __init__(self, spreadsheet_id, cred_file):
        self.ggsheet = GoogleSheet(spreadsheet_id, cred_file)
        self.categories = list(self.ggsheet.categories_id.keys())
        self.training_data = []
        self.model = MultinomialNB()
        self.vectorizer = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()
        pass

    def get_training_data(self, size):
        for category_i in range(0, len(self.categories)):
            tmp = [[x[0], category_i] for x in (self.ggsheet.get_data(1, size, 1, self.categories[category_i])['values'])]
            for x in tmp:
                self.training_data.append(x)
    
    def get_testing_data_from_sheet(self, size):
        testing_data = []
        for category_i in range(0, len(self.categories)):
            tmp = [[x[0], category_i] for x in (self.ggsheet.get_data(self.test_row, self.test_row + size, 1, self.categories[category_i])['values'])]
            for x in tmp:
                testing_data.append(x)
        return testing_data
            
    def train_classifier(self, size):
        self.get_training_data(size)
        X_train_counts = self.vectorizer.fit_transform([data[0] for data in self.training_data])
        X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)
        y_train = np.array([data[1] for data in self.training_data])

        # Train the classifier
        self.model.fit(X_train_tfidf, y_train)
    
    def get_accuracy(self, testing_data = None): 
        if testing_data == None:
            testing_data = self.get_testing_data_from_sheet(500)
        X_test_counts = self.vectorizer.transform([data[0] for data in testing_data])
        X_test_tfidf = self.tfidf_transformer.transform(X_test_counts)
        y_test = np.array([data[1] for data in testing_data])

        # Predict the test data
        y_pred = self.model.predict(X_test_tfidf)

        # Calculate the accuracy
        accuracy = np.mean(y_pred == y_test)
        return accuracy

    def save_model(self):
        pickle.dump(self.model, open("classifier.sav", "wb"))
        pickle.dump(self.vectorizer, open("vectorizer.sav", "wb"))
        pickle.dump(self.tfidf_transformer, open("tfidf_transformer.sav", "wb"))

    def load_model(self):
        if (os.path.isfile("classifier.sav") and os.path.isfile("vectorizer.sav") 
            and os.path.isfile("tfidf_transformer.sav")):
            self.model = pickle.load(open("classifier.sav", "rb"))
            self.vectorizer = pickle.load(open("vectorizer.sav", 'rb'))
            self.tfidf_transformer = pickle.load(open("tfidf_transformer.sav", 'rb'))
            return 1
        else:
            return 0
    
    def predict(self, input_string):
        # Vectorize the input string
        X_input_counts = self.vectorizer.transform([input_string])
        X_input_tfidf = self.tfidf_transformer.transform(X_input_counts)

        # Classify the input string
        y_pred = self.model.predict(X_input_tfidf)[0]
        category = self.categories[y_pred]
        return category

if __name__ == "__main__":
    tester = ProductClassifier("1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g", "client_secret.json")
    if (tester.load_model()):
        print("model loaded succesfully yay")
        print(tester.predict("Laptop ASUS"))
    else:
        tester.train_classifier()
        tester.get_accuracy()
        print(tester.predict("Laptop ASUS"))
        tester.save_model()