from pathlib import Path

app = r'''
import random
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

# ============================================================
# MODERN BOT BOARD THEME
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(99,102,241,.18), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(168,85,247,.14), transparent 25%),
        #070a12;
    color: #f8fafc;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c101c 0%, #080b13 100%);
    border-right: 1px solid rgba(255,255,255,.07);
}

[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 42px;
    border-radius: 30px;
    background:
        radial-gradient(circle at 80% 20%, rgba(139,92,246,.35), transparent 30%),
        linear-gradient(135deg, #111827, #161b32 55%, #24143b);
    border: 1px solid rgba(255,255,255,.10);
    box-shadow: 0 25px 70px rgba(0,0,0,.35);
}

.hero:after {
    content: "🤖";
    position: absolute;
    right: 50px;
    top: 12px;
    font-size: 130px;
    opacity: .12;
    transform: rotate(10deg);
}

.hero h1 {
    font-size: clamp(42px, 6vw, 72px);
    font-weight: 900;
    letter-spacing: -4px;
    margin: 0;
    color: #fff;
}

.hero p {
    color: #aab4c7;
    font-size: 18px;
    margin: 8px 0 0;
}

.balance-pill {
    margin-top: 22px;
    display: inline-block;
    padding: 12px 18px;
    border-radius: 999px;
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.10);
    font-weight: 700;
}

.game-card {
    min-height: 215px;
    padding: 24px;
    margin: 8px 0 16px;
    border-radius: 24px;
    background: linear-gradient(145deg, rgba(20,26,42,.96), rgba(12,16,27,.96));
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: 0 14px 35px rgba(0,0,0,.20);
}

.game-icon {
    font-size: 48px;
    margin-bottom: 8px;
}

.game-card h3 {
    font-size: 23px;
    margin: 0;
    font-weight: 800;
}

.game-card p {
    color: #8e9ab0;
    min-height: 42px;
}

.stat-card {
    padding: 20px;
    border-radius: 20px;
    background: rgba(17,24,39,.82);
    border: 1px solid rgba(255,255,255,.07);
}

.stat-label {
    color: #8d98aa;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stat-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 4px;
}

.game-header {
    padding: 18px 22px;
    border-radius: 20px;
    background: rgba(17,24,39,.82);
    border: 1px solid rgba(255,255,255,.08);
    margin-bottom: 18px;
}

div[data-testid="stButton"] > button {
    border-radius: 13px !important;
    min-height: 44px;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,.09);
    background: #171d2d;
    transition: .18s ease;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    border-color: rgba(139,92,246,.65);
    background: #202840;
}

[data-testid="stMetric"] {
    background: rgba(17,24,39,.75);
    border: 1px solid rgba(255,255,255,.07);
    padding: 16px;
    border-radius: 18px;
}

/* ---------------- BLACKJACK TABLE ---------------- */

.blackjack-wrap {
    padding: 12px;
}

.blackjack-table {
    position: relative;
    min-height: 650px;
    padding: 34px 28px 30px;
    border-radius: 42px;
    background:
        radial-gradient(ellipse at center, #167346 0%, #0d5a36 48%, #063b24 100%);
    border: 18px solid #24170f;
    box-shadow:
        inset 0 0 0 3px #7b4c27,
        inset 0 0 60px rgba(0,0,0,.42),
        0 28px 70px rgba(0,0,0,.48);
}

.blackjack-table:before {
    content: "";
    position: absolute;
    inset: 30px;
    border: 2px solid rgba(255,255,255,.18);
    border-radius: 50% 50% 46% 46%;
    pointer-events: none;
}

.casino-title {
    text-align: center;
    position: relative;
    z-index: 2;
    font-size: 24px;
    font-weight: 900;
    letter-spacing: 5px;
    color: rgba(255,255,255,.88);
    text-transform: uppercase;
}

.casino-subtitle {
    text-align: center;
    position: relative;
    z-index: 2;
    color: rgba(255,255,255,.55);
    font-size: 12px;
    margin-top: 3px;
}

.hand-zone {
    position: relative;
    z-index: 2;
    text-align: center;
    margin-top: 30px;
}

.hand-label {
    color: rgba(255,255,255,.72);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hand-total {
    color: white;
    font-size: 24px;
    font-weight: 900;
    margin-top: 8px;
}

.cards {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 12px 0 5px;
    min-height: 126px;
}

.playing-card {
    width: 82px;
    height: 116px;
    background: linear-gradient(145deg, #fff, #e9edf4);
    color: #111827;
    border-radius: 10px;
    box-shadow:
        0 7px 0 rgba(0,0,0,.14),
        0 12px 20px rgba(0,0,0,.25);
    position: relative;
    text-align: left;
    padding: 7px;
    box-sizing: border-box;
    font-family: Georgia, serif;
}

.playing-card .corner {
    font-size: 17px;
    line-height: 18px;
    font-weight: 800;
}

.playing-card .suit-center {
    font-size: 38px;
    text-align: center;
    margin-top: 15px;
}

.card-red {
    color: #d71920;
}

.card-black {
    color: #111827;
}

.card-back {
    background:
        linear-gradient(45deg, rgba(255,255,255,.10) 25%, transparent 25%),
        linear-gradient(-45deg, rgba(255,255,255,.10) 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, rgba(255,255,255,.10) 75%),
        linear-gradient(-45deg, transparent 75%, rgba(255,255,255,.10) 75%),
        #162a66;
    background-size: 14px 14px;
    border: 5px solid white;
    color: transparent;
}

.chip-row {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: center;
    gap: 9px;
    margin: 8px 0 15px;
}

.casino-chip {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f4f4f5;
    color: #18181b;
    border: 6px dashed #18181b;
    box-shadow: 0 5px 10px rgba(0,0,0,.35);
    font-size: 11px;
    font-weight: 900;
}

.bj-status {
    position: relative;
    z-index: 2;
    text-align: center;
    margin: 12px auto;
    padding: 12px 18px;
    max-width: 500px;
    border-radius: 999px;
    background: rgba(0,0,0,.18);
    border: 1px solid rgba(255,255,255,.10);
    color: white;
    font-weight: 700;
}

.bj-controls {
    position: relative;
    z-index: 2;
    margin-top: 16px;
}

.bj-side {
    background: rgba(0,0,0,.20);
    padding: 16px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.09);
    margin-top: 16px;
}

/* Responsive */
@media (max-width: 700px) {
    .hero { padding: 28px 22px; }
    .hero h1 { letter-spacing: -2px; }
    .blackjack-table {
        border-width: 9px;
        border-radius: 26px;
        padding: 25px 12px;
        min-height: 570px;
    }
    .playing-card {
        width: 58px;
        height: 84px;
    }
    .playing-card .suit-center { font-size: 26px; margin-top: 8px; }
    .playing-card .corner { font-size: 13px; }
    .cards { gap: 5px; min-height: 95px; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# STATE
# ============================================================
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

def unlock(name):
    st.session_state.achievements.add(name)

def add_money(amount):
    st.session_state.balance += amount
    if amount > 0:
        st.session_state.total_earned += amount
        st.session_state.biggest_win = max(st.session_state.biggest_win, amount)
    elif amount < 0:
        st.session_state.total_lost += abs(amount)

def finish_game(result, reward=0):
    if st.session_state.reward_given:
        return
    st.session_state.reward_given = True
    st.session_state.games_played += 1
    st.session_state.last_result = result

    if result == "win":
        st.session_state.wins += 1
        st.session_state.streak += 1
        st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
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

def reward_for(name):
    return REWARDS.get(name, {}).get(st.session_state.difficulty, 0)

def bot_strength():
    return DIFFICULTIES.index(st.session_state.difficulty)

# ============================================================
# TIC TAC TOE
# ============================================================
def init_ttt():
    st.session_state.ttt = [""] * 9
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
            scores.append(ttt_minimax(board, not maximizing))
            board[i] = ""
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
    st.caption("You are X • Bot is O")
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
                    elif result == "draw":
                        st.session_state.ttt_over = True
                        finish_game("draw")
                    else:
                        ttt_bot_move()
                        result = ttt_winner(st.session_state.ttt)
                        if result:
                            st.session_state.ttt_over = True
                            finish_game("loss" if result == "O" else "draw")
                    st.rerun()

# ============================================================
# CONNECT 4
# ============================================================
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
    for c in valid:
        r = c4_drop(c, 2)
        if c4_winner(st.session_state.c4) == 2: return
        st.session_state.c4[r][c] = 0
    if bot_strength() >= 1:
        for c in valid:
            r = c4_drop(c, 1)
            if c4_winner(st.session_state.c4) == 1:
                st.session_state.c4[r][c] = 0
                c4_drop(c, 2)
                return
            st.session_state.c4[r][c] = 0
    preferred = [3,2,4,1,5,0,6]
    choices = [c for c in preferred if c in valid]
    c4_drop(random.choice(choices), 2)

def play_connect4():
    st.subheader("🟡 Connect 4")
    st.caption("Drop four pieces in a row before the bot.")
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

# ============================================================
# OTHELLO
# ============================================================
DIRS = [(dr,dc) for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc)!=(0,0)]

def init_othello():
    b = [[0]*8 for _ in range(8)]
    b[3][3]=2; b[4][4]=2; b[3][4]=1; b[4][3]=1
    st.session_state.oth = b
    st.session_state.oth_over = False

def oth_moves(b, player):
    out=[]; opp=3-player
    for r in range(8):
        for c in range(8):
            if b[r][c]: continue
            for dr,dc in DIRS:
                rr,cc=r+dr,c+dc; seen=False
                while 0<=rr<8 and 0<=cc<8 and b[rr][cc]==opp:
                    seen=True; rr+=dr; cc+=dc
                if seen and 0<=rr<8 and 0<=cc<8 and b[rr][cc]==player:
                    out.append((r,c)); break
    return list(dict.fromkeys(out))

def oth_play(r,c,player):
    b=st.session_state.oth; b[r][c]=player; opp=3-player
    for dr,dc in DIRS:
        path=[]; rr,cc=r+dr,c+dc
        while 0<=rr<8 and 0<=cc<8 and b[rr][cc]==opp:
            path.append((rr,cc)); rr+=dr; cc+=dc
        if path and 0<=rr<8 and 0<=cc<8 and b[rr][cc]==player:
            for pr,pc in path: b[pr][pc]=player

def oth_bot():
    moves=oth_moves(st.session_state.oth,2)
    if not moves: return
    corners={(0,0),(0,7),(7,0),(7,7)}
    def score(m):
        temp=[row[:] for row in st.session_state.oth]
        before=sum(row.count(2) for row in temp)
        oth_play_on=temp
        r,c=m; oth_play_on[r][c]=2
        opp=1
        for dr,dc in DIRS:
            path=[]; rr,cc=r+dr,c+dc
            while 0<=rr<8 and 0<=cc<8 and oth_play_on[rr][cc]==opp:
                path.append((rr,cc)); rr+=dr; cc+=dc
            if path and 0<=rr<8 and 0<=cc<8 and oth_play_on[rr][cc]==2:
                for x,y in path: oth_play_on[x][y]=2
        return (100 if m in corners else 0) + (sum(row.count(2) for row in oth_play_on)-before)*8
    oth_play(*max(moves,key=score),2)

def play_othello():
    st.subheader("🟢 Othello")
    legal=oth_moves(st.session_state.oth,1)
    for r in range(8):
        cols=st.columns(8)
        for c in range(8):
            v=st.session_state.oth[r][c]
            label="⚫" if v==2 else "⚪" if v==1 else ("🟢" if (r,c) in legal else "·")
            if cols[c].button(label,key=f"oth{r}_{c}",use_container_width=True):
                if (r,c) in legal and not st.session_state.oth_over:
                    oth_play(r,c,1)
                    if not oth_moves(st.session_state.oth,1) and not oth_moves(st.session_state.oth,2):
                        p=sum(x.count(1) for x in st.session_state.oth)
                        q=sum(x.count(2) for x in st.session_state.oth)
                        st.session_state.oth_over=True
                        finish_game("win" if p>q else "loss" if q>p else "draw")
                    else:
                        oth_bot()
                    st.rerun()
    p=sum(x.count(1) for x in st.session_state.oth)
    q=sum(x.count(2) for x in st.session_state.oth)
    st.caption(f"You: {p}  •  Bot: {q}")

# ============================================================
# GOMOKU
# ============================================================
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
        if n>=5:return True
    return False

def gom_bot():
    b=st.session_state.gom
    empty=[(r,c) for r in range(15) for c in range(15) if b[r][c]==0]
    if not empty:return
    for p in (2,1):
        for r,c in empty:
            b[r][c]=p
            won=gom_win(b,r,c,p)
            b[r][c]=0
            if won:
                b[r][c]=2
                return
    if bot_strength()>=2:
        m=max(empty,key=lambda x: sum(
            1 for dr,dc in DIRS
            if 0<=x[0]+dr<15 and 0<=x[1]+dc<15 and b[x[0]+dr][x[1]+dc]
        )*10 + 14-abs(x[0]-7)-abs(x[1]-7))
    else:
        m=random.choice(empty)
    b[m[0]][m[1]]=2

def play_gomoku():
    st.subheader("🟨 Gomoku")
    st.caption("Five connected pieces wins.")
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
                        won=any(st.session_state.gom[rr][cc]==2 and gom_win(st.session_state.gom,rr,cc,2)
                                for rr in range(15) for cc in range(15))
                        if won:
                            st.session_state.gom_over=True
                            finish_game("loss")
                        elif all(st.session_state.gom[x][y] for x in range(15) for y in range(15)):
                            st.session_state.gom_over=True
                            finish_game("draw")
                    st.rerun()

# ============================================================
# BATTLESHIP
# ============================================================
def place_fleet(board, ships):
    for size in ships:
        while True:
            horizontal=random.choice([True,False])
            r=random.randrange(8); c=random.randrange(8)
            cells=[(r,c+i) for i in range(size)] if horizontal else [(r+i,c) for i in range(size)]
            if all(0<=rr<8 and 0<=cc<8 and board[rr][cc]==0 for rr,cc in cells):
                for rr,cc in cells: board[rr][cc]=1
                break

def init_battleship():
    st.session_state.bs_player=[[0]*8 for _ in range(8)]
    st.session_state.bs_bot=[[0]*8 for _ in range(8)]
    st.session_state.bs_shots=[[0]*8 for _ in range(8)]
    st.session_state.bs_bot_shots=[[0]*8 for _ in range(8)]
    place_fleet(st.session_state.bs_player,[3,2,2])
    place_fleet(st.session_state.bs_bot,[3,2,2])
    st.session_state.bs_over=False

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
    st.caption("Find and destroy the bot's fleet.")
    for r in range(8):
        cols=st.columns(8)
        for c in range(8):
            shot=st.session_state.bs_shots[r][c]
            label="💥" if shot==2 else "💧" if shot==1 else "?"
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

# ============================================================
# CHECKERS
# ============================================================
def init_checkers():
    b=[[0]*8 for _ in range(8)]
    for r in range(3):
        for c in range(8):
            if (r+c)%2:b[r][c]=2
    for r in range(5,8):
        for c in range(8):
            if (r+c)%2:b[r][c]=1
    st.session_state.chk=b
    st.session_state.chk_selected=None
    st.session_state.chk_over=False

def chk_moves(b,p):
    moves=[]; captures=[]
    dirs=[(-1,-1),(-1,1),(1,-1),(1,1)]
    for r in range(8):
        for c in range(8):
            if b[r][c] not in (p,p+2): continue
            piece=b[r][c]; king=piece in (3,4)
            ds=dirs if king else ([(-1,-1),(-1,1)] if p==1 else [(1,-1),(1,1)])
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
    b=st.session_state.chk; piece=b[r][c]
    b[r][c]=0; b[rr][cc]=piece
    if cap:b[cap[0]][cap[1]]=0
    if piece==1 and rr==0:b[rr][cc]=3
    if piece==2 and rr==7:b[rr][cc]=4

def chk_bot():
    moves=chk_moves(st.session_state.chk,2)
    if moves:
        caps=[m for m in moves if m[2] is not None]
        chk_apply(random.choice(caps if caps else moves))

def play_checkers():
    st.subheader("🏁 Checkers")
    moves=chk_moves(st.session_state.chk,1)
    selected=st.session_state.chk_selected
    for r in range(8):
        cols=st.columns(8)
        for c in range(8):
            v=st.session_state.chk[r][c]
            label={0:"·",1:"⚪",2:"⚫",3:"👑",4:"👑"}.get(v,"·")
            if selected==(r,c):label="🟢"
            if cols[c].button(label,key=f"chk{r}_{c}",use_container_width=True):
                if st.session_state.chk_over:continue
                if selected is None:
                    if v in (1,3):st.session_state.chk_selected=(r,c)
                else:
                    candidate=[m for m in moves if m[0]==selected and m[1]==(r,c)]
                    if candidate:
                        chk_apply(candidate[0]);st.session_state.chk_selected=None
                        if not chk_moves(st.session_state.chk,2):
                            st.session_state.chk_over=True;finish_game("win",reward_for("Checkers"))
                        else:
                            chk_bot()
                            if not chk_moves(st.session_state.chk,1):
                                st.session_state.chk_over=True;finish_game("loss")
                    elif v in (1,3):
                        st.session_state.chk_selected=(r,c)
                    else:st.session_state.chk_selected=None
                    st.rerun()

# ============================================================
# CHESS
# ============================================================
def init_chess():
    st.session_state.chess_board=chess.Board() if chess else None
    st.session_state.chess_selected=None
    st.session_state.chess_over=False

def chess_bot():
    b=st.session_state.chess_board
    moves=list(b.legal_moves)
    if not moves:return
    captures=[m for m in moves if b.is_capture(m)]
    checks=[m for m in moves if b.gives_check(m)]
    if bot_strength()>=2 and checks:move=random.choice(checks)
    elif captures:move=random.choice(captures)
    else:move=random.choice(moves)
    b.push(move)

def play_chess():
    st.subheader("♟ Chess")
    if chess is None:
        st.error("Add python-chess to requirements.txt.")
        return
    b=st.session_state.chess_board
    if b.is_game_over():
        st.info("Game over.")
        return
    files="abcdefgh";ranks="87654321";legal=list(b.legal_moves)
    selected=st.session_state.chess_selected
    for ri in range(8):
        cols=st.columns(8)
        for ci in range(8):
            sq=chess.parse_square(files[ci]+ranks[ri])
            piece=b.piece_at(sq)
            symbol=piece.unicode_symbol() if piece else "·"
            target=selected is not None and any(m.from_square==selected and m.to_square==sq for m in legal)
            if target:symbol="🟢"
            if cols[ci].button(symbol,key=f"chess{ri}_{ci}",use_container_width=True):
                if b.turn != chess.WHITE or st.session_state.chess_over:continue
                if selected is None:
                    if piece and piece.color==chess.WHITE:st.session_state.chess_selected=sq
                else:
                    move=next((m for m in legal if m.from_square==selected and m.to_square==sq),None)
                    if move:
                        b.push(move);st.session_state.chess_selected=None
                        if b.is_game_over():
                            st.session_state.chess_over=True
                            finish_game("win" if b.is_checkmate() else "draw",reward_for("Chess") if b.is_checkmate() else 0)
                        else:
                            chess_bot()
                            if b.is_game_over():
                                st.session_state.chess_over=True
                                finish_game("loss" if b.is_checkmate() else "draw")
                    elif piece and piece.color==chess.WHITE:st.session_state.chess_selected=sq
                    else:st.session_state.chess_selected=None
                    st.rerun()
    st.caption("You are White. Select a piece, then its destination.")

# ============================================================
# BLACKJACK — 2D CASINO TABLE
# ============================================================
SUITS=["♠","♥","♦","♣"]
RANKS=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

def make_deck():
    return [(r,s) for s in SUITS for r in RANKS]

def card_value(cards):
    total=0; aces=0
    for r,_ in cards:
        if r=="A":total+=11;aces+=1
        elif r in ("K","Q","J"):total+=10
        else:total+=int(r)
    while total>21 and aces:
        total-=10;aces-=1
    return total

def init_blackjack():
    st.session_state.bj_deck=make_deck();random.shuffle(st.session_state.bj_deck)
    st.session_state.bj_player=[];st.session_state.bj_dealer=[]
    st.session_state.bj_bet=25
    st.session_state.bj_active=False;st.session_state.bj_over=False
    st.session_state.bj_message="Place your bet to begin."
    st.session_state.bj_last_payout=0

def bj_draw():
    if not st.session_state.bj_deck:
        st.session_state.bj_deck=make_deck();random.shuffle(st.session_state.bj_deck)
    return st.session_state.bj_deck.pop()

def bj_start():
    bet=int(st.session_state.bj_bet)
    if bet<=0 or bet>st.session_state.balance:
        st.session_state.bj_message="Not enough BOT BUCKS for that bet."
        return
    st.session_state.balance-=bet
    st.session_state.total_lost+=bet
    st.session_state.bj_player=[bj_draw(),bj_draw()]
    st.session_state.bj_dealer=[bj_draw(),bj_draw()]
    st.session_state.bj_active=True;st.session_state.bj_over=False
    st.session_state.bj_message=""
    pv=card_value(st.session_state.bj_player);dv=card_value(st.session_state.bj_dealer)
    if pv==21:
        profit=int(bet*1.5);st.session_state.balance+=bet+profit
        st.session_state.total_earned+=profit;st.session_state.biggest_win=max(st.session_state.biggest_win,profit)
        st.session_state.bj_message=f"BLACKJACK! +{profit:,} BB"
        st.session_state.bj_over=True;unlock("Blackjack!")
    elif dv==21:
        st.session_state.balance+=bet
        st.session_state.bj_message="Dealer blackjack — push."
        st.session_state.bj_over=True

def bj_finish():
    bet=int(st.session_state.bj_bet)
    pv=card_value(st.session_state.bj_player)
    if pv>21:
        st.session_state.bj_message=f"BUST — you lost {bet:,} BB."
        st.session_state.bj_over=True;return
    while card_value(st.session_state.bj_dealer)<17:
        st.session_state.bj_dealer.append(bj_draw())
    dv=card_value(st.session_state.bj_dealer)
    if dv>21 or pv>dv:
        st.session_state.balance+=bet*2
        st.session_state.total_earned+=bet;st.session_state.biggest_win=max(st.session_state.biggest_win,bet)
        st.session_state.bj_message=f"YOU WIN — +{bet:,} BB"
        if bet>=500:unlock("High Roller")
    elif pv==dv:
        st.session_state.balance+=bet;st.session_state.bj_message="PUSH — bet returned."
    else:
        st.session_state.bj_message=f"DEALER WINS — you lost {bet:,} BB."
    st.session_state.bj_over=True

def card_html(card, hidden=False):
    if hidden:
        return "<div class='playing-card card-back'></div>"
    r,s=card
    red=s in ("♥","♦")
    cls="card-red" if red else "card-black"
    return f"""
    <div class="playing-card {cls}">
        <div class="corner">{r}<br>{s}</div>
        <div class="suit-center">{s}</div>
        <div class="corner" style="position:absolute;right:7px;bottom:6px;transform:rotate(180deg)">{r}<br>{s}</div>
    </div>
    """

def cards_html(cards, hide_first=False):
    return "<div class='cards'>" + "".join(card_html(c, hide_first and i==0) for i,c in enumerate(cards)) + "</div>"

def chip_html(amount):
    return f"<div class='casino-chip'>{amount}</div>"

def play_blackjack():
    st.markdown("<div class='blackjack-wrap'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="blackjack-table">
        <div class="casino-title">BOT BOARD CASINO</div>
        <div class="casino-subtitle">BLACKJACK • DEALER STANDS ON 17</div>
    """, unsafe_allow_html=True)

    # Dealer
    st.markdown("<div class='hand-zone'><div class='hand-label'>Dealer</div>", unsafe_allow_html=True)
    dealer=st.session_state.bj_dealer
    hide=not st.session_state.bj_over
    if dealer:
        st.markdown(cards_html(dealer,hide),unsafe_allow_html=True)
        total="?" if hide else str(card_value(dealer))
    else:
        st.markdown("<div class='cards'></div>",unsafe_allow_html=True)
        total="—"
    st.markdown(f"<div class='hand-total'>{total}</div></div>",unsafe_allow_html=True)

    # Middle status
    msg=st.session_state.bj_message or "Good luck."
    st.markdown(f"<div class='bj-status'>{msg}</div>",unsafe_allow_html=True)

    # Player
    st.markdown("<div class='hand-zone'><div class='hand-label'>Your Hand</div>",unsafe_allow_html=True)
    player=st.session_state.bj_player
    if player:
        st.markdown(cards_html(player),unsafe_allow_html=True)
        total=str(card_value(player))
    else:
        st.markdown("<div class='cards'></div>",unsafe_allow_html=True)
        total="—"
    st.markdown(f"<div class='hand-total'>{total}</div></div>",unsafe_allow_html=True)

    # Chips
    bet=int(st.session_state.bj_bet)
    st.markdown("<div class='chip-row'>"+chip_html(bet)+"</div>",unsafe_allow_html=True)

    st.markdown("<div class='bj-controls'>",unsafe_allow_html=True)
    if not st.session_state.bj_active and not st.session_state.bj_over:
        st.markdown("<div style='text-align:center;color:white;font-weight:800;margin-bottom:8px'>SELECT YOUR BET</div>",unsafe_allow_html=True)
        options=[x for x in [10,25,50,100,250,500] if x<=st.session_state.balance]
        if options:
            selected=st.radio("Bet",options,horizontal=True,key="bj_bet_radio",label_visibility="collapsed")
            st.session_state.bj_bet=selected
            st.markdown(f"<div style='text-align:center;color:white'>Bet <b>{selected:,} BB</b> • Balance <b>{st.session_state.balance:,} BB</b></div>",unsafe_allow_html=True)
            if st.button("🎴 DEAL",type="primary",use_container_width=True):
                bj_start();st.rerun()
        else:
            st.warning("You don't have enough BOT BUCKS. Claim your daily bonus from Wallet.")
    elif not st.session_state.bj_over:
        c1,c2=st.columns(2)
        with c1:
            if st.button("👊 HIT",type="primary",use_container_width=True):
                st.session_state.bj_player.append(bj_draw())
                if card_value(st.session_state.bj_player)>21:bj_finish()
                st.rerun()
        with c2:
            if st.button("✋ STAND",use_container_width=True):
                bj_finish();st.rerun()
    else:
        if st.button("🔄 NEW HAND",type="primary",use_container_width=True):
            st.session_state.bj_active=False;st.session_state.bj_over=False
            st.session_state.bj_player=[];st.session_state.bj_dealer=[]
            st.session_state.bj_message="Place your bet to begin."
            st.rerun()
    st.markdown("</div></div></div>",unsafe_allow_html=True)

# ============================================================
# ROUTER
# ============================================================
def init_game(name):
    st.session_state.game=name
    st.session_state.difficulty="Medium"
    st.session_state.reward_given=False
    st.session_state.last_result=""
    {
        "Tic Tac Toe":init_ttt,
        "Connect 4":init_connect4,
        "Checkers":init_checkers,
        "Othello":init_othello,
        "Gomoku":init_gomoku,
        "Battleship":init_battleship,
        "Chess":init_chess,
        "Blackjack":init_blackjack,
    }[name]()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🤖 BOT BOARD")
    st.caption("THE BOT ARCADE")
    st.markdown(f"### 💰 {st.session_state.balance:,} BB")
    st.divider()
    page=st.radio("Navigation",["🎮 Games","💰 Wallet","🏆 Achievements"])
    if st.session_state.game:
        st.divider()
        if st.button("← Back to Games",use_container_width=True):
            st.session_state.game=None;st.rerun()
        if st.button("↻ Restart Game",use_container_width=True):
            init_game(st.session_state.game);st.rerun()

# ============================================================
# PAGES
# ============================================================
if page=="💰 Wallet":
    st.markdown("<div class='hero'><h1>Wallet</h1><p>Your BOT BOARD arcade balance and stats.</p></div>",unsafe_allow_html=True)
    st.write("")
    cols=st.columns(3)
    for col,label,value in zip(cols,["Balance","Total earned","Total lost"],[
        f"{st.session_state.balance:,} BB",f"{st.session_state.total_earned:,} BB",f"{st.session_state.total_lost:,} BB"]):
        col.markdown(f"<div class='stat-card'><div class='stat-label'>{label}</div><div class='stat-value'>{value}</div></div>",unsafe_allow_html=True)
    st.write("")
    cols=st.columns(3)
    for col,label,value in zip(cols,["Biggest win","Current streak","Best streak"],[
        f"{st.session_state.biggest_win:,} BB",st.session_state.streak,st.session_state.best_streak]):
        col.markdown(f"<div class='stat-card'><div class='stat-label'>{label}</div><div class='stat-value'>{value}</div></div>",unsafe_allow_html=True)
    st.write("")
    if not st.session_state.daily_bonus:
        if st.button("🎁 CLAIM DAILY BONUS  +250 BB",type="primary",use_container_width=True):
            st.session_state.balance+=250;st.session_state.total_earned+=250
            st.session_state.daily_bonus=True;st.rerun()
    else:
        st.success("Daily bonus already claimed this session.")
    st.info("BOT BUCKS are fictional in-game currency only. They cannot be purchased, withdrawn or converted into real money.")

elif page=="🏆 Achievements":
    st.markdown("<div class='hero'><h1>Achievements</h1><p>Build your record and collect every badge.</p></div>",unsafe_allow_html=True)
    all_ach=[
        ("First Win","Win your first game"),
        ("Hot Streak","Win 5 games in a row"),
        ("Big Winner","Earn 1,000 BOT BUCKS"),
        ("Blackjack!","Get a natural blackjack"),
        ("High Roller","Win a 500 BB blackjack hand"),
    ]
    st.write("")
    for name,desc in all_ach:
        if name in st.session_state.achievements:
            st.success(f"🏆 **{name}** — {desc}")
        else:
            st.markdown(f"<div class='stat-card'>🔒 <b>{name}</b><br><span style='color:#8d98aa'>{desc}</span></div><br>",unsafe_allow_html=True)

else:
    if st.session_state.game is None:
        st.markdown(
            f"<div class='hero'><h1>BOT BOARD</h1><p>Beat the bots. Build your balance. Own the leaderboard.</p><div class='balance-pill'>💰 {st.session_state.balance:,} BOT BUCKS</div></div>",
            unsafe_allow_html=True
        )
        st.write("")
        st.markdown("### 🎮 Choose a game")
        games=[
            ("🎯","Tic Tac Toe","Quick classic strategy."),
            ("🟡","Connect 4","Get four in a row."),
            ("🏁","Checkers","Capture the bot's pieces."),
            ("🟢","Othello","Flip the board."),
            ("🟨","Gomoku","Five in a row."),
            ("🛳️","Battleship","Find and sink the fleet."),
            ("♟️","Chess","Classic strategy."),
            ("🃏","Blackjack","Play the full casino-style table."),
        ]
        cols=st.columns(2)
        for i,(icon,name,desc) in enumerate(games):
            with cols[i%2]:
                st.markdown(f"<div class='game-card'><div class='game-icon'>{icon}</div><h3>{name}</h3><p>{desc}</p></div>",unsafe_allow_html=True)
                if st.button(f"PLAY {name.upper()}",key=f"play_{name}",use_container_width=True):
                    init_game(name);st.rerun()
    else:
        name=st.session_state.game
        st.markdown(f"<div class='game-header'><h2 style='margin:0'>{name}</h2><span style='color:#8d98aa'>💰 {st.session_state.balance:,} BB</span></div>",unsafe_allow_html=True)
        if name!="Blackjack":
            c1,c2=st.columns([2,1])
            with c1:
                st.session_state.difficulty=st.selectbox("Bot difficulty",DIFFICULTIES,index=DIFFICULTIES.index(st.session_state.difficulty))
            with c2:
                st.metric("Win reward",f"+{reward_for(name)} BB")

        if name=="Tic Tac Toe":play_ttt()
        elif name=="Connect 4":play_connect4()
        elif name=="Checkers":play_checkers()
        elif name=="Othello":play_othello()
        elif name=="Gomoku":play_gomoku()
        elif name=="Battleship":play_battleship()
        elif name=="Chess":play_chess()
        elif name=="Blackjack":play_blackjack()

        if st.session_state.last_result and name!="Blackjack":
            if st.session_state.last_result=="win":
                st.success(f"🎉 YOU WON  •  +{reward_for(name)} BB")
            elif st.session_state.last_result=="loss":
                st.error("🤖 THE BOT WON")
            else:
                st.info("🤝 DRAW")
'''

req = "streamlit\npython-chess\n"

Path("/mnt/data/app.py").write_text(app, encoding="utf-8")
Path("/mnt/data/requirements.txt").write_text(req, encoding="utf-8")

print("Created:")
print("/mnt/data/app.py")
print("/mnt/data/requirements.txt")
print(f"app.py: {len(app.splitlines())} lines")
