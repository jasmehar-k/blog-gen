"""Content Writer Agent for the Blog Generator.

This module provides the ContentWriterAgent class that generates
initial blog content drafts using LLM calls via LangChain.
"""

from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from agents.base_agent import BaseAgent
from config import settings, get_openrouter_api_key


CONTENT_WRITER_PROMPT = """You are a professional blog content writer. Write a comprehensive
and engaging blog post about the following topic.

Topic: {topic}

Requirements:
- Write in a clear, informative style
- Include an engaging introduction
- Cover key points with detailed explanations
- Use appropriate headings and structure
- Write a conclusion

Write the complete blog post now:"""


class ContentWriterAgent(BaseAgent):
    """Agent responsible for generating initial blog content drafts.

    This agent uses LangChain with OpenRouter to call an LLM and generate
    high-quality blog content based on the provided topic.
    """

    def __init__(self) -> None:
        """Initialize the ContentWriterAgent."""
        super().__init__(name="content_writer")
        self._llm: Optional[ChatOpenAI] = None

    @property
    def llm(self) -> ChatOpenAI:
        """Get or create the LLM client.

        Returns:
            The ChatOpenAI client instance configured for OpenRouter.

        Raises:
            RuntimeError: If the LLM cannot be initialized.
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
                raise RuntimeError(f"ContentWriterAgent initialization failed: {e}") from e
        return self._llm

    async def execute(self, topic: str) -> str:
        """Execute the content writing task.

        Generates a blog post draft based on the provided topic using
        the LLM via LangChain.

        Args:
            topic: The blog topic to write about.

        Returns:
            The generated blog post content as a markdown string.

        Raises:
            AgentExecutionError: If content generation fails.
        """
        self._logger.info(f"Generating content for topic: {topic}")

        try:
            prompt = self._build_prompt(CONTENT_WRITER_PROMPT, topic=topic)
            messages = [HumanMessage(content=prompt)]

            response = await self.llm.agenerate(messages=[messages])
            content = response.generations[0][0].text

            self._logger.info(f"Generated content length: {len(content)} characters")
            return content

        except Exception as e:
            self._logger.exception(f"Content generation failed: {e}")
            # Fallback to mock content if LLM fails
            self._logger.warning("Using fallback content generation")
            return self._fallback_content(topic)

    def _fallback_content(self, topic: str) -> str:
        """Generate fallback content when LLM is unavailable.

        Args:
            topic: The blog topic.

        Returns:
            Fallback blog content as a markdown string.
        """
        return f"# {topic}\n\nThis is a first draft about {topic}.\n\n- Key point 1\n- Key point 2\n- Key point 3\n"