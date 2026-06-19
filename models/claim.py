from pydantic import BaseModel


class Claim(BaseModel):
    claim: str
    claim_type: str