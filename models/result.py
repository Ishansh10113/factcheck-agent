from pydantic import BaseModel


class VerificationResult(BaseModel):
    claim: str
    status: str
    confidence: int
    evidence: str
    source: str
    corrected_fact: str