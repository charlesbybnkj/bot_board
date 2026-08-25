import random
import streamlit as st

try:
    import chess
except ImportError:
    chess = None


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="BOT BOARD",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# MODERN UI
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(99,102,241,.16), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(168,85,247,.12), transparent 28%),
        #070b14;
    color: #f8fafc;
}

header {
    visibility: hidden;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: #0b1020;
    border-right: 1px solid #1e293b;
}

[data-testid="stSidebar"] * {
    color: #f8fafc;
}

/* Buttons */

.stButton > button {
    border-radius: 12px;
    border: 1px solid #263247;
    background: #111827;
    color: white;
    font-weight: 700;
    min-height: 44px;
    transition: .15s;
}

.stButton > button:hover {
    border-color: #6366f1;
    background: #171f35;
    color: white;
    transform: translateY(-1px);
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border: none;
}

/* Hero */

.hero {
    padding: 42px;
    border-radius: 28px;
    background:
        linear-gradient(135deg, rgba(99,102,241,.30), rgba(139,92,246,.18)),
        #0d1425;
    border: 1px solid #263247;
    box-shadow: 0 20px 60px rgba(0,0,0,.25);
    margin-bottom: 24px;
}

.hero h1 {
    font-size: clamp(38px, 6vw, 68px);
    font-weight: 900;
    letter-spacing: -3px;
    margin: 0;
}

.hero p {
    font-size: 18px;
    color: #a8b3c7;
    margin-top: 10px;
}

/* Balance */

.balance {
    background: linear-gradient(135deg, #171f35, #101827);
    border: 1px solid #29364d;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    margin-bottom: 24px;
}

.balance-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.balance-value {
    font-size: 30px;
    font-weight: 900;
    color: #facc15;
    margin-top: 5px;
}

/* Game cards */

.game-card {
    background: linear-gradient(145deg, #111827, #0d1422);
    border: 1px solid #253147;
    border-radius: 22px;
    padding: 24px;
    min-height: 175px;
    margin-bottom: 12px;
    transition: .2s;
}

.game-card:hover {
    border-color: #6366f1;
    transform: translateY(-2px);
}

.game-icon {
    font-size: 42px;
    margin-bottom: 10px;
}

.game-title {
    font-size: 21px;
    font-weight: 800;
}

.game-desc {
    color: #8794aa;
    font-size: 14px;
    margin-top: 5px;
}

/* Panels */

.panel {
    background: #0d1422;
    border: 1px solid #253147;
    border-radius: 22px;
    padding: 24px;
    margin-bottom: 18px;
}

/* Stats */

.stat {
    background: #101827;
    border: 1px solid #253147;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
}

.stat-number {
    font-size: 27px;
    font-weight: 900;
}

.stat-label {
    color: #8491a7;
    font-size: 12px;
    margin-top: 4px;
}

/* Blackjack */

.blackjack-table {
    background:
        radial-gradient(circle at center, #176b48 0%, #0b5639 48%, #073b2a 100%);
    border: 10px solid #3d2b1f;
    border-radius: 34px;
    padding: 35px;
    min-height: 540px;
    box-shadow:
        inset 0 0 0 2px #8b6b42,
        inset 0 0 80px rgba(0,0,0,.35),
        0 20px 60px rgba(0,0,0,.35);
    text-align: center;
}

.table-label {
    color: rgba(255,255,255,.72);
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 800;
}

.table-total {
    font-size: 22px;
    font-weight: 900;
    margin: 10px;
}

.playing-card {
    display: inline-flex;
    flex-direction: column;
    justify-content: center;
    width: 75px;
    height: 108px;
    background: linear-gradient(145deg, #ffffff, #e8e8e8);
    border-radius: 10px;
    color: #111827;
    margin: 5px;
    box-shadow: 0 7px 15px rgba(0,0,0,.35);
    font-weight: 900;
    position: relative;
    vertical-align: middle;
}

.card-rank {
    font-size: 26px;
    line-height: 1;
}

.card-suit {
    font-size: 28px;
    line-height: 1;
    margin-top: 5px;
}

.red-card {
    color: #dc2626;
}

.card-back {
    background:
        repeating-linear-gradient(
            45deg,
            #172554,
            #172554 5px,
            #312e81 5px,
            #312e81 10px
        );
    border: 4px solid white;
    color: white;
    font-size: 35px;
}

/* Board */

.board-cell {
    text-align: center;
    font-size: 30px;
    font-weight: 900;
}

/* Messages */

.win-box {
    background: rgba(34,197,94,.12);
    border: 1px solid rgba(34,197,94,.35);
    color: #86efac;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    font-weight: 800;
}

.loss-box {
    background: rgba(239,68,68,.12);
    border: 1px solid rgba(239,68,68,.35);
    color: #fca5a5;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    font-weight: 800;
}

.info-box {
    background: rgba(59,130,246,.12);
    border: 1px solid rgba(59,130,246,.3);
    color: #93c5fd;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
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
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "games": 0,
    "streak": 0,
    "best_streak": 0,
    "biggest_win": 0,
    "achievements": set(),
    "daily_bonus": False,
    "game": None,
    "difficulty": "Medium",
    "result": "",
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


def reward(game):
    return REWARDS.get(game, [0, 0, 0, 0])[difficulty_level()]


def unlock(name):
    st.session_state.achievements.add(name)


def money(amount):
    st.session_state.balance += amount

    if amount > 0:
        st.session_state.earned += amount
        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            amount
        )

    if amount < 0:
        st.session_state.lost += abs(amount)


def finish(result, amount=0):

    st.session_state.games += 1
    st.session_state.result = result

    if result == "win":
        st.session_state.wins += 1
        st.session_state.streak += 1

        st.session_state.best_streak = max(
            st.session_state.best_streak,
            st.session_state.streak
        )

        if amount:
            money(amount)

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


def start_game(name):
    st.session_state.game = name
    st.session_state.result = ""
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
        (0,1,2),
        (3,4,5),
        (6,7,8),
        (0,3,6),
        (1,4,7),
        (2,5,8),
        (0,4,8),
        (2,4,6)
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

    st.markdown("### ❌ Tic Tac Toe")
    st.caption("You are X • Bot is O")

    cols = st.columns(3)

    for i in range(9):

        with cols[i % 3]:

            value = st.session_state.ttt[i]

            label = value if value else " "

            if st.button(
                label,
                key=f"ttt_{i}",
                use_container_width=True
            ):

                if not st.session_state.ttt_over and not value:

                    st.session_state.ttt[i] = "X"

                    result = ttt_winner(st.session_state.ttt)

                    if result == "X":

                        st.session_state.ttt_over = True
                        finish("win", reward("Tic Tac Toe"))

                    elif result == "draw":

                        st.session_state.ttt_over = True
                        finish("draw")

                    else:

                        ttt_bot()

                        result = ttt_winner(st.session_state.ttt)

                        if result:

                            st.session_state.ttt_over = True

                            finish(
                                "loss" if result == "O" else "draw"
                            )

                    st.rerun()


# ============================================================
# CONNECT 4
# ============================================================

def init_connect4():

    st.session_state.c4 = [
        [0] * 7
        for _ in range(6)
    ]

    st.session_state.c4_over = False


def c4_winner(board):

    for r in range(6):

        for c in range(7):

            p = board[r][c]

            if not p:
                continue

            for dr,dc in [
                (1,0),
                (0,1),
                (1,1),
                (1,-1)
            ]:

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

    # Try winning.
    for c in valid:

        r = c4_drop(c, 2)

        if c4_winner(st.session_state.c4) == 2:
            return

        st.session_state.c4[r][c] = 0

    # Block player.
    if difficulty_level() >= 1:

        for c in valid:

            r = c4_drop(c, 1)

            if c4_winner(st.session_state.c4) == 1:

                st.session_state.c4[r][c] = 0
                c4_drop(c, 2)
                return

            st.session_state.c4[r][c] = 0

    preferred = [3,2,4,1,5,0,6]

    choices = [x for x in preferred if x in valid]

    c4_drop(random.choice(choices), 2)


def play_connect4():

    st.markdown("### 🟡 Connect 4")
    st.caption("Get four pieces in a row before the bot.")

    cols = st.columns(7)

    for c in range(7):

        with cols[c]:

            if st.button(
                "↓",
                key=f"c4_{c}",
                use_container_width=True,
                disabled=st.session_state.c4_over
            ):

                if c4_drop(c,1) is not None:

                    result = c4_winner(st.session_state.c4)

                    if result == 1:

                        st.session_state.c4_over = True
                        finish("win", reward("Connect 4"))

                    else:

                        c4_bot()

                        result = c4_winner(st.session_state.c4)

                        if result == 2:

                            st.session_state.c4_over = True
                            finish("loss")

                        elif all(
                            st.session_state.c4[0][x]
                            for x in range(7)
                        ):

                            st.session_state.c4_over = True
                            finish("draw")

                    st.rerun()

    symbols = {
        0: "⚪",
        1: "🔴",
        2: "🟡"
    }

    for row in st.session_state.c4:

        cols = st.columns(7)

        for c, value in enumerate(row):

            cols[c].markdown(
                f"<div class='board-cell'>{symbols[value]}</div>",
                unsafe_allow_html=True
            )


# ============================================================
# CHECKERS
# ============================================================

def init_checkers():

    board = [[0]*8 for _ in range(8)]

    for r in range(3):

        for c in range(8):

            if (r+c) % 2:
                board[r][c] = 2

    for r in range(5,8):

        for c in range(8):

            if (r+c) % 2:
                board[r][c] = 1

    st.session_state.checkers = board
    st.session_state.check_selected = None
    st.session_state.check_over = False


def checker_moves(board, player):

    moves = []
    captures = []

    directions = [
        (-1,-1),
        (-1,1),
        (1,-1),
        (1,1)
    ]

    for r in range(8):

        for c in range(8):

            piece = board[r][c]

            if piece not in (
                player,
                player + 2
            ):
                continue

            king = piece >= 3

            if king:

                dirs = directions

            elif player == 1:

                dirs = [
                    (-1,-1),
                    (-1,1)
                ]

            else:

                dirs = [
                    (1,-1),
                    (1,1)
                ]

            for dr,dc in dirs:

                rr = r + dr
                cc = c + dc

                if 0 <= rr < 8 and 0 <= cc < 8:

                    if board[rr][cc] == 0:

                        moves.append(
                            ((r,c),(rr,cc),None)
                        )

                    elif board[rr][cc] not in (
                        0,
                        player,
                        player + 2
                    ):

                        jr = rr + dr
                        jc = cc + dc

                        if (
                            0 <= jr < 8
                            and 0 <= jc < 8
                            and board[jr][jc] == 0
                        ):

                            captures.append(
                                (
                                    (r,c),
                                    (jr,jc),
                                    (rr,cc)
                                )
                            )

    return captures if captures else moves


def apply_checker(move):

    start,end,capture = move

    r,c = start
    rr,cc = end

    board = st.session_state.checkers

    piece = board[r][c]

    board[r][c] = 0
    board[rr][cc] = piece

    if capture:
        board[capture[0]][capture[1]] = 0

    if piece == 1 and rr == 0:
        board[rr][cc] = 3

    if piece == 2 and rr == 7:
        board[rr][cc] = 4


def checker_bot():

    moves = checker_moves(
        st.session_state.checkers,
        2
    )

    if moves:

        captures = [
            m for m in moves
            if m[2] is not None
        ]

        apply_checker(
            random.choice(
                captures if captures else moves
            )
        )


def play_checkers():

    st.markdown("### ⚫ Checkers")
    st.caption("Select one of your pieces, then select where to move it.")

    moves = checker_moves(
        st.session_state.checkers,
        1
    )

    selected = st.session_state.check_selected

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            piece = st.session_state.checkers[r][c]

            icons = {
                0: "·",
                1: "⚪",
                2: "⚫",
                3: "👑",
                4: "👑"
            }

            label = icons[piece]

            if selected == (r,c):
                label = "🟢"

            if cols[c].button(
                label,
                key=f"checker_{r}_{c}",
                use_container_width=True
            ):

                if st.session_state.check_over:
                    continue

                if selected is None:

                    if piece in (1,3):
                        st.session_state.check_selected = (r,c)

                else:

                    candidate = [
                        m for m in moves
                        if m[0] == selected
                        and m[1] == (r,c)
                    ]

                    if candidate:

                        apply_checker(candidate[0])

                        st.session_state.check_selected = None

                        if not checker_moves(
                            st.session_state.checkers,
                            2
                        ):

                            st.session_state.check_over = True
                            finish(
                                "win",
                                reward("Checkers")
                            )

                        else:

                            checker_bot()

                            if not checker_moves(
                                st.session_state.checkers,
                                1
                            ):

                                st.session_state.check_over = True
                                finish("loss")

                    elif piece in (1,3):

                        st.session_state.check_selected = (r,c)

                    else:

                        st.session_state.check_selected = None

                    st.rerun()


# ============================================================
# OTHELLO
# ============================================================

DIRECTIONS = [
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

    st.session_state.othello = board
    st.session_state.othello_over = False


def legal_othello(board, player):

    moves = []

    opponent = 3 - player

    for r in range(8):

        for c in range(8):

            if board[r][c]:
                continue

            for dr,dc in DIRECTIONS:

                rr = r + dr
                cc = c + dc
                found = False

                while (
                    0 <= rr < 8
                    and 0 <= cc < 8
                    and board[rr][cc] == opponent
                ):

                    found = True
                    rr += dr
                    cc += dc

                if (
                    found
                    and 0 <= rr < 8
                    and 0 <= cc < 8
                    and board[rr][cc] == player
                ):

                    moves.append((r,c))
                    break

    return moves


def place_othello(r,c,player):

    board = st.session_state.othello

    opponent = 3 - player

    board[r][c] = player

    for dr,dc in DIRECTIONS:

        path = []

        rr = r + dr
        cc = c + dc

        while (
            0 <= rr < 8
            and 0 <= cc < 8
            and board[rr][cc] == opponent
        ):

            path.append((rr,cc))

            rr += dr
            cc += dc

        if (
            path
            and 0 <= rr < 8
            and 0 <= cc < 8
            and board[rr][cc] == player
        ):

            for pr,pc in path:
                board[pr][pc] = player


def othello_bot():

    moves = legal_othello(
        st.session_state.othello,
        2
    )

    if not moves:
        return

    corners = [
        (0,0),
        (0,7),
        (7,0),
        (7,7)
    ]

    corner_moves = [
        m for m in moves
        if m in corners
    ]

    if corner_moves:

        move = random.choice(corner_moves)

    else:

        move = random.choice(moves)

    place_othello(*move,2)


def play_othello():

    st.markdown("### 🟢 Othello")
    st.caption("Flip the bot's pieces and finish with the highest score.")

    legal = legal_othello(
        st.session_state.othello,
        1
    )

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            value = st.session_state.othello[r][c]

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
                key=f"oth_{r}_{c}",
                use_container_width=True
            ):

                if (
                    (r,c) in legal
                    and not st.session_state.othello_over
                ):

                    place_othello(r,c,1)

                    bot_moves = legal_othello(
                        st.session_state.othello,
                        2
                    )

                    if bot_moves:
                        othello_bot()

                    else:

                        player_moves = legal_othello(
                            st.session_state.othello,
                            1
                        )

                        if not player_moves:

                            p = sum(
                                row.count(1)
                                for row in st.session_state.othello
                            )

                            b = sum(
                                row.count(2)
                                for row in st.session_state.othello
                            )

                            st.session_state.othello_over = True

                            finish(
                                "win" if p > b
                                else "loss" if b > p
                                else "draw",
                                reward("Othello") if p > b else 0
                            )

                    st.rerun()

    player_score = sum(
        row.count(1)
        for row in st.session_state.othello
    )

    bot_score = sum(
        row.count(2)
        for row in st.session_state.othello
    )

    st.caption(
        f"⚪ You: {player_score}   •   ⚫ Bot: {bot_score}"
    )


# ============================================================
# GOMOKU
# ============================================================

def init_gomoku():

    st.session_state.gomoku = [
        [0]*15
        for _ in range(15)
    ]

    st.session_state.gomoku_over = False


def gomoku_win(board,r,c,player):

    for dr,dc in DIRECTIONS:

        count = 1

        for direction in (1,-1):

            rr = r + dr*direction
            cc = c + dc*direction

            while (
                0 <= rr < 15
                and 0 <= cc < 15
                and board[rr][cc] == player
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

    if not empty:
        return

    # Winning move.
    for r,c in empty:

        board[r][c] = 2

        if gomoku_win(board,r,c,2):
            return

        board[r][c] = 0

    # Blocking move.
    for r,c in empty:

        board[r][c] = 1

        if gomoku_win(board,r,c,1):

            board[r][c] = 2
            return

        board[r][c] = 0

    # Centre-ish move.
    choices = sorted(
        empty,
        key=lambda x:
        abs(x[0]-7) + abs(x[1]-7)
    )

    if difficulty_level() == 0:
        move = random.choice(empty)
    else:
        move = random.choice(
            choices[:min(25,len(choices))]
        )

    board[move[0]][move[1]] = 2


def play_gomoku():

    st.markdown("### 🟨 Gomoku")
    st.caption("Get five stones in a row.")

    for r in range(15):

        cols = st.columns(15)

        for c in range(15):

            value = st.session_state.gomoku[r][c]

            label = (
                "⚪" if value == 1
                else "⚫" if value == 2
                else "·"
            )

            if cols[c].button(
                label,
                key=f"gom_{r}_{c}",
                use_container_width=True
            ):

                if (
                    value == 0
                    and not st.session_state.gomoku_over
                ):

                    st.session_state.gomoku[r][c] = 1

                    if gomoku_win(
                        st.session_state.gomoku,
                        r,c,
                        1
                    ):

                        st.session_state.gomoku_over = True

                        finish(
                            "win",
                            reward("Gomoku")
                        )

                    else:

                        gomoku_bot()

                        won = False

                        for rr in range(15):

                            for cc in range(15):

                                if (
                                    st.session_state.gomoku[rr][cc] == 2
                                    and gomoku_win(
                                        st.session_state.gomoku,
                                        rr,cc,
                                        2
                                    )
                                ):

                                    won = True
                                    break

                            if won:
                                break

                        if won:

                            st.session_state.gomoku_over = True
                            finish("loss")

                        elif all(
                            st.session_state.gomoku[r][c]
                            for r in range(15)
                            for c in range(15)
                        ):

                            st.session_state.gomoku_over = True
                            finish("draw")

                    st.rerun()


# ============================================================
# BATTLESHIP
# ============================================================

def init_battleship():

    st.session_state.bs_player = [
        [0]*8 for _ in range(8)
    ]

    st.session_state.bs_bot = [
        [0]*8 for _ in range(8)
    ]

    st.session_state.bs_shots = [
        [0]*8 for _ in range(8)
    ]

    st.session_state.bs_bot_shots = [
        [0]*8 for _ in range(8)
    ]

    ships = [3,2,2]

    place_ships(
        st.session_state.bs_player,
        ships
    )

    place_ships(
        st.session_state.bs_bot,
        ships
    )

    st.session_state.bs_over = False


def place_ships(board, ships):

    for size in ships:

        while True:

            horizontal = random.choice([True,False])

            r = random.randrange(8)
            c = random.randrange(8)

            cells = (
                [(r,c+i) for i in range(size)]
                if horizontal
                else [(r+i,c) for i in range(size)]
            )

            if all(
                0 <= rr < 8
                and 0 <= cc < 8
                and board[rr][cc] == 0
                for rr,cc in cells
            ):

                for rr,cc in cells:
                    board[rr][cc] = 1

                break


def ships_remaining(board):

    return sum(
        cell == 1
        for row in board
        for cell in row
    )


def battleship_bot():

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

    st.markdown("### 🚢 Battleship")
    st.caption("Find and destroy the bot's fleet.")

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            shot = st.session_state.bs_shots[r][c]

            label = (
                "💥" if shot == 2
                else "💧" if shot == 1
                else "·"
            )

            if cols[c].button(
                label,
                key=f"ship_{r}_{c}",
                use_container_width=True
            ):

                if (
                    shot == 0
                    and not st.session_state.bs_over
                ):

                    if st.session_state.bs_bot[r][c] == 1:

                        st.session_state.bs_bot[r][c] = 2
                        st.session_state.bs_shots[r][c] = 2

                    else:

                        st.session_state.bs_shots[r][c] = 1

                    if ships_remaining(
                        st.session_state.bs_bot
                    ) == 0:

                        st.session_state.bs_over = True

                        finish(
                            "win",
                            reward("Battleship")
                        )

                    else:

                        battleship_bot()

                        if ships_remaining(
                            st.session_state.bs_player
                        ) == 0:

                            st.session_state.bs_over = True
                            finish("loss")

                    st.rerun()

    with st.expander("Your Fleet"):

        for row in st.session_state.bs_player:

            st.write(
                " ".join(
                    "🚢" if x == 1
                    else "💥" if x == 2
                    else "·"
                    for x in row
                )
            )


# ============================================================
# CHESS
# ============================================================

def init_chess():

    if chess is None:

        st.session_state.chess_board = None

    else:

        st.session_state.chess_board = chess.Board()

    st.session_state.chess_selected = None
    st.session_state.chess_over = False


def chess_bot():

    board = st.session_state.chess_board

    moves = list(board.legal_moves)

    if not moves:
        return

    level = difficulty_level()

    if level == 0:

        move = random.choice(moves)

    else:

        captures = [
            m for m in moves
            if board.is_capture(m)
        ]

        checks = [
            m for m in moves
            if board.gives_check(m)
        ]

        if checks and level >= 2:
            move = random.choice(checks)

        elif captures:
            move = random.choice(captures)

        else:
            move = random.choice(moves)

    board.push(move)


def chess_symbol(piece):

    symbols = {
        "P": "♙",
        "N": "♘",
        "B": "♗",
        "R": "♖",
        "Q": "♕",
        "K": "♔",
        "p": "♟",
        "n": "♞",
        "b": "♝",
        "r": "♜",
        "q": "♛",
        "k": "♚"
    }

    return symbols.get(piece.symbol(), "")


def play_chess():

    st.markdown("### ♟ Chess")
    st.caption("You are White.")

    if chess is None:

        st.error(
            "Chess is unavailable. "
            "Make sure python-chess is in requirements.txt."
        )

        return

    board = st.session_state.chess_board

    legal = list(board.legal_moves)

    selected = st.session_state.chess_selected

    files = "abcdefgh"
    ranks = "87654321"

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            square = chess.parse_square(
                files[c] + ranks[r]
            )

            piece = board.piece_at(square)

            label = (
                chess_symbol(piece)
                if piece
                else " "
            )

            target = any(
                m.from_square == selected
                and m.to_square == square
                for m in legal
            ) if selected is not None else False

            if target:
                label = "🟢"

            if cols[c].button(
                label,
                key=f"chess_{r}_{c}",
                use_container_width=True
            ):

                if board.turn != chess.WHITE:
                    continue

                if selected is None:

                    if (
                        piece
                        and piece.color == chess.WHITE
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

                        if board.is_game_over():

                            st.session_state.chess_over = True

                            if board.is_checkmate():

                                finish(
                                    "win",
                                    reward("Chess")
                                )

                            else:
                                finish("draw")

                        else:

                            chess_bot()

                            if board.is_game_over():

                                st.session_state.chess_over = True

                                if board.is_checkmate():
                                    finish("loss")
                                else:
                                    finish("draw")

                    elif (
                        piece
                        and piece.color == chess.WHITE
                    ):

                        st.session_state.chess_selected = square

                    else:

                        st.session_state.chess_selected = None

                st.rerun()


# ============================================================
# BLACKJACK
# ============================================================

SUITS = ["♠","♥","♦","♣"]

RANKS = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K"
]


def blackjack_deck():

    return [
        (rank,suit)
        for suit in SUITS
        for rank in RANKS
    ]


def blackjack_value(cards):

    total = 0
    aces = 0

    for rank,suit in cards:

        if rank == "A":

            total += 11
            aces += 1

        elif rank in ("K","Q","J"):

            total += 10

        else:

            total += int(rank)

    while total > 21 and aces:

        total -= 10
        aces -= 1

    return total


def init_blackjack():

    deck = blackjack_deck()

    random.shuffle(deck)

    st.session_state.bj_deck = deck
    st.session_state.bj_player = []
    st.session_state.bj_dealer = []
    st.session_state.bj_bet = 25
    st.session_state.bj_active = False
    st.session_state.bj_over = False
    st.session_state.bj_message = ""
    st.session_state.bj_type = ""


def bj_draw():

    if not st.session_state.bj_deck:

        st.session_state.bj_deck = blackjack_deck()

        random.shuffle(
            st.session_state.bj_deck
        )

    return st.session_state.bj_deck.pop()


def render_blackjack_cards(
    cards,
    hidden=False
):

    html = ""

    for i,(rank,suit) in enumerate(cards):

        if hidden and i == 0:

            html += """
            <span class="playing-card card-back">
                🂠
            </span>
            """

            continue

        red = suit in ("♥","♦")

        cls = "red-card" if red else ""

        html += f"""
        <span class="playing-card {cls}">
            <span class="card-rank">{rank}</span>
            <span class="card-suit">{suit}</span>
        </span>
        """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def bj_deal():

    bet = int(st.session_state.bj_bet)

    if bet <= 0:

        st.session_state.bj_message = (
            "Choose a valid bet."
        )

        return

    if bet > st.session_state.balance:

        st.session_state.bj_message = (
            "You don't have enough BOT BUCKS."
        )

        return

    money(-bet)

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
    st.session_state.bj_type = ""

    player = blackjack_value(
        st.session_state.bj_player
    )

    dealer = blackjack_value(
        st.session_state.bj_dealer
    )

    if player == 21:

        profit = int(bet * 1.5)

        money(bet + profit)

        st.session_state.bj_message = (
            f"BLACKJACK! +{profit} BB"
        )

        st.session_state.bj_type = "win"
        st.session_state.bj_over = True

        st.session_state.earned += 0

        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            profit
        )

        unlock("Blackjack!")

    elif dealer == 21:

        money(bet)

        st.session_state.bj_message = (
            "Dealer has Blackjack."
        )

        st.session_state.bj_type = "loss"
        st.session_state.bj_over = True


def bj_finish():

    bet = int(st.session_state.bj_bet)

    player = blackjack_value(
        st.session_state.bj_player
    )

    if player > 21:

        st.session_state.bj_message = (
            f"BUST — You lost {bet} BB."
        )

        st.session_state.bj_type = "loss"
        st.session_state.bj_over = True

        return

    while blackjack_value(
        st.session_state.bj_dealer
    ) < 17:

        st.session_state.bj_dealer.append(
            bj_draw()
        )

    dealer = blackjack_value(
        st.session_state.bj_dealer
    )

    if dealer > 21 or player > dealer:

        money(bet * 2)

        st.session_state.bj_message = (
            f"YOU WIN +{bet} BB"
        )

        st.session_state.bj_type = "win"

        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            bet
        )

        if bet >= 500:
            unlock("High Roller")

    elif player == dealer:

        money(bet)

        st.session_state.bj_message = (
            "PUSH — Bet returned."
        )

        st.session_state.bj_type = "draw"

    else:

        st.session_state.bj_message = (
            f"DEALER WINS — You lost {bet} BB."
        )

        st.session_state.bj_type = "loss"

    st.session_state.bj_over = True


def play_blackjack():

    st.markdown("### 🃏 Blackjack")

    st.caption(
        "Classic blackjack • BOT BUCKS are fictional in-game currency."
    )

    # BETTING SCREEN

    if (
        not st.session_state.bj_active
        and not st.session_state.bj_over
    ):

        st.markdown(
            """
            <div class="blackjack-table">

                <div class="table-label">
                    BOT BOARD CASINO
                </div>

                <br>

                <div style="font-size:65px;">
                    🃏
                </div>

                <div style="
                    font-size:32px;
                    font-weight:900;
                    margin:15px;
                ">
                    BLACKJACK
                </div>

                <div style="
                    color:rgba(255,255,255,.7);
                ">
                    Beat the dealer. Get as close to 21 as possible.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("###")

        col1,col2,col3 = st.columns([1,2,1])

        with col2:

            max_bet = max(
                1,
                st.session_state.balance
            )

            st.session_state.bj_bet = st.number_input(
                "Bet",
                min_value=1,
                max_value=max_bet,
                value=min(25,max_bet),
                step=5
            )

            st.markdown(
                f"""
                <div class="balance">
                    <div class="balance-label">
                        AVAILABLE
                    </div>
                    <div class="balance-value">
                        💰 {st.session_state.balance:,} BB
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "🃏 DEAL CARDS",
                type="primary",
                use_container_width=True
            ):

                bj_deal()

                st.rerun()

        return

    # REALISTIC TABLE

    player_total = blackjack_value(
        st.session_state.bj_player
    )

    dealer_total = blackjack_value(
        st.session_state.bj_dealer
    )

    st.markdown(
        """
        <div class="blackjack-table">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="table-label">DEALER</div>',
        unsafe_allow_html=True
    )

    render_blackjack_cards(
        st.session_state.bj_dealer,
        hidden=not st.session_state.bj_over
    )

    if st.session_state.bj_over:

        st.markdown(
            f'<div class="table-total">Dealer — {dealer_total}</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="table-total">Dealer — ?</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="table-label">YOU</div>',
        unsafe_allow_html=True
    )

    render_blackjack_cards(
        st.session_state.bj_player
    )

    st.markdown(
        f'<div class="table-total">You — {player_total}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("###")

    if not st.session_state.bj_over:

        c1,c2 = st.columns(2)

        with c1:

            if st.button(
                "👊 HIT",
                use_container_width=True
            ):

                st.session_state.bj_player.append(
                    bj_draw()
                )

                if blackjack_value(
                    st.session_state.bj_player
                ) > 21:

                    bj_finish()

                st.rerun()

        with c2:

            if st.button(
                "✋ STAND",
                type="primary",
                use_container_width=True
            ):

                bj_finish()

                st.rerun()

    else:

        msg = st.session_state.bj_message

        if st.session_state.bj_type == "win":

            st.markdown(
                f'<div class="win-box">🎉 {msg}</div>',
                unsafe_allow_html=True
            )

        elif st.session_state.bj_type == "loss":

            st.markdown(
                f'<div class="loss-box">🤖 {msg}</div>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f'<div class="info-box">🤝 {msg}</div>',
                unsafe_allow_html=True
            )

        st.markdown("###")

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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:25px;
            font-weight:900;
            padding:10px 0 20px;
        ">
            🤖 BOT BOARD
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="balance">
            <div class="balance-label">
                BALANCE
            </div>
            <div class="balance-value">
                💰 {st.session_state.balance:,} BB
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
            "← Back to Games",
            use_container_width=True
        ):

            st.session_state.game = None
            st.rerun()

        if st.button(
            "↻ Restart Game",
            use_container_width=True
        ):

            start_game(
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
            <p>Your BOT BOARD stats and BOT BUCKS.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="stat">
                <div class="stat-number">
                    {st.session_state.balance:,}
                </div>
                <div class="stat-label">
                    BALANCE
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="stat">
                <div class="stat-number">
                    {st.session_state.earned:,}
                </div>
                <div class="stat-label">
                    TOTAL EARNED
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="stat">
                <div class="stat-number">
                    {st.session_state.lost:,}
                </div>
                <div class="stat-label">
                    TOTAL LOST
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("###")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric(
            "Biggest Win",
            f"{st.session_state.biggest_win:,} BB"
        )

    with c2:
        st.metric(
            "Current Streak",
            st.session_state.streak
        )

    with c3:
        st.metric(
            "Best Streak",
            st.session_state.best_streak
        )

    st.markdown("###")

    if not st.session_state.daily_bonus:

        if st.button(
            "🎁 Claim Daily Bonus — +250 BB",
            type="primary",
            use_container_width=True
        ):

            st.session_state.balance += 250
            st.session_state.earned += 250
            st.session_state.daily_bonus = True

            st.rerun()

    else:

        st.success(
            "Daily bonus already claimed this session."
        )

    st.info(
        "BOT BUCKS are fictional game currency only. "
        "They cannot be purchased, withdrawn or converted to real money."
    )


# ============================================================
# ACHIEVEMENTS
# ============================================================

elif page == "🏆 Achievements":

    st.markdown(
        """
        <div class="hero">
            <h1>🏆 Achievements</h1>
            <p>Complete challenges and collect every badge.</p>
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
                f"🏆 **{name}**  —  {description}"
            )

        else:

            st.markdown(
                f"""
                <div class="panel">
                    🔒 <b>{name}</b>
                    <br>
                    <span style="color:#718096;">
                        {description}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# GAMES HOME
# ============================================================

elif st.session_state.game is None:

    st.markdown(
        """
        <div class="hero">
            <h1>🤖 BOT BOARD</h1>
            <p>
                Play classic games. Beat the bots.
                Build your balance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="balance">
            <div class="balance-label">
                YOUR BOT BUCKS
            </div>
            <div class="balance-value">
                💰 {st.session_state.balance:,} BB
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    games = [
        (
            "🎯",
            "Tic Tac Toe",
            "Quick classic strategy."
        ),
        (
            "🟡",
            "Connect 4",
            "Get four in a row."
        ),
        (
            "⚫",
            "Checkers",
            "Capture the bot's pieces."
        ),
        (
            "🟢",
            "Othello",
            "Flip the board."
        ),
        (
            "🟨",
            "Gomoku",
            "Five in a row wins."
        ),
        (
            "🚢",
            "Battleship",
            "Find and destroy the fleet."
        ),
        (
            "♟️",
            "Chess",
            "Classic strategy."
        ),
        (
            "🃏",
            "Blackjack",
            "Beat the dealer."
        )
    ]

    cols = st.columns(2)

    for i,(icon,name,description) in enumerate(games):

        with cols[i % 2]:

            st.markdown(
                f"""
                <div class="game-card">
                    <div class="game-icon">
                        {icon}
                    </div>

                    <div class="game-title">
                        {name}
                    </div>

                    <div class="game-desc">
                        {description}
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

                start_game(name)

                st.rerun()


# ============================================================
# ACTIVE GAME
# ============================================================

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
                "Bot Difficulty",
                DIFFICULTIES,
                index=DIFFICULTIES.index(
                    st.session_state.difficulty
                )
            )

    with top3:

        st.markdown(
            f"""
            <div class="balance">
                <div class="balance-label">
                    BALANCE
                </div>
                <div style="
                    color:#facc15;
                    font-size:20px;
                    font-weight:900;
                ">
                    💰 {st.session_state.balance:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if name != "Blackjack":

        st.caption(
            f"🏆 Win reward: +{reward(name)} BB"
        )

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

        if st.session_state.result == "win":

            st.markdown(
                f"""
                <div class="win-box">
                    🎉 YOU WON! &nbsp; +{reward(name)} BB
                </div>
                """,
                unsafe_allow_html=True
            )

        elif st.session_state.result == "loss":

            st.markdown(
                """
                <div class="loss-box">
                    🤖 THE BOT WON
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="info-box">
                    🤝 DRAW
                </div>
                """,
                unsafe_allow_html=True
            )
