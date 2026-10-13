import pandas as pd

from database.connection import engine


print("Shubham Sharma 23051870")


def execute_query(query):

    with engine.connect() as connection:

        return pd.read_sql(
            query,
            connection
        )


def get_sales_dataframe():

    query = """
    SELECT
        transaction_date,
        customer_id,
        customer_name,
        product_id,
        product_name,
        category,
        region,
        quantity,
        unit_price,
        revenue,
        cost,
        profit
    FROM sales_transactions
    """

    return execute_query(query)


def get_top_customers(limit=10):

    query = f"""
    SELECT
        customer_id,
        customer_name,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit,
        COUNT(*) AS transactions
    FROM sales_transactions
    GROUP BY customer_id, customer_name
    ORDER BY revenue DESC
    LIMIT {int(limit)}
    """

    return execute_query(query)


def get_region_performance():

    query = """
    SELECT
        region,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY region
    ORDER BY revenue DESC
    """

    return execute_query(query)