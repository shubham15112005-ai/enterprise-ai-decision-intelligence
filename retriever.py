from rag.embeddings import (
    TfidfEmbeddingModel,
)

from rag.vector_store import (
    VectorStore,
)


print("Shubham Sharma 23051870")


class Retriever:

    def __init__(self):

        self.embedding_model = (
            TfidfEmbeddingModel()
        )

        self.vector_store = (
            VectorStore()
        )

    def index(
        self,
        documents
    ):

        self.vector_store.build(
            documents,
            self.embedding_model
        )

    def retrieve(
        self,
        query,
        top_k=5,
        min_score=0.10
    ):

        return (
            self.vector_store.search(
                query=query,
                top_k=top_k,
                min_score=min_score
            )
        )