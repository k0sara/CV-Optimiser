"""Convenient Streamlit entry point for local development and deployment."""

import runpy
from pathlib import Path

# Execute on every Streamlit rerun; importing a module caches its first render.
runpy.run_path(str(Path(__file__).resolve().parent / "src" / "app.py"), run_name="__main__")
