from services.tavily_service import TavilyService
from utils.helpers import (
    log,
    log_error,
    log_warning
)

tavily = TavilyService()

# Cache to avoid repeated API calls
search_cache = {}


def search_claim(claim: str):

    claim = claim.strip()

    if not claim:
        log_warning(
            "Empty claim received."
        )
        return []

    # ---------------- CACHE ---------------- #

    if claim in search_cache:

        log(
            f"Search Cache Hit -> {claim}"
        )

        return search_cache[claim]

    # ---------------- SEARCH ---------------- #

    try:

        log(
            f"Searching Web -> {claim}"
        )

        results = tavily.search(
            claim
        )

        if not results:

            log_warning(
                f"No results found -> {claim}"
            )

            return []

        cleaned_results = []

        for item in results:

            cleaned_result = {

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
                    )
            }

            cleaned_results.append(
                cleaned_result
            )

        # Save in cache
        search_cache[
            claim
        ] = cleaned_results

        log(
            f"Sources Found: "
            f"{len(cleaned_results)}"
        )

        return cleaned_results

    except Exception as e:

        log_error(
            f"Web Search Error -> {e}"
        )

        return []