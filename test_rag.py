from rag.chunking import (
    chunk_text,
    chunk_documents,
)

from rag.embeddings import (
    TfidfEmbeddingModel,
)

from rag.retriever import (
    Retriever,
)


print("Shubham Sharma 23051870")


def test_chunk_text():

    text = (
        "Enterprise decision intelligence "
        "helps organizations analyze business "
        "data and make evidence-based decisions."
        * 20
    )

    chunks = chunk_text(
        text,
        chunk_size=100,
        overlap=20,
    )

    assert len(chunks) > 1

    for chunk in chunks:

        assert len(chunk) > 0


def test_chunk_documents():

    documents = [
        {
            "title": "Business Policy",
            "source": "policy.txt",
            "content": (
                "Customer retention is important "
                "for enterprise growth."
            ),
        }
    ]

    chunks = chunk_documents(
        documents
    )

    assert len(chunks) >= 1

    assert (
        chunks[0]["title"]
        == "Business Policy"
    )


def test_tfidf_embeddings():

    model = TfidfEmbeddingModel()

    matrix = model.fit([
        "customer revenue growth",
        "product profitability",
    ])

    assert matrix.shape[0] == 2


def test_retriever():

    documents = [
        {
            "title": "Sales",
            "source": "sales.txt",
            "chunk_id": 0,
            "content": (
                "Revenue increased significantly "
                "during the quarter."
            ),
        },

        {
            "title": "Security",
            "source": "security.txt",
            "chunk_id": 0,
            "content": (
                "Security policies require "
                "regular audits."
            ),
        },
    ]

    retriever = Retriever()

    retriever.index(
        documents
    )

    results = retriever.retrieve(
        "revenue growth",
        top_k=1,
    )

    assert len(results) == 1

    assert results[0]["title"] == "Sales"