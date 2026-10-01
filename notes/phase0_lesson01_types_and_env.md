# Phase 0, Lesson 1: Python for Dart Devs — Typing, Runtime Realities, and Environment Isolation

## 1. Concept in Simple Words

As a Flutter/Dart developer, you are accustomed to two safety blankets:
1. **Dart Compiler & Sound Null Safety:** Dart catches type errors and null reference bugs *before* your code ever runs (`String?` vs `String`).
2. **`pubspec.yaml` Dependency Isolation:** Dependencies are locked and managed cleanly per project.

In **Python**:
- **Dynamically Typed & Interpreted:** Python does not have a compile step that verifies types. Type hints (e.g. `name: str | None = None`) are **annotations for humans and linters (`mypy`)**, but the Python runtime will run invalid types anyway until it executes the offending line and crashes.
- **Global Package State:** `pip install` installs packages globally by default. If project A needs `numpy 1.24` and project B needs `numpy 2.0`, they will overwrite each other unless isolated.
- **Virtual Environments (`venv`):** A lightweight directory (usually named `.venv`) that houses a dedicated Python binary and `site-packages` directory isolated strictly for this project.

### Cheat Sheet: Dart vs Modern Python (3.10+)

| Concept | Dart | Python (3.10+) |
| :--- | :--- | :--- |
| **Nullable String** | `String? name` | `name: str \| None` |
| **List of Strings** | `List<String> tags` | `tags: list[str]` |
| **Key-Value Map** | `Map<String, dynamic> data` | `data: dict[str, Any]` |
| **Object / Record** | `class Model { final String id; }` | `class Model(TypedDict): id: str` or `@dataclass` |
| **Package File** | `pubspec.yaml` | `pyproject.toml` or `requirements.txt` |
| **Package Installer**| `flutter pub get` | `pip install -r requirements.txt` (inside `.venv`) |
| **Type Checker** | Built into `dart analyze` / compiler | `mypy <filename>.py` |

---

## 2. Why It Matters in Real AI Products

- **Handling LLM Non-Determinism:** LLMs output plain text strings, often with missing keys, malformed markdown, or unexpected nulls. If your backend doesn't enforce strict typing, runtime crashes (`KeyError`, `TypeError`, `AttributeError`) will disconnect your Flutter app.
- **Dependency Conflicts in AI Stacks:** AI libraries (e.g., PyTorch, Hugging Face Transformers, ChromaDB, LangChain) have massive dependency trees. Without virtual environments, updating one library breaks your entire AI dev environment.

---

## 3. Minimal Working Code Example

### Side-by-Side: Data Structure & Extraction

#### Dart:
```dart
class LLMMessage {
  final String role;
  final String content;
  final int? tokenCount;

  LLMMessage({
    required this.role,
    required this.content,
    this.tokenCount,
  });
}

List<String> extractUserPrompts(List<LLMMessage> history) {
  return history
      .where((msg) => msg.role == 'user')
      .map((msg) => msg.content)
      .toList();
}
```

#### Python:
```python
from typing import TypedDict, Any

class LLMMessage(TypedDict):
    role: str
    content: str
    token_count: int | None

def extract_user_prompts(history: list[LLMMessage]) -> list[str]:
    return [msg["content"] for msg in history if msg["role"] == "user"]
```

---

## 4. Setting Up Your Isolated Environment (Windows)

Run the following inside PowerShell in your project folder:

```powershell
# 1. Create the virtual environment
python -m venv .venv

# 2. Activate the virtual environment
.venv\Scripts\Activate.ps1

# If script execution is blocked on Windows, run once:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3. Verify activation: your prompt starts with (.venv)
# 4. Install type-checker:
pip install mypy
```

---

## 5. Hands-On Exercise

### Target File: `exercises/phase0_lesson1.py`

**Requirements:**
1. Define a `TypedDict` or class named `LLMResponse`:
   - `model_name`: `str`
   - `prompt_tokens`: `int`
   - `completion_tokens`: `int`
   - `total_cost`: `float`
   - `finish_reason`: `str | None` (e.g. `"stop"`, `"length"`, or `None`)
2. Write a function `calculate_usage_summary(responses: list[LLMResponse]) -> dict[str, float | int]`:
   - Returns a dictionary with:
     - `"total_tokens"`: sum of all prompt and completion tokens (`int`)
     - `"total_cost"`: sum of all costs, rounded to 4 decimal places (`float`)
     - `"failed_requests"`: count of responses where `finish_reason` is `None` or not `"stop"` (`int`)
3. Create a test list with 3 sample responses (ensure at least one has `finish_reason=None`).
4. Print the output summary.
5. Verify the types with `mypy exercises/phase0_lesson1.py`.

---

## 6. Quiz Questions

1. In Dart, `String? text = null; text.length;` is blocked at compile time. What happens in Python if you declare `text: str | None = None` and immediately call `len(text)`?
2. What is the difference between Dart's `List<Map<String, dynamic>>` and Python's type annotation for the same structure?
3. Why should you never commit the `.venv` directory to Git, and what file should you commit instead to specify dependencies?

---

## 7. Common Mistakes & Pitfalls

- **Mutable Default Arguments:** Never use `def add_history(item: str, history: list = []):`. In Python, default arguments are instantiated once at definition time. Every call without an explicit history parameter will mutate the exact same list instance! Instead, write:
  ```python
  def add_history(item: str, history: list[str] | None = None) -> list[str]:
      if history is None:
          history = []
      history.append(item)
      return history
  ```
- **Trusting Annotations Blindly:** Python type annotations do not validate types at runtime. Passing invalid data will run until an operation fails.
- **Installing Packages Globally:** Always verify `(.venv)` is visible in your terminal before running `pip install`.
