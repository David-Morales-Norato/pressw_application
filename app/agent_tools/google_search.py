from serpapi import GoogleSearch


class GoogleSearchTool:
    def __init__(self, api_key: str, top_k: int = 10) -> None:
        self.api_key = api_key
        self.top_k = top_k

    def search(self, query: str) -> str:
        params = {"engine": "google", "q": query, "api_key": self.api_key}

        search = GoogleSearch(params)
        results = search.get_dict()
        recipes_results = results.get("recipes_results", [])

        return recipes_results


if __name__ == "__main__":
    import os

    api_key = os.getenv("SERPAPI_API_KEY")
    tool = GoogleSearchTool(api_key=api_key)
    search_results = tool.search("How to make Exprresso Coffee")
    print("Search results:")
    print("Found", len(search_results), "recipes")
