# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.agent import process_user_query
from app.events import event_router

app = FastAPI()
app.include_router(event_router)  # if you still ingest amazon-events

@app.get("/", response_class=HTMLResponse)
def root():
    return """
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<title>🧠 AI Customer Order Agent</title>
<style>body{font-family:Arial;padding:2em;}
input{width:300px;padding:8px;}button{padding:8px 12px;margin-left:4px;}
#mic{cursor:pointer;vertical-align:middle;}#status{margin-top:8px;color:gray;}
#response{margin-top:1em;background:#f4f4f4;padding:1em;white-space:pre-wrap;}
</style></head><body>
  <!-- example removed here -->
  <h2>Ask anything about a customer</h2>
  <div>
    <input id="query" type="text" placeholder="eg: What is Alice Johnson’s average rating?"/>
    <button id="askBtn">Ask</button>
    <img id="mic" src="https://img.icons8.com/ios-filled/24/000000/microphone.png"
         title="Click to start/stop"/>
  </div>
  <div id="status"></div>
  <div id="response"></div>
<script>
const Q = q=>document.getElementById(q),
      sendQ=async q=>{
        S.textContent='⏳ Thinking…'; R.textContent='';
        try{
          let r=await fetch('/ask',{method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({query:q})
          });
          let j=await r.json();
          R.textContent=JSON.stringify(j,null,2);
        }catch(e){ R.textContent='❌ '+e }
        S.textContent=''
      };
const I=Q('query'), B=Q('askBtn'), M=Q('mic'),
      S=Q('status'), R=Q('response');
B.onclick=()=>{let v=I.value.trim(); if(v) sendQ(v)};
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
if(!SR) M.style.display='none'; else {
  let r=new SR(), listening=false,
      iconOn='https://img.icons8.com/ios-filled/24/000000/microphone.png',
      iconOff='https://img.icons8.com/ios-filled/24/ff0000/stop.png';
  M.src=iconOn; r.lang='en-US';r.interimResults=false;r.maxAlternatives=1;
  M.onclick=()=>{ if(!listening){
      listening=true;M.src=iconOff;S.textContent='🎙 Listening…';r.start()
    } else r.stop();
  };
  r.onresult=e=>{
    let t=e.results[0][0].transcript;
    S.textContent=`🎙 You said: "${t}"`; I.value=t;
  };
  r.onend=_=>{
    if(listening){
      listening=false;M.src=iconOn;S.textContent='⏸️ Stopped';
      let v=I.value.trim(); if(v) sendQ(v)
    }
  };
  r.onerror=e=>{S.textContent='⚠️ '+e.error;listening=false;M.src=iconOn;}
}
</script>
</body></html>
    """

@app.post("/ask")
async def ask_agent(request: Request):
    body = await request.json()
    q = body.get("query","").strip()
    if not q:
        return JSONResponse(400, {"error":"Missing 'query'"})
    return await process_user_query(q)