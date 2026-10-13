from typing import List


print("Shubham Sharma 23051870")


def chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 100
) -> List[str]:

    if not text:
        return []

    text = " ".join(
        text.split()
    )

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def chunk_documents(
    documents,
    chunk_size=700,
    overlap=100
):

    result = []

    for document in documents:

        chunks = chunk_text(
            document["content"],
            chunk_size,
            overlap
        )

        for index, chunk in enumerate(chunks):

            result.append({
                "title": document["title"],
                "source": document["source"],
                "chunk_id": index,
                "content": chunk,
            })

    return result