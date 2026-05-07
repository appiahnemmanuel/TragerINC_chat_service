from fastapi import FastAPI
from pydantic import BaseModel
from chain import generate_chatbot_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TragerInc Chat Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    customer_id: str
    message: str

class ChatResponse(BaseModel):
    response: str


@app.post('/chat', response_model=ChatResponse)
def chat(request: ChatRequest):
    response_text = generate_chatbot_response(
        user_input=request.message,
        customer_id=request.customer_id
    )
    return ChatResponse(response=response_text)