from pathlib import Path
import zipfile

base = Path("/mnt/data/bot_board")
base.mkdir(exist_ok=True)

app = r'''
import random
import time
from collections import Counter

import streamlit as st

try:
    import chess
except ImportError:
    chess = None

st.set_page_config(
    page_title="BOT BOARD",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Styling
# ----------------------------
st.markdown("""
<style>
    .stApp {
        background: #0b1020;
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background: #111827;
    }
    .hero {
        padding: 28px 30px;
        border-radius: 24px;
        background: linear-gradient(135deg, #172554, #312e81 55%, #581c87);
        margin-bottom: 20px;
        border: 1px solid #334155;
    }
    .hero h1 {
        font-size: 48px;
        margin: 0;
        color: white;
    }
    .hero p {
        color: #dbeafe;
        font-size: 18px;
        margin-top: 8px;
    }
    .wallet {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 15px 18px;
        text-align: center;
    }
    .wallet-number {
        font-size: 28px;
        font-weight: 800;
        color: #facc15;
    }
    .game-card {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 20px;
        min-height: 170px;
        margin-bottom: 12px;
    }
    .game-card h3 {
        margin-top: 0;
    }
    .muted {
        color: #94a3b8;
    }
    .result {
        padding: 14px;
        border-radius: 14px;
        background: #172033;
        border: 1px solid #334155;
        margin: 10px 0;
    }
    .big-center {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
    }
    .card {
        display: inline-block;
        width: 64px;
        height: 90px;
        background: white;
        color: #111827;
        border-radius: 10px;
        margin: 4px;
        text-align: center;
        vertical-align: middle;
        font-size: 28px;
        padding-top: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,.25);
    }
    .redcard { color: #dc2626; }
    .board-title {
        font-size: 20px;
        font-weight: 700;
        margin: 8px 0;
    }
    div[data-testid="stButton"] > button {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Global session state
# ----------------------------
DEFAULTS = {
    "balance": 1000,
    "total_earned": 0,
    "total_lost": 0,
    "biggest_win": 0,
    "games_played": 0,
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "streak": 0,
    "best_streak": 0,
    "achievements": set(),
    "daily_bonus": False,
    "game": None,
    "difficulty": "Medium",
    "last_result": "",
    "reward_given": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

DIFFICULTIES = ["Easy", "Medium", "Hard", "Impossible"]

REWARDS = {
    "Tic Tac Toe": {"Easy": 25, "Medium": 50, "Hard": 100, "Impossible": 200},
    "Connect 4": {"Easy": 50, "Medium": 100, "Hard": 200, "Impossible": 400},
    "Checkers": {"Easy": 75, "Medium": 150, "Hard": 300, "Impossible": 600},
    "Othello": {"Easy": 100, "Medium": 200, "Hard": 400, "Impossible": 800},
    "Gomoku": {"Easy": 75, "Medium": 150, "Hard": 300, "Impossible": 600},
    "Battleship": {"Easy": 100, "Medium": 200, "Hard": 400, "Impossible": 800},
    "Chess": {"Easy": 150, "Medium": 300, "Hard": 600, "Impossible": 1200},
}

def add_money(amount):
    st.session_state.balance += amount
    if amount > 0:
        st.session_state.total_earned += amount
        st.session_state.biggest_win = max(st.session_state.biggest_win, amount)
    elif amount < 0:
        st.session_state.total_lost += abs(amount)

def finish_game(result, reward=0):
    """Call exactly once when a game ends."""
    if st.session_state.reward_given:
        return
    st.session_state.reward_given = True
    st.session_state.games_played += 1
    st.session_state.last_result = result

    if result == "win":
        st.session_state.wins += 1
        st.session_state.streak += 1
        st.session_state.best_streak = max(
            st.session_state.best_streak, st.session_state.streak
        )
        if reward:
            add_money(reward)
        unlock("First Win")
        if st.session_state.streak >= 5:
            unlock("Hot Streak")
    elif result == "loss":
        st.session_state.losses += 1
        st.session_state.streak = 0
    else:
        st.session_state.draws += 1

    if st.session_state.total_earned >= 1000:
        unlock("Big Winner")

def unlock(name):
    if name not in st.session_state.achievements:
        st.session_state.achievements.add(name)

def reset_for_game(name):
    st.session_state.game = name
    st.session_state.difficulty = "Medium"
    st.session_state.reward_given = False
    st.session_state.last_result = ""
    init_game(name)

def reward_for(name):
    return REWARDS.get(name, {}).get(st.session_state.difficulty, 0)

def bot_strength():
    return DIFFICULTIES.index(st.session_state.difficulty)

# ----------------------------
# Tic Tac Toe
# ----------------------------
def init_ttt():
    st.session_state.ttt = [""] * 9
    st.session_state.ttt_turn = "X"
    st.session_state.ttt_over = False

def ttt_winner(b):
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b1,c in lines:
        if b[a] and b[a] == b[b1] == b[c]:
            return b[a]
    return "draw" if all(b) else None

def ttt_minimax(board, maximizing):
    result = ttt_winner(board)
    if result == "O": return 10
    if result == "X": return -10
    if result == "draw": return 0
    scores = []
    for i in range(9):
        if not board[i]:
            board[i] = "O" if maximizing else "X"
            score = ttt_minimax(board, not maximizing)
            board[i] = ""
            scores.append(score)
    return max(scores) if maximizing else min(scores)

def ttt_bot_move():
    b = st.session_state.ttt
    empty = [i for i,x in enumerate(b) if not x]
    if not empty:
        return
    level = bot_strength()
    if level == 0:
        move = random.choice(empty)
    elif level == 1:
        # Win if possible, otherwise block, otherwise random.
        move = None
        for i in empty:
            b[i] = "O"
            if ttt_winner(b) == "O":
                move = i
            b[i] = ""
            if move is not None: break
        if move is None:
            for i in empty:
                b[i] = "X"
                if ttt_winner(b) == "X":
                    move = i
                b[i] = ""
                if move is not None: break
        move = move if move is not None else random.choice(empty)
    else:
        best, best_score = None, -999
        for i in empty:
            b[i] = "O"
            score = ttt_minimax(b, False)
            b[i] = ""
            if score > best_score:
                best_score, best = score, i
        move = best
    b[move] = "O"

def play_ttt():
    st.subheader("❌ Tic Tac Toe")
    if st.session_state.ttt_over:
        st.info(st.session_state.last_result)
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            label = st.session_state.ttt[i] or " "
            if st.button(label, key=f"ttt_{i}", use_container_width=True):
                if not st.session_state.ttt_over and not st.session_state.ttt[i]:
                    st.session_state.ttt[i] = "X"
                    result = ttt_winner(st.session_state.ttt)
                    if result == "X":
                        st.session_state.ttt_over = True
                        finish_game("win", reward_for("Tic Tac Toe"))
                        st.rerun()
                    elif result == "draw":
                        st.session_state.ttt_over = True
                        finish_game("draw")
                        st.rerun()
                    ttt_bot_move()
                    result = ttt_winner(st.session_state.ttt)
                    if result:
                        st.session_state.ttt_over = True
                        finish_game("loss" if result == "O" else "draw")
                    st.rerun()

# ----------------------------
# Connect 4
# ----------------------------
def init_connect4():
    st.session_state.c4 = [[0]*7 for _ in range(6)]
    st.session_state.c4_over = False

def c4_winner(board):
    for r in range(6):
        for c in range(7):
            p = board[r][c]
            if not p: continue
            for dr,dc in [(1,0),(0,1),(1,1),(1,-1)]:
                cells = []
                for k in range(4):
                    rr,cc=r+dr*k,c+dc*k
                    if 0<=rr<6 and 0<=cc<7:
                        cells.append(board[rr][cc])
                if len(cells)==4 and cells == [p]*4:
                    return p
    return None

def c4_drop(col, player):
    for r in range(5,-1,-1):
        if st.session_state.c4[r][col] == 0:
            st.session_state.c4[r][col] = player
            return r
    return None

def c4_bot_move():
    valid = [c for c in range(7) if st.session_state.c4[0][c] == 0]
    if not valid: return
    level = bot_strength()
    # Try immediate win.
    for c in valid:
        r = c4_drop(c, 2)
        if c4_winner(st.session_state.c4) == 2:
            return
        st.session_state.c4[r][c] = 0
    # Block immediate player win.
    if level >= 1:
        for c in valid:
            r = c4_drop(c, 1)
            if c4_winner(st.session_state.c4) == 1:
                st.session_state.c4[r][c] = 0
                c4_drop(c, 2)
                return
            st.session_state.c4[r][c] = 0
    preferred = [3,2,4,1,5,0,6]
    choices = [c for c in preferred if c in valid]
    c4_drop(random.choice(choices if level < 2 else choices[:max(1, len(choices)-1)]), 2)

def play_connect4():
    st.subheader("🟡 Connect 4")
    cols = st.columns(7)
    for c in range(7):
        with cols[c]:
            if st.button("↓", key=f"c4drop{c}", use_container_width=True, disabled=st.session_state.c4_over):
                if c4_drop(c, 1) is not None:
                    w = c4_winner(st.session_state.c4)
                    if w == 1:
                        st.session_state.c4_over = True
                        finish_game("win", reward_for("Connect 4"))
                    elif all(st.session_state.c4[0][x] for x in range(7)):
                        st.session_state.c4_over = True
                        finish_game("draw")
                    else:
                        c4_bot_move()
                        w = c4_winner(st.session_state.c4)
                        if w == 2:
                            st.session_state.c4_over = True
                            finish_game("loss")
                        elif all(st.session_state.c4[0][x] for x in range(7)):
                            st.session_state.c4_over = True
                            finish_game("draw")
                    st.rerun()
    symbols = {0:"⚪", 1:"🔴", 2:"🟡"}
    for row in st.session_state.c4:
        cols = st.columns(7)
        for c,cell in enumerate(row):
            cols[c].markdown(f"<div class='big-center'>{symbols[cell]}</div>", unsafe_allow_html=True)

# ----------------------------
# Othello
# ----------------------------
DIRS = [(dr,dc) for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc)!=(0,0)]

def init_othello():
    b = [[0]*8 for _ in range(8)]
    b[3][3]=2; b[4][4]=2; b[3][4]=1; b[4][3]=1
    st.session_state.oth = b
    st.session_state.oth_turn = 1
    st.session_state.oth_over = False
    st.session_state.oth_pass = False

def oth_moves(b, player):
    out=[]
    opp=3-player
    for r in range(8):
        for c in range(8):
            if b[r][c]: continue
            good=False
            for dr,dc in DIRS:
                rr,cc=r+dr,c+dc
                seen=False
                while 0<=rr<8 and 0<=cc<8 and b[rr][cc]==opp:
                    seen=True; rr+=dr; cc+=dc
                if seen and 0<=rr<8 and 0<=cc<8 and b[rr][cc]==player:
                    good=True; break
            if good: out.append((r,c))
    return out

def oth_play(r,c,player):
    b=st.session_state.oth
    b[r][c]=player
    opp=3-player
    for dr,dc in DIRS:
        path=[]
        rr,cc=r+dr,c+dc
        while 0<=rr<8 and 0<=cc<8 and b[rr][cc]==opp:
            path.append((rr,cc)); rr+=dr; cc+=dc
        if path and 0<=rr<8 and 0<=cc<8 and b[rr][cc]==player:
            for pr,pc in path: b[pr][pc]=player

def oth_bot():
    moves=oth_moves(st.session_state.oth,2)
    if not moves: return False
    # Prefer corners and moves with more flips.
    scored=[]
    for m in moves:
        r,c=m
        score=(100 if m in [(0,0),(0,7),(7,0),(7,7)] else 0)
        temp=[row[:] for row in st.session_state.oth]
        before=sum(x.count(2) for x in temp)
        # rough scoring via simulated placement
        st.session_state.oth=temp
        oth_play(r,c,2)
        after=sum(x.count(2) for x in st.session_state.oth)
        st.session_state.oth=temp
        score += (after-before)*10
        scored.append((score,m))
    _,m=max(scored)
    oth_play(*m,2)
    return True

def oth_check_end():
    b=st.session_state.oth
    if not oth_moves(b,1) and not oth_moves(b,2):
        p=sum(x.count(1) for x in b); q=sum(x.count(2) for x in b)
        st.session_state.oth_over=True
        finish_game("win" if p>q else "loss" if q>p else "draw")
        return True
    return False

def play_othello():
    st.subheader("🟢 Othello / Reversi")
    legal=oth_moves(st.session_state.oth,1)
    for r in range(8):
        cols=st.columns(8)
        for c in range(8):
            v=st.session_state.oth[r][c]
            label="⚫" if v==2 else "⚪" if v==1 else "·"
            if (r,c) in legal and not st.session_state.oth_over:
                label="🟢"
            if cols[c].button(label, key=f"oth{r}_{c}", use_container_width=True):
                if (r,c) in legal:
                    oth_play(r,c,1)
                    if not oth_check_end():
                        if not oth_moves(st.session_state.oth,2):
                            st.session_state.oth_turn=1
                        else:
                            oth_bot()
                            oth_check_end()
                    st.rerun()
    p=sum(x.count(1) for x in st.session_state.oth)
    q=sum(x.count(2) for x in st.session_state.oth)
    st.caption(f"You: {p}   |   Bot: {q}")

# ----------------------------
# Gomoku
# ----------------------------
def init_gomoku():
    st.session_state.gom=[[0]*15 for _ in range(15)]
    st.session_state.gom_over=False

def gom_win(b,r,c,p):
    for dr,dc in DIRS:
        n=1
        for sign in (1,-1):
            rr,cc=r+dr*sign,c+dc*sign
            while 0<=rr<15 and 0<=cc<15 and b[rr][cc]==p:
                n+=1; rr+=dr*sign; cc+=dc*sign
        if n>=5: return True
    return False

def gom_bot():
    b=st.session_state.gom
    empty=[(r,c) for r in range(15) for c in range(15) if b[r][c]==0]
    if not empty:return
    # immediate win / block
    for p in (2,1):
        for r,c in empty:
            b[r][c]=p
            if gom_win(b,r,c,p):
                b[r][c]=0
                if p==2: b[r][c]=2; return
                b[r][c]=0
                b[r][c]=2; return
            b[r][c]=0
    if bot_strength()>=2:
        # Prefer cells adjacent to existing pieces and center.
        scored=[]
        for r,c in empty:
            neigh=sum(
                1 for dr,dc in DIRS
                for rr,cc in [(r+dr,c+dc)]
                if 0<=rr<15 and 0<=cc<15 and b[rr][cc]
            )
            center=14-abs(r-7)-abs(c-7)
            scored.append((neigh*10+center,(r,c)))
        _,m=max(scored)
    else:
        m=random.choice(empty)
    b[m[0]][m[1]]=2

def play_gomoku():
    st.subheader("🟨 Gomoku")
    for r in range(15):
        cols=st.columns(15)
        for c in range(15):
            v=st.session_state.gom[r][c]
            label="⚫" if v==2 else "⚪" if v==1 else "·"
            if cols[c].button(label,key=f"gom{r}_{c}",use_container_width=True):
                if not st.session_state.gom_over and v==0:
                    st.session_state.gom[r][c]=1
                    if gom_win(st.session_state.gom,r,c,1):
                        st.session_state.gom_over=True
                        finish_game("win",reward_for("Gomoku"))
                    else:
                        gom_bot()
                        # find whether bot just won
                        won=False
                        for rr in range(15):
                            for cc in range(15):
                                if st.session_state.gom[rr][cc]==2 and gom_win(st.session_state.gom,rr,cc,2):
                                    won=True; break
                            if won: break
                        if won:
                            st.session_state.gom_over=True
                            finish_game("loss")
                        elif all(st.session_state.gom[x][y] for x in range(15) for y in range(15)):
                            st.session_state.gom_over=True
                            finish_game("draw")
                    st.rerun()

# ----------------------------
# Battleship
# ----------------------------
def init_battleship():
    st.session_state.bs_player=[[0]*8 for _ in range(8)]
    st.session_state.bs_bot=[[0]*8 for _ in range(8)]
    st.session_state.bs_shots=[[0]*8 for _ in range(8)]
    st.session_state.bs_bot_shots=[[0]*8 for _ in range(8)]
    ships=[3,2,2]
    place_fleet(st.session_state.bs_player,ships)
    place_fleet(st.session_state.bs_bot,ships)
    st.session_state.bs_over=False

def place_fleet(board, ships):
    for size in ships:
        placed=False
        while not placed:
            horizontal=random.choice([True,False])
            r=random.randrange(8); c=random.randrange(8)
            cells=[(r,c+i) for i in range(size)] if horizontal else [(r+i,c) for i in range(size)]
            if all(0<=rr<8 and 0<=cc<8 and board[rr][cc]==0 for rr,cc in cells):
                for rr,cc in cells: board[rr][cc]=1
                placed=True

def bs_remaining(board):
    return sum(x==1 for row in board for x in row)

def bs_bot_shot():
    available=[(r,c) for r in range(8) for c in range(8) if st.session_state.bs_bot_shots[r][c]==0]
    if not available:return
    r,c=random.choice(available)
    st.session_state.bs_bot_shots[r][c]=1
    if st.session_state.bs_player[r][c]==1:
        st.session_state.bs_player[r][c]=2

def play_battleship():
    st.subheader("🛳 Battleship")
    st.caption("Click a square to fire. Red = hit, gray = miss.")
    for r in range(8):
        cols=st.columns(8)
        for c in range(8):
            shot=st.session_state.bs_shots[r][c]
            label="💥" if shot==2 else "💧" if shot==1 else "❓"
            if cols[c].button(label,key=f"bs{r}_{c}",use_container_width=True):
                if not st.session_state.bs_over and shot==0:
                    if st.session_state.bs_bot[r][c]==1:
                        st.session_state.bs_bot[r][c]=2
                        st.session_state.bs_shots[r][c]=2
                    else:
                        st.session_state.bs_shots[r][c]=1
                    if bs_remaining(st.session_state.bs_bot)==0:
                        st.session_state.bs_over=True
                        finish_game("win",reward_for("Battleship"))
                    else:
                        bs_bot_shot()
                        if bs_remaining(st.session_state.bs_player)==0:
                            st.session_state.bs_over=True
                            finish_game("loss")
                    st.rerun()
    with st.expander("Your fleet"):
        for row in st.session_state.bs_player:
            st.write(" ".join("🚢" if x==1 else "💥" if x==2 else "·" for x in row))

# ----------------------------
# Checkers
# ----------------------------
def init_checkers():
    b=[[0]*8 for _ in range(8)]
    for r in range(3):
        for c in range(8):
            if (r+c)%2: b[r][c]=2
    for r in range(5,8):
        for c in range(8):
            if (r+c)%2: b[r][c]=1
    st.session_state.chk=b
    st.session_state.chk_selected=None
    st.session_state.chk_over=False

def chk_moves(b,p):
    moves=[]
    captures=[]
    dirs=[(-1,-1),(-1,1),(1,-1),(1,1)]
    for r in range(8):
        for c in range(8):
            if b[r][c] not in (p,p+2): continue
            piece=b[r][c]
            isking=piece in (3,4)
            ds=dirs if isking else ([(-1,-1),(-1,1)] if p==1 else [(1,-1),(1,1)])
            for dr,dc in ds:
                rr,cc=r+dr,c+dc
                if 0<=rr<8 and 0<=cc<8 and b[rr][cc]==0:
                    moves.append(((r,c),(rr,cc),None))
                elif 0<=rr<8 and 0<=cc<8 and b[rr][cc] not in (0,p,p+2):
                    jr,jc=rr+dr,cc+dc
                    if 0<=jr<8 and 0<=jc<8 and b[jr][jc]==0:
                        captures.append(((r,c),(jr,jc),(rr,cc)))
    return captures if captures else moves

def chk_apply(move):
    (r,c),(rr,cc),cap=move
    b=st.session_state.chk
    piece=b[r][c]
    b[r][c]=0
    b[rr][cc]=piece
    if cap:
        b[cap[0]][cap[1]]=0
    if piece==1 and rr==0: b[rr][cc]=3
    if piece==2 and rr==7: b[rr][cc]=4

def chk_bot():
    moves=chk_moves(st.session_state.chk,2)
    if not moves:return
    # Prefer captures, then random.
    cap=[m for m in moves if m[2] is not None]
    move=random.choice(cap if cap else moves)
    chk_apply(move)

def play_checkers():
    st.subheader("🏁 Checkers")
    moves=chk_moves(st.session_state.chk,1)
    selected=st.session_state.chk_selected
    for r in range(8):
        cols=st.columns(8)
        for c in range(8):
            v=st.session_state.chk[r][c]
            label={0:"·",1:"⚪",2:"⚫",3:"👑",4:"👑"}.get(v,"·")
            if selected==(r,c): label="🟢"
            if cols[c].button(label,key=f"chk{r}_{c}",use_container_width=True):
                if st.session_state.chk_over: continue
                if selected is None:
                    if v in (1,3):
                        st.session_state.chk_selected=(r,c)
                else:
                    candidate=[m for m in moves if m[0]==selected and m[1]==(r,c)]
                    if candidate:
                        chk_apply(candidate[0])
                        st.session_state.chk_selected=None
                        if not chk_moves(st.session_state.chk,2):
                            st.session_state.chk_over=True
                            finish_game("win",reward_for("Checkers"))
                        else:
                            chk_bot()
                            if not chk_moves(st.session_state.chk,1):
                                st.session_state.chk_over=True
                                finish_game("loss")
                    elif v in (1,3):
                        st.session_state.chk_selected=(r,c)
                    else:
                        st.session_state.chk_selected=None
                    st.rerun()

# ----------------------------
# Chess
# ----------------------------
def init_chess():
    if chess is None:
        st.session_state.chess_board=None
    else:
        st.session_state.chess_board=chess.Board()
    st.session_state.chess_selected=None
    st.session_state.chess_over=False

def chess_bot():
    b=st.session_state.chess_board
    moves=list(b.legal_moves)
    if not moves:return
    level=bot_strength()
    if level==0:
        move=random.choice(moves)
    else:
        captures=[m for m in moves if b.is_capture(m)]
        checks=[m for m in moves if b.gives_check(m)]
        if checks and level>=2:
            move=random.choice(checks)
        elif captures:
            move=random.choice(captures)
        else:
            # prefer moves toward center
            move=random.choice(moves)
    b.push(move)

def play_chess():
    st.subheader("♟ Chess")
    if chess is None:
        st.error("Chess dependency is missing. Add python-chess to requirements.txt.")
        return
    b=st.session_state.chess_board
    if b.is_game_over():
        st.info("Game over: " + str(b.outcome()))
        return
    files="abcdefgh"
    ranks="87654321"
    legal=list(b.legal_moves)
    selected=st.session_state.chess_selected
    for ri in range(8):
        cols=st.columns(8)
        for ci in range(8):
            sq=chess.parse_square(files[ci]+ranks[ri])
            piece=b.piece_at(sq)
            symbol=piece.symbol() if piece else "·"
            target=selected is not None and any(m.from_square==selected and m.to_square==sq for m in legal)
            if target: symbol="🟢"
            if cols[ci].button(symbol,key=f"chess{ri}_{ci}",use_container_width=True):
                if b.turn != chess.WHITE or st.session_state.chess_over:
                    continue
                if selected is None:
                    if piece and piece.color==chess.WHITE:
                        st.session_state.chess_selected=sq
                else:
                    move=next((m for m in legal if m.from_square==selected and m.to_square==sq),None)
                    if move:
                        b.push(move)
                        st.session_state.chess_selected=None
                        if b.is_game_over():
                            st.session_state.chess_over=True
                            if b.is_checkmate():
                                finish_game("win",reward_for("Chess"))
                            else:
                                finish_game("draw")
                        else:
                            chess_bot()
                            if b.is_game_over():
                                st.session_state.chess_over=True
                                if b.is_checkmate():
                                    finish_game("loss")
                                else:
                                    finish_game("draw")
                    elif piece and piece.color==chess.WHITE:
                        st.session_state.chess_selected=sq
                    else:
                        st.session_state.chess_selected=None
                    st.rerun()
    st.caption("You are White. Select a piece, then select its destination.")

# ----------------------------
# Blackjack
# ----------------------------
SUITS=["♠","♥","♦","♣"]
RANKS=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

def make_deck():
    return [(r,s) for s in SUITS for r in RANKS]

def card_value(cards):
    total=0
    aces=0
    for r,_ in cards:
        if r=="A":
            total+=11; aces+=1
        elif r in ("K","Q","J"):
            total+=10
        else:
            total+=int(r)
    while total>21 and aces:
        total-=10; aces-=1
    return total

def init_blackjack():
    st.session_state.bj_deck=make_deck()
    random.shuffle(st.session_state.bj_deck)
    st.session_state.bj_player=[]
    st.session_state.bj_dealer=[]
    st.session_state.bj_bet=10
    st.session_state.bj_active=False
    st.session_state.bj_over=False
    st.session_state.bj_message=""
    st.session_state.bj_last_payout=0

def bj_draw():
    if not st.session_state.bj_deck:
        st.session_state.bj_deck=make_deck()
        random.shuffle(st.session_state.bj_deck)
    return st.session_state.bj_deck.pop()

def bj_start():
    bet=int(st.session_state.bj_bet)
    if bet<=0 or bet>st.session_state.balance:
        st.session_state.bj_message="You don't have enough BOT BUCKS for that bet."
        return
    st.session_state.balance-=bet
    st.session_state.total_lost+=bet
    st.session_state.bj_player=[bj_draw(),bj_draw()]
    st.session_state.bj_dealer=[bj_draw(),bj_draw()]
    st.session_state.bj_active=True
    st.session_state.bj_over=False
    st.session_state.bj_message=""
    st.session_state.bj_last_payout=0

    pv=card_value(st.session_state.bj_player)
    dv=card_value(st.session_state.bj_dealer)
    if pv==21:
        payout=int(bet*2.5)  # return stake + 1.5x profit
        st.session_state.balance+=payout
        st.session_state.total_earned+=int(bet*1.5)
        st.session_state.biggest_win=max(st.session_state.biggest_win,int(bet*1.5))
        st.session_state.bj_last_payout=int(bet*1.5)
        st.session_state.bj_message=f"🃏 BLACKJACK! You won {int(bet*1.5)} BB profit."
        st.session_state.bj_over=True
        unlock("Blackjack!")
    elif dv==21:
        st.session_state.balance+=bet
        st.session_state.total_earned+=0
        st.session_state.bj_message="Dealer has blackjack. You lose."
        st.session_state.bj_over=True

def bj_finish():
    bet=int(st.session_state.bj_bet)
    pv=card_value(st.session_state.bj_player)
    dv=card_value(st.session_state.bj_dealer)
    if pv>21:
        st.session_state.bj_message=f"💥 Bust! You lost {bet} BB."
        st.session_state.bj_over=True
        return
    while card_value(st.session_state.bj_dealer)<17:
        st.session_state.bj_dealer.append(bj_draw())
    dv=card_value(st.session_state.bj_dealer)
    if dv>21 or pv>dv:
        st.session_state.balance+=bet*2
        st.session_state.total_earned+=bet
        st.session_state.biggest_win=max(st.session_state.biggest_win,bet)
        st.session_state.bj_last_payout=bet
        st.session_state.bj_message=f"🎉 You won {bet} BB profit!"
        if bet>=500: unlock("High Roller")
    elif pv==dv:
        st.session_state.balance+=bet
        st.session_state.bj_message="🤝 Push — your bet was returned."
    else:
        st.session_state.bj_message=f"🤖 Dealer wins. You lost {bet} BB."
    st.session_state.bj_over=True

def render_cards(cards, hide_first=False):
    html=""
    for i,(r,s) in enumerate(cards):
        if hide_first and i==0:
            html += "<span class='card'>🂠</span>"
        else:
            cls="redcard" if s in ("♥","♦") else ""
            html += f"<span class='card {cls}'>{r}{s}</span>"
    st.markdown(html,unsafe_allow_html=True)

def play_blackjack():
    st.subheader("🃏 Blackjack")
    st.caption("BOT BUCKS are fictional in-game currency and have no real-world value.")
    st.markdown(f"### 💰 Balance: **{st.session_state.balance:,} BB**")
    if not st.session_state.bj_active and not st.session_state.bj_over:
        options=[10,25,50,100,250,500]
        valid=[x for x in options if x<=st.session_state.balance]
        if valid:
            st.session_state.bj_bet=st.radio("Choose your bet",valid,horizontal=True,key="bj_bet_radio")
        st.number_input("Custom bet",min_value=1,max_value=max(1,st.session_state.balance),
                        value=min(st.session_state.bj_bet,max(1,st.session_state.balance)),
                        step=1,key="bj_custom")
        if st.button("🎲 Deal",type="primary",use_container_width=True):
            st.session_state.bj_bet=st.session_state.bj_custom
            bj_start()
            st.rerun()
    else:
        st.markdown("**Dealer**")
        render_cards(st.session_state.bj_dealer, hide_first=not st.session_state.bj_over)
        if st.session_state.bj_over:
            st.caption(f"Dealer total: {card_value(st.session_state.bj_dealer)}")
        st.markdown("**You**")
        render_cards(st.session_state.bj_player)
        st.caption(f"Your total: {card_value(st.session_state.bj_player)}")
        if not st.session_state.bj_over:
            c1,c2=st.columns(2)
            if c1.button("👊 HIT",use_container_width=True):
                st.session_state.bj_player.append(bj_draw())
                if card_value(st.session_state.bj_player)>21:
                    bj_finish()
                st.rerun()
            if c2.button("✋ STAND",use_container_width=True):
                bj_finish()
                st.rerun()
        else:
            st.success(st.session_state.bj_message)
            if st.button("🔄 New Hand",use_container_width=True):
                st.session_state.bj_active=False
                st.session_state.bj_over=False
                st.session_state.bj_message=""
                st.rerun()

# ----------------------------
# Game initialization router
# ----------------------------
def init_game(name):
    if name=="Tic Tac Toe": init_ttt()
    elif name=="Connect 4": init_connect4()
    elif name=="Checkers": init_checkers()
    elif name=="Othello": init_othello()
    elif name=="Gomoku": init_gomoku()
    elif name=="Battleship": init_battleship()
    elif name=="Chess": init_chess()
    elif name=="Blackjack": init_blackjack()

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("## 🤖 BOT BOARD")
    st.markdown(f"### 💰 {st.session_state.balance:,} BB")
    st.divider()
    page=st.radio("Menu",["🎮 Games","💰 Wallet","🏆 Achievements"])
    if st.session_state.game:
        st.divider()
        if st.button("🏠 Back to Games",use_container_width=True):
            st.session_state.game=None
            st.rerun()
        if st.button("🔄 Restart Game",use_container_width=True):
            reset_for_game(st.session_state.game)
            st.rerun()

# ----------------------------
# Pages
# ----------------------------
if page=="💰 Wallet":
    st.markdown("<div class='hero'><h1>💰 Wallet</h1><p>Your BOT BOARD arcade balance.</p></div>",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    c1.metric("Balance",f"{st.session_state.balance:,} BB")
    c2.metric("Total earned",f"{st.session_state.total_earned:,} BB")
    c3.metric("Total lost",f"{st.session_state.total_lost:,} BB")
    c1,c2,c3=st.columns(3)
    c1.metric("Biggest win",f"{st.session_state.biggest_win:,} BB")
    c2.metric("Win streak",st.session_state.streak)
    c3.metric("Best streak",st.session_state.best_streak)
    st.divider()
    if not st.session_state.daily_bonus:
        if st.button("🎁 Claim Daily Bonus — +250 BB",type="primary"):
            st.session_state.balance+=250
            st.session_state.total_earned+=250
            st.session_state.daily_bonus=True
            st.rerun()
    else:
        st.success("Daily bonus already claimed this session.")
    st.info("BOT BUCKS are fictional game currency only. They cannot be purchased, withdrawn, or converted to real money.")

elif page=="🏆 Achievements":
    st.markdown("<div class='hero'><h1>🏆 Achievements</h1><p>Collect them all.</p></div>",unsafe_allow_html=True)
    all_ach=[
        ("First Win","Win your first game"),
        ("Hot Streak","Win 5 games in a row"),
        ("Big Winner","Earn 1,000 BOT BUCKS"),
        ("Blackjack!","Get a natural blackjack"),
        ("High Roller","Win a 500 BB blackjack hand"),
    ]
    for name,desc in all_ach:
        if name in st.session_state.achievements:
            st.success(f"🏆 **{name}** — {desc}")
        else:
            st.write(f"🔒 **{name}** — {desc}")

else:
    if st.session_state.game is None:
        st.markdown("<div class='hero'><h1>🤖 BOT BOARD</h1><p>Beat the bots. Build your balance.</p></div>",unsafe_allow_html=True)
        st.markdown(f"<div class='wallet'><div>YOUR BALANCE</div><div class='wallet-number'>💰 {st.session_state.balance:,} BB</div></div>",unsafe_allow_html=True)
        st.divider()

        games=[
            ("🎯","Tic Tac Toe","Quick classic strategy."),
            ("🟡","Connect 4","Get four in a row."),
            ("🏁","Checkers","Capture the bot's pieces."),
            ("🟢","Othello","Flip the board."),
            ("🟨","Gomoku","Five in a row wins."),
            ("🛳️","Battleship","Find and sink the fleet."),
            ("♟️","Chess","Classic strategy."),
            ("🃏","Blackjack","Risk BOT BUCKS against the dealer."),
        ]
        cols=st.columns(2)
        for i,(icon,name,desc) in enumerate(games):
            with cols[i%2]:
                st.markdown(
                    f"<div class='game-card'><h3>{icon} {name}</h3><p class='muted'>{desc}</p></div>",
                    unsafe_allow_html=True
                )
                if st.button(f"PLAY {name}",key=f"play_{name}",use_container_width=True):
                    reset_for_game(name)
                    st.rerun()
    else:
        name=st.session_state.game
        c1,c2,c3=st.columns([2,2,1])
        with c1:
            st.markdown(f"## {name}")
        with c2:
            if name!="Blackjack":
                st.session_state.difficulty=st.selectbox("Bot difficulty",DIFFICULTIES,index=DIFFICULTIES.index(st.session_state.difficulty))
                st.caption(f"Win reward: **+{reward_for(name)} BB**")
        with c3:
            st.markdown(f"<div class='wallet'>💰<br><b>{st.session_state.balance:,} BB</b></div>",unsafe_allow_html=True)

        if name=="Tic Tac Toe": play_ttt()
        elif name=="Connect 4": play_connect4()
        elif name=="Checkers": play_checkers()
        elif name=="Othello": play_othello()
        elif name=="Gomoku": play_gomoku()
        elif name=="Battleship": play_battleship()
        elif name=="Chess": play_chess()
        elif name=="Blackjack": play_blackjack()

        if st.session_state.last_result and name!="Blackjack":
            if st.session_state.last_result=="win":
                st.success(f"🎉 You won! +{reward_for(name)} BB")
            elif st.session_state.last_result=="loss":
                st.error("🤖 The bot won.")
            else:
                st.info("🤝 Draw.")
'''

requirements = """streamlit>=1.38,<2
python-chess>=1.999
"""

readme = """# 🤖 BOT BOARD

A Streamlit arcade of board/card games against bots.

Games:
- Tic Tac Toe
- Connect 4
- Checkers
- Othello
- Gomoku
- Battleship
- Chess
- Blackjack

Includes fictional BOT BUCKS, achievements, streaks and a daily bonus.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
