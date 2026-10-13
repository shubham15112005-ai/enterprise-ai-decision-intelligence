from pathlib import Path

from pypdf import PdfReader


print("Shubham Sharma 23051870")


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".md",
}


def load_text_file(path):

    path = Path(path)

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def load_pdf_file(path):

    path = Path(path)

    reader = PdfReader(
        str(path)
    )

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def load_document(path):

    path = Path(path)

    extension = path.suffix.lower()

    if extension in {
        ".txt",
        ".md"
    }:

        return load_text_file(
            path
        )

    if extension == ".pdf":

        return load_pdf_file(
            path
        )

    raise ValueError(
        f"Unsupported document type: {extension}"
    )


def load_documents(directory):

    directory = Path(
        directory
    )

    documents = []

    if not directory.exists():

        return documents

    for path in directory.rglob("*"):

        if (
            path.is_file()
            and
            path.suffix.lower()
            in SUPPORTED_EXTENSIONS
        ):

            try:

                content = load_document(
                    path
                )

                if not content.strip():

                    continue

                documents.append({

                    "title":
                        path.stem,

                    "source":
                        str(path),

                    "content":
                        content,

                    "document_type":
                        path.suffix.lower(),

                })

            except Exception as error:

                print(
                    f"Could not load "
                    f"{path}: {error}"
                )

    return documents