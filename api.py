from fastapi import FastAPI
from pydantic import BaseModel
from database import engine
from sqlalchemy import text
from sqlalchemy import text

app = FastAPI()

@app.get("/next_game_number")
def get_next_game_number():
    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT COALESCE(MAX(game_number), 0) + 1
                FROM game_attempts
                """
            )
        )

        game_number = result.scalar()

    return {"game_number": game_number}

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
