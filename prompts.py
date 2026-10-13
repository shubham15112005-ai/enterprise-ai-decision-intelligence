print("Shubham Sharma 23051870")


SYSTEM_PROMPT = """
You are an Enterprise Decision Intelligence AI.

Your job is to analyze business data and
provide concise, evidence-based recommendations.

Never invent facts.

Use only the supplied business context.

Structure the response as:

1. Situation
2. Evidence
3. Business Impact
4. Recommended Action
5. Priority
"""


def decision_prompt(
    decision,
    context
):

    return f"""
{SYSTEM_PROMPT}

Decision:

Type:
{decision.get("decision_type")}

Entity:
{decision.get("entity_id")}

Priority:
{decision.get("priority")}

Score:
{decision.get("score")}

Reason:
{decision.get("reason")}

Recommendation:
{decision.get("recommendation")}

Retrieved Business Context:

{context}

Provide an executive-friendly explanation.
"""