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
    initial_sidebar_state="expanded",
)


# ============================================================
# MODERN UI
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(99,102,241,.18), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(168,85,247,.14), transparent 28%),
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

/* HERO */

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

.hero h1 {
    font-size: clamp(42px, 6vw, 72px);
    font-weight: 900;
    letter-spacing: -4px;
    margin: 0;
    color: white;
}

.hero p {
    color: #aab4c7;
    font-size: 18px;
    margin: 8px 0 0;
}

.balance-pill {
    display: inline-block;
    margin-top: 22px;
    padding: 12px 18px;
    border-radius: 999px;
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.10);
    font-weight: 700;
}

/* GAME CARDS */

.game-card {
    min-height: 205px;
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

/* STATS */

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

/* BUTTONS */

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

/* ============================================================
   BLACKJACK TABLE
   ============================================================ */

.blackjack-wrap {
    padding: 8px;
}

.blackjack-table {
    position: relative;
    min-height: 650px;
    padding: 35px 28px 30px;
    border-radius: 42px;
    background:
        radial-gradient(
            ellipse at center,
            #167346 0%,
            #0d5a36 48%,
            #063b24 100%
        );
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
    border-radius: 50%;
    pointer-events: none;
}

.casino-title {
    text-align: center;
    position: relative;
    z-index: 2;
    font-size: 25px;
    font-weight: 900;
    letter-spacing: 5px;
    color: rgba(255,255,255,.92);
}

.casino-subtitle {
    text-align: center;
    position: relative;
    z-index: 2;
    color: rgba(255,255,255,.55);
    font-size: 12px;
    margin-top: 3px;
    letter-spacing: 1px;
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
    background: linear-gradient(145deg, #ffffff, #e9edf4);
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

.chip-row {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: center;
    gap: 9px;
    margin: 8px 0 15px;
}

.casino-chip {
    width: 52px;
    height: 52px;
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

/* RESPONSIVE */

@media (max-width: 700px) {

    .hero {
        padding: 28px 22px;
    }

    .hero h1 {
        letter-spacing: -2px;
    }

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

    .playing-card .suit-center {
        font-size: 26px;
        margin-top: 8px;
    }

    .playing-card .corner {
        font-size: 13px;
    }

    .cards {
        gap: 5px;
        min-height: 95px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
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

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


DIFFICULTIES = [
    "Easy",
    "Medium",
    "Hard",
    "Impossible",
]


REWARDS = {
    "Tic Tac Toe": {
        "Easy": 25,
        "Medium": 50,
        "Hard": 100,
        "Impossible": 200,
    },
    "Connect 4": {
        "Easy": 50,
        "Medium": 100,
        "Hard": 200,
        "Impossible": 400,
    },
    "Checkers": {
        "Easy": 75,
        "Medium": 150,
        "Hard": 300,
        "Impossible": 600,
    },
    "Othello": {
        "Easy": 100,
        "Medium": 200,
        "Hard": 400,
        "Impossible": 800,
    },
    "Gomoku": {
        "Easy": 75,
        "Medium": 150,
        "Hard": 300,
        "Impossible": 600,
    },
    "Battleship": {
        "Easy": 100,
        "Medium": 200,
        "Hard": 400,
        "Impossible": 800,
    },
    "Chess": {
        "Easy": 150,
        "Medium": 300,
        "Hard": 600,
        "Impossible": 1200,
    },
}


# ============================================================
# GENERAL FUNCTIONS
# ============================================================

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


def reward_for(name):
    return REWARDS.get(name, {}).get(
        st.session_state.difficulty,
        0
    )


def bot_strength():
    return DIFFICULTIES.index(
        st.session_state.difficulty
    )


# ============================================================
# TIC TAC TOE
# ============================================================

def init_ttt():

    st.session_state.ttt = [""] * 9
    st.session_state.ttt_over = False


def ttt_winner(board):

    lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    for a, b, c in lines:

        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if all(board):
        return "draw"

    return None


def ttt_minimax(board, maximizing):

    result = ttt_winner(board)

    if result == "O":
        return 10

    if result == "X":
        return -10

    if result == "draw":
        return 0

    scores = []

    for i in range(9):

        if not board[i]:

            board[i] = "O" if maximizing else "X"

            score = ttt_minimax(
                board,
                not maximizing
            )

            board[i] = ""

            scores.append(score)

    return max(scores) if maximizing else min(scores)


def ttt_bot_move():

    board = st.session_state.ttt

    empty = [
        i
        for i, value in enumerate(board)
        if not value
    ]

    if not empty:
        return

    level = bot_strength()

    if level == 0:

        move = random.choice(empty)

    elif level == 1:

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

    else:

        best = None
        best_score = -999

        for i in empty:

            board[i] = "O"

            score = ttt_minimax(
                board,
                False
            )

            board[i] = ""

            if score > best_score:

                best_score = score
                best = i

        move = best

    board[move] = "O"


def play_ttt():

    st.subheader("❌ Tic Tac Toe")
    st.caption("You are X • Bot is O")

    cols = st.columns(3)

    for i in range(9):

        with cols[i % 3]:

            label = st.session_state.ttt[i] or " "

            if st.button(
                label,
                key=f"ttt_{i}",
                use_container_width=True
            ):

                if (
                    not st.session_state.ttt_over
                    and not st.session_state.ttt[i]
                ):

                    st.session_state.ttt[i] = "X"

                    result = ttt_winner(
                        st.session_state.ttt
                    )

                    if result == "X":

                        st.session_state.ttt_over = True

                        finish_game(
                            "win",
                            reward_for("Tic Tac Toe")
                        )

                    elif result == "draw":

                        st.session_state.ttt_over = True
                        finish_game("draw")

                    else:

                        ttt_bot_move()

                        result = ttt_winner(
                            st.session_state.ttt
                        )

                        if result:

                            st.session_state.ttt_over = True

                            finish_game(
                                "loss"
                                if result == "O"
                                else "draw"
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

            player = board[r][c]

            if not player:
                continue

            for dr, dc in [
                (1, 0),
                (0, 1),
                (1, 1),
                (1, -1),
            ]:

                cells = []

                for k in range(4):

                    rr = r + dr * k
                    cc = c + dc * k

                    if (
                        0 <= rr < 6
                        and 0 <= cc < 7
                    ):
                        cells.append(
                            board[rr][cc]
                        )

                if (
                    len(cells) == 4
                    and cells == [player] * 4
                ):
                    return player

    return None


def c4_drop(column, player):

    for row in range(5, -1, -1):

        if st.session_state.c4[row][column] == 0:

            st.session_state.c4[row][column] = player

            return row

    return None


def c4_bot_move():

    valid = [
        c
        for c in range(7)
        if st.session_state.c4[0][c] == 0
    ]

    if not valid:
        return

    # Try winning.
    for column in valid:

        row = c4_drop(column, 2)

        if c4_winner(st.session_state.c4) == 2:
            return

        st.session_state.c4[row][column] = 0

    # Block player.
    if bot_strength() >= 1:

        for column in valid:

            row = c4_drop(column, 1)

            if c4_winner(st.session_state.c4) == 1:

                st.session_state.c4[row][column] = 0

                c4_drop(column, 2)

                return

            st.session_state.c4[row][column] = 0

    preferred = [
        3,
        2,
        4,
        1,
        5,
        0,
        6,
    ]

    choices = [
        c
        for c in preferred
        if c in valid
    ]

    c4_drop(
        random.choice(choices),
        2
    )


def play_connect4():

    st.subheader("🟡 Connect 4")

    st.caption(
        "Drop four pieces in a row before the bot."
    )

    cols = st.columns(7)

    for c in range(7):

        with cols[c]:

            if st.button(
                "↓",
                key=f"c4drop{c}",
                use_container_width=True,
                disabled=st.session_state.c4_over
            ):

                if c4_drop(c, 1) is not None:

                    winner = c4_winner(
                        st.session_state.c4
                    )

                    if winner == 1:

                        st.session_state.c4_over = True

                        finish_game(
                            "win",
                            reward_for("Connect 4")
                        )

                    elif all(
                        st.session_state.c4[0][x]
                        for x in range(7)
                    ):

                        st.session_state.c4_over = True

                        finish_game("draw")

                    else:

                        c4_bot_move()

                        winner = c4_winner(
                            st.session_state.c4
                        )

                        if winner == 2:

                            st.session_state.c4_over = True
                            finish_game("loss")

                        elif all(
                            st.session_state.c4[0][x]
                            for x in range(7)
                        ):

                            st.session_state.c4_over = True
                            finish_game("draw")

                    st.rerun()

    symbols = {
        0: "⚪",
        1: "🔴",
        2: "🟡",
    }

    for row in st.session_state.c4:

        cols = st.columns(7)

        for c, cell in enumerate(row):

            cols[c].markdown(
                f"""
                <div style="
                    text-align:center;
                    font-size:30px;
                    padding:3px;
                ">
                    {symbols[cell]}
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# OTHELLO
# ============================================================

DIRS = [
    (dr, dc)
    for dr in (-1, 0, 1)
    for dc in (-1, 0, 1)
    if (dr, dc) != (0, 0)
]


def init_othello():

    board = [
        [0] * 8
        for _ in range(8)
    ]

    board[3][3] = 2
    board[4][4] = 2
    board[3][4] = 1
    board[4][3] = 1

    st.session_state.oth = board
    st.session_state.oth_over = False


def oth_moves(board, player):

    moves = []
    opponent = 3 - player

    for r in range(8):

        for c in range(8):

            if board[r][c]:
                continue

            for dr, dc in DIRS:

                rr = r + dr
                cc = c + dc
                seen = False

                while (
                    0 <= rr < 8
                    and 0 <= cc < 8
                    and board[rr][cc] == opponent
                ):

                    seen = True

                    rr += dr
                    cc += dc

                if (
                    seen
                    and 0 <= rr < 8
                    and 0 <= cc < 8
                    and board[rr][cc] == player
                ):

                    moves.append((r, c))
                    break

    return list(dict.fromkeys(moves))


def oth_play(row, col, player):

    board = st.session_state.oth

    board[row][col] = player

    opponent = 3 - player

    for dr, dc in DIRS:

        path = []

        rr = row + dr
        cc = col + dc

        while (
            0 <= rr < 8
            and 0 <= cc < 8
            and board[rr][cc] == opponent
        ):

            path.append((rr, cc))

            rr += dr
            cc += dc

        if (
            path
            and 0 <= rr < 8
            and 0 <= cc < 8
            and board[rr][cc] == player
        ):

            for r, c in path:
                board[r][c] = player


def oth_bot():

    moves = oth_moves(
        st.session_state.oth,
        2
    )

    if not moves:
        return

    corners = {
        (0, 0),
        (0, 7),
        (7, 0),
        (7, 7),
    }

    def score(move):

        temp = [
            row[:]
            for row in st.session_state.oth
        ]

        before = sum(
            row.count(2)
            for row in temp
        )

        r, c = move

        temp[r][c] = 2

        for dr, dc in DIRS:

            path = []

            rr = r + dr
            cc = c + dc

            while (
                0 <= rr < 8
                and 0 <= cc < 8
                and temp[rr][cc] == 1
            ):

                path.append((rr, cc))

                rr += dr
                cc += dc

            if (
                path
                and 0 <= rr < 8
                and 0 <= cc < 8
                and temp[rr][cc] == 2
            ):

                for x, y in path:
                    temp[x][y] = 2

        gained = (
            sum(row.count(2) for row in temp)
            - before
        )

        return (
            100 if move in corners else 0
        ) + gained * 8

    best_move = max(
        moves,
        key=score
    )

    oth_play(
        best_move[0],
        best_move[1],
        2
    )


def play_othello():

    st.subheader("🟢 Othello")

    legal = oth_moves(
        st.session_state.oth,
        1
    )

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            value = st.session_state.oth[r][c]

            if value == 2:
                label = "⚫"
            elif value == 1:
                label = "⚪"
            elif (r, c) in legal:
                label = "🟢"
            else:
                label = "·"

            if cols[c].button(
                label,
                key=f"oth{r}_{c}",
                use_container_width=True
            ):

                if (
                    (r, c) in legal
                    and not st.session_state.oth_over
                ):

                    oth_play(r, c, 1)

                    if (
                        not oth_moves(
                            st.session_state.oth,
                            1
                        )
                        and not oth_moves(
                            st.session_state.oth,
                            2
                        )
                    ):

                        player_score = sum(
                            row.count(1)
                            for row in st.session_state.oth
                        )

                        bot_score = sum(
                            row.count(2)
                            for row in st.session_state.oth
                        )

                        st.session_state.oth_over = True

                        finish_game(
                            "win"
                            if player_score > bot_score
                            else "loss"
                            if bot_score > player_score
                            else "draw"
                        )

                    else:

                        oth_bot()

                    st.rerun()

    player_score = sum(
        row.count(1)
        for row in st.session_state.oth
    )

    bot_score = sum(
        row.count(2)
        for row in st.session_state.oth
    )

    st.caption(
        f"You: {player_score}  •  Bot: {bot_score}"
    )


# ============================================================
# GOMOKU
# ============================================================

def init_gomoku():

    st.session_state.gom = [
        [0] * 15
        for _ in range(15)
    ]

    st.session_state.gom_over = False


def gom_win(board, row, col, player):

    for dr, dc in DIRS:

        count = 1

        for sign in (1, -1):

            rr = row + dr * sign
            cc = col + dc * sign

            while (
                0 <= rr < 15
                and 0 <= cc < 15
                and board[rr][cc] == player
            ):

                count += 1

                rr += dr * sign
                cc += dc * sign

        if count >= 5:
            return True

    return False


def gom_bot():

    board = st.session_state.gom

    empty = [
        (r, c)
        for r in range(15)
        for c in range(15)
        if board[r][c] == 0
    ]

    if not empty:
        return

    # Win or block.
    for player in (2, 1):

        for r, c in empty:

            board[r][c] = player

            won = gom_win(
                board,
                r,
                c,
                player
            )

            board[r][c] = 0

            if won:

                board[r][c] = 2

                return

    if bot_strength() >= 2:

        def score(move):

            r, c = move

            nearby = 0

            for dr, dc in DIRS:

                rr = r + dr
                cc = c + dc

                if (
                    0 <= rr < 15
                    and 0 <= cc < 15
                    and board[rr][cc]
                ):
                    nearby += 1

            center = (
                14
                - abs(r - 7)
                - abs(c - 7)
            )

            return nearby * 10 + center

        move = max(
            empty,
            key=score
        )

    else:

        move = random.choice(empty)

    board[move[0]][move[1]] = 2


def play_gomoku():

    st.subheader("🟨 Gomoku")
    st.caption("Five connected pieces wins.")

    for r in range(15):

        cols = st.columns(15)

        for c in range(15):

            value = st.session_state.gom[r][c]

            if value == 2:
                label = "⚫"
            elif value == 1:
                label = "⚪"
            else:
                label = "·"

            if cols[c].button(
                label,
                key=f"gom{r}_{c}",
                use_container_width=True
            ):

                if (
                    not st.session_state.gom_over
                    and value == 0
                ):

                    st.session_state.gom[r][c] = 1

                    if gom_win(
                        st.session_state.gom,
                        r,
                        c,
                        1
                    ):

                        st.session_state.gom_over = True

                        finish_game(
                            "win",
                            reward_for("Gomoku")
                        )

                    else:

                        gom_bot()

                        bot_won = any(
                            st.session_state.gom[rr][cc] == 2
                            and gom_win(
                                st.session_state.gom,
                                rr,
                                cc,
                                2
                            )
                            for rr in range(15)
                            for cc in range(15)
                        )

                        if bot_won:

                            st.session_state.gom_over = True

                            finish_game("loss")

                        elif all(
                            st.session_state.gom[x][y]
                            for x in range(15)
                            for y in range(15)
                        ):

                            st.session_state.gom_over = True

                            finish_game("draw")

                    st.rerun()


# ============================================================
# BATTLESHIP
# ============================================================

def place_fleet(board, ships):

    for size in ships:

        while True:

            horizontal = random.choice(
                [True, False]
            )

            row = random.randrange(8)
            col = random.randrange(8)

            if horizontal:

                cells = [
                    (row, col + i)
                    for i in range(size)
                ]

            else:

                cells = [
                    (row + i, col)
                    for i in range(size)
                ]

            if all(
                0 <= r < 8
                and 0 <= c < 8
                and board[r][c] == 0
                for r, c in cells
            ):

                for r, c in cells:
                    board[r][c] = 1

                break


def init_battleship():

    st.session_state.bs_player = [
        [0] * 8
        for _ in range(8)
    ]

    st.session_state.bs_bot = [
        [0] * 8
        for _ in range(8)
    ]

    st.session_state.bs_shots = [
        [0] * 8
        for _ in range(8)
    ]

    st.session_state.bs_bot_shots = [
        [0] * 8
        for _ in range(8)
    ]

    place_fleet(
        st.session_state.bs_player,
        [3, 2, 2]
    )

    place_fleet(
        st.session_state.bs_bot,
        [3, 2, 2]
    )

    st.session_state.bs_over = False


def bs_remaining(board):

    return sum(
        value == 1
        for row in board
        for value in row
    )


def bs_bot_shot():

    available = [
        (r, c)
        for r in range(8)
        for c in range(8)
        if st.session_state.bs_bot_shots[r][c] == 0
    ]

    if not available:
        return

    r, c = random.choice(available)

    st.session_state.bs_bot_shots[r][c] = 1

    if st.session_state.bs_player[r][c] == 1:
        st.session_state.bs_player[r][c] = 2


def play_battleship():

    st.subheader("🛳 Battleship")

    st.caption(
        "Find and destroy the bot's fleet."
    )

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            shot = st.session_state.bs_shots[r][c]

            if shot == 2:
                label = "💥"
            elif shot == 1:
                label = "💧"
            else:
                label = "?"

            if cols[c].button(
                label,
                key=f"bs{r}_{c}",
                use_container_width=True
            ):

                if (
                    not st.session_state.bs_over
                    and shot == 0
                ):

                    if st.session_state.bs_bot[r][c] == 1:

                        st.session_state.bs_bot[r][c] = 2
                        st.session_state.bs_shots[r][c] = 2

                    else:

                        st.session_state.bs_shots[r][c] = 1

                    if (
                        bs_remaining(
                            st.session_state.bs_bot
                        ) == 0
                    ):

                        st.session_state.bs_over = True

                        finish_game(
                            "win",
                            reward_for("Battleship")
                        )

                    else:

                        bs_bot_shot()

                        if (
                            bs_remaining(
                                st.session_state.bs_player
                            ) == 0
                        ):

                            st.session_state.bs_over = True

                            finish_game("loss")

                    st.rerun()

    with st.expander("Your fleet"):

        for row in st.session_state.bs_player:

            st.write(
                " ".join(
                    "🚢" if value == 1
                    else "💥" if value == 2
                    else "·"
                    for value in row
                )
            )


# ============================================================
# CHECKERS
# ============================================================

def init_checkers():

    board = [
        [0] * 8
        for _ in range(8)
    ]

    for r in range(3):

        for c in range(8):

            if (r + c) % 2:
                board[r][c] = 2

    for r in range(5, 8):

        for c in range(8):

            if (r + c) % 2:
                board[r][c] = 1

    st.session_state.chk = board
    st.session_state.chk_selected = None
    st.session_state.chk_over = False


def chk_moves(board, player):

    moves = []
    captures = []

    directions = [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    ]

    for r in range(8):

        for c in range(8):

            if board[r][c] not in (
                player,
                player + 2
            ):
                continue

            piece = board[r][c]
            king = piece in (3, 4)

            if king:

                dirs = directions

            elif player == 1:

                dirs = [
                    (-1, -1),
                    (-1, 1)
                ]

            else:

                dirs = [
                    (1, -1),
                    (1, 1)
                ]

            for dr, dc in dirs:

                rr = r + dr
                cc = c + dc

                if (
                    0 <= rr < 8
                    and 0 <= cc < 8
                    and board[rr][cc] == 0
                ):

                    moves.append(
                        (
                            (r, c),
                            (rr, cc),
                            None
                        )
                    )

                elif (
                    0 <= rr < 8
                    and 0 <= cc < 8
                    and board[rr][cc] not in (
                        0,
                        player,
                        player + 2
                    )
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
                                (r, c),
                                (jr, jc),
                                (rr, cc)
                            )
                        )

    return captures if captures else moves


def chk_apply(move):

    (
        (r, c),
        (rr, cc),
        captured
    ) = move

    board = st.session_state.chk

    piece = board[r][c]

    board[r][c] = 0
    board[rr][cc] = piece

    if captured:
        board[captured[0]][captured[1]] = 0

    if piece == 1 and rr == 0:
        board[rr][cc] = 3

    if piece == 2 and rr == 7:
        board[rr][cc] = 4


def chk_bot():

    moves = chk_moves(
        st.session_state.chk,
        2
    )

    if not moves:
        return

    captures = [
        move
        for move in moves
        if move[2] is not None
    ]

    chk_apply(
        random.choice(
            captures if captures else moves
        )
    )


def play_checkers():

    st.subheader("🏁 Checkers")

    moves = chk_moves(
        st.session_state.chk,
        1
    )

    selected = st.session_state.chk_selected

    for r in range(8):

        cols = st.columns(8)

        for c in range(8):

            value = st.session_state.chk[r][c]

            pieces = {
                0: "·",
                1: "⚪",
                2: "⚫",
                3: "👑",
                4: "👑",
            }

            label = pieces.get(
                value,
                "·"
            )

            if selected == (r, c):
                label = "🟢"

            if cols[c].button(
                label,
                key=f"chk{r}_{c}",
                use_container_width=True
            ):

                if st.session_state.chk_over:
                    continue

                if selected is None:

                    if value in (1, 3):
                        st.session_state.chk_selected = (
                            r,
                            c
                        )

                else:

                    candidate = [
                        move
                        for move in moves
                        if (
                            move[0] == selected
                            and move[1] == (r, c)
                        )
                    ]

                    if candidate:

                        chk_apply(
                            candidate[0]
                        )

                        st.session_state.chk_selected = None

                        if not chk_moves(
                            st.session_state.chk,
                            2
                        ):

                            st.session_state.chk_over = True

                            finish_game(
                                "win",
                                reward_for("Checkers")
                            )

                        else:

                            chk_bot()

                            if not chk_moves(
                                st.session_state.chk,
                                1
                            ):

                                st.session_state.chk_over = True

                                finish_game("loss")

                    elif value in (1, 3):

                        st.session_state.chk_selected = (
                            r,
                            c
                        )

                    else:

                        st.session_state.chk_selected = None

                    st.rerun()


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

    moves = list(
        board.legal_moves
    )

    if not moves:
        return

    captures = [
        move
        for move in moves
        if board.is_capture(move)
    ]

    checks = [
        move
        for move in moves
        if board.gives_check(move)
    ]

    if (
        bot_strength() >= 2
        and checks
    ):
        move = random.choice(checks)

    elif captures:
        move = random.choice(captures)

    else:
        move = random.choice(moves)

    board.push(move)


def play_chess():

    st.subheader("♟ Chess")

    if chess is None:

        st.error(
            "Chess dependency is missing. "
            "Make sure python-chess is in requirements.txt."
        )

        return

    board = st.session_state.chess_board

    if board.is_game_over():

        st.info("Game over.")

        return

    files = "abcdefgh"
    ranks = "87654321"

    legal = list(
        board.legal_moves
    )

    selected = st.session_state.chess_selected

    for row in range(8):

        cols = st.columns(8)

        for col in range(8):

            square = chess.parse_square(
                files[col] + ranks[row]
            )

            piece = board.piece_at(square)

            if piece:

                symbol = piece.unicode_symbol()

            else:

                symbol = "·"

            target = (
                selected is not None
                and any(
                    move.from_square == selected
                    and move.to_square == square
                    for move in legal
                )
            )

            if target:
                symbol = "🟢"

            if cols[col].button(
                symbol,
                key=f"chess{row}_{col}",
                use_container_width=True
            ):

                if (
                    board.turn != chess.WHITE
                    or st.session_state.chess_over
                ):
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
                            m
                            for m in legal
                            if (
                                m.from_square == selected
                                and m.to_square == square
                            )
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

                    elif (
                        piece
                        and piece.color == chess.WHITE
                    ):

                        st.session_state.chess_selected = square

                    else:

                        st.session_state.chess_selected = None

                    st.rerun()

    st.caption(
        "You are White. Select a piece, then select its destination."
    )


# ============================================================
# BLACKJACK
# ============================================================

SUITS = [
    "♠",
    "♥",
    "♦",
    "♣",
]

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
    "K",
]


def make_deck():

    return [
        (rank, suit)
        for suit in SUITS
        for rank in RANKS
    ]


def card_value(cards):

    total = 0
    aces = 0

    for rank, suit in cards:

        if rank == "A":

            total += 11
            aces += 1

        elif rank in (
            "K",
            "Q",
            "J"
        ):

            total += 10

        else:

            total += int(rank)

    while total > 21 and aces:

        total -= 10
        aces -= 1

    return total


def init_blackjack():

    st.session_state.bj_deck = make_deck()

    random.shuffle(
        st.session_state.bj_deck
    )

    st.session_state.bj_player = []
    st.session_state.bj_dealer = []

    st.session_state.bj_bet = 25

    st.session_state.bj_active = False
    st.session_state.bj_over = False

    st.session_state.bj_message = (
        "Place your bet to begin."
    )


def bj_draw():

    if not st.session_state.bj_deck:

        st.session_state.bj_deck = make_deck()

        random.shuffle(
            st.session_state.bj_deck
        )

    return st.session_state.bj_deck.pop()


def bj_start():

    bet = int(
        st.session_state.bj_bet
    )

    if (
        bet <= 0
        or bet > st.session_state.balance
    ):

        st.session_state.bj_message = (
            "Not enough BOT BUCKS for that bet."
        )

        return

    st.session_state.balance -= bet

    st.session_state.total_lost += bet

    st.session_state.bj_player = [
        bj_draw(),
        bj_draw(),
    ]

    st.session_state.bj_dealer = [
        bj_draw(),
        bj_draw(),
    ]

    st.session_state.bj_active = True
    st.session_state.bj_over = False

    st.session_state.bj_message = ""

    player_total = card_value(
        st.session_state.bj_player
    )

    dealer_total = card_value(
        st.session_state.bj_dealer
    )

    # Natural blackjack
    if player_total == 21:

        profit = int(bet * 1.5)

        st.session_state.balance += (
            bet + profit
        )

        st.session_state.total_earned += profit

        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            profit
        )

        st.session_state.bj_message = (
            f"🃏 BLACKJACK! +{profit:,} BB"
        )

        st.session_state.bj_over = True

        unlock("Blackjack!")

    elif dealer_total == 21:

        st.session_state.balance += bet

        st.session_state.bj_message = (
            "Dealer blackjack — push."
        )

        st.session_state.bj_over = True


def bj_finish():

    bet = int(
        st.session_state.bj_bet
    )

    player_total = card_value(
        st.session_state.bj_player
    )

    if player_total > 21:

        st.session_state.bj_message = (
            f"💥 BUST — you lost {bet:,} BB."
        )

        st.session_state.bj_over = True

        return

    while (
        card_value(
            st.session_state.bj_dealer
        ) < 17
    ):

        st.session_state.bj_dealer.append(
            bj_draw()
        )

    dealer_total = card_value(
        st.session_state.bj_dealer
    )

    if (
        dealer_total > 21
        or player_total > dealer_total
    ):

        st.session_state.balance += (
            bet * 2
        )

        st.session_state.total_earned += bet

        st.session_state.biggest_win = max(
            st.session_state.biggest_win,
            bet
        )

        st.session_state.bj_message = (
            f"🎉 YOU WIN — +{bet:,} BB"
        )

        if bet >= 500:
            unlock("High Roller")

    elif player_total == dealer_total:

        st.session_state.balance += bet

        st.session_state.bj_message = (
            "🤝 PUSH — bet returned."
        )

    else:

        st.session_state.bj_message = (
            f"🤖 DEALER WINS — you lost {bet:,} BB."
        )

    st.session_state.bj_over = True


def card_html(card, hidden=False):

    if hidden:

        return """
        <div class="playing-card card-back"></div>
        """

    rank, suit = card

    red = suit in (
        "♥",
        "♦"
    )

    colour_class = (
        "card-red"
        if red
        else "card-black"
    )

    return f"""
    <div class="playing-card {colour_class}">

        <div class="corner">
            {rank}<br>{suit}
        </div>

        <div class="suit-center">
            {suit}
        </div>

        <div class="corner"
             style="
                position:absolute;
                right:7px;
                bottom:6px;
                transform:rotate(180deg);
             ">

            {rank}<br>{suit}

        </div>

    </div>
    """


def cards_html(
    cards,
    hide_first=False
):

    html = '<div class="cards">'

    for index, card in enumerate(cards):

        html += card_html(
            card,
            hide_first and index == 0
        )

    html += "</div>"

    return html


def play_blackjack():

    st.markdown(
        '<div class="blackjack-wrap">',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="blackjack-table">

            <div class="casino-title">
                BOT BOARD CASINO
            </div>

            <div class="casino-subtitle">
                BLACKJACK • DEALER STANDS ON 17
            </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # DEALER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hand-zone">
            <div class="hand-label">
                Dealer
            </div>
        """,
        unsafe_allow_html=True
    )

    dealer = st.session_state.bj_dealer

    hide_dealer = (
        not st.session_state.bj_over
    )

    if dealer:

        st.markdown(
            cards_html(
                dealer,
                hide_dealer
            ),
            unsafe_allow_html=True
        )

        if hide_dealer:

            dealer_total = "?"

        else:

            dealer_total = str(
                card_value(dealer)
            )

    else:

        st.markdown(
            '<div class="cards"></div>',
            unsafe_allow_html=True
        )

        dealer_total = "—"

    st.markdown(
        f"""
            <div class="hand-total">
                {dealer_total}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    message = (
        st.session_state.bj_message
        or "Good luck."
    )

    st.markdown(
        f"""
        <div class="bj-status">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # PLAYER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hand-zone">
            <div class="hand-label">
                Your Hand
            </div>
        """,
        unsafe_allow_html=True
    )

    player = st.session_state.bj_player

    if player:

        st.markdown(
            cards_html(player),
            unsafe_allow_html=True
        )

        player_total = str(
            card_value(player)
        )

    else:

        st.markdown(
            '<div class="cards"></div>',
            unsafe_allow_html=True
        )

        player_total = "—"

    st.markdown(
        f"""
            <div class="hand-total">
                {player_total}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # BET CHIP
    # --------------------------------------------------------

    bet = int(
        st.session_state.bj_bet
    )

    st.markdown(
        f"""
        <div class="chip-row">

            <div class="casino-chip">
                {bet}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # CONTROLS
    # --------------------------------------------------------

    if (
        not st.session_state.bj_active
        and not st.session_state.bj_over
    ):

        st.markdown(
            """
            <div style="
                text-align:center;
                color:white;
                font-weight:800;
                margin-bottom:10px;
            ">
                SELECT YOUR BET
            </div>
            """,
            unsafe_allow_html=True
        )

        options = [
            amount
            for amount in [
                10,
                25,
                50,
                100,
                250,
                500,
            ]
            if amount <= st.session_state.balance
        ]

        if options:

            selected_bet = st.radio(
                "Bet",
                options,
                horizontal=True,
                key="bj_bet_radio",
                label_visibility="collapsed"
            )

            st.session_state.bj_bet = selected_bet

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    color:white;
                    margin:10px;
                ">
                    Bet <b>{selected_bet:,} BB</b>
                    &nbsp; • &nbsp;
                    Balance <b>
                        {st.session_state.balance:,} BB
                    </b>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "🎴 DEAL",
                type="primary",
                use_container_width=True
            ):

                bj_start()

                st.rerun()

        else:

            st.warning(
                "You don't have enough BOT BUCKS. "
                "Claim your daily bonus from Wallet."
            )

    elif not st.session_state.bj_over:

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "👊 HIT",
                type="primary",
                use_container_width=True
            ):

                st.session_state.bj_player.append(
                    bj_draw()
                )

                if (
                    card_value(
                        st.session_state.bj_player
                    ) > 21
                ):

                    bj_finish()

                st.rerun()

        with col2:

            if st.button(
                "✋ STAND",
                use_container_width=True
            ):

                bj_finish()

                st.rerun()

    else:

        if st.button(
            "🔄 NEW HAND",
            type="primary",
            use_container_width=True
        ):

            st.session_state.bj_active = False
            st.session_state.bj_over = False

            st.session_state.bj_player = []
            st.session_state.bj_dealer = []

            st.session_state.bj_message = (
                "Place your bet to begin."
            )

            st.rerun()

    st.markdown(
        "</div></div>",
        unsafe_allow_html=True
    )


# ============================================================
# GAME INITIALISATION
# ============================================================

def init_game(name):

    st.session_state.game = name

    st.session_state.difficulty = "Medium"

    st.session_state.reward_given = False

    st.session_state.last_result = ""

    initialisers = {

        "Tic Tac Toe": init_ttt,

        "Connect 4": init_connect4,

        "Checkers": init_checkers,

        "Othello": init_othello,

        "Gomoku": init_gomoku,

        "Battleship": init_battleship,

        "Chess": init_chess,

        "Blackjack": init_blackjack,
    }

    initialisers[name]()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🤖 BOT BOARD"
    )

    st.caption(
        "THE BOT ARCADE"
    )

    st.markdown(
        f"### 💰 {st.session_state.balance:,} BB"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🎮 Games",
            "💰 Wallet",
            "🏆 Achievements",
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

            init_game(
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
            <h1>Wallet</h1>
            <p>
                Your BOT BOARD arcade balance
                and statistics.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    columns = st.columns(3)

    stats = [
        (
            "Balance",
            f"{st.session_state.balance:,} BB"
        ),
        (
            "Total earned",
            f"{st.session_state.total_earned:,} BB"
        ),
        (
            "Total lost",
            f"{st.session_state.total_lost:,} BB"
        ),
    ]

    for column, (label, value) in zip(
        columns,
        stats
    ):

        column.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-label">
                    {label}
                </div>

                <div class="stat-value">
                    {value}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    columns = st.columns(3)

    stats = [
        (
            "Biggest win",
            f"{st.session_state.biggest_win:,} BB"
        ),
        (
            "Current streak",
            st.session_state.streak
        ),
        (
            "Best streak",
            st.session_state.best_streak
        ),
    ]

    for column, (label, value) in zip(
        columns,
        stats
    ):

        column.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-label">
                    {label}
                </div>

                <div class="stat-value">
                    {value}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    if not st.session_state.daily_bonus:

        if st.button(
            "🎁 CLAIM DAILY BONUS  +250 BB",
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
        "BOT BUCKS are fictional in-game currency only. "
        "They cannot be purchased, withdrawn or converted "
        "into real money."
    )


# ============================================================
# ACHIEVEMENTS
# ============================================================

elif page == "🏆 Achievements":

    st.markdown(
        """
        <div class="hero">
            <h1>Achievements</h1>
            <p>
                Build your record and collect
                every badge.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

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
        (
            "High Roller",
            "Win a 500 BB blackjack hand"
        ),
    ]

    for name, description in achievements:

        if name in st.session_state.achievements:

            st.success(
                f"🏆 **{name}** — {description}"
            )

        else:

            st.markdown(
                f"""
                <div class="stat-card">
                    🔒 <b>{name}</b>
                    <br>
                    <span style="color:#8d98aa">
                        {description}
                    </span>
                </div>
                <br>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# GAMES
# ============================================================

else:

    if st.session_state.game is None:

        st.markdown(
            f"""
            <div class="hero">

                <h1>BOT BOARD</h1>

                <p>
                    Beat the bots.
                    Build your balance.
                    Own the arcade.
                </p>

                <div class="balance-pill">
                    💰 {st.session_state.balance:,}
                    BOT BUCKS
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            "### 🎮 Choose a game"
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
                "🏁",
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
                "Five in a row."
            ),

            (
                "🛳️",
                "Battleship",
                "Find and sink the fleet."
            ),

            (
                "♟️",
                "Chess",
                "Classic strategy."
            ),

            (
                "🃏",
                "Blackjack",
                "Play the casino table."
            ),
        ]

        columns = st.columns(2)

        for i, (
            icon,
            name,
            description
        ) in enumerate(games):

            with columns[i % 2]:

                st.markdown(
                    f"""
                    <div class="game-card">

                        <div class="game-icon">
                            {icon}
                        </div>

                        <h3>
                            {name}
                        </h3>

                        <p>
                            {description}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"PLAY {name.upper()}",
                    key=f"play_{name}",
                    use_container_width=True
                ):

                    init_game(name)

                    st.rerun()

    else:

        name = st.session_state.game

        st.markdown(
            f"""
            <div class="game-header">

                <h2 style="margin:0">
                    {name}
                </h2>

                <span style="color:#8d98aa">
                    💰 {st.session_state.balance:,} BB
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )

        if name != "Blackjack":

            col1, col2 = st.columns(
                [2, 1]
            )

            with col1:

                st.session_state.difficulty = st.selectbox(
                    "Bot difficulty",
                    DIFFICULTIES,
                    index=DIFFICULTIES.index(
                        st.session_state.difficulty
                    )
                )

            with col2:

                st.metric(
                    "Win reward",
                    f"+{reward_for(name)} BB"
                )

        # ----------------------------------------------------
        # RUN GAME
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        if (
            st.session_state.last_result
            and name != "Blackjack"
        ):

            if (
                st.session_state.last_result
                == "win"
            ):

                st.success(
                    f"🎉 YOU WON  •  "
                    f"+{reward_for(name)} BB"
                )

            elif (
                st.session_state.last_result
                == "loss"
            ):

                st.error(
                    "🤖 THE BOT WON"
                )

            else:

                st.info(
                    "🤝 DRAW"
                )
