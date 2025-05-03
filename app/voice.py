from fastapi import APIRouter, Request
from app.agent import process_user_query

voice_router = APIRouter()

@voice_router.post("/vapi-webhook")
async def handle_voice(request: Request):
    payload = await request.json()
    # Vapi may send either 'transcript' or 'query'
    user_query = payload.get("transcript") or payload.get("query") or ""
    result = await process_user_query(user_query)

    # Return the response Vapi will speak:
    text = ""
    if "error" in result:
        text = "Sorry, I ran into an error."
    elif "message" in result and not result.get("order_status"):
        text = result["message"]
    else:
        text = f"{result['order_status']} for {result['customer']}"

    return {"response": {"type": "text", "content": text}}