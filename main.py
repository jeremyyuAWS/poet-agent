from fastapi import FastAPI
from pydantic import BaseModel
from gitagent import Agent

app = FastAPI()
agent = Agent()

class Prompt(BaseModel):
    prompt: str

@app.get("/")
def health():
    return {"status": "poet-agent running"}

@app.post("/poem")
def generate_poem(data: Prompt):
    result = agent.run(data.prompt)
    return {"poem": result}