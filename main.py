from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]


def classify_sentiment(sentence: str) -> str:
    text = sentence.lower()

    positive = [
        "love", "great", "good", "amazing", "excellent",
        "happy", "wonderful", "awesome", "fantastic",
        "nice", "enjoy", "excited", "perfect", "best"
    ]

    negative = [
        "hate", "bad", "terrible", "horrible", "awful",
        "sad", "angry", "disappointed", "poor", "worst",
        "annoying", "frustrated", "pain", "problem"
    ]

    positive_score = sum(word in text for word in positive)
    negative_score = sum(word in text for word in negative)

    if positive_score > negative_score:
        return "happy"
    elif negative_score > positive_score:
        return "sad"
    else:
        return "neutral"


@app.post("/sentiment")
async def sentiment_analysis(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": classify_sentiment(sentence)
            }
            for sentence in request.sentences
        ]
    }
