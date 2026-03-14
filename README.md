# Tic Tac Toe AI

A web-based Tic Tac Toe game with an unbeatable AI opponent and Claude-powered live commentary.

## Features

- **Three difficulty levels** — Easy (random), Medium (mixed), Unbeatable (minimax algorithm)
- **AI commentary** — Claude gives comment after every move with witty, context-aware reactions
- **Hint system** — Ask Claude for the best move, highlighted directly on the board
- **Win detection** — Animated line drawn across the winning combo
- **Move history** — Track every move made in the game
- **Score tracking** — Persists across rounds until you close the tab

## Tech Stack

- **Backend:** FastAPI (Python) — serves the game logic and AI endpoints
- **Game AI:** Minimax algorithm for unbeatable play
- **Commentary & Hints:** Anthropic Claude API (`claude-sonnet-4-20250514`)
- **Frontend:** Vanilla HTML, CSS, JavaScript — glassmorphism UI

## Project Structure

```
tictactoe/
├── main.py       # FastAPI app — /move and /hint endpoints
├── game.py       # TicTacToe board logic
├── player.py     # HumanPlayer, RandomComputerPlayer, SmartComputerPlayer (minimax)
├── index.html    # Frontend UI
└── .env          # API keys (not committed)
```

## Running Locally

1. Clone the repo and install dependencies:
```bash
pip install fastapi uvicorn anthropic python-dotenv
```

2. Add your Anthropic API key to a `.env` file:
```
ANTHROPIC_API_KEY=your-key-here
```

3. Start the server:
```bash
uvicorn main:app --reload
```

4. Open `http://localhost:8000` in your browser.

## How It Works

The frontend sends the current board state to the `/move` endpoint after each human move. FastAPI runs the minimax algorithm to pick the best AI move, then calls the Claude API to generate a one-line commentary. The `/hint` endpoint works the same way — Claude analyzes the board and suggests the best square for the human player.