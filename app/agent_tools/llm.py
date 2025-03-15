from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class LLM:
    def __init__(
        self, model: str, temperature: float, prompt: ChatPromptTemplate
    ) -> None:
        llm = ChatOllama(
            model=model,
            temperature=temperature,
        )

        self.llm = prompt | llm

    def invoke(self, input: str) -> str:
        return self.llm.invoke(input).content
