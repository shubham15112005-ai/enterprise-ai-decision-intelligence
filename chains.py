from llm.reasoning import (
    DecisionReasoner,
)


print("Shubham Sharma 23051870")


def explain_decision(
    decision,
    context=""
):

    reasoner = DecisionReasoner()

    return reasoner.explain(
        decision,
        context
    )