"""
Phase 0, Lesson 1 Task: Python Types & Static Analysis for Dart Devs
====================================================================

Instructions:
1. Complete the type definition for `LLMResponse` using `TypedDict`.
2. Implement the `calculate_usage_summary` function with proper type hints.
3. Populate `sample_responses` with at least 3 mock responses (including one failed/interrupted request).
4. Run this file: python exercises/phase0_lesson01_task.py
5. Check types with mypy: mypy exercises/phase0_lesson01_task.py
"""

from typing import TypedDict


# =====================================================================
# STEP 1: Define the Data Structure
# Dart equivalent:
# class LLMResponse {
#   final String modelName;
#   final int promptTokens;
#   final int completionTokens;
#   final double totalCost;
#   final String? finishReason;
#   ...
# }
# =====================================================================
class LLMResponse(TypedDict):
    # TODO: Add fields:
    # - model_name: str
    # - prompt_tokens: int
    # - completion_tokens: int
    # - total_cost: float
    # - finish_reason: str | None
    pass


# =====================================================================
# STEP 2: Implement the Aggregator Function
# =====================================================================
def calculate_usage_summary(
    responses: list[LLMResponse],
) -> dict[str, float | int]:
    """Calculates total token usage, aggregated cost, and count of failed requests.

    Requirements:
    - "total_tokens": sum of prompt_tokens + completion_tokens for all responses (int)
    - "total_cost": sum of total_cost for all responses rounded to 4 decimal places (float)
    - "failed_requests": number of responses where finish_reason is None or NOT equal to "stop" (int)
    """
    # TODO: Implement the calculation logic here
    ...


# =====================================================================
# STEP 3: Test Data and Execution
# =====================================================================
if __name__ == "__main__":
    # TODO: Create a list of 3 LLMResponse items:
    # 1. Successful gpt-4o response (finish_reason="stop")
    # 2. Successful gemini-1.5-pro response (finish_reason="stop")
    # 3. Interrupted/failed claude-3-5-sonnet response (finish_reason=None or "length")
    sample_responses: list[LLMResponse] = [
        # Fill in sample data
    ]

    print("Running Usage Summary Calculation...")
    # summary = calculate_usage_summary(sample_responses)
    # print("Summary Result:", summary)
