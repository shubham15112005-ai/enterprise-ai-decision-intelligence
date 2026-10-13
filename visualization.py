import plotly.express as px


print("Shubham Sharma 23051870")


def revenue_by_region_chart(df):

    return px.bar(
        df,
        x="region",
        y="revenue",
        title="Revenue by Region",
        text_auto=".2s",
    )


def revenue_by_category_chart(df):

    return px.bar(
        df,
        x="category",
        y="revenue",
        title="Revenue by Category",
        text_auto=".2s",
    )


def monthly_revenue_chart(df):

    return px.line(
        df,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend",
    )


def customer_revenue_chart(df):

    return px.bar(
        df,
        x="customer_name",
        y="revenue",
        title="Customer Revenue",
        text_auto=".2s",
    )