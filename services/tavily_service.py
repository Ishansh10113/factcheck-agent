from tavily import TavilyClient
from utils.config import TAVILY_API_KEY
from utils.helpers import (
    log,
    log_error,
    log_warning
)


class TavilyService:

    def __init__(self):

        if not TAVILY_API_KEY:
            raise ValueError(
                "TAVILY_API_KEY not found in .env"
            )

        self.client = TavilyClient(
            api_key=TAVILY_API_KEY
        )

    def search(
            self,
            query: str,
            max_results: int = 5
    ):

        try:

            log(
                f"Tavily Search -> {query}"
            )

            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_answer=True,
                include_raw_content=False
            )

            results = response.get(
                "results",
                []
            )

            if not results:

                log_warning(
                    f"No search results for: {query}"
                )

                return []

            cleaned_results = []

            for item in results:

                cleaned_results.append({

                    "title":
                        item.get(
                            "title",
                            ""
                        ),

                    "content":
                        item.get(
                            "content",
                            ""
                        ),

                    "url":
                        item.get(
                            "url",
                            ""
                        ),

                    "score":
                        item.get(
                            "score",
                            0
                        )
                })

            log(
                f"Sources Retrieved: "
                f"{len(cleaned_results)}"
            )

            return cleaned_results

        except Exception as e:

            log_error(
                f"Tavily Error -> {e}"
            )

            return []