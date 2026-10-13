import streamlit as st
import pandas as pd

from analytics.sql_engine import (
    get_sales_dataframe,
    get_top_customers,
)

from analytics.metrics import (
    calculate_kpis,
    calculate_customer_metrics,
)

from analytics.statistics import (
    monthly_revenue,
)

from decision_engine.insight_generator import (
    generate_customer_insights,
    generate_product_insights,
)

from ui.charts import (
    region_chart,
    category_chart,
    monthly_chart,
    customer_chart,
)

from ui.components import (
    metric_card,
    section_title,
)


print("Shubham Sharma 23051870")


def render_priority_badge(priority):

    if priority == "HIGH":
        return "🔴 HIGH"

    if priority == "MEDIUM":
        return "🟡 MEDIUM"

    return "🟢 LOW"


def render_dashboard():

    st.title(
        "Enterprise AI Decision Intelligence"
    )

    st.caption(
        "AI-powered business analytics, "
        "risk detection and decision support"
    )

    # =====================================================
    # LOAD DATA
    # =====================================================

    df = get_sales_dataframe()

    if df.empty:

        st.warning(
            "No business data available."
        )

        return

    # =====================================================
    # KPI CALCULATION
    # =====================================================

    kpis = calculate_kpis(
        df
    )

    # =====================================================
    # KPI ROW
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        metric_card(
            "Total Revenue",
            f"₹{kpis['revenue']:,.0f}"
        )

    with col2:

        metric_card(
            "Total Profit",
            f"₹{kpis['profit']:,.0f}"
        )

    with col3:

        metric_card(
            "Transactions",
            f"{kpis['transactions']:,}"
        )

    with col4:

        metric_card(
            "Profit Margin",
            f"{kpis['profit_margin']:.1%}"
        )

    st.divider()

    # =====================================================
    # REVENUE INTELLIGENCE
    # =====================================================

    section_title(
        "Revenue Intelligence",
        "Historical business performance"
    )

    monthly = monthly_revenue(
        df
    )

    if not monthly.empty:

        st.plotly_chart(
            monthly_chart(monthly),
            use_container_width=True
        )

    # =====================================================
    # REGIONAL / CATEGORY ANALYTICS
    # =====================================================

    col1, col2 = st.columns(2)

    region_data = (
        df.groupby("region")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum")
        )
        .reset_index()
    )

    category_data = (
        df.groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum")
        )
        .reset_index()
    )

    with col1:

        st.plotly_chart(
            region_chart(region_data),
            use_container_width=True
        )

    with col2:

        st.plotly_chart(
            category_chart(category_data),
            use_container_width=True
        )

    # =====================================================
    # CUSTOMER INTELLIGENCE
    # =====================================================

    section_title(
        "Customer Intelligence",
        "Customer revenue, profitability and engagement"
    )

    customers = get_top_customers(
        10
    )

    if not customers.empty:

        st.plotly_chart(
            customer_chart(
                customers
            ),
            use_container_width=True
        )

        st.dataframe(
            customers,
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # DECISION INTELLIGENCE
    # =====================================================

    st.divider()

    section_title(
        "AI Decision Intelligence",
        "Evidence-based business risks and opportunities"
    )

    # -----------------------------------------------------
    # Customer metrics
    # -----------------------------------------------------

    customer_metrics = (
        calculate_customer_metrics(
            df
        )
    )

    # -----------------------------------------------------
    # Generate customer insights
    # -----------------------------------------------------

    customer_insights = (
        generate_customer_insights(
            customer_metrics
        )
    )

    # -----------------------------------------------------
    # Generate product insights
    # -----------------------------------------------------

    product_insights = (
        generate_product_insights(
            df
        )
    )

    # Combine all insights
    all_insights = (
        customer_insights
        +
        product_insights
    )

    # =====================================================
    # DECISION SUMMARY
    # =====================================================

    high_priority = sum(
        1
        for insight in all_insights
        if insight["priority"] == "HIGH"
    )

    medium_priority = sum(
        1
        for insight in all_insights
        if insight["priority"] == "MEDIUM"
    )

    opportunity_count = sum(
        1
        for insight in all_insights
        if insight["decision_type"]
        == "PRODUCT_OPPORTUNITY"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        metric_card(
            "Insights Detected",
            f"{len(all_insights):,}"
        )

    with col2:

        metric_card(
            "High Priority",
            f"{high_priority:,}"
        )

    with col3:

        metric_card(
            "Medium Priority",
            f"{medium_priority:,}"
        )

    with col4:

        metric_card(
            "Opportunities",
            f"{opportunity_count:,}"
        )

    st.divider()

    # =====================================================
    # INSIGHT TABLE
    # =====================================================

    if not all_insights:

        st.success(
            "No significant business risks or "
            "opportunities were detected."
        )

        return

    decision_rows = []

    for insight in all_insights:

        decision_rows.append({

            "Priority":
                render_priority_badge(
                    insight["priority"]
                ),

            "Decision Type":
                insight["decision_type"],

            "Entity":
                insight["entity_name"],

            "Score":
                insight["score"],

            "Reason":
                insight["reason"],

            "Recommendation":
                insight["recommendation"],
        })

    decisions_df = pd.DataFrame(
        decision_rows
    )

    st.dataframe(
        decisions_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.NumberColumn(
                "Score",
                format="%.0f"
            )
        }
    )

    # =====================================================
    # DETAILED BUSINESS INSIGHTS
    # =====================================================

    st.subheader(
        "Detailed Business Insights"
    )

    st.caption(
        "Every recommendation is backed by measurable "
        "business evidence."
    )

    # Show highest priority insights first
    sorted_insights = sorted(
        all_insights,
        key=lambda x: x["score"],
        reverse=True
    )

    # Limit initial dashboard display
    for index, insight in enumerate(
        sorted_insights[:10],
        start=1
    ):

        priority = insight[
            "priority"
        ]

        entity_name = insight[
            "entity_name"
        ]

        title = (
            f"{render_priority_badge(priority)} "
            f"  {entity_name}"
        )

        with st.expander(
            title,
            expanded=(index == 1)
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    "**Decision Type**"
                )

                st.write(
                    insight[
                        "decision_type"
                    ]
                )

            with col2:

                st.markdown(
                    "**Decision Score**"
                )

                st.write(
                    f"{insight['score']:.0f}/100"
                )

            st.markdown(
                "**Why was this detected?**"
            )

            st.write(
                insight["reason"]
            )

            st.markdown(
                "**Supporting Evidence**"
            )

            evidence = insight.get(
                "evidence",
                []
            )

            if evidence:

                evidence_rows = []

                for item in evidence:

                    evidence_rows.append({

                        "Metric":
                            item.get(
                                "metric",
                                "N/A"
                            ),

                        "Value":
                            item.get(
                                "value",
                                "N/A"
                            ),

                        "Interpretation":
                            item.get(
                                "interpretation",
                                ""
                            ),

                        "Source":
                            item.get(
                                "source",
                                "Analytics"
                            ),
                    })

                st.dataframe(
                    pd.DataFrame(
                        evidence_rows
                    ),
                    use_container_width=True,
                    hide_index=True
                )

            st.markdown(
                "**Recommended Action**"
            )

            st.info(
                insight[
                    "recommendation"
                ]
            )