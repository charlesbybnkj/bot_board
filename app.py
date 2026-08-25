import random
import streamlit as st

try:
    import chess
except ImportError:
    chess = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BOT BOARD",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GAME ARTWORK
# ============================================================

GAME_IMAGES = {
    "Tic Tac Toe": "https://images.unsplash.com/photo-1611996575749-79a3a250f948?auto=format&fit=crop&w=1200&q=85",
    "Connect 4": "https://images.unsplash.com/photo-1606167668584-78701c57f13d?auto=format&fit=crop&w=1200&q=85",
    "Checkers": "https://images.unsplash.com/photo-1560174038-da43ac74f01b?auto=format&fit=crop&w=1200&q=85",
    "Othello": "https://images.unsplash.com/photo-1586165368502-1bad197a6461?auto=format&fit=crop&w=1200&q=85",
    "Gomoku": "https://images.unsplash.com/photo-1598514982901-ae627f0f0e0d?auto=format&fit=crop&w=1200&q=85",
    "Battleship": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=85",
    "Chess": "https://images.unsplash.com/photo-1586165368502-1bad197a6461?auto=format&fit=crop&w=1200&q=85",
    "Blackjack": "https://images.unsplash.com/photo-1518893883800-45cd0954574b?auto=format&fit=crop&w=1200&q=85",
}


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(59,130,246,.13), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(139,92,246,.12), transparent 30%),
        #070b14;
    color: #f8fafc;
}

header {
    background: transparent !important;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {
    background: #0b1020;
    border-right: 1px solid #1e293b;
}


/* ---------- HERO ---------- */

.hero {
    position: relative;
    overflow: hidden;
    border-radius: 28px;
    padding: 42px;
    margin-bottom: 28px;
    background:
        radial-gradient(circle at 85% 30%, rgba(99,102,241,.4), transparent 30%),
        linear-gradient(135deg,#111827,#172554,#312e81);
    border: 1px solid rgba(148,163,184,.2);
    box-shadow: 0 25px 70px rgba(0,0,0,.3);
}

.hero h1 {
    font-size: 54px;
    font-weight: 900;
    margin: 0;
    letter-spacing: -2px;
}

.hero p {
    color: #cbd5e1;
    font-size: 18px;
    margin-top: 8px;
}


/* ---------- BALANCE ---------- */

.balance {
    background: rgba(15,23,42,.9);
    border: 1px solid #263449;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
}

.balance-title {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.balance-number {
    font-size: 30px;
    font-weight: 900;
    color: #facc15;
    margin-top: 5px;
}


/* ---------- GAME CARDS ---------- */

.game-card {
    overflow: hidden;
    background: #0f172a;
    border: 1px solid #243147;
    border-radius: 22px;
    margin-bottom: 22px;
    box-shadow: 0 15px 40px rgba(0,0,0,.2);
    transition: .2s;
}

.game-card:hover {
    border-color: #6366f1;
    transform: translateY(-3px);
}

.game-image {
    width: 100%;
    height: 190px;
    object-fit: cover;
    display: block;
}

.game-content {
    padding: 20px;
}

.game-title {
    font-size: 23px;
    font-weight: 800;
}

.game-description {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 5px;
}


/* ---------- GAME HEADER ---------- */

.game-header {
    background: rgba(15,23,42,.85);
    border: 1px solid #263449;
    border-radius: 22px;
    padding: 20px 25px;
    margin-bottom: 20px;
}


/* ---------- BOARD ---------- */

.board-container {
    background: #0b1220;
    border: 1px solid #243147;
    border-radius: 24px;
    padding: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,.25);
}


/* ---------- BLACKJACK ---------- */

.blackjack-table {
    background:
        radial-gradient(circle at center, #11633d 0%, #08452b 45%, #052b1c 100%);
    border: 12px solid #6b4426;
    border-radius: 45px;
    padding: 35px;
    min-height: 570px;
    box-shadow:
        inset 0 0 50px rgba(0,0,0,.5),
        0 25px 60px rgba(0,0,0,.4);
}

.poker-line {
    border: 2px solid rgba(255,255,255,.5);
    border-radius: 50%;
    padding: 20px;
}

.hand-title {
    text-align: center;
    color: #e2e8f0;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.card {
    display: inline-flex;
    width: 72px;
    height: 102px;
    margin: 5px;
    background: #fff;
    color: #111827;
    border-radius: 9px;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    font-weight: 800;
    box-shadow: 0 8px 15px rgba(0,0,0,.4);
}

.card.red {
    color: #dc2626;
}

.card-back {
    display: inline-flex;
    width: 72px;
    height: 102px;
    margin: 5px;
    background:
        repeating-linear-gradient(
            45deg,
            #1e3a8a,
            #1e3a8a 5px,
            #2563eb 5px,
            #2563eb 10px
        );
    border: 4px solid white;
    border-radius: 9px;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    box-shadow: 0 8px 15px rgba(0,0,0,.4);
}

.chip {
    display: inline-block;
    background: #ef4444;
    border: 5px dashed white;
    border-radius: 50%;
    width: 62px;
    height: 62px;
    line-height: 52px;
    text-align: center;
    font-weight: 900;
    margin: 5px;
}


/* ---------- BUTTONS ---------- */

.stButton > button {
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
    background: #111827 !important;
    color: white !important;
    font-weight: 700 !important;
    min-height: 44px;
}

.stButton > button:hover {
    border-color: #6366f1 !important;
    background: #172033 !important;
}

button[kind="primary"] {
    background: linear-gradient(135deg,#4f46e5,#7c3aed) !important;
    border: none !important;
}


/* ---------- METRICS ---------- */

[data-testid="stMetric"] {
    background: #0f172a;
    border: 1px solid #243147;
    border-radius: 18px;
    padding: 18px;
}


/* ---------- MOBILE ---------- */

@media (max-width: 700px) {

    .hero {
        padding: 28px;
    }

    .hero h1 {
        font-size: 38px;
    }

    .blackjack-table {
        padding: 15px;
        border-width: 7px;
    }

    .card,
    .card-back {
        width: 55px;
        height: 80px;
        font-size: 19px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "balance": 1000,
    "earned": 0,
    "lost": 0,
    "games": 0,
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "streak": 0,
    "best_streak": 0,
    "biggest_win": 0,
    "achievements": set(),
    "game": None,
    "difficulty": "Medium",
    "result": "",
    "reward_given": False,
    "daily_bonus": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


DIFFICULTIES = ["Easy", "Medium", "Hard", "Impossible"]

REWARDS = {
    "Tic Tac Toe": [25, 50, 100, 200],
    "Connect 4": [50, 100, 200, 400],
    "Checkers": [75, 150, 300, 600],
    "Othello": [100, 200, 400, 800],
    "Gomoku": [75, 150, 300, 600],
    "Battleship": [100, 200, 400, 800],
    "Chess": [150, 300, 600, 1200],
}


def difficulty_level():
    return DIFFICULTIES.index(st.session_state.difficulty)


def reward_for(game):
    return REWARDS.get(game, [0, 0, 0, 0])[difficulty_level()]


def unlock(name):
    st.session_state.achievements.add(name)


def finish_game(result, reward=0):
    if st.session_state.reward_given:
        return

    st.session_state.reward_given = True
    st.session_state.games += 1
    st.session_state.result = result

    if result == "win":
        st.session_state.wins += 1
        st.session_state.streak += 1

        st.session_state.best_streak = max(
            st.session_state.best_streak,
            st.session_state.streak
        )

        if reward:
            st.session_state.balance += reward
            st.session_state.earned += reward
            st.session_state.biggest_win = max(
                st.session_state.biggest_win,
                reward
            )

        unlock("First Win")

        if st.session_state.streak >= 5:
            unlock("Hot Streak")

    elif result == "loss":
        st.session_state.losses += 1
        st.session_state.streak = 0

    else:
        st.session_state.draws += 1

    if st.session_state.earned >= 1000:
        unlock("Big Winner")


def reset_game(name):
    st.session_state.game = name
    st.session_state.result = ""
    st.session_state.reward_given = False
    st.session_state.difficulty = "Medium"

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


# ============================================================
# TIC TAC TOE
# ============================================================

def init_ttt():
    st.session_state.ttt = [""] * 9
    st.session_state.ttt_over = False


def ttt_winner(board):
    lines = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b,c in lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if all(board):
        return "draw"

    return None


def ttt_bot():
    board = st.session_state.ttt
    empty = [i for i,x in enumerate(board) if not x]

    if not empty:
        return

    level = difficulty_level()

    if level == 0:
        move = random.choice(empty)

    else:
        move = None

        for i in empty:
            board[i] = "O"

            if ttt_winner(board) == "O":
                move = i

            board[i] = ""

            if move is not None:
                break

        if move is None:
            for i in empty:
                board[i] = "X"

                if ttt_winner(board) == "X":
                    move = i

                board[i] = ""

                if move is not None:
                    break

        if move is None:
            move = random.choice(empty)

    board[move] = "O"


def play_ttt():
    st.markdown("<div class='board-container'>", unsafe_allow_html=True)

    cols = st.columns(3)

    for i in range(9):
        with cols[i % 3]:

            label = st.session_state.ttt[i] or " "

            if st.button(
                label,
                key=f"ttt_{i}",
                use_container_width=True
            ):

                if st.session_state.ttt_over:
                    continue

                if st.session_state.ttt[i]:
                    continue

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

    st.markdown("</div>", unsafe_allow_html=True)


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

    move = random.choice(valid)

    if difficulty_level() >= 1:

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

    move = random.choice(valid)
    c4_drop(move,2)


def play_connect4():

    cols = st.columns(7)

    for c in range(7):

        if cols[c].button(
            "↓",
            key=f"c4_{c}",
            use_container_width=True
        ):

            if st.session_state.c4_over:
                continue

            if c4_drop(c,1) is None:
                continue

            winner = c4_winner(st.session_state.c4)

            if winner == 1:

                st.session_state.c4_over = True
                finish_game("win", reward_for("Connect 4"))

            else:

                c4_bot()

                winner = c4_winner(st.session_state.c4)

                if winner == 2:

                    st.session_state.c4_over = True
                    finish_game("loss")

            st.rerun()

    symbols = {
        0: "⚪",
        1: "🔴",
        2: "🟡"
    }

    for row in st.session_state.c4:

        cols = st.columns(7)

        for c,cell in enumerate(row):

            cols[c].markdown(
                f"<div class='big-center'>{symbols[cell]}</div>",
                unsafe_allow_html=True
            )


# ============================================================
# CHECKERS
# ============================================================

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

    st.session_state.checkers = board
    st.session_state.selected = None
    st.session_state.checkers_over = False


def checkers_moves(board, player):

    moves = []

    directions = [
        (-1,-1),(-1,1),
        (1,-1),(1,1)
    ]

    for r in range(8):

        for c in range(8):

            piece = board[r][c]

            if piece not in (player, player+2):
                continue

            king = piece >= 3

            if king:
                dirs = directions

            elif player == 1:
                dirs = [(-1,-1),(-1,1)]

            else:
                dirs = [(1,-1),(1,1)]

            for dr,dc in dirs:

                rr = r+dr
                cc = c+dc

                if (
                    0 <= rr < 8 and
                    0 <= cc < 8 and
                    board[rr][cc] == 0
                ):
                    moves.append(
                        ((r,c),(rr,cc))
                    )

    return moves


def checkers_move(move):

    (r,c),(rr,cc) = move

    board = st.session_state.checkers

    piece = board[r][c]

    board[r][c] = 0
    board[rr][cc] = piece

    if piece == 1 and rr == 0:
        board[rr][cc] = 3

    if piece == 2 and rr == 7:
        board[rr][cc] = 4


def checkers_bot():

    moves = checkers_moves(
        st.session_state.checkers,
        2
    )

    if moves:
        checkers_move(random.choice(moves))


def play_checkers():

    board = st.session_state.checkers

    moves = checkers_moves(board,1)

    cols = st.columns(8)

    for r in range(8):

        for c in range(8):

            piece = board[r][c]

            if piece == 1:
                symbol = "⚪"

            elif piece == 2:
                symbol = "⚫"

            elif piece in (3,4):
                symbol = "👑"

            else:
                symbol = "·"

            if cols[c].button(
                symbol,
                key=f"check_{r}_{c}",
                use_container_width=True
            ):

                if st.session_state.checkers_over:
                    continue

                selected = st.session_state.selected

                if selected is None:

                    if piece in (1,3):
                        st.session_state.selected = (r,c)

                else:

                    move = (
                        (selected,(r,c))
                    )

                    if move in moves:

                        checkers_move(move)

                        st.session_state.selected = None

                        checkers_bot()

                    elif piece in (1,3):

                        st.session_state.selected = (r,c)

                    else:

                        st.session_state.selected = None

                    st.rerun()


# ============================================================
# OTHELLO
# ============================================================

DIRECTIONS = [
    (-1,-1),(-1,0),(-1,1),
    (0,-1),(0,1),
    (1,-1),(1,0),(1,1)
]


def init_othello():

    board = [[0]*8 for _ in range(8)]

    board[3][3] = 2
    board[4][4] = 2
    board[3][4] = 1
    board[4][3] = 1

    st.session_state.othello = board


def othello_moves(board,player):

    moves = []

    opponent = 3-player

    for r in range(8):

        for c in range(8):

            if board[r][c]:
                continue

            valid = False

            for dr,dc in DIRECTIONS:

                rr = r+dr
                cc = c+dc

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
                moves.append((r,c))

    return moves


def othello_play(r,c,player):

    board = st.session_state.othello

    board[r][c] = player

    opponent = 3-player

    for dr,dc in DIRECTIONS:

        captured = []

        rr = r+dr
        cc = c+dc

        while (
            0 <= rr < 8 and
            0 <= cc < 8 and
            board[rr][cc] == opponent
        ):

            captured.append((rr,cc))

            rr += dr
            cc += dc

        if (
            captured and
            0 <= rr < 8 and
            0 <= cc < 8 and
            board[rr][cc] == player
        ):

            for cr,cc2 in captured:
                board[cr][cc2] = player


def othello_bot():

    moves = othello_moves(
        st.session_state.othello,
        2
    )

    if not moves:
        return

    corners = [
        (0,0),(0,7),
        (7,0),(7,7)
    ]

    corner_moves = [
        m for m in moves
        if m in corners
    ]

    move = (
        random.choice(corner_moves)
        if corner_moves
        else random.choice(moves)
    )

    othello_play(*move,2)


def play_othello():

    board = st.session_state.othello

    legal = othello_moves(board,1)

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            piece = board[r][c]

            if piece == 1:
                symbol = "⚪"

            elif piece == 2:
                symbol = "⚫"

            else:
                symbol = "🟢" if (r,c) in legal else "·"

            if cols[c].button(
                symbol,
                key=f"oth_{r}_{c}",
                use_container_width=True
            ):

                if (r,c) in legal:

                    othello_play(r,c,1)

                    othello_bot()

                    st.rerun()


# ============================================================
# GOMOKU
# ============================================================

def init_gomoku():

    st.session_state.gomoku = [
        [0]*15 for _ in range(15)
    ]


def gomoku_win(board,r,c,player):

    for dr,dc in DIRECTIONS:

        count = 1

        for direction in (1,-1):

            rr = r + dr*direction
            cc = c + dc*direction

            while (
                0 <= rr < 15 and
                0 <= cc < 15 and
                board[rr][cc] == player
            ):

                count += 1

                rr += dr*direction
                cc += dc*direction

        if count >= 5:
            return True

    return False


def gomoku_bot():

    board = st.session_state.gomoku

    empty = [
        (r,c)
        for r in range(15)
        for c in range(15)
        if board[r][c] == 0
    ]

    if empty:

        # Centre-biased bot.
        empty.sort(
            key=lambda x:
            abs(x[0]-7)+abs(x[1]-7)
        )

        choice = random.choice(
            empty[:min(20,len(empty))]
        )

        board[choice[0]][choice[1]] = 2


def play_gomoku():

    board = st.session_state.gomoku

    for r in range(15):

        cols = st.columns(15)

        for c in range(15):

            piece = board[r][c]

            symbol = (
                "⚪" if piece == 1
                else "⚫" if piece == 2
                else "·"
            )

            if cols[c].button(
                symbol,
                key=f"gom_{r}_{c}",
                use_container_width=True
            ):

                if piece != 0:
                    continue

                board[r][c] = 1

                if gomoku_win(board,r,c,1):

                    finish_game(
                        "win",
                        reward_for("Gomoku")
                    )

                else:

                    gomoku_bot()

                st.rerun()


# ============================================================
# BATTLESHIP
# ============================================================

def init_battleship():

    def create_board():

        board = [
            [0]*8 for _ in range(8)
        ]

        ships = [3,2,2]

        for size in ships:

            placed = False

            while not placed:

                horizontal = random.choice(
                    [True,False]
                )

                r = random.randrange(8)
                c = random.randrange(8)

                cells = []

                for i in range(size):

                    rr = r + (0 if horizontal else i)
                    cc = c + (i if horizontal else 0)

                    if not (
                        0 <= rr < 8 and
                        0 <= cc < 8
                    ):
                        break

                    cells.append((rr,cc))

                if (
                    len(cells) == size and
                    all(board[rr][cc] == 0 for rr,cc in cells)
                ):

                    for rr,cc in cells:
                        board[rr][cc] = 1

                    placed = True

        return board

    st.session_state.player_fleet = create_board()
    st.session_state.bot_fleet = create_board()
    st.session_state.player_shots = [
        [0]*8 for _ in range(8)
    ]


def play_battleship():

    st.caption("🔥 Fire at the enemy fleet.")

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            shot = st.session_state.player_shots[r][c]

            symbol = (
                "💥" if shot == 2
                else "💧" if shot == 1
                else "🎯"
            )

            if cols[c].button(
                symbol,
                key=f"ship_{r}_{c}",
                use_container_width=True
            ):

                if shot:
                    continue

                if st.session_state.bot_fleet[r][c] == 1:

                    st.session_state.bot_fleet[r][c] = 2
                    st.session_state.player_shots[r][c] = 2

                else:

                    st.session_state.player_shots[r][c] = 1

                st.rerun()


# ============================================================
# CHESS
# ============================================================

def init_chess():

    if chess:

        st.session_state.chess_board = chess.Board()

    else:

        st.session_state.chess_board = None

    st.session_state.chess_selected = None


def chess_bot():

    board = st.session_state.chess_board

    moves = list(board.legal_moves)

    if not moves:
        return

    captures = [
        move for move in moves
        if board.is_capture(move)
    ]

    if captures:
        move = random.choice(captures)

    else:
        move = random.choice(moves)

    board.push(move)


def play_chess():

    if chess is None:

        st.error(
            "python-chess is missing from requirements.txt"
        )

        return

    board = st.session_state.chess_board

    files = "abcdefgh"
    ranks = "87654321"

    legal = list(board.legal_moves)

    selected = st.session_state.chess_selected

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            square = chess.parse_square(
                files[c] + ranks[r]
            )

            piece = board.piece_at(square)

            symbol = (
                piece.symbol()
                if piece
                else "·"
            )

            if selected is not None:

                if any(
                    m.from_square == selected
                    and m.to_square == square
                    for m in legal
                ):
                    symbol = "🟢"

            if cols[c].button(
                symbol,
                key=f"chess_{r}_{c}",
                use_container_width=True
            ):

                if board.turn != chess.WHITE:
                    continue

                if selected is None:

                    if (
                        piece and
                        piece.color == chess.WHITE
                    ):
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

                        if not board.is_game_over():

                            chess_bot()

                        else:

                            finish_game(
                                "win",
                                reward_for("Chess")
                            )

                    else:

                        st.session_state.chess_selected = None

                st.rerun()


# ============================================================
# BLACKJACK
# ============================================================

SUITS = ["♠","♥","♦","♣"]

RANKS = [
    "A","2","3","4","5","6","7",
    "8","9","10","J","Q","K"
]


def blackjack_deck():

    deck = [
        (rank,suit)
        for suit in SUITS
        for rank in RANKS
    ]

    random.shuffle(deck)

    return deck


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

    st.session_state.bj_deck = blackjack_deck()
    st.session_state.bj_player = []
    st.session_state.bj_dealer = []
    st.session_state.bj_bet = 25
    st.session_state.bj_active = False
    st.session_state.bj_over = False
    st.session_state.bj_message = ""


def bj_draw():

    if not st.session_state.bj_deck:

        st.session_state.bj_deck = blackjack_deck()

    return st.session_state.bj_deck.pop()


def render_cards(cards, hidden=False):

    html = ""

    for i,(rank,suit) in enumerate(cards):

        if hidden and i == 0:

            html += """
            <span class="card-back">★</span>
            """

        else:

            red = suit in ["♥","♦"]

            html += f"""
            <span class="card {'red' if red else ''}">
                {rank}{suit}
            </span>
            """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def blackjack_deal():

    bet = int(st.session_state.bj_bet)

    if bet > st.session_state.balance:

        st.error("You don't have enough BOT BUCKS.")

        return

    st.session_state.balance -= bet
    st.session_state.lost += bet

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

    if card_value(st.session_state.bj_player) == 21:

        profit = int(bet * 1.5)

        st.session_state.balance += bet + profit
        st.session_state.earned += profit
        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            profit
        )

        st.session_state.bj_message = (
            f"🃏 BLACKJACK! +{profit} BB"
        )

        st.session_state.bj_over = True

        unlock("Blackjack!")


def blackjack_finish():

    bet = int(st.session_state.bj_bet)

    player = card_value(
        st.session_state.bj_player
    )

    if player > 21:

        st.session_state.bj_message = (
            f"💥 Bust! You lost {bet} BB."
        )

        st.session_state.bj_over = True

        return

    while card_value(
        st.session_state.bj_dealer
    ) < 17:

        st.session_state.bj_dealer.append(
            bj_draw()
        )

    dealer = card_value(
        st.session_state.bj_dealer
    )

    if dealer > 21 or player > dealer:

        st.session_state.balance += bet * 2
        st.session_state.earned += bet

        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            bet
        )

        st.session_state.bj_message = (
            f"🎉 You win +{bet} BB!"
        )

    elif player == dealer:

        st.session_state.balance += bet

        st.session_state.bj_message = (
            "🤝 Push — your bet is returned."
        )

    else:

        st.session_state.bj_message = (
            f"🤖 Dealer wins. -{bet} BB"
        )

    st.session_state.bj_over = True


def play_blackjack():

    # Real-looking table

    st.markdown(
        "<div class='blackjack-table'>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='hand-title'>DEALER</div>",
        unsafe_allow_html=True
    )

    if st.session_state.bj_active:

        render_cards(
            st.session_state.bj_dealer,
            hidden=not st.session_state.bj_over
        )

        if st.session_state.bj_over:

            st.markdown(
                f"<div class='hand-title'>"
                f"{card_value(st.session_state.bj_dealer)}"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown(
        "<br><div class='poker-line'></div><br>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='hand-title'>YOUR HAND</div>",
        unsafe_allow_html=True
    )

    if st.session_state.bj_active:

        render_cards(
            st.session_state.bj_player
        )

        st.markdown(
            f"<div class='hand-title'>"
            f"{card_value(st.session_state.bj_player)}"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.write("")

    if not st.session_state.bj_active:

        st.session_state.bj_bet = st.number_input(
            "Bet",
            min_value=1,
            max_value=max(
                1,
                st.session_state.balance
            ),
            value=min(
                25,
                max(1,st.session_state.balance)
            ),
            step=5
        )

        if st.button(
            "🎲 DEAL CARDS",
            type="primary",
            use_container_width=True
        ):

            blackjack_deal()

            st.rerun()

    elif not st.session_state.bj_over:

        c1,c2 = st.columns(2)

        if c1.button(
            "👊 HIT",
            use_container_width=True
        ):

            st.session_state.bj_player.append(
                bj_draw()
            )

            if card_value(
                st.session_state.bj_player
            ) > 21:

                blackjack_finish()

            st.rerun()

        if c2.button(
            "✋ STAND",
            use_container_width=True
        ):

            blackjack_finish()

            st.rerun()

    else:

        st.success(
            st.session_state.bj_message
        )

        if st.button(
            "🔄 NEW HAND",
            type="primary",
            use_container_width=True
        ):

            st.session_state.bj_active = False
            st.session_state.bj_over = False
            st.session_state.bj_message = ""

            st.rerun()


# ============================================================
# GAME DATA
# ============================================================

GAMES = [

    (
        "🎯",
        "Tic Tac Toe",
        "Classic strategy. Get three in a row."
    ),

    (
        "🟡",
        "Connect 4",
        "Drop four pieces in a row."
    ),

    (
        "🏁",
        "Checkers",
        "Capture the bot's pieces."
    ),

    (
        "🟢",
        "Othello",
        "Flip your opponent's pieces."
    ),

    (
        "🟨",
        "Gomoku",
        "Five pieces in a row wins."
    ),

    (
        "🚢",
        "Battleship",
        "Find and destroy the enemy fleet."
    ),

    (
        "♟️",
        "Chess",
        "Classic strategic battle."
    ),

    (
        "🃏",
        "Blackjack",
        "Beat the dealer and build your balance."
    ),
]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🤖 BOT BOARD")

    st.markdown(
        f"### 💰 {st.session_state.balance:,} BB"
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

            reset_game(
                st.session_state.game
            )

            st.rerun()


# ============================================================
# WALLET
# ============================================================

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
        "Total Earned",
        f"{st.session_state.earned:,} BB"
    )

    c3.metric(
        "Total Lost",
        f"{st.session_state.lost:,} BB"
    )

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Biggest Win",
        f"{st.session_state.biggest_win:,} BB"
    )

    c2.metric(
        "Win Streak",
        st.session_state.streak
    )

    c3.metric(
        "Best Streak",
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
            st.session_state.earned += 250
            st.session_state.daily_bonus = True

            st.rerun()

    else:

        st.success(
            "Daily bonus already claimed."
        )

    st.info(
        "BOT BUCKS are fictional in-game currency. "
        "They have no real-world value."
    )


# ============================================================
# ACHIEVEMENTS
# ============================================================

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
            "Win your first game"
        ),

        (
            "Hot Streak",
            "Win 5 games in a row"
        ),

        (
            "Big Winner",
            "Earn 1,000 BOT BUCKS"
        ),

        (
            "Blackjack!",
            "Get a natural blackjack"
        ),

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


# ============================================================
# GAMES HOME
# ============================================================

elif st.session_state.game is None:

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
        <div class="balance">
            <div class="balance-title">
                YOUR BOT BUCKS
            </div>
            <div class="balance-number">
                💰 {st.session_state.balance:,} BB
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.divider()

    cols = st.columns(2)

    for i,(icon,name,description) in enumerate(GAMES):

        with cols[i % 2]:

            image = GAME_IMAGES[name]

            st.markdown(
                f"""
                <div class="game-card">
                    <img
                        class="game-image"
                        src="{image}"
                    >

                    <div class="game-content">

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
                use_container_width=True
            ):

                reset_game(name)

                st.rerun()


# ============================================================
# ACTIVE GAME
# ============================================================

else:

    name = st.session_state.game

    st.markdown(
        f"""
        <div class="game-header">
            <h1>{name}</h1>
            <p style="color:#94a3b8;">
                BOT BOARD • {name}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if name != "Blackjack":

        c1,c2 = st.columns([3,1])

        with c1:

            st.selectbox(
                "BOT DIFFICULTY",
                DIFFICULTIES,
                key="difficulty"
            )

        with c2:

            st.markdown(
                f"""
                <div class="balance">
                    <div class="balance-title">
                        WIN REWARD
                    </div>
                    <div class="balance-number">
                        +{reward_for(name)} BB
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            f"""
            <div class="balance">
                <div class="balance-title">
                    YOUR BALANCE
                </div>
                <div class="balance-number">
                    💰 {st.session_state.balance:,} BB
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # GAME ROUTER

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

    # RESULT

    if (
        st.session_state.result
        and name != "Blackjack"
    ):

        st.divider()

        if st.session_state.result == "win":

            st.success(
                f"🎉 YOU WON! +{reward_for(name)} BB"
            )

        elif st.session_state.result == "loss":

            st.error(
                "🤖 The bot won this round."
            )

        else:

            st.info(
                "🤝 It's a draw."
            )
