"""Streamlit web interface for the Blog Generator.

This module provides a web-based UI for generating blog content
using the multi-agent pipeline.
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.exceptions import BlogGenerationError, ConfigurationError
from core.orchestrator import Orchestrator


def main() -> None:
    """Render the Streamlit application."""
    st.set_page_config(
        page_title="Blog Generator",
        page_icon="📝",
        layout="centered",
    )

    st.title("📝 Blog Generator")
    st.markdown("Generate SEO-optimized blog posts using AI agents")

    # Topic input
    topic = st.text_input(
        "Enter a topic",
        value="AI in 2026",
        placeholder="e.g., Getting Started with Python",
    )

    # Generate button
    if st.button("Generate Blog Post", type="primary"):
        if not topic.strip():
            st.error("Please enter a topic")
            return

        with st.spinner("Generating blog post..."):
            try:
                orchestrator = Orchestrator()
                output = orchestrator.run_sync(topic=topic)

                st.success("Blog generated successfully!")
                st.divider()
                st.markdown(output)

            except ConfigurationError as e:
                st.error("Configuration Error")
                st.markdown(f"""
                **Error:** {e}

                Please ensure your `.env` file is configured with:
                ```
                OPENROUTER_API_KEY=your_api_key_here
                ```
                """)

            except BlogGenerationError as e:
                st.error("Generation Error")
                st.markdown(f"**Error:** {e}")

            except Exception as e:
                st.error("Unexpected Error")
                st.markdown(f"**An unexpected error occurred:** {e}")


if __name__ == "__main__":
    main()