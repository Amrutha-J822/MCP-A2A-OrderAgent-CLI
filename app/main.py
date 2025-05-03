# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.agent import process_user_query
from app.events import event_router

app = FastAPI()

# Mount your real-time event endpoint (if you have one)
app.include_router(event_router)


@app.get("/", response_class=HTMLResponse)
def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>🧠 AI Customer Order Agent</title>
  <style>
    body { font-family: Arial; padding: 2em; }
    input { width: 300px; padding: 8px; }
    button { padding: 8px 12px; margin-left: 4px; }
    #mic { cursor: pointer; vertical-align: middle; }
    #status { margin-top: 8px; color: gray; }
    #response { margin-top: 1em; background: #f4f4f4; padding: 1em; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h2>Ask for a Customer’s Latest Order</h2>
  <div>
    <input id="query" type="text"
           placeholder="What is Alice Johnson’s last order status?" />
    <button id="askBtn">Ask</button>
    <img id="mic"
         src="https://img.icons8.com/ios-filled/24/000000/microphone.png"
         title="Click to start/stop listening" />
  </div>
  <div id="status"></div>
  <div id="response"></div>

  <script>
  const queryInput = document.getElementById('query');
  const askBtn     = document.getElementById('askBtn');
  const micBtn     = document.getElementById('mic');
  const statusDiv  = document.getElementById('status');
  const respDiv    = document.getElementById('response');

  async function sendQuery(q) {
    statusDiv.textContent = '⏳ Thinking…';
    respDiv.textContent = '';
    try {
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q })
      });
      const data = await res.json();
      respDiv.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      respDiv.textContent = '❌ Error: ' + err;
    } finally {
      statusDiv.textContent = '';
    }
  }

  askBtn.onclick = () => {
    const q = queryInput.value.trim();
    if (q) sendQuery(q);
  };

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    micBtn.style.display = 'none';
  } else {
    const recog = new SpeechRecognition();
    recog.lang = 'en-US';
    recog.interimResults = false;
    recog.maxAlternatives = 1;

    let isListening = false;
    const icons = {
      listen: 'https://img.icons8.com/ios-filled/24/000000/microphone.png',
      stop:   'https://img.icons8.com/ios-filled/24/ff0000/stop.png'
    };
    micBtn.src = icons.listen;

    micBtn.onclick = () => {
      if (!isListening) {
        isListening = true;
        micBtn.src = icons.stop;
        statusDiv.textContent = '🎙 Listening… click again to stop';
        recog.start();
      } else {
        recog.stop();              // trigger onend
      }
    };

    recog.onresult = (evt) => {
      const spoken = evt.results[0][0].transcript;
      statusDiv.textContent = '🎙 You said: "' + spoken + '"';
      queryInput.value = spoken;
    };

    // **Fires when recognition stops, either manually or automatically**
    recog.onend = () => {
      if (isListening) {
        isListening = false;
        micBtn.src = icons.listen;
        statusDiv.textContent = '⏸️ Stopped';
        const q = queryInput.value.trim();
        if (q) sendQuery(q);
      }
    };

    recog.onerror = (evt) => {
      statusDiv.textContent = '⚠️ ' + evt.error;
      isListening = false;
      micBtn.src = icons.listen;
    };
  }
</script>

</body>
</html>
    """


@app.post("/ask")
async def ask_agent(request: Request):
    payload = await request.json()
    q = payload.get("query")
    if not q:
        return JSONResponse(status_code=400, content={"error": "Missing 'query'"})
    return await process_user_query(q)

