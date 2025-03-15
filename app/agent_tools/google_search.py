from serpapi import GoogleSearch


class GoogleSearchTool:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def search(self, query: str) -> str:
        params = {"engine": "google", "q": query, "api_key": self.api_key}

        search = GoogleSearch(params)
        results = search.get_dict()
        recipes_results = results["recipes_results"]

        return recipes_results


if __name__ == "__main__":
    import os

    api_key = os.getenv("SERPAPI_API_KEY")
    tool = GoogleSearchTool(api_key=api_key)
    print(tool.search("How to make Exprresso Coffee"))
