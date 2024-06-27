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
    ("What is your activity level? (e.g., Sedentary, Lightly active, Moderately active, Very active)", "Okay, nice! This is important for me to know to provide the best results that fit into your lifestyle!"),
    ("Do you have any medical conditions? (e.g., diabetes, hypertension, cholesterol)", "Thank you for letting me know."),
    ("Do you have any allergies? (e.g., nuts, shellfish)", "Got it, we'll make sure to keep that in mind."),
    ("What are your health goals? (e.g., weight loss, muscle gain, maintenance, specific health improvements)", "Great! Those goals are definitely achievable!"),
    ("What is your diet type? (e.g., Vegetarian, Vegan, Pescatarian, Omnivore)", "Got it."),
    ("What are your preferred cuisines? (e.g., Italian, Mexican, Indian, Chinese)", "Delicious choices! What most people don't know is that it's possible to eat all your favorite cuisines at home with a little practice!"),
    ("What are your favorite foods?", "Yum! I'm going to figure out how to let you eat all your favorite foods while staying on track with your health goals!"),
    ("What foods do you prefer to avoid?", "Got it, we'll make sure to avoid those."),
    ("Do you have meal timing preferences? (e.g., intermittent fasting, specific meal times)", "Good to know."),
    ("Do you have any food allergies? (e.g., peanuts, gluten, dairy)", "Got it, I'll take note of that."),
    ("Do you have any intolerances? (e.g., lactose, gluten)", "Good to know."),
    ("Do you have any religious dietary restrictions? (e.g., Halal, Kosher)", "Got it, I'll make sure to accommodate those."),
    ("Do you have any personal dietary restrictions? (e.g., no red meat, no processed foods)", "Thank you for sharing."),
    ("Do you have any macro preferences? (e.g., high protein, low carb)", "Got it."),
    ("What is your caloric intake goal?", "Great, thank you."),
    ("Do you have any nutrient focuses? (e.g., high fiber, high iron)", "Good to know."),
    ("What is your cooking skill level? (e.g., Beginner, Intermediate, Advanced)", "Got it."),
    ("What are your preferred cooking methods? (e.g., baking, grilling, steaming)", "Great!"),
    ("How much time do you have available for cooking?", "Got it, I'll make sure to consider that."),
    ("What kitchen equipment do you have available? (e.g., blender, microwave, oven, slow cooker)", "Wonderful! I'll make sure to curate meals that don't require any new equipment!"),
    ("What is your preferred shopping frequency? (e.g., weekly, bi-weekly)", "Got it."),
    ("What are your preferred shopping days?", "Good to know."),
    ("Do you have any budget constraints? (e.g., specific budget per week)", "Got it, I'll make sure to consider that."),
    ("What are your preferred grocery stores? (e.g., local markets, specific supermarket chains)", "Nice.")
]


@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    try:
        db = get_firestore_client()
        user_ref = db.collection('users').document(chat_message.user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists():
            raise HTTPException(status_code=404, detail="User not found")

        conversation = user_doc.to_dict().get('conversation', [])

        if chat_message.message.lower() == "start":
            if len(conversation) == 0:
                conversation.append({'sender': 'bot', 'message': survey_questions[0][0]})
        else:
            conversation.append({'sender': 'user', 'message': chat_message.message})
            question_index = (len(conversation) // 2) - 1
            if question_index < len(survey_questions):
                response_message = survey_questions[question_index][1]
                conversation.append({'sender': 'bot', 'message': response_message})
                
                next_question_index = question_index + 1
                if next_question_index < len(survey_questions):
                    next_question = survey_questions[next_question_index][0]
                    conversation.append({'sender': 'bot', 'message': next_question})
        
        user_ref.update({'conversation': conversation})
        
        if len(conversation) > 1:
            return {"response": conversation[-2]['message'], "next_question": conversation[-1]['message']}
        else:
            return {"response": conversation[-1]['message'], "next_question": ""}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))