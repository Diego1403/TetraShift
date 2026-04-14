# Contributing to TetraShift

Contributions are welcome! Here's how to get started:

1. **Fork** the repository and create a feature branch.
2. **Install** dependencies: `pip install -r requirements.txt`
3. **Make changes** — follow the existing code style (PEP 8, type hints, snake_case).
4. **Test** by running the game: `python main.py`
5. **Submit a pull request** with a clear description of your changes.

## Code style

- Python 3.10+ with `from __future__ import annotations`
- Type hints on all public function signatures
- Brief Google-style docstrings on public methods
- Constants live in `data/config.py` — avoid hardcoded magic numbers

## Reporting issues

Open an issue on GitHub with steps to reproduce, expected behaviour, and your OS/Python version.
