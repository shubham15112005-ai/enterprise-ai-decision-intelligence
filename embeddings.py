import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer


print("Shubham Sharma 23051870")


class TfidfEmbeddingModel:

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=10000,
        )

    def fit(self, texts):

        return self.vectorizer.fit_transform(
            texts
        )

    def transform(self, texts):

        return self.vectorizer.transform(
            texts
        )

    def save(self, path):

        with open(
            path,
            "wb"
        ) as file:

            pickle.dump(
                self.vectorizer,
                file
            )

    def load(self, path):

        with open(
            path,
            "rb"
        ) as file:

            self.vectorizer = pickle.load(
                file
            )