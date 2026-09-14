from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, AlertSubscription
from .providers import PUNE, provider
from .services import warnings, freshness, reply

app=FastAPI(title="WeatherGPT API",version="0.1.0",description="Pune-first grounded weather assistant. Rule alerts are not official alerts.")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
history=[]; subscriptions=[]
async def bundle(location="Pune"):
    if location.lower() not in ("pune", "pune, india"): raise HTTPException(404,"Demo currently supports Pune. Use /locations/search.")
    p=provider()
    try: current=await p.current(PUNE); forecast=await p.forecast(PUNE)
    except Exception: p=__import__("app.providers",fromlist=["MockWeatherProvider"]).MockWeatherProvider(); current=await p.current(PUNE); forecast=await p.forecast(PUNE)
    return current,forecast
@app.get("/health")
def health(): return {"status":"ok","service":"WeatherGPT"}
@app.get("/weather/current")
async def current(location:str="Pune"): w,_=await bundle(location); return {"data":w,"freshness":freshness(w)}
@app.get("/weather/forecast")
async def forecast(location:str="Pune"): w,f=await bundle(location); return {"data":f,"source":w.source,"is_mock":w.is_mock,"freshness":freshness(w)}
@app.get("/warnings")
async def get_warnings(location:str="Pune"): w,f=await bundle(location); return {"data":warnings(w,f),"disclaimer":"Rule-engine advisories only; not official government warnings.","source":w.source}
@app.get("/locations/search")
def locations_search(q:str="Pune"): return {"data":[PUNE] if "pune" in q.lower() else []}
@app.get("/history")
def get_history(): return {"data":history[-20:]}
@app.post("/chat")
async def chat(req:ChatRequest):
    w,f=await bundle(req.location); ws=warnings(w,f); item={"answer":reply(req.message,w,f,ws,req.language),"weather":w,"warnings":ws,"grounding":{"source":w.source,"is_mock":w.is_mock,"freshness":freshness(w),"llm":"template fallback; no unverified LLM claims"}}
    history.append({"question":req.message,"answer":item["answer"],"location":req.location}); return item
@app.post("/alerts/subscribe")
def subscribe(req:AlertSubscription): subscriptions.append(req.model_dump()); return {"status":"saved","message":"Subscription recorded locally; delivery connector is not configured."}
