import json

from services.gemini_service import GeminiService
from utils.helpers import (
    log,
    log_error,
    log_warning
)

gemini = GeminiService()

# Cache duplicate extractions
claim_cache = {}


def extract_claims(text):

    if not text:

        log_warning(
            "Empty text received."
        )

        return []

    # Prevent huge prompts
    text = text[:15000]

    with open(
            "prompts/claim_extraction.txt",
            "r",
            encoding="utf-8"
    ) as f:

        prompt = f.read()

    final_prompt = f"""
{prompt}

TEXT:

{text}
"""

    try:

        log(
            "Starting Claim Extraction..."
        )

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

        claims = json.loads(
            response
        )

        if not isinstance(
                claims,
                list
        ):

            log_warning(
                "Gemini did not return a list."
            )

            return []

        cleaned_claims = []
        seen = set()

        for item in claims:

            if not isinstance(
                    item,
                    dict
            ):
                continue

            claim = (
                item.get(
                    "claim",
                    ""
                )
                .strip()
            )

            claim_type = (
                item.get(
                    "claim_type",
                    "Unknown"
                )
                .strip()
            )

            # Skip empty claims
            if not claim:
                continue

            # Remove duplicates
            if claim in seen:
                continue

            seen.add(
                claim
            )

            cleaned_claims.append({

                "claim":
                    claim,

                "claim_type":
                    claim_type
            })

        log(
            f"Claims Extracted: "
            f"{len(cleaned_claims)}"
        )

        for c in cleaned_claims:
            log(
                f"Claim -> {c['claim']}"
            )

        return cleaned_claims

    except json.JSONDecodeError as e:

        log_error(
            f"JSON Error -> {e}"
        )

        return []

    except Exception as e:

        log_error(
            f"Claim Extraction Error -> {e}"
        )

        return []