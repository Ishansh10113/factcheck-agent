import time
from google import genai
from utils.config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)


class GeminiService:

    def generate(self, prompt):

        MAX_RETRIES = 5

        for attempt in range(MAX_RETRIES):

            try:

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )

                if hasattr(response, "text"):
                    return response.text

                return ""

            except Exception as e:

                error = str(e)

                print(
                    f"Gemini Error (Attempt {attempt+1}/{MAX_RETRIES}):",
                    error
                )

                # Server overloaded
                if (
                    "503" in error
                    or "UNAVAILABLE" in error
                    or "high demand" in error.lower()
                ):

                    wait_time = (attempt + 1) * 5

                    print(
                        f"Gemini overloaded. Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                    continue

                # Quota exhausted
                elif (
                    "429" in error
                    or "RESOURCE_EXHAUSTED" in error
                ):

                    raise Exception(
                        "Gemini quota exceeded. Please try later or use another API key."
                    )

                # Invalid API key
                elif (
                    "API_KEY_INVALID" in error
                    or "API key expired" in error
                ):

                    raise Exception(
                        "Invalid or expired Gemini API key."
                    )

                else:
                    raise e

        raise Exception(
            "Gemini service is currently unavailable after multiple retries."
        )
