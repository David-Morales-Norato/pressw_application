class GoogleSearchTool:
    def __init__(self, api_key: str | None = None) -> None:
        if api_key is None:
            raise ValueError("api_key is required")
        self.api_key = api_key

    def search(self, query: str) -> str:
        return "This is a placeholder for the Google Search API"


if __name__ == "__main__":
    import os

    api_key = os.getenv("SERPAPI_API_KEY")
    tool = GoogleSearchTool(api_key=api_key)
    print(tool.search("How to make Exprresso Coffee"))
