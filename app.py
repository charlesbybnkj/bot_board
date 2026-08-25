import random
import streamlit as st

try:
    import chess
except ImportError:
    chess = None

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BOT BOARD",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# MODERN UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #172554 0%, transparent 35%),
        radial-gradient(circle at top right, #312e81 0%, transparent 30%),
        #070b14;
    color: white;
}

[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid #1e293b;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    padding: 38px;
    border-radius: 28px;
    margin-bottom: 24px;
    background:
        linear-gradient(135deg, rgba(30,41,59,.95), rgba(49,46,129,.9)),
        #111827;
    border: 1px solid #334155;
    box-shadow: 0 20px 60px rgba(0,0,0,.3);
}

.hero h1 {
    font-size: 52px;
    font-weight: 900;
    margin: 0;
    color: white;
}

.hero p {
    color: #cbd5e1;
    font-size: 18px;
    margin: 8px 0 0;
}

.wallet {
    background: linear-gradient(135deg,#111827,#172033);
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,.2);
}

.wallet-number {
    font-size: 30px;
    font-weight: 900;
    color: #facc15;
}

.game-card {
    overflow: hidden;
    border-radius: 22px;
    background: #111827;
    border: 1px solid #263244;
    box-shadow: 0 12px 35px rgba(0,0,0,.28);
    margin-bottom: 10px;
}

.game-card img {
    width: 100%;
    height: 190px;
    object-fit: cover;
    display: block;
}

.game-info {
    padding: 18px;
}

.game-title {
    font-size: 24px;
    font-weight: 900;
}

.game-description {
    color: #94a3b8;
    margin-top: 5px;
    min-height: 25px;
}

.section-title {
    font-size: 28px;
    font-weight: 900;
    margin: 25px 0 15px;
}

.result-box {
    padding: 18px;
    border-radius: 18px;
    background: #111827;
    border: 1px solid #334155;
    text-align: center;
    font-size: 20px;
    font-weight: 700;
}

.metric-card {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
}

.big-number {
    font-size: 30px;
    font-weight: 900;
    color: #facc15;
}

.card {
    display: inline-flex;
    width: 72px;
    height: 102px;
    background: #fff;
    color: #111;
    border-radius: 10px;
    margin: 4px;
    align-items: center;
    justify-content: center;
    font-size: 29px;
    font-weight: 700;
    box-shadow: 0 8px 18px rgba(0,0,0,.3);
}

.redcard {
    color: #dc2626;
}

.blackjack-table {
    background:
        radial-gradient(circle at center, #15803d, #064e3b);
    border: 12px solid #713f12;
    border-radius: 180px;
    padding: 50px 30px;
    min-height: 520px;
    box-shadow:
        inset 0 0 50px rgba(0,0,0,.45),
        0 20px 50px rgba(0,0,0,.4);
}

.table-label {
    text-align: center;
    color: #d1fae5;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 15px;
}

.total {
    text-align: center;
    color: white;
    font-size: 22px;
    font-weight: 900;
}

.chip {
    display: inline-block;
    padding: 10px 18px;
    border-radius: 50%;
    background: #dc2626;
    border: 4px dashed white;
    color: white;
    font-weight: 900;
}

div[data-testid="stButton"] > button {
    border-radius: 12px;
    font-weight: 800;
    min-height: 42px;
}

@media (max-width: 750px) {
    .hero h1 {
        font-size: 36px;
    }

    .game-card img {
        height: 160px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
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
    "reward_given": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

DIFFICULTIES = ["Easy", "Medium", "Hard", "Impossible"]

REWARDS = {
    "Tic Tac Toe": {"Easy":25,"Medium":50,"Hard":100,"Impossible":200},
    "Connect 4": {"Easy":50,"Medium":100,"Hard":200,"Impossible":400},
    "Checkers": {"Easy":75,"Medium":150,"Hard":300,"Impossible":600},
    "Othello": {"Easy":100,"Medium":200,"Hard":400,"Impossible":800},
    "Gomoku": {"Easy":75,"Medium":150,"Hard":300,"Impossible":600},
    "Battleship": {"Easy":100,"Medium":200,"Hard":400,"Impossible":800},
    "Chess": {"Easy":150,"Medium":300,"Hard":600,"Impossible":1200}
}

def unlock(name):
    st.session_state.achievements.add(name)

def add_money(amount):
    st.session_state.balance += amount

    if amount > 0:
        st.session_state.total_earned += amount
        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            amount
        )

    if amount < 0:
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
        st.session_state.best_streak = max(
            st.session_state.best_streak,
            st.session_state.streak
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

def bot_strength():
    return DIFFICULTIES.index(st.session_state.difficulty)

def reward_for(name):
    return REWARDS.get(name, {}).get(
        st.session_state.difficulty,
        0
    )

# =========================================================
# TIC TAC TOE
# =========================================================

def init_ttt():
    st.session_state.ttt = [""] * 9
    st.session_state.ttt_over = False

def ttt_winner(b):
    lines = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b1,c in lines:
        if b[a] and b[a] == b[b1] == b[c]:
            return b[a]

    return "draw" if all(b) else None

def ttt_bot():
    b = st.session_state.ttt
    empty = [i for i,x in enumerate(b) if not x]

    if not empty:
        return

    for i in empty:
        b[i] = "O"
        if ttt_winner(b) == "O":
            return
        b[i] = ""

    for i in empty:
        b[i] = "X"
        if ttt_winner(b) == "X":
            b[i] = "O"
            return
        b[i] = ""

    if bot_strength() >= 2:
        if 4 in empty:
            b[4] = "O"
            return

    b[random.choice(empty)] = "O"

def play_ttt():

    st.markdown("## ❌ Tic Tac Toe")

    cols = st.columns(3)

    for i in range(9):

        with cols[i % 3]:

            label = st.session_state.ttt[i] or " "

            if st.button(
                label,
                key=f"ttt{i}",
                use_container_width=True
            ):

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
                        ttt_bot()

                        result = ttt_winner(st.session_state.ttt)

                        if result:
                            st.session_state.ttt_over = True
                            finish_game(
                                "loss" if result == "O" else "draw"
                            )

                    st.rerun()

# =========================================================
# CONNECT 4
# =========================================================

def init_connect4():
    st.session_state.c4 = [[0]*7 for _ in range(6)]
    st.session_state.c4_over = False

def c4_winner(board):

    for r in range(6):
        for c in range(7):

            p = board[r][c]

            if not p:
                continue

            for dr,dc in [(1,0),(0,1),(1,1),(1,-1)]:

                cells = []

                for k in range(4):

                    rr = r + dr*k
                    cc = c + dc*k

                    if 0 <= rr < 6 and 0 <= cc < 7:
                        cells.append(board[rr][cc])

                if len(cells) == 4 and cells == [p]*4:
                    return p

    return None

def c4_drop(col, player):

    for r in range(5,-1,-1):

        if st.session_state.c4[r][col] == 0:
            st.session_state.c4[r][col] = player
            return r

    return None

def c4_bot():

    valid = [
        c for c in range(7)
        if st.session_state.c4[0][c] == 0
    ]

    if not valid:
        return

    for c in valid:
        r = c4_drop(c,2)

        if c4_winner(st.session_state.c4) == 2:
            return

        st.session_state.c4[r][c] = 0

    for c in valid:

        r = c4_drop(c,1)

        if c4_winner(st.session_state.c4) == 1:

            st.session_state.c4[r][c] = 0
            c4_drop(c,2)
            return

        st.session_state.c4[r][c] = 0

    preferred = [3,2,4,1,5,0,6]

    choices = [x for x in preferred if x in valid]

    c4_drop(random.choice(choices),2)

def play_connect4():

    st.markdown("## 🟡 Connect 4")

    cols = st.columns(7)

    for c in range(7):

        with cols[c]:

            if st.button(
                "↓",
                key=f"c4{c}",
                use_container_width=True,
                disabled=st.session_state.c4_over
            ):

                if c4_drop(c,1) is not None:

                    w = c4_winner(st.session_state.c4)

                    if w == 1:
                        st.session_state.c4_over = True
                        finish_game("win", reward_for("Connect 4"))

                    else:
                        c4_bot()

                        w = c4_winner(st.session_state.c4)

                        if w == 2:
                            st.session_state.c4_over = True
                            finish_game("loss")

                    st.rerun()

    symbols = {
        0:"⚪",
        1:"🔴",
        2:"🟡"
    }

    for row in st.session_state.c4:

        cols = st.columns(7)

        for c,value in enumerate(row):
            cols[c].markdown(
                f"<div class='total'>{symbols[value]}</div>",
                unsafe_allow_html=True
            )

# =========================================================
# CHECKERS
# =========================================================

def init_checkers():

    board = [[0]*8 for _ in range(8)]

    for r in range(3):
        for c in range(8):
            if (r+c)%2:
                board[r][c] = 2

    for r in range(5,8):
        for c in range(8):
            if (r+c)%2:
                board[r][c] = 1

    st.session_state.chk = board
    st.session_state.chk_selected = None
    st.session_state.chk_over = False

def chk_moves(board, player):

    moves = []

    directions = [
        (-1,-1),(-1,1),
        (1,-1),(1,1)
    ]

    for r in range(8):
        for c in range(8):

            piece = board[r][c]

            if piece not in [player, player+2]:
                continue

            king = piece >= 3

            dirs = directions if king else (
                [(-1,-1),(-1,1)]
                if player == 1
                else [(1,-1),(1,1)]
            )

            for dr,dc in dirs:

                rr,cc = r+dr,c+dc

                if 0 <= rr < 8 and 0 <= cc < 8:

                    if board[rr][cc] == 0:
                        moves.append(((r,c),(rr,cc),None))

                    elif board[rr][cc] not in [0,player,player+2]:

                        jr,jc = rr+dr,cc+dc

                        if (
                            0 <= jr < 8 and
                            0 <= jc < 8 and
                            board[jr][jc] == 0
                        ):
                            moves.append(
                                ((r,c),(jr,jc),(rr,cc))
                            )

    captures = [m for m in moves if m[2]]

    return captures if captures else moves

def chk_apply(move):

    (r,c),(rr,cc),cap = move

    board = st.session_state.chk

    piece = board[r][c]

    board[r][c] = 0
    board[rr][cc] = piece

    if cap:
        board[cap[0]][cap[1]] = 0

    if piece == 1 and rr == 0:
        board[rr][cc] = 3

    if piece == 2 and rr == 7:
        board[rr][cc] = 4

def chk_bot():

    moves = chk_moves(st.session_state.chk,2)

    if moves:
        captures = [m for m in moves if m[2]]
        chk_apply(random.choice(captures or moves))

def play_checkers():

    st.markdown("## 🏁 Checkers")

    moves = chk_moves(st.session_state.chk,1)
    selected = st.session_state.chk_selected

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            value = st.session_state.chk[r][c]

            symbols = {
                0:"·",
                1:"⚪",
                2:"⚫",
                3:"👑",
                4:"👑"
            }

            label = symbols[value]

            if selected == (r,c):
                label = "🟢"

            if cols[c].button(
                label,
                key=f"chk{r}_{c}",
                use_container_width=True
            ):

                if selected is None:

                    if value in [1,3]:
                        st.session_state.chk_selected = (r,c)

                else:

                    candidate = [
                        m for m in moves
                        if m[0] == selected and m[1] == (r,c)
                    ]

                    if candidate:

                        chk_apply(candidate[0])
                        st.session_state.chk_selected = None

                        if not chk_moves(st.session_state.chk,2):
                            st.session_state.chk_over = True
                            finish_game(
                                "win",
                                reward_for("Checkers")
                            )
                        else:
                            chk_bot()

                            if not chk_moves(st.session_state.chk,1):
                                st.session_state.chk_over = True
                                finish_game("loss")

                    elif value in [1,3]:
                        st.session_state.chk_selected = (r,c)

                    else:
                        st.session_state.chk_selected = None

                    st.rerun()

# =========================================================
# OTHELLO
# =========================================================

DIRS = [
    (dr,dc)
    for dr in (-1,0,1)
    for dc in (-1,0,1)
    if (dr,dc) != (0,0)
]

def init_othello():

    board = [[0]*8 for _ in range(8)]

    board[3][3] = 2
    board[4][4] = 2
    board[3][4] = 1
    board[4][3] = 1

    st.session_state.oth = board
    st.session_state.oth_over = False

def oth_moves(board, player):

    result = []
    opponent = 3-player

    for r in range(8):
        for c in range(8):

            if board[r][c]:
                continue

            valid = False

            for dr,dc in DIRS:

                rr,cc = r+dr,c+dc
                seen = False

                while (
                    0 <= rr < 8 and
                    0 <= cc < 8 and
                    board[rr][cc] == opponent
                ):
                    seen = True
                    rr += dr
                    cc += dc

                if (
                    seen and
                    0 <= rr < 8 and
                    0 <= cc < 8 and
                    board[rr][cc] == player
                ):
                    valid = True
                    break

            if valid:
                result.append((r,c))

    return result

def oth_play(r,c,player):

    board = st.session_state.oth

    board[r][c] = player
    opponent = 3-player

    for dr,dc in DIRS:

        path = []
        rr,cc = r+dr,c+dc

        while (
            0 <= rr < 8 and
            0 <= cc < 8 and
            board[rr][cc] == opponent
        ):
            path.append((rr,cc))
            rr += dr
            cc += dc

        if (
            path and
            0 <= rr < 8 and
            0 <= cc < 8 and
            board[rr][cc] == player
        ):
            for pr,pc in path:
                board[pr][pc] = player

def oth_bot():

    moves = oth_moves(st.session_state.oth,2)

    if not moves:
        return

    corners = [
        (0,0),(0,7),
        (7,0),(7,7)
    ]

    move = random.choice(moves)

    for m in moves:
        if m in corners:
            move = m
            break

    oth_play(*move,2)

def play_othello():

    st.markdown("## 🟢 Othello")

    legal = oth_moves(st.session_state.oth,1)

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            value = st.session_state.oth[r][c]

            if value == 1:
                label = "⚪"
            elif value == 2:
                label = "⚫"
            elif (r,c) in legal:
                label = "🟢"
            else:
                label = "·"

            if cols[c].button(
                label,
                key=f"oth{r}_{c}",
                use_container_width=True
            ):

                if (r,c) in legal:

                    oth_play(r,c,1)

                    if oth_moves(st.session_state.oth,2):
                        oth_bot()

                    else:
                        if not oth_moves(st.session_state.oth,1):
                            p = sum(row.count(1) for row in st.session_state.oth)
                            q = sum(row.count(2) for row in st.session_state.oth)

                            st.session_state.oth_over = True

                            finish_game(
                                "win" if p > q else
                                "loss" if q > p else
                                "draw",
                                reward_for("Othello") if p > q else 0
                            )

                    st.rerun()

# =========================================================
# GOMOKU
# =========================================================

def init_gomoku():

    st.session_state.gom = [[0]*15 for _ in range(15)]
    st.session_state.gom_over = False

def gom_win(board,r,c,player):

    for dr,dc in DIRS:

        count = 1

        for sign in [1,-1]:

            rr = r + dr*sign
            cc = c + dc*sign

            while (
                0 <= rr < 15 and
                0 <= cc < 15 and
                board[rr][cc] == player
            ):
                count += 1
                rr += dr*sign
                cc += dc*sign

        if count >= 5:
            return True

    return False

def gom_bot():

    board = st.session_state.gom

    empty = [
        (r,c)
        for r in range(15)
        for c in range(15)
        if board[r][c] == 0
    ]

    if not empty:
        return

    for player in [2,1]:

        for r,c in empty:

            board[r][c] = player

            if gom_win(board,r,c,player):

                if player == 2:
                    return

            board[r][c] = 0

    center = (7,7)

    if board[7][7] == 0:
        board[7][7] = 2
    else:
        board[random.choice(empty)] = 2

def play_gomoku():

    st.markdown("## 🟨 Gomoku")

    for r in range(15):

        cols = st.columns(15)

        for c in range(15):

            value = st.session_state.gom[r][c]

            label = "⚫" if value == 2 else "⚪" if value == 1 else "·"

            if cols[c].button(
                label,
                key=f"gom{r}_{c}",
                use_container_width=True
            ):

                if not st.session_state.gom_over and value == 0:

                    st.session_state.gom[r][c] = 1

                    if gom_win(st.session_state.gom,r,c,1):

                        st.session_state.gom_over = True
                        finish_game(
                            "win",
                            reward_for("Gomoku")
                        )

                    else:

                        gom_bot()

                        won = False

                        for rr in range(15):
                            for cc in range(15):

                                if (
                                    st.session_state.gom[rr][cc] == 2 and
                                    gom_win(
                                        st.session_state.gom,
                                        rr,
                                        cc,
                                        2
                                    )
                                ):
                                    won = True

                        if won:
                            st.session_state.gom_over = True
                            finish_game("loss")

                    st.rerun()

# =========================================================
# BATTLESHIP
# =========================================================

def place_fleet(board):

    for size in [3,2,2]:

        placed = False

        while not placed:

            horizontal = random.choice([True,False])
            r = random.randrange(8)
            c = random.randrange(8)

            cells = (
                [(r,c+i) for i in range(size)]
                if horizontal
                else
                [(r+i,c) for i in range(size)]
            )

            if all(
                0 <= rr < 8 and
                0 <= cc < 8 and
                board[rr][cc] == 0
                for rr,cc in cells
            ):

                for rr,cc in cells:
                    board[rr][cc] = 1

                placed = True

def init_battleship():

    st.session_state.bs_player = [[0]*8 for _ in range(8)]
    st.session_state.bs_bot = [[0]*8 for _ in range(8)]
    st.session_state.bs_shots = [[0]*8 for _ in range(8)]
    st.session_state.bs_bot_shots = [[0]*8 for _ in range(8)]
    st.session_state.bs_over = False

    place_fleet(st.session_state.bs_player)
    place_fleet(st.session_state.bs_bot)

def bs_remaining(board):
    return sum(
        cell == 1
        for row in board
        for cell in row
    )

def bs_bot_shot():

    available = [
        (r,c)
        for r in range(8)
        for c in range(8)
        if st.session_state.bs_bot_shots[r][c] == 0
    ]

    if not available:
        return

    r,c = random.choice(available)

    st.session_state.bs_bot_shots[r][c] = 1

    if st.session_state.bs_player[r][c] == 1:
        st.session_state.bs_player[r][c] = 2

def play_battleship():

    st.markdown("## 🚢 Battleship")

    st.caption("💥 Hit   •   💧 Miss   •   ❓ Unknown")

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            shot = st.session_state.bs_shots[r][c]

            label = (
                "💥" if shot == 2
                else "💧" if shot == 1
                else "❓"
            )

            if cols[c].button(
                label,
                key=f"bs{r}_{c}",
                use_container_width=True
            ):

                if not st.session_state.bs_over and shot == 0:

                    if st.session_state.bs_bot[r][c] == 1:

                        st.session_state.bs_bot[r][c] = 2
                        st.session_state.bs_shots[r][c] = 2

                    else:
                        st.session_state.bs_shots[r][c] = 1

                    if bs_remaining(st.session_state.bs_bot) == 0:

                        st.session_state.bs_over = True

                        finish_game(
                            "win",
                            reward_for("Battleship")
                        )

                    else:

                        bs_bot_shot()

                        if bs_remaining(st.session_state.bs_player) == 0:

                            st.session_state.bs_over = True
                            finish_game("loss")

                    st.rerun()

# =========================================================
# CHESS
# =========================================================

def init_chess():

    if chess:

        st.session_state.chess_board = chess.Board()

    else:

        st.session_state.chess_board = None

    st.session_state.chess_selected = None
    st.session_state.chess_over = False

def chess_bot():

    board = st.session_state.chess_board

    moves = list(board.legal_moves)

    if not moves:
        return

    captures = [
        m for m in moves
        if board.is_capture(m)
    ]

    if captures and bot_strength() >= 1:
        board.push(random.choice(captures))
    else:
        board.push(random.choice(moves))

def play_chess():

    st.markdown("## ♟ Chess")

    if chess is None:

        st.error(
            "Chess dependency missing. Add python-chess to requirements.txt."
        )

        return

    board = st.session_state.chess_board

    if board.is_game_over():

        st.info("Game over.")

        return

    files = "abcdefgh"
    ranks = "87654321"

    legal = list(board.legal_moves)

    selected = st.session_state.chess_selected

    for ri in range(8):

        cols = st.columns(8)

        for ci in range(8):

            square = chess.parse_square(
                files[ci] + ranks[ri]
            )

            piece = board.piece_at(square)

            symbol = piece.symbol() if piece else "·"

            target = (
                selected is not None and
                any(
                    m.from_square == selected and
                    m.to_square == square
                    for m in legal
                )
            )

            if target:
                symbol = "🟢"

            if cols[ci].button(
                symbol,
                key=f"chess{ri}_{ci}",
                use_container_width=True
            ):

                if board.turn != chess.WHITE:
                    continue

                if selected is None:

                    if piece and piece.color == chess.WHITE:
                        st.session_state.chess_selected = square

                else:

                    move = next(
                        (
                            m for m in legal
                            if m.from_square == selected
                            and m.to_square == square
                        ),
                        None
                    )

                    if move:

                        board.push(move)

                        st.session_state.chess_selected = None

                        if board.is_game_over():

                            st.session_state.chess_over = True

                            if board.is_checkmate():
                                finish_game(
                                    "win",
                                    reward_for("Chess")
                                )
                            else:
                                finish_game("draw")

                        else:

                            chess_bot()

                            if board.is_game_over():

                                st.session_state.chess_over = True

                                if board.is_checkmate():
                                    finish_game("loss")
                                else:
                                    finish_game("draw")

                    elif piece and piece.color == chess.WHITE:

                        st.session_state.chess_selected = square

                    else:

                        st.session_state.chess_selected = None

                    st.rerun()

    st.caption("You are White. Select a piece and then select its destination.")

# =========================================================
# BLACKJACK
# =========================================================

SUITS = ["♠","♥","♦","♣"]

RANKS = [
    "A","2","3","4","5","6","7",
    "8","9","10","J","Q","K"
]

def make_deck():
    return [
        (rank,suit)
        for suit in SUITS
        for rank in RANKS
    ]

def card_value(cards):

    total = 0
    aces = 0

    for rank,_ in cards:

        if rank == "A":
            total += 11
            aces += 1

        elif rank in ["K","Q","J"]:
            total += 10

        else:
            total += int(rank)

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total

def init_blackjack():

    deck = make_deck()
    random.shuffle(deck)

    st.session_state.bj_deck = deck
    st.session_state.bj_player = []
    st.session_state.bj_dealer = []
    st.session_state.bj_bet = 25
    st.session_state.bj_active = False
    st.session_state.bj_over = False
    st.session_state.bj_message = ""

def bj_draw():

    if not st.session_state.bj_deck:

        st.session_state.bj_deck = make_deck()
        random.shuffle(st.session_state.bj_deck)

    return st.session_state.bj_deck.pop()

def bj_start():

    bet = int(st.session_state.bj_bet)

    if bet <= 0 or bet > st.session_state.balance:

        st.session_state.bj_message = "Not enough BOT BUCKS."

        return

    st.session_state.balance -= bet
    st.session_state.total_lost += bet

    st.session_state.bj_player = [
        bj_draw(),
        bj_draw()
    ]

    st.session_state.bj_dealer = [
        bj_draw(),
        bj_draw()
    ]

    st.session_state.bj_active = True
    st.session_state.bj_over = False
    st.session_state.bj_message = ""

    if card_value(st.session_state.bj_player) == 21:

        profit = int(bet * 1.5)

        st.session_state.balance += bet + profit
        st.session_state.total_earned += profit
        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            profit
        )

        st.session_state.bj_message = (
            f"🃏 BLACKJACK! +{profit} BB"
        )

        st.session_state.bj_over = True

        unlock("Blackjack!")

def bj_finish():

    bet = int(st.session_state.bj_bet)

    player = card_value(st.session_state.bj_player)

    if player > 21:

        st.session_state.bj_message = (
            f"💥 Bust! -{bet} BB"
        )

        st.session_state.bj_over = True

        return

    while card_value(st.session_state.bj_dealer) < 17:
        st.session_state.bj_dealer.append(
            bj_draw()
        )

    dealer = card_value(st.session_state.bj_dealer)

    if dealer > 21 or player > dealer:

        st.session_state.balance += bet * 2
        st.session_state.total_earned += bet
        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            bet
        )

        st.session_state.bj_message = (
            f"🎉 You win! +{bet} BB"
        )

        if bet >= 500:
            unlock("High Roller")

    elif player == dealer:

        st.session_state.balance += bet

        st.session_state.bj_message = (
            "🤝 Push — bet returned."
        )

    else:

        st.session_state.bj_message = (
            f"🤖 Dealer wins. -{bet} BB"
        )

    st.session_state.bj_over = True

def render_cards(cards, hidden=False):

    html = ""

    for i,(rank,suit) in enumerate(cards):

        if hidden and i == 0:

            html += """
            <span class="card"
            style="
            background:
            repeating-linear-gradient(
                45deg,
                #172554,
                #172554 8px,
                #1e40af 8px,
                #1e40af 16px
            );
            color:white;
            ">
            🂠
            </span>
            """

        else:

            red = suit in ["♥","♦"]

            html += f"""
            <span class="card {'redcard' if red else ''}">
                {rank}{suit}
            </span>
            """

    st.markdown(
        f"<div style='text-align:center'>{html}</div>",
        unsafe_allow_html=True
    )

def play_blackjack():

    st.markdown("## 🃏 Blackjack")

    st.caption(
        "BOT BUCKS are fictional in-game currency."
    )

    # -------------------------
    # Betting screen
    # -------------------------

    if not st.session_state.bj_active:

        st.markdown(
            f"""
            <div class="blackjack-table">

                <div class="table-label">
                    BOT BOARD CASINO
                </div>

                <div class="total">
                    💰 {st.session_state.balance:,} BB
                </div>

                <br>

                <div style="
                    text-align:center;
                    color:#dcfce7;
                    font-size:18px;
                    font-weight:700;
                ">
                    PLACE YOUR BET
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 💰 Choose your bet")

        available = [
            x for x in [10,25,50,100,250,500]
            if x <= st.session_state.balance
        ]

        if available:

            st.session_state.bj_bet = st.radio(
                "Bet",
                available,
                horizontal=True,
                key="bj_bet_select"
            )

            if st.button(
                "🃏 DEAL CARDS",
                type="primary",
                use_container_width=True
            ):

                bj_start()
                st.rerun()

        else:

            st.warning("You don't have enough BOT BUCKS.")

        return

    # -------------------------
    # Actual table
    # -------------------------

    dealer_hidden = not st.session_state.bj_over

    st.markdown(
        "<div class='blackjack-table'>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='table-label'>DEALER</div>",
        unsafe_allow_html=True
    )

    render_cards(
        st.session_state.bj_dealer,
        hidden=dealer_hidden
    )

    if st.session_state.bj_over:

        st.markdown(
            f"""
            <div class="total">
                Dealer: {card_value(st.session_state.bj_dealer)}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "<br><div class='table-label'>YOUR HAND</div>",
        unsafe_allow_html=True
    )

    render_cards(
        st.session_state.bj_player
    )

    st.markdown(
        f"""
        <div class="total">
            {card_value(st.session_state.bj_player)}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # -------------------------
    # Controls
    # -------------------------

    if not st.session_state.bj_over:

        st.markdown("### Your move")

        c1,c2 = st.columns(2)

        with c1:

            if st.button(
                "👊 HIT",
                use_container_width=True,
                type="primary"
            ):

                st.session_state.bj_player.append(
                    bj_draw()
                )

                if card_value(st.session_state.bj_player) > 21:
                    bj_finish()

                st.rerun()

        with c2:

            if st.button(
                "✋ STAND",
                use_container_width=True
            ):

                bj_finish()
                st.rerun()

    else:

        st.markdown(
            f"""
            <div class="result-box">
                {st.session_state.bj_message}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🔄 PLAY AGAIN",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.bj_active = False
            st.session_state.bj_over = False
            st.session_state.bj_message = ""

            st.rerun()

# =========================================================
# GAME ROUTER
# =========================================================

def init_game(name):

    if name == "Tic Tac Toe":
        init_ttt()

    elif name == "Connect 4":
        init_connect4()

    elif name == "Checkers":
        init_checkers()

    elif name == "Othello":
        init_othello()

    elif name == "Gomoku":
        init_gomoku()

    elif name == "Battleship":
        init_battleship()

    elif name == "Chess":
        init_chess()

    elif name == "Blackjack":
        init_blackjack()

def reset_for_game(name):

    st.session_state.game = name
    st.session_state.difficulty = "Medium"
    st.session_state.reward_given = False
    st.session_state.last_result = ""

    init_game(name)

# =========================================================
# GAME IMAGES
# =========================================================

GAMES = [

    (
        "❌",
        "Tic Tac Toe",
        "Quick classic strategy.",
        "https://images.unsplash.com/photo-1611996575749-79a3a250f948?auto=format&fit=crop&w=900&q=80"
    ),

    (
        "🟡",
        "Connect 4",
        "Get four in a row.",
        "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?auto=format&fit=crop&w=900&q=80"
    ),

    (
        "🏁",
        "Checkers",
        "Capture the bot's pieces.",
        "https://images.unsplash.com/photo-1586165368502-1bad197a6461?auto=format&fit=crop&w=900&q=80"
    ),

    (
        "🟢",
        "Othello",
        "Flip the board.",
        "https://images.unsplash.com/photo-1605870445919-838d190e8e1b?auto=format&fit=crop&w=900&q=80"
    ),

    (
        "🟨",
        "Gomoku",
        "Five in a row wins.",
        "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=900&q=80"
    ),

    (
        "🚢",
        "Battleship",
        "Find and sink the fleet.",
        "https://images.unsplash.com/photo-1528127269322-539801943592?auto=format&fit=crop&w=900&q=80"
    ),

    (
        "♟️",
        "Chess",
        "Classic strategy.",
        "https://images.unsplash.com/photo-1586165368502-1bad197a6461?auto=format&fit=crop&w=900&q=80"
    ),

    (
        "🃏",
        "Blackjack",
        "Beat the dealer.",
        "https://images.unsplash.com/photo-1518893883800-45cd0954574b?auto=format&fit=crop&w=900&q=80"
    )
]

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🤖 BOT BOARD")

    st.markdown(
        f"""
        <div class="wallet">
            💰<br>
            <b>{st.session_state.balance:,} BB</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "MENU",
        [
            "🎮 Games",
            "💰 Wallet",
            "🏆 Achievements"
        ]
    )

    if st.session_state.game:

        st.divider()

        if st.button(
            "🏠 Back to Games",
            use_container_width=True
        ):

            st.session_state.game = None
            st.rerun()

        if st.button(
            "🔄 Restart Game",
            use_container_width=True
        ):

            reset_for_game(
                st.session_state.game
            )

            st.rerun()

# =========================================================
# WALLET
# =========================================================

if page == "💰 Wallet":

    st.markdown(
        """
        <div class="hero">
            <h1>💰 Wallet</h1>
            <p>Your BOT BOARD arcade balance.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Balance",
        f"{st.session_state.balance:,} BB"
    )

    c2.metric(
        "Total earned",
        f"{st.session_state.total_earned:,} BB"
    )

    c3.metric(
        "Total lost",
        f"{st.session_state.total_lost:,} BB"
    )

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Biggest win",
        f"{st.session_state.biggest_win:,} BB"
    )

    c2.metric(
        "Win streak",
        st.session_state.streak
    )

    c3.metric(
        "Best streak",
        st.session_state.best_streak
    )

    st.divider()

    if not st.session_state.daily_bonus:

        if st.button(
            "🎁 CLAIM DAILY BONUS — +250 BB",
            type="primary",
            use_container_width=True
        ):

            st.session_state.balance += 250
            st.session_state.total_earned += 250
            st.session_state.daily_bonus = True

            st.rerun()

    else:

        st.success(
            "Daily bonus already claimed this session."
        )

    st.info(
        "BOT BUCKS are fictional game currency only. "
        "They cannot be purchased, withdrawn, or converted "
        "to real money."
    )

# =========================================================
# ACHIEVEMENTS
# =========================================================

elif page == "🏆 Achievements":

    st.markdown(
        """
        <div class="hero">
            <h1>🏆 Achievements</h1>
            <p>Collect them all.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    achievements = [

        (
            "First Win",
            "Win your first game."
        ),

        (
            "Hot Streak",
            "Win 5 games in a row."
        ),

        (
            "Big Winner",
            "Earn 1,000 BOT BUCKS."
        ),

        (
            "Blackjack!",
            "Get a natural blackjack."
        ),

        (
            "High Roller",
            "Win a 500 BB blackjack hand."
        )
    ]

    for name,description in achievements:

        if name in st.session_state.achievements:

            st.success(
                f"🏆 **{name}** — {description}"
            )

        else:

            st.write(
                f"🔒 **{name}** — {description}"
            )

# =========================================================
# GAMES
# =========================================================

else:

    if st.session_state.game is None:

        st.markdown(
            """
            <div class="hero">
                <h1>🤖 BOT BOARD</h1>
                <p>Beat the bots. Build your balance.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="wallet">
                <div>YOUR BALANCE</div>
                <div class="wallet-number">
                    💰 {st.session_state.balance:,} BB
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='section-title'>🎮 Choose a game</div>",
            unsafe_allow_html=True
        )

        for i in range(0,len(GAMES),2):

            cols = st.columns(2)

            for j in range(2):

                index = i+j

                if index >= len(GAMES):
                    continue

                icon,name,description,image = GAMES[index]

                with cols[j]:

                    st.markdown(
                        f"""
                        <div class="game-card">

                            <img src="{image}">

                            <div class="game-info">

                                <div class="game-title">
                                    {icon} {name}
                                </div>

                                <div class="game-description">
                                    {description}
                                </div>

                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        f"PLAY {name.upper()}",
                        key=f"play_{name}",
                        use_container_width=True,
                        type="primary"
                    ):

                        reset_for_game(name)
                        st.rerun()

    else:

        name = st.session_state.game

        top1,top2,top3 = st.columns([2,2,1])

        with top1:
            st.markdown(
                f"## {name}"
            )

        with top2:

            if name != "Blackjack":

                st.session_state.difficulty = st.selectbox(
                    "Bot difficulty",
                    DIFFICULTIES,
                    index=DIFFICULTIES.index(
                        st.session_state.difficulty
                    )
                )

        with top3:

            st.markdown(
                f"""
                <div class="wallet">
                    💰<br>
                    <b>{st.session_state.balance:,} BB</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        if name == "Tic Tac Toe":
            play_ttt()

        elif name == "Connect 4":
            play_connect4()

        elif name == "Checkers":
            play_checkers()

        elif name == "Othello":
            play_othello()

        elif name == "Gomoku":
            play_gomoku()

        elif name == "Battleship":
            play_battleship()

        elif name == "Chess":
            play_chess()

        elif name == "Blackjack":
            play_blackjack()

        if (
            st.session_state.last_result
            and name != "Blackjack"
        ):

            if st.session_state.last_result == "win":

                st.success(
                    f"🎉 You won! +{reward_for(name)} BB"
                )

            elif st.session_state.last_result == "loss":

                st.error(
                    "🤖 The bot won."
                )

            else:

                st.info(
                    "🤝 Draw."
                )
