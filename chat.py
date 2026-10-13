import streamlit as st

from services.decision_service import DecisionService


print("Shubham Sharma 23051870")


# =========================================================
# DECISION SERVICE
# =========================================================

@st.cache_resource
def get_decision_service():
    """
    Create and cache the application decision service.

    Streamlit keeps one service instance available across
    reruns so the RAG pipeline and other dependencies do not
    need to be rebuilt for every user question.
    """

    return DecisionService()


# =========================================================
# BUSINESS QUESTION ANSWER
# =========================================================

def business_question_answer(question: str) -> str:
    """
    Send a business question to the application service
    and convert the structured result into UI-friendly text.
    """

    service = get_decision_service()

    result = service.answer(question)

    answer = result.get(
        "answer",
        "No answer was generated."
    )

    if not isinstance(answer, str):
        answer = str(answer)

    # -----------------------------------------------------
    # Sources
    # -----------------------------------------------------

    rag = result.get("rag", {})

    sources = rag.get(
        "sources",
        []
    )

    if sources and "### Sources" not in answer:

        answer += "\n\n### Sources\n"

        for source in sources:

            title = source.get(
                "title",
                "Unknown document"
            )

            score = source.get(
                "score",
                0
            )

            answer += (
                f"- {title} "
                f"(relevance: {score:.2f})\n"
            )

    return answer


# =========================================================
# RESULT METADATA
# =========================================================

def render_result_metadata(result):
    """
    Display metadata from the structured DecisionResponse.
    """

    route = result.route

    st.caption(
        f"Query route: `{route.route}` "
        f"| Confidence: `{route.confidence:.0%}`"
    )

    if isinstance(route, dict):

        route_name = route.get(
            "route",
            "UNKNOWN"
        )

        confidence = route.get(
            "confidence"
        )

        if confidence is not None:

            st.caption(
                f"Query route: `{route_name}` "
                f"| Confidence: `{confidence:.0%}`"
            )

        else:

            st.caption(
                f"Query route: `{route_name}`"
            )


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

EXAMPLE_QUESTIONS = [

    "What is our total revenue?",

    "What is our profit margin?",

    "Which customers are at risk?",

    "What product opportunities do we have?",

    "What does the customer retention policy recommend?",

    "What should we do about high-risk customers?",
]


# =========================================================
# STREAMLIT CHAT UI
# =========================================================

def render_chat():

    st.subheader(
        "AI Decision Assistant"
    )

    st.caption(
        "Ask questions about business performance, "
        "customer risk, opportunities and enterprise "
        "knowledge."
    )

    # =====================================================
    # EXAMPLE QUESTIONS
    # =====================================================

    st.markdown(
        "**Try asking:**"
    )

    for index, example in enumerate(
        EXAMPLE_QUESTIONS
    ):

        if st.button(
            example,
            key=f"example_question_{index}"
        ):

            with st.chat_message(
                "user"
            ):

                st.write(
                    example
                )

            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "Analyzing business data "
                    "and enterprise knowledge..."
                ):

                    service = (
                        get_decision_service()
                    )

                    result = (
                        service.answer_response(
                            example
                        )
                    )

                    answer = result.answer

                st.markdown(
                    str(answer)
                )

                render_result_metadata(
                    result
                )

    # =====================================================
    # CHAT INPUT
    # =====================================================

    question = st.chat_input(
        "Ask a business question..."
    )

    if question:

        with st.chat_message(
            "user"
        ):

            st.write(
                question
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Analyzing business data "
                "and enterprise knowledge..."
            ):

                service = (
                    get_decision_service()
                )

                result = (
                    service.answer_response(
                        question
                    )
                )

                answer = result.answer

            st.markdown(
                str(answer)
            )

            render_result_metadata(
                result
            )