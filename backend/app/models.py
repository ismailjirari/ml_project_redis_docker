from pydantic import BaseModel, ConfigDict
from typing import Optional, Union, List

class PhraseCreate(BaseModel):
    phrase: Union[str, List[str]]
    modelnumber: int

class PhraseResponse(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=()  # This disables the protected namespaces warning
    )
    
    id: int
    text: Union[str, List[str]]
    embedding: Optional[List[float]] = None
    embedding_dim: Optional[int] = None
    model_used: str

class PhraseListResponse(BaseModel):
    phrases: List[dict]
    count: int

class ModelsResponse(BaseModel):
    models: dict