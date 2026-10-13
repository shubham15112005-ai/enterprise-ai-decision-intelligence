import plotly.express as px


print("Shubham Sharma 23051870")


def region_chart(df):

    return px.bar(
        df,
        x="region",
        y="revenue",
        title="Revenue by Region",
        text_auto=".2s",
    )


def category_chart(df):

    return px.bar(
        df,
        x="category",
        y="revenue",
        title="Revenue by Category",
        text_auto=".2s",
    )


def monthly_chart(df):

    return px.line(
        df,
        x="month",
        y="revenue",
        title="Revenue Trend",
        markers=True,
    )


def customer_chart(df):

    return px.bar(
        df,
        x="customer_name",
        y="revenue",
        title="Top Customers",
        text_auto=".2s",
    )