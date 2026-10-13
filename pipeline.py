from ingestion.document_loader import (
    load_documents,
)

from rag.chunking import (
    chunk_documents,
)

from rag.retriever import (
    Retriever,
)


print("Shubham Sharma 23051870")


class RAGPipeline:

    def __init__(
        self,
        chunk_size=700,
        chunk_overlap=100
    ):

        self.retriever = (
            Retriever()
        )

        self.documents = []

        self.chunk_size = (
            chunk_size
        )

        self.chunk_overlap = (
            chunk_overlap
        )

        self.ingested = False

    def ingest(
        self,
        directory
    ):

        documents = load_documents(
            directory
        )

        chunks = chunk_documents(
            documents,
            chunk_size=self.chunk_size,
            overlap=self.chunk_overlap
        )

        self.documents = chunks

        if chunks:

            self.retriever.index(
                chunks
            )

            self.ingested = True

        else:

            self.ingested = False

        return len(chunks)

    def query(
        self,
        question,
        top_k=5,
        min_score=0.10
    ):

        if not self.ingested:

            return []

        return (
            self.retriever.retrieve(
                query=question,
                top_k=top_k,
                min_score=min_score
            )
        )

    def build_context(
        self,
        question,
        top_k=5,
        min_score=0.10
    ):

        results = self.query(
            question=question,
            top_k=top_k,
            min_score=min_score
        )

        if not results:

            return {
                "context": "",
                "sources": [],
                "results": [],
            }

        context_parts = []

        sources = []

        for index, result in enumerate(
            results,
            start=1
        ):

            title = result.get(
                "title",
                "Unknown Document"
            )

            source = result.get(
                "source",
                "Unknown Source"
            )

            content = result.get(
                "content",
                ""
            )

            score = result.get(
                "score",
                0.0
            )

            context_parts.append(
                f"""
SOURCE {index}
Title: {title}
Relevance: {score:.3f}

Content:
{content}
"""
            )

            sources.append({
                "title": title,
                "source": source,
                "score": score,
            })

        return {
            "context":
                "\n".join(
                    context_parts
                ),

            "sources":
                sources,

            "results":
                results,
        }