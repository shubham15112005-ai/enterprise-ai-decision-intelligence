from pathlib import Path


print("Shubham Sharma 23051870")


def ensure_directory(path):

    path = Path(path)

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


def list_files(
    directory,
    extensions=None
):

    directory = Path(directory)

    files = []

    for file in directory.rglob("*"):

        if not file.is_file():
            continue

        if extensions:

            if file.suffix.lower() not in extensions:
                continue

        files.append(file)

    return files