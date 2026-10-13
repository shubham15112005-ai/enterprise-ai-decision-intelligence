import pickle

from sklearn.metrics.pairwise import cosine_similarity


print("Shubham Sharma 23051870")


class VectorStore:

    def __init__(self):

        self.documents = []

        self.matrix = None

        self.embedding_model = None

    def build(
        self,
        documents,
        embedding_model
    ):

        self.documents = list(
            documents
        )

        self.embedding_model = (
            embedding_model
        )

        if not self.documents:

            self.matrix = None

            return

        texts = [
            document["content"]
            for document
            in self.documents
        ]

        self.matrix = (
            embedding_model.fit(
                texts
            )
        )

    def search(
        self,
        query,
        top_k=5,
        min_score=0.10
    ):

        if (
            self.matrix is None
            or not self.documents
        ):

            return []

        query_vector = (
            self.embedding_model
            .transform(
                [query]
            )
        )

        similarities = (
            cosine_similarity(
                query_vector,
                self.matrix
            )[0]
        )

        indices = similarities.argsort()[
            ::-1
        ]

        results = []

        for index in indices:

            score = float(
                similarities[index]
            )

            if score < min_score:

                continue

            document = dict(
                self.documents[index]
            )

            document["score"] = score

            results.append(
                document
            )

            if len(results) >= top_k:

                break

        return results

    def save(self, path):

        with open(
            path,
            "wb"
        ) as file:

            pickle.dump(
                self,
                file
            )

    @staticmethod
    def load(path):

        with open(
            path,
            "rb"
        ) as file:

            return pickle.load(
                file
            )