from pydantic import BaseModel
 
 
class SuccessResponse(BaseModel):
     status: str = "success"
     message: str
     data: dict | None = None
 
 
class ErrorResponse(BaseModel):
     status: str = "error" 
     message: str
     error_code: int | None = None
     details: dict | None = None