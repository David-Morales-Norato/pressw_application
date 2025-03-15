from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

supported_llms = {
    "llama3.2:1b": "ollama",
    "gpt-4o-mini": "openai",
}


class LLM:
    def __init__(
        self,
        model: str,
        temperature: float,
        prompt: ChatPromptTemplate,
        openai_api_key: str | None = None,
    ) -> None:
        if model not in supported_llms:
            raise ValueError(
                f"Unsupported model: {model}. Supported models: {supported_llms}"
            )

        if supported_llms[model] == "openai":
            llm = ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=openai_api_key,
            )

        else:
            llm = ChatOllama(
                model=model,
                temperature=temperature,
            )

        self.llm = prompt | llm

    def invoke(self, input: dict) -> str:
        return self.llm.invoke(input).content
