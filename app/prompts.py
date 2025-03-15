from langchain_core.prompts import ChatPromptTemplate


cooking_related_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "TBD"),
        ("user", "{input}"),
    ]
)

sufficient_info_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "TBD"),
        ("user", "{input}"),
    ]
)

generate_response_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "TBD"),
        ("user", "{input}"),
    ]
)
