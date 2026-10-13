from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import pandas as pd

from analytics.sql_engine import get_sales_dataframe

from decision_engine.orchestrator import DecisionOrchestrator

from llm.reasoning import DecisionReasoner

from rag.pipeline import RAGPipeline

from models.response import (
    DecisionResponse,
    EvidenceItem,
    RecommendationItem,
    RouteMetadata,
    SourceItem,
)


print("Shubham Sharma 23051870")


class DecisionService:
    """
    Application service for Enterprise AI Decision Intelligence.

    Responsibilities:
    - Load business data
    - Initialize the decision orchestrator
    - Execute business questions
    - Provide backward-compatible dictionary responses
    - Provide strongly typed DecisionResponse objects
    - Keep UI/API code independent from internal analytics,
      decision-engine, RAG and LLM implementation details
    """

    def __init__(
        self,
        dataframe: Optional[pd.DataFrame] = None,
        orchestrator: Optional[DecisionOrchestrator] = None,
        rag_pipeline: Optional[RAGPipeline] = None,
        reasoner: Optional[DecisionReasoner] = None,
    ) -> None:

        self._dataframe = dataframe

        if orchestrator is not None:

            self.orchestrator = orchestrator

        else:

            self.orchestrator = self._build_orchestrator(
                rag_pipeline=rag_pipeline,
                reasoner=reasoner,
            )

    # =====================================================
    # ORCHESTRATOR
    # =====================================================

    def _build_orchestrator(
        self,
        rag_pipeline: Optional[RAGPipeline] = None,
        reasoner: Optional[DecisionReasoner] = None,
    ) -> DecisionOrchestrator:

        if rag_pipeline is None:

            rag_pipeline = self._build_rag_pipeline()

        if reasoner is None:

            reasoner = DecisionReasoner()

        return DecisionOrchestrator(
            rag_pipeline=rag_pipeline,
            reasoner=reasoner,
        )

    # =====================================================
    # RAG
    # =====================================================

    @staticmethod
    def _build_rag_pipeline() -> Optional[RAGPipeline]:

        documents_path = (
            Path("data")
            / "documents"
        )

        if not documents_path.exists():

            return None

        try:

            return RAGPipeline(
                documents_path=documents_path
            )

        except TypeError:

            try:

                pipeline = RAGPipeline()

                pipeline.ingest(
                    documents_path
                )

                return pipeline

            except Exception:

                return None

        except Exception:

            return None

    # =====================================================
    # DATA
    # =====================================================

    def get_dataframe(self) -> pd.DataFrame:
        """
        Return the active business DataFrame.
        """

        if self._dataframe is None:

            try:

                self._dataframe = (
                    get_sales_dataframe()
                )

            except Exception:

                self._dataframe = (
                    pd.DataFrame()
                )

        return self._dataframe

    # =====================================================
    # RAW ANSWER
    # =====================================================

    def answer(
        self,
        question: str,
    ) -> dict[str, Any]:
        """
        Execute a business question and return the
        existing dictionary response.

        This method intentionally remains backward-compatible
        with the previous service interface.
        """

        if not isinstance(
            question,
            str,
        ):

            raise TypeError(
                "question must be a string"
            )

        question = question.strip()

        if not question:

            raise ValueError(
                "question cannot be empty"
            )

        dataframe = (
            self.get_dataframe()
        )

        return self.orchestrator.analyze(
            question=question,
            df=dataframe,
        )

    # =====================================================
    # STRUCTURED RESPONSE
    # =====================================================

    def answer_response(
        self,
        question: str,
    ) -> DecisionResponse:
        """
        Execute a business question and return the
        strongly typed DecisionResponse contract.

        This is the preferred interface for new UI,
        API and application-layer integrations.
        """

        raw_result = self.answer(
            question
        )

        return self._build_response(
            question=question,
            result=raw_result,
        )

    # =====================================================
    # RESPONSE MAPPING
    # =====================================================

    @staticmethod
    def _build_response(
        question: str,
        result: dict[str, Any],
    ) -> DecisionResponse:

        route_data = (
            result.get(
                "route",
                {}
            )
        )

        if not isinstance(
            route_data,
            dict,
        ):

            route_data = {
                "route": str(
                    route_data
                ),
                "confidence": 0.0,
            }

        route = RouteMetadata(
            route=str(
                route_data.get(
                    "route",
                    "unknown",
                )
            ),
            confidence=float(
                route_data.get(
                    "confidence",
                    0.0,
                )
            ),
        )

        # -------------------------------------------------
        # Insights
        # -------------------------------------------------

        customer_insights = result.get(
            "customer_insights",
            [],
        )

        product_insights = result.get(
            "product_insights",
            [],
        )

        if not isinstance(
            customer_insights,
            list,
        ):

            customer_insights = []

        if not isinstance(
            product_insights,
            list,
        ):

            product_insights = []

        # -------------------------------------------------
        # Evidence
        # -------------------------------------------------

        evidence_items = []

        for insight in (
            customer_insights
            + product_insights
        ):

            if not isinstance(
                insight,
                dict,
            ):

                continue

            insight_evidence = (
                insight.get(
                    "evidence",
                    [],
                )
            )

            if not isinstance(
                insight_evidence,
                list,
            ):

                continue

            for item in insight_evidence:

                if not isinstance(
                    item,
                    dict,
                ):

                    continue

                evidence_items.append(
                    EvidenceItem(
                        source=str(
                            item.get(
                                "source",
                                "Unknown",
                            )
                        ),
                        metric=item.get(
                            "metric"
                        ),
                        value=item.get(
                            "value"
                        ),
                        interpretation=item.get(
                            "interpretation"
                        ),
                        confidence=item.get(
                            "confidence"
                        ),
                    )
                )

        # -------------------------------------------------
        # Recommendations
        # -------------------------------------------------

        recommendations = []

        for insight in (
            customer_insights
            + product_insights
        ):

            if not isinstance(
                insight,
                dict,
            ):

                continue

            recommendations.append(
                RecommendationItem(
                    decision_type=insight.get(
                        "decision_type"
                    ),
                    entity_type=insight.get(
                        "entity_type"
                    ),
                    entity_id=(
                        str(
                            insight["entity_id"]
                        )
                        if insight.get(
                            "entity_id"
                        )
                        is not None
                        else None
                    ),
                    entity_name=(
                        str(
                            insight["entity_name"]
                        )
                        if insight.get(
                            "entity_name"
                        )
                        is not None
                        else None
                    ),
                    priority=insight.get(
                        "priority"
                    ),
                    score=insight.get(
                        "score"
                    ),
                    reason=insight.get(
                        "reason"
                    ),
                    recommendation=insight.get(
                        "recommendation"
                    ),
                    evidence=insight.get(
                        "evidence",
                        [],
                    ),
                )
            )

        # -------------------------------------------------
        # RAG sources
        # -------------------------------------------------

        rag = result.get(
            "rag",
            {}
        )

        if not isinstance(
            rag,
            dict,
        ):

            rag = {}

        rag_sources = rag.get(
            "sources",
            [],
        )

        if not isinstance(
            rag_sources,
            list,
        ):

            rag_sources = []

        sources = []

        for source in rag_sources:

            if not isinstance(
                source,
                dict,
            ):

                continue

            sources.append(
                SourceItem(
                    title=str(
                        source.get(
                            "title",
                            "Unknown",
                        )
                    ),
                    source=source.get(
                        "source"
                    ),
                    score=float(
                        source.get(
                            "score",
                            0.0,
                        )
                    ),
                )
            )

        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        metadata = {
            "matched_terms": (
                route_data.get(
                    "matched_terms",
                    [],
                )
            ),
            "rag_result_count": len(
                rag.get(
                    "results",
                    [],
                )
            ),
            "customer_insight_count": len(
                customer_insights
            ),
            "product_insight_count": len(
                product_insights
            ),
        }

        return DecisionResponse(
            question=question,

            answer=str(
                result.get(
                    "answer",
                    "No answer was generated.",
                )
            ),

            route=route,

            kpis=result.get(
                "kpis",
                {},
            ),

            customer_insights=(
                customer_insights
            ),

            product_insights=(
                product_insights
            ),

            evidence=evidence_items,

            recommendations=(
                recommendations
            ),

            sources=sources,

            rag_context=rag.get(
                "context"
            ),

            llm_used=bool(
                result.get(
                    "llm_used",
                    False,
                )
            ),

            evidence_available=bool(
                result.get(
                    "evidence_available",
                    False,
                )
            ),

            metadata=metadata,
        )

    # =====================================================
    # ANALYZE ALIAS
    # =====================================================

    def analyze(
        self,
        question: str,
    ) -> dict[str, Any]:

        return self.answer(
            question
        )

    # =====================================================
    # REFRESH DATA
    # =====================================================

    def refresh_data(
        self,
        dataframe: Optional[pd.DataFrame] = None,
    ) -> pd.DataFrame:

        if dataframe is not None:

            if not isinstance(
                dataframe,
                pd.DataFrame,
            ):

                raise TypeError(
                    "dataframe must be a pandas DataFrame"
                )

            self._dataframe = (
                dataframe.copy()
            )

            return self._dataframe

        try:

            self._dataframe = (
                get_sales_dataframe()
            )

        except Exception:

            self._dataframe = (
                pd.DataFrame()
            )

        return self._dataframe

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health_check(
        self,
    ) -> dict[str, Any]:

        dataframe = (
            self.get_dataframe()
        )

        return {
            "service": "DecisionService",
            "status": "healthy",
            "data_available": (
                not dataframe.empty
            ),
            "row_count": int(
                len(dataframe)
            ),
            "orchestrator_available": (
                self.orchestrator is not None
            ),
        }