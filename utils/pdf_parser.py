import fitz
from utils.helpers import log

# Maximum characters to send to Gemini
MAX_CHARS = 15000


def extract_text(pdf_path):

    print("\n========== PDF EXTRACTION STARTED ==========\n")

    try:

        doc = fitz.open(pdf_path)

        total_pages = len(doc)

        print(f"Pages Found: {total_pages}")

        log(f"Pages Found: {total_pages}")

        text = ""

        for page_num, page in enumerate(doc):

            page_text = page.get_text()

            text += page_text

            print(
                f"Page {page_num + 1}/{total_pages} "
                f"Extracted ({len(page_text)} chars)"
            )

        doc.close()

        original_length = len(text)

        print(
            f"\nTotal Characters Extracted: "
            f"{original_length}"
        )

        log(
            f"Characters Extracted: "
            f"{original_length}"
        )

        # ----------------------------
        # Handle Huge PDFs
        # ----------------------------

        if original_length > MAX_CHARS:

            print(
                f"Text exceeded "
                f"{MAX_CHARS} characters."
            )

            print(
                "Applying smart truncation..."
            )

            log(
                f"Text exceeded "
                f"{MAX_CHARS} chars."
            )

            first_half = text[:7500]
            last_half = text[-7500:]

            text = (
                first_half
                + "\n\n...[TRUNCATED]...\n\n"
                + last_half
            )

            print(
                f"Final Characters Sent to LLM: "
                f"{len(text)}"
            )

            log(
                f"Text truncated to "
                f"{len(text)} chars."
            )

        else:

            print(
                f"Final Characters Sent to LLM: "
                f"{len(text)}"
            )

        print(
            "\n========== PDF EXTRACTION COMPLETED ==========\n"
        )

        return text

    except Exception as e:

        print(
            f"PDF Extraction Error: {e}"
        )

        log(
            f"PDF Extraction Error: {e}"
        )

        return ""