import logging

from typing import Any, Dict, Optional

import pandas as pd

from analytics.metrics import (
    calculate_kpis,
    calculate_customer_metrics,
    calculate_product_metrics,
)

from decision_engine.query_router import (
    route_query,
)

from decision_engine.insight_generator import (
    generate_customer_insights,
    generate_product_insights,
)

from llm.reasoning import (
    DecisionReasoner,
)

from rag.pipeline import (
    RAGPipeline,
)
from utils.logger import get_logger
print("Shubham Sharma 23051870")
logger = logging.getLogger(__name__)


class DecisionOrchestrator:
    """
    Central orchestration layer for the Enterprise AI
    Decision Intelligence platform.

    Responsibilities:

    1. Receive a natural-language business question.
    2. Route the question.
    3. Calculate quantitative business analytics.
    4. Generate deterministic business insights.
    5. Retrieve relevant enterprise knowledge through RAG.
    6. Combine all evidence into a unified context.
    7. Invoke the LLM reasoning layer when available.
    8. Provide a deterministic fallback when the LLM
       is unavailable.

    The orchestrator contains business workflow logic,
    while Streamlit remains responsible only for UI.
    """

    def __init__(
        self,
        rag_pipeline: Optional[RAGPipeline] = None,
        reasoner: Optional[DecisionReasoner] = None,
    ):
        """
        Initialize the decision orchestrator.

        Dependencies can be injected for testing.

        Parameters
        ----------
        rag_pipeline:
            Optional RAGPipeline instance.

        reasoner:
            Optional DecisionReasoner instance.
        """

        self.rag_pipeline = rag_pipeline
        self.reasoner = reasoner

    # =========================================================
    # PUBLIC API
    # =========================================================

    def analyze(
        self,
        question: str,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Analyze a business question using analytics,
        decision intelligence, RAG and LLM reasoning.

        Returns a structured response rather than a
        presentation-specific string.
        """
        logger.info(
        "Starting decision analysis | question=%r | rows=%d",
        question,
        len(df),
    )

        if not isinstance(question, str):
            raise TypeError(
                "Question must be a string."
            )

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                "df must be a pandas DataFrame."
            )

        if df.empty:
            return self._empty_data_response(
                question
            )

        # -----------------------------------------------------
        # 1. QUERY ROUTING
        # -----------------------------------------------------

        route = route_query(
            question
        )
        logger.info(
            "Query routed | route=%s | confidence=%.3f",
            route.get("route"),
            route.get("confidence", 0.0),
        )

        # -----------------------------------------------------
        # 2. QUANTITATIVE ANALYTICS
        # -----------------------------------------------------

        kpis = calculate_kpis(
            df
        )

        customer_metrics = (
            calculate_customer_metrics(
                df
            )
        )

        product_metrics = (
            calculate_product_metrics(
                df
            )
        )

        # -----------------------------------------------------
        # 3. DETERMINISTIC DECISION ENGINE
        # -----------------------------------------------------

        customer_insights = (
            generate_customer_insights(
                customer_metrics
            )
        )

        product_insights = (
            generate_product_insights(
                df
            )
        )
        logger.info(
            "Analytics completed | customer_insights=%d | product_insights=%d",
            len(customer_insights),
            len(product_insights),
        )

        all_insights = (
            customer_insights
            +
            product_insights
        )

        # -----------------------------------------------------
        # 4. RAG
        # -----------------------------------------------------

        rag_result = self._retrieve_knowledge(
            question
        )
        logger.info(
            "Knowledge retrieval completed | results=%d",
            len(rag_result.get("results", [])),
        )

        # -----------------------------------------------------
        # 5. BUILD UNIFIED EVIDENCE CONTEXT
        # -----------------------------------------------------

        context = self._build_business_context(
            question=question,
            route=route,
            kpis=kpis,
            customer_insights=customer_insights,
            product_insights=product_insights,
            rag_context=rag_result["context"],
        )

        # -----------------------------------------------------
        # 6. LLM REASONING
        # -----------------------------------------------------

        answer = None
        llm_used = False

        if self.reasoner is not None:

            try:

                decision = self._select_primary_decision(
                    route=route,
                    insights=all_insights,
                )

                if decision is not None:

                    answer = self.reasoner.explain(
                        decision,
                        context
                    )

                else:

                    answer = self.reasoner.explain(
                        {
                            "decision_type": (
                                "BUSINESS_ANALYSIS"
                            ),
                            "entity_type": "BUSINESS",
                            "entity_id": "ENTERPRISE",
                            "priority": "INFO",
                            "score": 0,
                            "reason": (
                                "General business "
                                "analysis request."
                            ),
                            "recommendation": (
                                "Use the supplied "
                                "business evidence "
                                "to answer the question."
                            ),
                        },
                        context
                    )

                if answer:
                    llm_used = bool(
                        getattr(
                            self.reasoner,
                                "last_used_llm",
                                False,
                        )
                    )
                    logger.info(
                        "Reasoning completed | llm_used=%s",
                        llm_used,
                    )

            except Exception:
                answer = None
                llm_used = False

                logger.exception(
                    "LLM reasoning failed; "
                    "using deterministic fallback."
                )

        # -----------------------------------------------------
        # 7. DETERMINISTIC FALLBACK
        # -----------------------------------------------------

        if not answer:

            answer = self._deterministic_answer(
                question=question,
                route=route,
                kpis=kpis,
                customer_insights=customer_insights,
                product_insights=product_insights,
                rag_result=rag_result,
            )
        logger.info(
            "Decision analysis completed | route=%s | "
            "insights=%d",
            route.get("route"),
            len(all_insights),
        )

        # -----------------------------------------------------
        # 8. STRUCTURED RESPONSE
        # -----------------------------------------------------

        return {
            "question": question,

            "route": route,

            "kpis": kpis,

            "customer_insights":
                customer_insights,

            "product_insights":
                product_insights,

            "insights":
                all_insights,

            "rag": {
                "context":
                    rag_result["context"],

                "sources":
                    rag_result["sources"],

                "results":
                    rag_result["results"],
            },

            "answer":
                answer,

            "llm_used":
                llm_used,

            "evidence_available":
                self._evidence_available(
                    kpis=kpis,
                    insights=all_insights,
                    rag_result=rag_result,
                ),
        }

    # =========================================================
    # RAG
    # =========================================================

    def _retrieve_knowledge(
        self,
        question: str,
    ) -> Dict[str, Any]:

        empty_result = {
            "context": "",
            "sources": [],
            "results": [],
        }

        if self.rag_pipeline is None:
            return empty_result

        try:

            return self.rag_pipeline.build_context(
                question=question,
                top_k=5,
                min_score=0.10,
            )

        except Exception:
                
            logger.exception(
                "RAG retrieval failed; "
                "continuing without retrieved knowledge."
            )
            return empty_result

    # =========================================================
    # CONTEXT BUILDING
    # =========================================================

    def _build_business_context(
        self,
        question: str,
        route: Dict[str, Any],
        kpis: Dict[str, Any],
        customer_insights,
        product_insights,
        rag_context: str,
    ) -> str:

        context_parts = []

        context_parts.append(
            "ENTERPRISE BUSINESS CONTEXT"
        )

        context_parts.append(
            f"""
Total Revenue:
₹{kpis["revenue"]:,.2f}

Total Profit:
₹{kpis["profit"]:,.2f}

Transactions:
{kpis["transactions"]:,}

Average Order Value:
₹{kpis["average_order_value"]:,.2f}

Profit Margin:
{kpis["profit_margin"]:.2%}

Detected Query Route:
{route["route"]}

Query Confidence:
{route["confidence"]:.2%}

User Question:
{question}
"""
        )

        # -----------------------------------------------------
        # Customer risks
        # -----------------------------------------------------

        high_risk_customers = [
            insight
            for insight
            in customer_insights
            if insight.get("priority")
            == "HIGH"
        ]

        if high_risk_customers:

            customer_context = [
                "HIGH PRIORITY CUSTOMER RISKS"
            ]

            for insight in (
                high_risk_customers[:5]
            ):

                customer_context.append(
                    f"""
Customer:
{insight["entity_name"]}

Risk Score:
{insight["score"]:.0f}/100

Reason:
{insight["reason"]}

Recommendation:
{insight["recommendation"]}
"""
                )

            context_parts.append(
                "\n".join(
                    customer_context
                )
            )

        # -----------------------------------------------------
        # Product opportunities
        # -----------------------------------------------------

        if product_insights:

            product_context = [
                "PRODUCT OPPORTUNITIES"
            ]

            for insight in (
                product_insights[:5]
            ):

                product_context.append(
                    f"""
Product:
{insight["entity_name"]}

Opportunity Score:
{insight["score"]:.0f}/100

Reason:
{insight["reason"]}

Recommendation:
{insight["recommendation"]}
"""
                )

            context_parts.append(
                "\n".join(
                    product_context
                )
            )

        # -----------------------------------------------------
        # Enterprise knowledge
        # -----------------------------------------------------

        if rag_context:

            context_parts.append(
                "ENTERPRISE KNOWLEDGE "
                "RETRIEVED FROM DOCUMENTS\n"
                + rag_context
            )

        return "\n\n".join(
            context_parts
        )

    # =========================================================
    # PRIMARY DECISION
    # =========================================================

    def _select_primary_decision(
        self,
        route: Dict[str, Any],
        insights,
    ) -> Optional[Dict[str, Any]]:

        if not insights:
            return None

        route_name = route.get(
            "route",
            "general"
        )

        # -----------------------------------------------------
        # Prefer decisions matching the query route.
        # -----------------------------------------------------

        if route_name in {
            "customer",
            "risk",
        }:

            customer_decisions = [
                insight
                for insight
                in insights
                if insight.get(
                    "decision_type"
                )
                == "CUSTOMER_RISK"
            ]

            if customer_decisions:

                return max(
                    customer_decisions,
                    key=lambda item:
                        item.get(
                            "score",
                            0
                        )
                )

        if route_name == "product":

            product_decisions = [
                insight
                for insight
                in insights
                if insight.get(
                    "decision_type"
                )
                == "PRODUCT_OPPORTUNITY"
            ]

            if product_decisions:

                return max(
                    product_decisions,
                    key=lambda item:
                        item.get(
                            "score",
                            0
                        )
                )

        # -----------------------------------------------------
        # Otherwise select highest scoring insight.
        # -----------------------------------------------------

        return max(
            insights,
            key=lambda item:
                item.get(
                    "score",
                    0
                )
        )

    # =========================================================
    # FALLBACK ANSWER
    # =========================================================

    def _deterministic_answer(
        self,
        question: str,
        route: Dict[str, Any],
        kpis: Dict[str, Any],
        customer_insights,
        product_insights,
        rag_result,
    ) -> str:

        question_lower = (
            question.lower()
        )

        # -----------------------------------------------------
        # Revenue
        # -----------------------------------------------------

        if "revenue" in question_lower:

            return (
                f"Total revenue is "
                f"₹{kpis['revenue']:,.2f} "
                f"across "
                f"{kpis['transactions']:,} "
                f"transactions."
            )

        # -----------------------------------------------------
        # Profit
        # -----------------------------------------------------

        if (
            "profit" in question_lower
            or
            "margin" in question_lower
        ):

            return (
                f"Total profit is "
                f"₹{kpis['profit']:,.2f}, "
                f"with an overall profit "
                f"margin of "
                f"{kpis['profit_margin']:.2%}."
            )

        # -----------------------------------------------------
        # Customer risk
        # -----------------------------------------------------

        if (
            "customer" in question_lower
            or
            "risk" in question_lower
        ):

            high_risk = [
                insight
                for insight
                in customer_insights
                if insight.get(
                    "priority"
                )
                == "HIGH"
            ]

            if not high_risk:

                return (
                    "The decision engine did not "
                    "identify any high-priority "
                    "customer risks."
                )

            response = (
                "The decision engine identified "
                f"{len(high_risk)} "
                "high-priority customer risk(s)."
                "\n\n"
            )

            for insight in high_risk[:5]:

                response += (
                    f"• {insight['entity_name']} — "
                    f"Risk score "
                    f"{insight['score']:.0f}/100\n"
                    f"  {insight['reason']}\n"
                    f"  Action: "
                    f"{insight['recommendation']}\n\n"
                )

            return response

        # -----------------------------------------------------
        # Product opportunities
        # -----------------------------------------------------

        if (
            "product" in question_lower
            or
            "opportun" in question_lower
        ):

            if not product_insights:

                return (
                    "No significant product "
                    "opportunities were detected."
                )

            response = (
                "The decision engine identified "
                f"{len(product_insights)} "
                "product opportunit(ies)."
                "\n\n"
            )

            for insight in product_insights[:5]:

                response += (
                    f"• {insight['entity_name']} — "
                    f"Score "
                    f"{insight['score']:.0f}/100\n"
                    f"  {insight['recommendation']}\n\n"
                )

            return response

        # -----------------------------------------------------
        # RAG answer
        # -----------------------------------------------------

        if rag_result["results"]:

            response = (
                "I found relevant information "
                "in the enterprise knowledge base:"
                "\n\n"
            )

            for result in (
                rag_result["results"][:3]
            ):

                response += (
                    f"**{result.get('title', 'Unknown')}**\n"
                    f"{result.get('content', '')}\n\n"
                )

            return response

        # -----------------------------------------------------
        # General
        # -----------------------------------------------------

        return (
            "The decision intelligence platform "
            "could not identify a specific "
            "deterministic answer from the "
            "available evidence. "
            "The detected query route is "
            f"'{route.get('route', 'general')}'."
        )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _evidence_available(
        kpis,
        insights,
        rag_result,
    ) -> bool:

        return bool(
            kpis
            or
            insights
            or
            rag_result.get("results")
        )

    @staticmethod
    def _empty_data_response(
        question: str,
    ) -> Dict[str, Any]:

        return {
            "question": question,

            "route": {
                "route": "general",
                "confidence": 0.0,
                "matched_terms": [],
            },

            "kpis": {},

            "customer_insights": [],

            "product_insights": [],

            "insights": [],

            "rag": {
                "context": "",
                "sources": [],
                "results": [],
            },

            "answer": (
                "No business data is currently "
                "available."
            ),

            "llm_used": False,

            "evidence_available": False,
        }