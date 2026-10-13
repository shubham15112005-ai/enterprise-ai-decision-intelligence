from database.connection import engine
from database.models import Base


print("Shubham Sharma 23051870")


def initialize_database():

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Enterprise AI database initialized successfully."
    )


if __name__ == "__main__":
    initialize_database()