from utils.pdf_parser import extract_text
from utils.claim_extractor import extract_claims
from utils.web_search import search_claim
from utils.verifier import verify_claim
from utils.helpers import log

# Cache for duplicate claims
claim_cache = {}


def run_pipeline(pdf_path):

    print("\n========== FACT CHECK PIPELINE STARTED ==========\n")

    # ---------------- Extract PDF ---------------- #

    print("Step 1: Extracting PDF Text...")

    text = extract_text(
        pdf_path
    )

    print(
        f"Characters Extracted: {len(text)}"
    )

    # ---------------- Extract Claims ---------------- #

    print(
        "Step 2: Extracting Claims..."
    )

    claims = extract_claims(
        text
    )

    print(
        f"Claims Found: {len(claims)}"
    )

    # Prevent huge API usage
    claims = claims[:20]

    final_results = []

    # ---------------- Verify Claims ---------------- #

    for index, item in enumerate(
            claims,
            start=1
    ):

        claim = item.get(
            "claim",
            ""
        ).strip()

        if not claim:
            continue

        print(
            f"\n[{index}/{len(claims)}]"
        )

        print(
            f"Claim: {claim}"
        )

        log(
            f"Verifying Claim: {claim}"
        )

        # ---------------- Cache ---------------- #

        if claim in claim_cache:

            print(
                "Cache Hit"
            )

            final_results.append(
                claim_cache[claim]
            )

            continue

        try:

            # ---------------- Web Search ---------------- #

            print(
                "Searching Web..."
            )

            search_results = search_claim(
                claim
            )

            print(
                f"Sources Found: {len(search_results)}"
            )

            # ---------------- Verification ---------------- #

            print(
                "Verifying..."
            )

            result = verify_claim(
                claim,
                search_results
            )

            final_result = {

                "claim":
                    result.get(
                        "claim",
                        claim
                    ),

                "status":
                    result.get(
                        "status",
                        "False"
                    ),

                "confidence":
                    result.get(
                        "confidence",
                        0
                    ),

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
                    result.get(
                        "source",
                        []
                    ),

                "sources_count":
                    result.get(
                        "sources_count",
                        0
                    )
            }

            # Save in cache
            claim_cache[
                claim
            ] = final_result

            final_results.append(
                final_result
            )

        except Exception as e:

            print(
                f"Pipeline Error: {e}"
            )

            final_results.append({

                "claim":
                    claim,

                "status":
                    "False",

                "confidence":
                    0,

                "corrected_fact":
                    "",

                "evidence":
                    str(e),

                "source":
                    [],

                "sources_count":
                    0
            })

    print(
        "\n========== PIPELINE COMPLETED ==========\n"
    )

    return final_results