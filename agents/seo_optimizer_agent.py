"""SEO Optimizer Agent for the Blog Generator.

This module provides the SeoOptimizerAgent class that optimizes
blog content for search engines using LLM calls via LangChain.
"""

from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from agents.base_agent import BaseAgent
from config import settings, get_openrouter_api_key


SEO_PROMPT = """You are an SEO expert. Analyze the following blog post and add
relevant SEO optimizations.

Blog Post:
{content}

Your task:
- Add a relevant SEO keywords section with appropriate keywords
- Optimize the content for search engines
- Include meta-relevant improvements
- Add schema markup suggestions if appropriate

Return the SEO-optimized blog post:"""


class SeoOptimizerAgent(BaseAgent):
    """Agent responsible for optimizing blog content for search engines.

    This agent uses LangChain with OpenRouter to call an LLM and add
    SEO enhancements to the blog content.
    """

    def __init__(self) -> None:
        """Initialize the SeoOptimizerAgent."""
        super().__init__(name="seo_optimizer")
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
                raise RuntimeError(f"SeoOptimizerAgent initialization failed: {e}") from e
        return self._llm

    async def execute(self, content: str) -> str:
        """Execute the SEO optimization task.

        Optimizes the provided blog content for search engines.

        Args:
            content: The blog content to optimize.

        Returns:
            The SEO-optimized blog content as a markdown string.

        Raises:
            AgentExecutionError: If optimization fails.
        """
        self._logger.info(f"Optimizing content for SEO, input length: {len(content)} characters")

        # Check if already has SEO keywords
        if "## SEO Keywords" in content:
            self._logger.info("Content already has SEO keywords section")
            return content

        try:
            prompt = self._build_prompt(SEO_PROMPT, content=content)
            messages = [HumanMessage(content=prompt)]

            response = await self.llm.agenerate(messages=[messages])
            optimized_content = response.generations[0][0].text

            self._logger.info(f"SEO optimization complete, new length: {len(optimized_content)} characters")
            return optimized_content

        except Exception as e:
            self._logger.exception(f"SEO optimization failed: {e}")
            # Fallback to basic SEO addition
            self._logger.warning("Using fallback SEO optimization")
            return self._fallback_seo(content)

    def _fallback_seo(self, content: str) -> str:
        """Add basic SEO keywords when LLM is unavailable.

        Args:
            content: The content to optimize.

        Returns:
            Content with SEO keywords added.
        """
        if "## SEO Keywords" in content:
            return content
        return f"{content}\n\n## SEO Keywords\n- blog\n- content strategy\n- search intent\n"
