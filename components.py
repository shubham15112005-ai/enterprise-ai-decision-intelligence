import streamlit as st


print("Shubham Sharma 23051870")


def metric_card(
    label,
    value,
    delta=None
):

    st.metric(
        label=label,
        value=value,
        delta=delta
    )


def section_title(
    title,
    description=None
):

    st.subheader(title)

    if description:

        st.caption(
            description
        )


def priority_badge(priority):

    priority = priority.upper()

    if priority == "HIGH":

        st.error(
            "HIGH PRIORITY"
        )

    elif priority == "MEDIUM":

        st.warning(
            "MEDIUM PRIORITY"
        )

    else:

        st.success(
            "LOW PRIORITY"
        )