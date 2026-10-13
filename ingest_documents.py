from config.settings import (
    DOCUMENTS_DIR,
)

from ingestion.document_loader import (
    load_documents,
)

from ingestion.pipeline import (
    ingest_documents,
)


print("Shubham Sharma 23051870")


def main():

    documents = load_documents(
        DOCUMENTS_DIR
    )

    if not documents:

        print(
            "No documents found."
        )

        print(
            f"Place PDF/TXT/MD files inside: "
            f"{DOCUMENTS_DIR}"
        )

        return

    count = ingest_documents(
        documents
    )

    print(
        f"Ingested {count} documents."
    )


if __name__ == "__main__":
    main()