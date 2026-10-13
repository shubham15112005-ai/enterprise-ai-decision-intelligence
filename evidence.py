from typing import Any, Dict, List


print("Shubham Sharma 23051870")


class Evidence:

    def __init__(
        self,
        source: str,
        metric: str,
        value: Any,
        interpretation: str,
        confidence: float = 1.0,
    ):
        self.source = source
        self.metric = metric
        self.value = value
        self.interpretation = interpretation
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:

        return {
            "source": self.source,
            "metric": self.metric,
            "value": self.value,
            "interpretation": self.interpretation,
            "confidence": self.confidence,
        }


def build_evidence(
    source: str,
    metric: str,
    value: Any,
    interpretation: str,
    confidence: float = 1.0,
) -> Dict[str, Any]:

    evidence = Evidence(
        source=source,
        metric=metric,
        value=value,
        interpretation=interpretation,
        confidence=confidence,
    )

    return evidence.to_dict()


def combine_evidence(
    evidence_items: List[Dict[str, Any]]
) -> str:

    if not evidence_items:
        return "No supporting evidence available."

    lines = []

    for index, item in enumerate(
        evidence_items,
        start=1
    ):

        lines.append(
            f"{index}. "
            f"{item.get('metric', 'Metric')}: "
            f"{item.get('value', 'N/A')} — "
            f"{item.get('interpretation', '')}"
        )

    return "\n".join(lines)