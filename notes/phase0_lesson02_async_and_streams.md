# Phase 0, Lesson 2: Python `asyncio` vs Dart Event Loop & Streams

## 1. Concept in Simple Words

As a Flutter developer, you live in an asynchronous, single-threaded world:
- **Dart:** Has a single-threaded **Event Loop**. A `Future<T>` represents a value arriving later. A `Stream<T>` represents a series of values arriving over time. Calling `Future.wait([...])` runs multiple asynchronous tasks concurrently.
- **Python:** Python's standard execution is synchronous, but `asyncio` gives Python a single-threaded **Event Loop** nearly identical in concept to Dart's!
  - `async def` defines a **coroutine** (like a function returning a `Future`).
  - `async def` with `yield` defines an **Async Generator** (this is Python's direct equivalent of Dart's `Stream<T> async* { yield ...; }`).
  - `asyncio.gather(*tasks)` runs multiple coroutines concurrently (like Dart's `Future.wait`).

### The Two Critical Differences Flutter Devs Must Know:
1. **Calling doesn't run it:** In Dart, calling `fetchData()` starts running immediately up to the first `await`. In Python, calling `fetch_data()` merely returns an unexecuted **coroutine object**. It does **nothing** until you explicitly `await` it or schedule it with `asyncio.create_task()`.
2. **The "Freeze" Danger (Thread Blocking):** In Flutter, if you run a heavy synchronous loop (`while(true)`) or synchronous I/O on the main isolate, your UI drops to 0 FPS (jank). In Python `asyncio`, if you use synchronous blocking code (like `time.sleep(5)` or `requests.get()`), **you freeze the entire server**. No other users can connect or receive LLM tokens until that blocking call finishes! Always use `asyncio.sleep()` and async HTTP clients like `httpx`.

### Dart vs Python Async Mapping

| Concept | Dart | Python (`asyncio`) |
| :--- | :--- | :--- |
| **Async Function** | `Future<String> fetch() async` | `async def fetch() -> str:` |
| **Awaiting** | `final res = await fetch();` | `res = await fetch()` |
| **Concurrent Execution** | `await Future.wait([task1(), task2()]);` | `await asyncio.gather(task1(), task2())` |
| **Background Task** | `unawaited(task());` | `asyncio.create_task(task())` |
| **Streams / Streaming** | `Stream<String> stream() async* { yield "..."; }` | `async def stream() -> AsyncGenerator[str, None]: yield "..."` |
| **Listen to Stream** | `await for (final token in stream())` | `async for token in stream():` |
| **Delay / Sleep** | `await Future.delayed(Duration(seconds: 1));` | `await asyncio.sleep(1)` |

---

## 2. Why It Matters in Real AI Products

LLM API calls are slow. Generating a 500-token response can take 2 to 10 seconds.
- In **FastAPI** (the industry-standard AI backend framework), endpoints are `async def`.
- If 100 mobile users ask your Flutter app a question simultaneously, and your Python backend handles them concurrently via `asyncio`, all 100 users receive streaming tokens smoothly in parallel.
- If you accidentally put a synchronous blocking call inside your route, user #2 has to wait for user #1's entire LLM generation to finish before their request even starts.

---

## 3. Minimal Working Code Example

### Side-by-Side: Streaming Tokens

#### Dart:
```dart
Stream<String> streamTokens(String prompt) async* {
  final tokens = ["Thinking", "...", " Here", " is", " your", " answer."];
  for (final token in tokens) {
    await Future.delayed(const Duration(milliseconds: 100));
    yield token;
  }
}

Future<void> main() async {
  await for (final token in streamTokens("Hi")) {
    print(token);
  }
}
```

#### Python:
```python
import asyncio
from typing import AsyncGenerator

async def stream_tokens(prompt: str) -> AsyncGenerator[str, None]:
    tokens = ["Thinking", "...", " Here", " is", " your", " answer."]
    for token in tokens:
        await asyncio.sleep(0.1)  # Non-blocking async sleep
        yield token

async def main() -> None:
    async for token in stream_tokens("Hi"):
        print(token, end="", flush=True)
    print()

if __name__ == "__main__":
    asyncio.run(main())  # Starts the asyncio event loop
```

---

## 4. Hands-On Exercise

### Target File: `exercises/phase0_lesson02_task.py`

**Scenario:** You are building an AI gateway that streams responses to multiple Flutter clients simultaneously.

**Requirements:**
1. Implement `stream_mock_llm(model: str, prompt: str) -> AsyncGenerator[str, None]`:
   - Split a dummy response into tokens (words).
   - Use `await asyncio.sleep(0.05)` before yielding each word to simulate realistic network streaming.
2. Implement `handle_user_client(user_id: str, prompt: str, model: str) -> dict[str, Any]`:
   - Consume `stream_mock_llm` using `async for`.
   - Measure the total duration taken for this user's stream (using `time.perf_counter()`).
   - Return a dictionary with:
     - `"user_id"`: `str`
     - `"full_text"`: joined words (`str`)
     - `"latency_seconds"`: duration rounded to 3 decimal places (`float`)
     - `"token_count"`: total tokens yielded (`int`)
3. In `main()`:
   - Simulate **3 concurrent users** sending requests simultaneously using `asyncio.gather(...)`.
   - Measure the total elapsed time of `asyncio.gather`.
   - **Verification:** If each request takes ~0.5 seconds, running 3 requests concurrently should take **~0.5 seconds total**, NOT 1.5 seconds!

---

## 5. Quiz Questions

1. In Python, what does calling `result = fetch_data()` return if `fetch_data` is defined with `async def`, and does it start running immediately?
2. If you use `import time; time.sleep(5)` inside an `async def` function in FastAPI, what happens to other concurrent Flutter users trying to connect to your server?
3. How does Python's `async def ... yield` compare to Dart's `Stream<T> async*`? How do you consume both on the caller side?

---

## 6. Common Mistakes & Pitfalls

- **Mixing `time.sleep()` with `asyncio.sleep()`:** Never use `time.sleep()` in async code. `time.sleep()` freezes the entire OS thread. `asyncio.sleep()` yields control back to the event loop so other coroutines can run.
- **Forgetting `await`:** If you call an async function without `await` (e.g. `res = fetch()`), Python will not throw an error immediately—it assigns a `<coroutine object>` to `res`. You will get warnings like `RuntimeWarning: coroutine 'fetch' was never awaited`.
- **Using synchronous requests:** Never use the popular `requests` library in async functions (`requests.get(...)` is blocking). For async HTTP in Python, always use `httpx.AsyncClient` or `aiohttp`.
