from fastapi import FastAPI
from pydantic import BaseModel
from database import engine
from sqlalchemy import text

app = FastAPI()


class Attempt(BaseModel):
    game_number: int
    game_id: str
    encounter: int
    attempt: int
    enemy: str
    enemy_length: int
    typed_word: str
    accuracy: float
    time_taken: float
    success: bool
    health: int


@app.get("/")
def home():
    return {"message": "Typing Game API is running"}


@app.post("/save_attempt")
def save_attempt(attempt: Attempt):

    with engine.begin() as connection:

        connection.execute(
            text("""
                INSERT INTO game_attempts
                (
                    game_number,
                    game_id,
                    encounter,
                    attempt,
                    enemy,
                    enemy_length,
                    typed_word,
                    accuracy,
                    time_taken,
                    success,
                    health
                )
                VALUES
                (
                    :game_number,
                    :game_id,
                    :encounter,
                    :attempt,
                    :enemy,
                    :enemy_length,
                    :typed_word,
                    :accuracy,
                    :time_taken,
                    :success,
                    :health
                )
            """),
            attempt.model_dump()
        )

    return {"message": "Attempt saved successfully"}