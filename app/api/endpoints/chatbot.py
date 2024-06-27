# app/api/endpoints/chatbot.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai

from ...dependencies import get_firestore_client

class ChatMessage(BaseModel):
    message: str
    user_id: str

router = APIRouter()

survey_questions = [
    "What is your activity level? (e.g., Sedentary, Lightly active, Moderately active, Very active)",
    "What is your current health status?",
    "Do you have any medical conditions? (e.g., diabetes, hypertension, cholesterol)",
    "Do you have any allergies? (e.g., nuts, shellfish)",
    "What are your health goals? (e.g., weight loss, muscle gain, maintenance, specific health improvements)",
    "What is your diet type? (e.g., Vegetarian, Vegan, Pescatarian, Omnivore)",
    "What are your preferred cuisines? (e.g., Italian, Mexican, Indian, Chinese)",
    "What are your favorite foods?",
    "What foods do you prefer to avoid?",
    "Do you have meal timing preferences? (e.g., intermittent fasting, specific meal times)",
    "Do you have any food allergies? (e.g., peanuts, gluten, dairy)",
    "Do you have any intolerances? (e.g., lactose, gluten)",
    "Do you have any religious dietary restrictions? (e.g., Halal, Kosher)",
    "Do you have any personal dietary restrictions? (e.g., no red meat, no processed foods)",
    "Do you have any macro preferences? (e.g., high protein, low carb)",
    "What is your caloric intake goal?",
    "Do you have any nutrient focuses? (e.g., high fiber, high iron)",
    "What is your cooking skill level? (e.g., Beginner, Intermediate, Advanced)",
    "What are your preferred cooking methods? (e.g., baking, grilling, steaming)",
    "How much time do you have available for cooking?",
    "What kitchen equipment do you have available? (e.g., blender, microwave, oven, slow cooker)",
    "What is your preferred shopping frequency? (e.g., weekly, bi-weekly)",
    "What are your preferred shopping days?",
    "Do you have any budget constraints? (e.g., specific budget per week)",
    "What are your preferred grocery stores? (e.g., local markets, specific supermarket chains)"
]

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

        # Determine the next question to ask
        question_index = len(conversation) // 2
        if question_index < len(survey_questions):
            next_question = survey_questions[question_index]
            conversation.append({'sender': 'bot', 'message': next_question})
        else:
            response = openai.Completion.create(
                engine="davinci",  # Use the appropriate engine
                prompt=chat_message.message,
                max_tokens=150
            )
            bot_message = response.choices[0].text.strip()
            conversation.append({'sender': 'bot', 'message': bot_message})
        
        user_ref.update({'conversation': conversation})
        
        return {"response": conversation[-1]['message']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))