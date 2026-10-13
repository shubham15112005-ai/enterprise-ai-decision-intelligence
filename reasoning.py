from llm.client import LLMClient

from llm.prompts import decision_prompt


print("Shubham Sharma 23051870")


class DecisionReasoner:
    """
    Generates business decision explanations using an LLM.

    Responsibilities:
    - Construct the decision prompt.
    - Invoke the LLM client.
    - Track successful LLM usage.
    - Propagate errors to the orchestration layer.

    The orchestrator handles failures and selects
    the appropriate deterministic fallback.
    """

    def __init__(self, client=None):
        """
        Initialize the decision reasoner.

        Args:
            client:
                Optional LLMClient instance.
                Dependency injection supports testing.
        """

        self.client = (
            client
            if client is not None
            else LLMClient()
        )

        self.last_used_llm = False

    def explain(
        self,
        decision,
        context="",
    ):
        """
        Generate an explanation for a business decision.

        Args:
            decision:
                Dictionary containing decision information.

            context:
                Supporting business context.

        Returns:
            A string containing the generated explanation.

        Raises:
            Exceptions from the LLM client are propagated
            to the orchestration layer.
        """

        # Reset status before every request.
        self.last_used_llm = False

        # Construct the evidence-grounded prompt.
        prompt = decision_prompt(
            decision,
            context,
        )

        # Generate the explanation.
        # Exceptions are intentionally propagated.
        response = self.client.generate(
            prompt
        )

        # Mark successful usage only after receiving
        # a valid, non-empty response.
        if (
            isinstance(response, str)
            and response.strip()
        ):
            self.last_used_llm = True

            return response.strip()

        raise RuntimeError(
            "The LLM did not generate a valid explanation."
        )