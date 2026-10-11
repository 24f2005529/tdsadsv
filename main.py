from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()


class SentimentRequest(BaseModel):
    sentences: list[str]


def classify_sentiment(sentence: str) -> str:
    text = sentence.strip()

    if not text:
        return "neutral"

    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "happy"
    elif score <= -0.05:
        return "sad"
    else:
        return "neutral"


@app.post("/sentiment")
async def sentiment(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": classify_sentiment(sentence)
            }
            for sentence in request.sentences
        ]
    }
