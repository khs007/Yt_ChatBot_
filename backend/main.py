from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from transcript import get_transcript
from vector_store import get_answer,build_vector_store
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    video_url:str
    question:str


@app.post("/ask")
def ask(query:QueryRequest):
    try:
        if not query.video_url.strip() or not query.question.strip():
            raise HTTPException(status_code=400, detail="Both video_url and question are required.")
        
        transcript_text=get_transcript(query.video_url)
        vector_store=build_vector_store( transcript_text)
        answer=get_answer(vector_store,query.question)
        return{'answer':answer}
    except Exception as e:
        return JSONResponse(status_code=500,content={"error":str(e)})
    