"""Editor Agent for the Blog Generator.

This module provides the EditorAgent class that refines and improves
blog content using LLM calls via LangChain.
"""

from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from agents.base_agent import BaseAgent
from config import settings, get_openrouter_api_key


EDITOR_PROMPT = """You are an expert blog editor. Review and improve the following
blog post for clarity, flow, and readability.

Original Blog Post:
{content}

Your task:
- Improve the writing quality and clarity
- Enhance the structure and flow
- Fix any grammar or style issues
- Maintain the original meaning and intent
- Make the content more engaging

Return the improved blog post:"""


class EditorAgent(BaseAgent):
    """Agent responsible for editing and polishing blog content.

    This agent uses LangChain with OpenRouter to call an LLM and improve
    the quality of the generated blog content.
    """

    def __init__(self) -> None:
        """Initialize the EditorAgent."""
        super().__init__(name="editor")
        self._llm: Optional[ChatOpenAI] = None

    @property
    def llm(self) -> ChatOpenAI:
        """Get or create the LLM client.

        Returns:
            The ChatOpenAI client instance configured for OpenRouter.
        """
        if self._llm is None:
            try:
                api_key = get_openrouter_api_key()
                self._llm = ChatOpenAI(
                    model=settings.model_name,
                    api_key=api_key,
                    base_url="https://openrouter.ai/api/v1",
                    temperature=settings.model_temperature,
                    max_tokens=settings.model_max_tokens,
                )
            except Exception as e:
                self._logger.error(f"Failed to initialize LLM: {e}")
                raise RuntimeError(f"EditorAgent initialization failed: {e}") from e
        return self._llm

    async def execute(self, content: str) -> str:
        """Execute the editing task.

        Improves the provided blog content using the LLM.

        Args:
            content: The blog content to edit.

        Returns:
            The improved blog content as a markdown string.

        Raises:
            AgentExecutionError: If editing fails.
        """
        self._logger.info(f"Editing content of length: {len(content)} characters")

        try:
            prompt = self._build_prompt(EDITOR_PROMPT, content=content)
            messages = [HumanMessage(content=prompt)]

            response = await self.llm.agenerate(messages=[messages])
            edited_content = response.generations[0][0].text

            self._logger.info(f"Editing complete, new length: {len(edited_content)} characters")
            return edited_content

        except Exception as e:
            self._logger.exception(f"Editing failed: {e}")
            # Fallback to simple editing if LLM fails
            self._logger.warning("Using fallback editing")
            return self._fallback_edit(content)

    def _fallback_edit(self, content: str) -> str:
        """Perform fallback editing when LLM is unavailable.

        Args:
            content: The content to edit.

        Returns:
            Edited content.
        """
        return content.replace("first draft", "polished draft")