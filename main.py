from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import anthropic
import os

from game import TicTacToe
from player import SmartComputerPlayer, RandomComputerPlayer

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MoveRequest(BaseModel):
    board: list[str]
    difficulty: str
    player_letter: str = "X"
    ai_letter: str = "O"

class MoveResponse(BaseModel):
    position: int
    board: list[str]
    winner: Optional[str]
    game_over: bool
    commentary: str

def get_ai_move(board: list[str], difficulty: str, ai_letter: str) -> int:
    game = TicTacToe()
    game.board = board.copy()

    if difficulty == "easy":
        player = RandomComputerPlayer(ai_letter)
    else:
        player = SmartComputerPlayer(ai_letter)
        if difficulty == "medium":
            import random
            if random.random() < 0.5:
                player = RandomComputerPlayer(ai_letter)

    return player.get_move(game)

def get_commentary(board: list[str], last_move: int, mover: str, winner: Optional[str], is_tie: bool, difficulty: str) -> str:
    client = anthropic.Anthropic()
    board_str = ""
    for i in range(3):
        row = board[i*3:(i+1)*3]
        board_str += " | ".join(cell if cell != " " else str(i*3+j) for j, cell in enumerate(row))
        if i < 2:
            board_str += "\n---------\n"

    if winner:
        context = f"{'You' if winner == 'X' else 'The AI'} just won the game!"
    elif is_tie:
        context = "The game ended in a tie!"
    else:
        context = f"{'You' if mover == 'X' else 'The AI (difficulty: ' + difficulty + ')'} just played square {last_move}."

    prompt = f"""You are a witty, enthusiastic Tic Tac Toe commentator. 
Current board:
{board_str}

{context}

Give a single short punchy comment (max 15 words). Be funny, dramatic, or insightful. No hashtags."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=60,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

@app.get("/")
def root():
    return FileResponse("index.html")

@app.post("/move", response_model=MoveResponse)
def make_move(req: MoveRequest):
    game = TicTacToe()
    game.board = req.board.copy()

    position = get_ai_move(req.board, req.difficulty, req.ai_letter)
    game.make_move(position, req.ai_letter)

    winner = None
    if game.current_winner:
        winner = req.ai_letter
    
    game_over = winner is not None or not game.empty_squares()
    is_tie = game_over and winner is None

    commentary = get_commentary(game.board, position, req.ai_letter, winner, is_tie, req.difficulty)

    return MoveResponse(
        position=position,
        board=game.board,
        winner=winner,
        game_over=game_over,
        commentary=commentary
    )