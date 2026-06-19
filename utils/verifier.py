import json
from services.gemini_service import GeminiService

gemini = GeminiService()

# ---------------- CACHE ---------------- #

verification_cache = {}


def verify_claim(
        claim: str,
        search_results: list
):

    # ===============================
    # Return cached result
    # ===============================

    if claim in verification_cache:
        print(f"Cache Hit -> {claim}")
        return verification_cache[claim]

    print(f"Verifying -> {claim}")

    evidence = ""
    source_urls = []

    # ===============================
    # Collect Evidence
    # ===============================

    for result in search_results:

        content = result.get(
            "content",
            ""
        )

        url = result.get(
            "url",
            ""
        )

        if content:
            evidence += (
                    content
                    + "\n\n"
            )

        if url:
            source_urls.append(url)

    # Prevent huge prompts
    evidence = evidence[:5000]

    # ===============================
    # Read Prompt
    # ===============================

    with open(
            "prompts/verification_prompt.txt",
            "r",
            encoding="utf-8"
    ) as f:

        prompt = f.read()

    final_prompt = f"""
{prompt}

CLAIM:
{claim}

WEB EVIDENCE:
{evidence}
"""

    # ===============================
    # Gemini Verification
    # ===============================

    try:

        response = gemini.generate(
            final_prompt
        )

        response = (
            response
            .replace(
                "```json",
                ""
            )
            .replace(
                "```",
                ""
            )
            .strip()
        )

        result = json.loads(
            response
        )

        status = result.get(
            "status",
            "False"
        )

        # ===============================
        # Confidence Scoring
        # ===============================

        if status == "Verified":
            confidence = 95

        elif status == "Inaccurate":
            confidence = 80

        else:
            confidence = 90

        final_result = {

            "claim":
                claim,

            "status":
                status,

            "confidence":
                confidence,

            "corrected_fact":
                result.get(
                    "corrected_fact",
                    ""
                ),

            "evidence":
                result.get(
                    "evidence",
                    ""
                ),

            "source":
                source_urls,

            "sources_count":
                len(source_urls)
        }

        # ===============================
        # Save to Cache
        # ===============================

        verification_cache[
            claim
        ] = final_result

        return final_result

    except Exception as e:

        print(
            f"Verification Error: {e}"
        )

        error_result = {

            "claim":
                claim,

            "status":
                "False",

            "confidence":
                0,

            "corrected_fact":
                "",

            "evidence":
                "Verification Failed",

            "source":
                [],

            "sources_count":
                0
        }

        verification_cache[
            claim
        ] = error_result

        return error_result