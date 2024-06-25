# app/api/endpoints/chatbot.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai

from ...dependencies import get_firestore_client

class ChatMessage(BaseModel):
    message: str
    user_id: str

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    try:
        # Retrieve user document from Firestore
        db = get_firestore_client()
        user_ref = db.collection('users').document(chat_message.user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")

        conversation = user_doc.to_dict().get('conversation', [])
        conversation.append({'sender': 'user', 'message': chat_message.message})

        response = openai.Completion.create(
            engine="davinci",  # Use the appropriate engine
            prompt=chat_message.message,
            max_tokens=150
        )
        
        bot_message = response.choices[0].text.strip()
        conversation.append({'sender': 'bot', 'message': bot_message})
        
        user_ref.update({'conversation': conversation})
        
        return {"response": bot_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
