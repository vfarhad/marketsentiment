from fastapi import FastAPI, Query
from pydantic import BaseModel
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class SentimentResponse(BaseModel):
    ticker: str
    sentiment: str
    reasoning: str

def get_market_sentiment(ticker: str) -> SentimentResponse:
    prompt = (
        f"Analyze current market sentiment for the stock ticker '{ticker}' "
        f"based on general public opinion, recent news, and stock market trends. "
        f"Label the sentiment as 'Bullish', 'Bearish', or 'Neutral', and explain the rationale."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    reply = response['choices'][0]['message']['content']

    # Optional: you can use a pattern to extract sentiment and reasoning
    # For simplicity, we return the whole message
    return SentimentResponse(ticker=ticker, sentiment="Unknown", reasoning=reply)

@app.get("/sentiment", response_model=SentimentResponse)
def sentiment(ticker: str = Query(..., description="Stock ticker symbol")):
    return get_market_sentiment(ticker)
