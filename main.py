from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def health():
    return {"status": "poet-agent running"}


@app.get("/debug")
def debug():
    key = os.environ.get("LYZR_API_KEY")
    return {
        "key_present": key is not None,
        "key_length": len(key) if key else 0,
        "key_prefix": key[:10] if key else None,
    }


@app.post("/poem")
def generate_poem(data: PromptRequest):
    key = os.environ.get("LYZR_API_KEY")

    if not key:
        return {
            "poem": "",
            "error": "LYZR_API_KEY is not set",
            "returncode": 1,
        }

    try:
        env = os.environ.copy()

        result = subprocess.run(
            [
                "npx",
                "@open-gitagent/gitagent@latest",
                "run",
                "-r",
                "https://github.com/jeremyyuAWS/poet-agent",
                "-a",
                "lyzr",
                "-p",
                data.prompt,
            ],
            capture_output=True,
            text=True,
            timeout=120,
            env=env,  # critical
        )

        return {
            "poem": result.stdout.strip(),
            "error": result.stderr.strip(),
            "returncode": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {
            "poem": "",
            "error": "GitAgent timed out after 120 seconds",
            "returncode": 124,
        }

    except Exception as e:
        return {
            "poem": "",
            "error": str(e),
            "returncode": 1,
        }