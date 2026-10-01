"""
Phase 0, Lesson 2 Task: Python AsyncIO vs Dart Event Loop & Streams
===================================================================

Scenario:
You are building an asynchronous backend gateway. Multiple Flutter clients
are requesting streaming completions from an LLM at the same time.

Requirements:
1. Implement `stream_mock_llm` as an async generator yielding tokens with a delay.
2. Implement `handle_user_client` to consume the stream, measure latency, and build the payload.
3. In `main()`, use `asyncio.gather()` to execute 3 requests concurrently.
4. Verify total execution time proves concurrent execution (~0.5s total, NOT ~1.5s).
"""

import asyncio
import time
from typing import Any, AsyncGenerator


# =====================================================================
# STEP 1: Async Generator (Equivalent to Dart's Stream<String> async*)
# =====================================================================
async def stream_mock_llm(model: str, prompt: str) -> AsyncGenerator[str, None]:
    """Simulates streaming token generation from an LLM.

    TODO:
    1. Define a list of words/tokens representing an AI response (at least 8-10 words).
    2. Loop over the words.
    3. Use `await asyncio.sleep(0.05)` before yielding each word to simulate generation delay.
    4. Yield the word.
    """
    # TODO: Implement here
    pass


# =====================================================================
# STEP 2: Client Request Handler (Consumes the Async Stream)
# =====================================================================
async def handle_user_client(
    user_id: str, prompt: str, model: str
) -> dict[str, Any]:
    """Simulates a FastAPI endpoint handling a connected Flutter user.

    TODO:
    1. Record the start time using `time.perf_counter()`.
    2. Collect tokens from `stream_mock_llm(model, prompt)` using `async for`.
    3. Calculate elapsed time: `time.perf_counter() - start_time`.
    4. Return a dictionary with:
       - "user_id": user_id
       - "full_text": string with all tokens joined
       - "latency_seconds": elapsed time rounded to 3 decimal places
       - "token_count": number of tokens collected
    """
    # TODO: Implement here
    ...


# =====================================================================
# STEP 3: Concurrency Test with asyncio.gather (Equivalent to Future.wait)
# =====================================================================
async def main() -> None:
    print("--- Starting Concurrent LLM Streaming Test ---")
    overall_start = time.perf_counter()

    # TODO:
    # 1. Use asyncio.gather(...) to launch 3 concurrent user requests:
    #    - User "flutter_client_1" asking "What is RAG?" using model "gpt-4o"
    #    - User "flutter_client_2" asking "How do agents work?" using model "gemini-1.5-pro"
    #    - User "flutter_client_3" asking "Explain embeddings" using model "claude-3-5-sonnet"
    # 2. Store results in `results`.
    #
    # results = await asyncio.gather(...)

    overall_elapsed = time.perf_counter() - overall_start

    # print("\n--- Results Summary ---")
    # for res in results:
    #     print(f"[{res['user_id']}] Tokens: {res['token_count']} | Time: {res['latency_seconds']}s")
    #     print(f"Response: {res['full_text']}\n")

    # print(f"Total Wall-Clock Time: {overall_elapsed:.3f} seconds")
    # print("Notice: If requests ran in parallel, total time is roughly equal to ONE request's duration!")


if __name__ == "__main__":
    # Start the event loop
    asyncio.run(main())
