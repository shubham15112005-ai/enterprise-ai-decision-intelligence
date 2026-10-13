import pandas as pd


print("Shubham Sharma 23051870")


def validate_dataframe(df):

    if not isinstance(
        df,
        pd.DataFrame
    ):

        raise TypeError(
            "Expected pandas DataFrame."
        )

    if df.empty:

        raise ValueError(
            "DataFrame cannot be empty."
        )

    return True


def validate_positive(
    value,
    field_name
):

    if value < 0:

        raise ValueError(
            f"{field_name} cannot be negative."
        )

    return True