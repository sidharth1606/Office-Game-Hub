"""
Report_Analysis.pyw
--------------------
A small game hub that hides behind a "work" disguise.

HOW TO USE
  - Run this with pythonw (not python) so no console window pops up:
        pythonw office_game.py
  - Press ESC any time  -> instantly snap back to your last disguise (boss key).
  - Press F2            -> open the game menu.
  - Press F3/F4/F5       -> switch disguise to Terminal / Excel / Code editor.

Games included: 2048, Snake, Blackjack.
No external dependencies - pure standard library (tkinter).
"""

import tkinter as tk
import random


# ----------------------------------------------------------------------
# App shell
# ----------------------------------------------------------------------
class OfficeGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Report_Analysis.xlsx")
        self.root.geometry("960x620")
        self.root.minsize(820, 560)

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_disguise = "terminal"

        TerminalDisguise(self).place(self, "terminal")
        ExcelDisguise(self).place(self, "excel")
        CodeDisguise(self).place(self, "code")
        MenuFrame(self).place(self, "menu")
        Game2048(self).place(self, "2048")
        SnakeGame(self).place(self, "snake")
        BlackjackGame(self).place(self, "blackjack")
        TicTacToeGame(self).place(self, "tictactoe")
        PongGame(self).place(self, "pong")
        MemoryGame(self).place(self, "memory")
        MinesweeperGame(self).place(self, "minesweeper")
        TypingGame(self).place(self, "typing")
        RockPaperScissorsGame(self).place(self, "rps")
        NumberGuessGame(self).place(self, "guess")

        self.root.bind("<Escape>", lambda e: self.show_disguise())
        self.root.bind("<F2>", lambda e: self.show_frame("menu"))
        self.root.bind("<F3>", lambda e: self.show_frame("terminal"))
        self.root.bind("<F4>", lambda e: self.show_frame("excel"))
        self.root.bind("<F5>", lambda e: self.show_frame("code"))

        self.show_disguise()

    def register(self, name, widget):
        self.frames[name] = widget

    def show_frame(self, name):
        self.frames[name].tkraise()
        self.frames[name].focus_set()
        if name in ("terminal", "excel", "code"):
            self.current_disguise = name
        # let games know they became visible/hidden (to pause loops etc.)
        for n, f in self.frames.items():
            if hasattr(f, "on_shown"):
                f.on_shown(n == name)

    def show_disguise(self):
        self.show_frame(self.current_disguise)


def place(self_frame_cls):
    pass


# small helper mixin so each Frame subclass can register itself in one line
class BaseFrame(tk.Frame):
    def place(self, app, name):
        self.grid(in_=app.container, row=0, column=0, sticky="nsew")
        app.register(name, self)
        return self


# ----------------------------------------------------------------------
# Disguise 1: fake terminal with scrolling log lines
# ----------------------------------------------------------------------
class TerminalDisguise(BaseFrame):
    LOG_TEMPLATES = [
        "INFO  data_pipeline: loaded batch {n} rows={r}",
        "INFO  etl.transform: normalizing column 'region_id'",
        "DEBUG cache: hit ratio {pct}%",
        "INFO  scheduler: job report_daily_{n} queued",
        "WARN  connector.sql: retrying connection (attempt {n})",
        "INFO  auth: token refreshed for service-account",
        "INFO  etl.load: writing {r} rows to warehouse.fact_sales",
        "DEBUG  worker-{n}: heartbeat ok",
        "INFO  report_builder: rendering section {n}/12",
        "INFO  metrics: p95_latency_ms={r}",
    ]

    def __init__(self, app):
        super().__init__(app.container, bg="black")
        self.app = app
        bar = tk.Label(self, text="bash - office-pc: ~/reports", bg="#2b2b2b",
                        fg="white", anchor="w", padx=6)
        bar.pack(fill="x")
        self.text = tk.Text(self, bg="black", fg="#39ff14", insertbackground="#39ff14",
                             font=("Consolas", 11), bd=0, highlightthickness=0)
        self.text.pack(fill="both", expand=True)
        self.text.config(state="disabled")
        self._running = False

    def on_shown(self, visible):
        self._running = visible
        if visible:
            self._tick()

    def _tick(self):
        if not self._running:
            return
        line = random.choice(self.LOG_TEMPLATES).format(
            n=random.randint(1, 999), r=random.randint(100, 99999),
            pct=random.randint(70, 99))
        self.text.config(state="normal")
        self.text.insert("end", line + "\n")
        self.text.see("end")
        # keep buffer small
        if int(self.text.index('end-1c').split('.')[0]) > 400:
            self.text.delete("1.0", "50.0")
        self.text.config(state="disabled")
        self.after(random.randint(250, 900), self._tick)


# ----------------------------------------------------------------------
# Disguise 2: fake Excel grid
# ----------------------------------------------------------------------
class ExcelDisguise(BaseFrame):
    def __init__(self, app):
        super().__init__(app.container, bg="white")
        self.app = app
        menubar = tk.Label(self, text="  File   Home   Insert   Page Layout   Formulas   Data   Review   View",
                            bg="#217346", fg="white", anchor="w", font=("Segoe UI", 10))
        menubar.pack(fill="x")
        formula_bar = tk.Frame(self, bg="#f3f3f3")
        formula_bar.pack(fill="x")
        tk.Label(formula_bar, text="A1", bg="#f3f3f3", width=6, anchor="w").pack(side="left")
        tk.Entry(formula_bar).pack(side="left", fill="x", expand=True, padx=4, pady=2)

        grid = tk.Frame(self, bg="white")
        grid.pack(fill="both", expand=True)

        cols = 8
        rows = 22
        headers = [chr(65 + i) for i in range(cols)]
        for c, h in enumerate(headers):
            tk.Label(grid, text=h, bg="#e6e6e6", relief="ridge", width=12).grid(row=0, column=c + 1, sticky="nsew")
        for r in range(1, rows):
            tk.Label(grid, text=str(r), bg="#e6e6e6", relief="ridge", width=3).grid(row=r, column=0, sticky="nsew")
            for c in range(cols):
                val = ""
                if r <= 3:
                    val = ["Region", "Q1", "Q2", "Q3", "Q4", "Total", "YoY%", "Notes"][c] if r == 1 else \
                        round(random.uniform(1000, 99999), 2)
                elif random.random() < 0.6:
                    val = round(random.uniform(10, 99999), 2)
                tk.Label(grid, text=val, relief="ridge", width=12, anchor="e", bg="white").grid(
                    row=r, column=c + 1, sticky="nsew")
        for c in range(cols + 1):
            grid.grid_columnconfigure(c, weight=1)


# ----------------------------------------------------------------------
# Disguise 3: fake code editor
# ----------------------------------------------------------------------
class CodeDisguise(BaseFrame):
    CODE_LINES = [
        "def transform_batch(df: pd.DataFrame) -> pd.DataFrame:",
        "    df = df.dropna(subset=['region_id', 'amount'])",
        "    df['amount'] = df['amount'].astype(float)",
        "    df['margin'] = df['amount'] - df['cost']",
        "    grouped = df.groupby('region_id').agg({'amount': 'sum'})",
        "    return grouped.reset_index()",
        "",
        "class ReportBuilder:",
        "    def __init__(self, config):",
        "        self.config = config",
        "        self._cache = {}",
        "",
        "    def build(self, period):",
        "        rows = self._load(period)",
        "        return self._render(rows)",
        "",
        "# TODO: optimize the join below, it's O(n^2) right now",
        "def join_tables(a, b, key):",
        "    result = []",
        "    for row in a:",
        "        match = next((x for x in b if x[key] == row[key]), None)",
        "        if match:",
        "            result.append({**row, **match})",
        "    return result",
    ]

    def __init__(self, app):
        super().__init__(app.container, bg="#1e1e1e")
        self.app = app
        bar = tk.Label(self, text="report_pipeline.py - Editor", bg="#323233", fg="white",
                        anchor="w", padx=6)
        bar.pack(fill="x")
        self.text = tk.Text(self, bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
                             font=("Consolas", 11), bd=0, highlightthickness=0)
        self.text.pack(fill="both", expand=True)
        for line in self.CODE_LINES:
            self.text.insert("end", line + "\n")
        self.text.config(state="disabled")
        self._running = False

    def on_shown(self, visible):
        self._running = visible
        if visible:
            self._tick()

    def _tick(self):
        if not self._running:
            return
        self.text.config(state="normal")
        extra = random.choice([
            "    logger.debug('checkpoint reached')",
            "    # reviewed - looks fine",
            "    cache.set(key, value, ttl=3600)",
            "    assert result is not None",
        ])
        self.text.insert("end", extra + "\n")
        self.text.see("end")
        if int(self.text.index('end-1c').split('.')[0]) > 300:
            self.text.delete("1.0", "40.0")
        self.text.config(state="disabled")
        self.after(random.randint(1500, 4000), self._tick)


# ----------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------
class MenuFrame(BaseFrame):
    def __init__(self, app):
        super().__init__(app.container, bg="#111")
        self.app = app
        tk.Label(self, text="Game Menu", fg="white", bg="#111",
                 font=("Segoe UI", 20, "bold")).pack(pady=12)
        for label, target in [
            ("2048", "2048"), ("Snake", "snake"), ("Blackjack", "blackjack"),
            ("Tic-Tac-Toe", "tictactoe"), ("Pong", "pong"),
            ("Memory Match", "memory"), ("Minesweeper", "minesweeper"),
            ("Typing Speed", "typing"), ("Rock Paper Scissors", "rps"),
            ("Number Guessing", "guess")
        ]:
            tk.Button(self, text=label, width=20, height=1,
                      command=lambda t=target: app.show_frame(t)).pack(pady=3)
        tk.Label(self, text="ESC = boss key (back to disguise)   |   F2 = this menu\n"
                             "F3 = terminal   F4 = excel   F5 = code editor",
                 fg="#888", bg="#111", justify="center").pack(pady=10)


# ----------------------------------------------------------------------
# Game 1: 2048
# ----------------------------------------------------------------------
class Game2048(BaseFrame):
    SIZE = 4
    COLORS = {
        0: "#3c3a32", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
        16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
        256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
    }

    def __init__(self, app):
        super().__init__(app.container, bg="#2f2f2f")
        self.app = app
        top = tk.Frame(self, bg="#2f2f2f")
        top.pack(fill="x")
        tk.Button(top, text="< Menu", command=lambda: app.show_frame("menu")).pack(side="left", padx=8, pady=8)
        self.score_lbl = tk.Label(top, text="Score: 0", bg="#2f2f2f", fg="white", font=("Segoe UI", 12))
        self.score_lbl.pack(side="left", padx=8)

        self.grid_frame = tk.Frame(self, bg="#bbada0")
        self.grid_frame.pack(padx=20, pady=10)
        self.cells = [[None] * self.SIZE for _ in range(self.SIZE)]
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                lbl = tk.Label(self.grid_frame, text="", width=4, height=2,
                                font=("Segoe UI", 20, "bold"), bg=self.COLORS[0])
                lbl.grid(row=r, column=c, padx=5, pady=5)
                self.cells[r][c] = lbl

        self.bind_all_keys()
        self.new_game()

    def bind_all_keys(self):
        self.bind("<Up>", lambda e: self.move(0, -1))
        self.bind("<Down>", lambda e: self.move(0, 1))
        self.bind("<Left>", lambda e: self.move(-1, 0))
        self.bind("<Right>", lambda e: self.move(1, 0))

    def on_shown(self, visible):
        if visible:
            self.focus_set()

    def new_game(self):
        self.board = [[0] * self.SIZE for _ in range(self.SIZE)]
        self.score = 0
        self.add_tile()
        self.add_tile()
        self.redraw()

    def add_tile(self):
        empties = [(r, c) for r in range(self.SIZE) for c in range(self.SIZE) if self.board[r][c] == 0]
        if not empties:
            return
        r, c = random.choice(empties)
        self.board[r][c] = 4 if random.random() < 0.1 else 2

    def redraw(self):
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                v = self.board[r][c]
                lbl = self.cells[r][c]
                lbl.config(text=str(v) if v else "", bg=self.COLORS.get(v, "#3c3a32"),
                           fg="#776e65" if v <= 4 else "white")
        self.score_lbl.config(text=f"Score: {self.score}")

    def move(self, dx, dy):
        moved = False
        rng_c = range(self.SIZE) if dx <= 0 else range(self.SIZE - 1, -1, -1)
        rng_r = range(self.SIZE) if dy <= 0 else range(self.SIZE - 1, -1, -1)

        def slide_line(get, setv):
            vals = [get(i) for i in range(self.SIZE)]
            nums = [v for v in vals if v != 0]
            merged = []
            skip = False
            for i in range(len(nums)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(nums) and nums[i] == nums[i + 1]:
                    merged.append(nums[i] * 2)
                    self.score += nums[i] * 2
                    skip = True
                else:
                    merged.append(nums[i])
            merged += [0] * (self.SIZE - len(merged))
            if merged != vals:
                nonlocal moved
                moved = True
            for i in range(self.SIZE):
                setv(i, merged[i])

        if dx != 0:
            for r in range(self.SIZE):
                idxs = list(range(self.SIZE)) if dx < 0 else list(range(self.SIZE - 1, -1, -1))
                get = lambda i, r=r, idxs=idxs: self.board[r][idxs[i]]
                setv = lambda i, val, r=r, idxs=idxs: self.board.__setitem__(r, self.board[r]) or self.board[r].__setitem__(idxs[i], val)
                slide_line(get, setv)
        else:
            for c in range(self.SIZE):
                idxs = list(range(self.SIZE)) if dy < 0 else list(range(self.SIZE - 1, -1, -1))
                get = lambda i, c=c, idxs=idxs: self.board[idxs[i]][c]
                setv = lambda i, val, c=c, idxs=idxs: self.board[idxs[i]].__setitem__(c, val)
                slide_line(get, setv)

        if moved:
            self.add_tile()
            self.redraw()


# ----------------------------------------------------------------------
# Game 2: Snake
# ----------------------------------------------------------------------
class SnakeGame(BaseFrame):
    CELL = 20
    W, H = 30, 22

    def __init__(self, app):
        super().__init__(app.container, bg="black")
        self.app = app
        top = tk.Frame(self, bg="black")
        top.pack(fill="x")
        tk.Button(top, text="< Menu", command=lambda: app.show_frame("menu")).pack(side="left", padx=8, pady=8)
        self.score_lbl = tk.Label(top, text="Score: 0", bg="black", fg="white", font=("Segoe UI", 12))
        self.score_lbl.pack(side="left", padx=8)

        self.canvas = tk.Canvas(self, width=self.W * self.CELL, height=self.H * self.CELL,
                                 bg="#111", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.bind("<Up>", lambda e: self.set_dir(0, -1))
        self.bind("<Down>", lambda e: self.set_dir(0, 1))
        self.bind("<Left>", lambda e: self.set_dir(-1, 0))
        self.bind("<Right>", lambda e: self.set_dir(1, 0))

        self._running = False
        self.new_game()

    def on_shown(self, visible):
        self._running = visible
        if visible:
            self.focus_set()
            self.loop()

    def new_game(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.pending_dir = (1, 0)
        self.food = self.random_food()
        self.score = 0
        self.alive = True
        self.draw()

    def random_food(self):
        while True:
            p = (random.randint(0, self.W - 1), random.randint(0, self.H - 1))
            if p not in self.snake:
                return p

    def set_dir(self, dx, dy):
        cx, cy = self.direction
        if (dx, dy) != (-cx, -cy):
            self.pending_dir = (dx, dy)

    def loop(self):
        if not self._running:
            return
        if self.alive:
            self.direction = self.pending_dir
            hx, hy = self.snake[0]
            dx, dy = self.direction
            new_head = ((hx + dx) % self.W, (hy + dy) % self.H)
            if new_head in self.snake:
                self.alive = False
            else:
                self.snake.insert(0, new_head)
                if new_head == self.food:
                    self.score += 10
                    self.food = self.random_food()
                else:
                    self.snake.pop()
            self.draw()
        else:
            self.canvas.create_text(self.W * self.CELL / 2, self.H * self.CELL / 2,
                                     text="GAME OVER - press R to restart", fill="white",
                                     font=("Segoe UI", 14))
            self.bind("<r>", lambda e: self.new_game())
        self.after(120, self.loop)

    def draw(self):
        self.canvas.delete("all")
        fx, fy = self.food
        self.canvas.create_oval(fx * self.CELL, fy * self.CELL, (fx + 1) * self.CELL, (fy + 1) * self.CELL,
                                 fill="red", outline="")
        for i, (x, y) in enumerate(self.snake):
            color = "#39ff14" if i == 0 else "#1fa30a"
            self.canvas.create_rectangle(x * self.CELL, y * self.CELL, (x + 1) * self.CELL, (y + 1) * self.CELL,
                                          fill=color, outline="")
        self.score_lbl.config(text=f"Score: {self.score}")


# ----------------------------------------------------------------------
# Game 3: Blackjack
# ----------------------------------------------------------------------
class BlackjackGame(BaseFrame):
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUITS = ["♠", "♥", "♦", "♣"]

    def __init__(self, app):
        super().__init__(app.container, bg="#0b5c2e")
        self.app = app
        top = tk.Frame(self, bg="#0b5c2e")
        top.pack(fill="x")
        tk.Button(top, text="< Menu", command=lambda: app.show_frame("menu")).pack(side="left", padx=8, pady=8)
        self.status_lbl = tk.Label(top, text="", bg="#0b5c2e", fg="white", font=("Segoe UI", 12, "bold"))
        self.status_lbl.pack(side="left", padx=12)

        self.dealer_lbl = tk.Label(self, text="Dealer: ", bg="#0b5c2e", fg="white", font=("Consolas", 16))
        self.dealer_lbl.pack(pady=20)
        self.player_lbl = tk.Label(self, text="You: ", bg="#0b5c2e", fg="white", font=("Consolas", 16))
        self.player_lbl.pack(pady=20)

        btns = tk.Frame(self, bg="#0b5c2e")
        btns.pack(pady=10)
        self.hit_btn = tk.Button(btns, text="Hit", width=10, command=self.hit)
        self.hit_btn.pack(side="left", padx=6)
        self.stand_btn = tk.Button(btns, text="Stand", width=10, command=self.stand)
        self.stand_btn.pack(side="left", padx=6)
        self.new_btn = tk.Button(btns, text="New Hand", width=10, command=self.new_hand)
        self.new_btn.pack(side="left", padx=6)

        self.new_hand()

    def on_shown(self, visible):
        if visible:
            self.focus_set()

    def fresh_deck(self):
        deck = [(r, s) for r in self.RANKS for s in self.SUITS]
        random.shuffle(deck)
        return deck

    def hand_value(self, hand):
        total = 0
        aces = 0
        for r, _ in hand:
            if r == "A":
                total += 11
                aces += 1
            elif r in ("J", "Q", "K"):
                total += 10
            else:
                total += int(r)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def fmt(self, hand, hide_first=False):
        cards = []
        for i, (r, s) in enumerate(hand):
            if hide_first and i == 1:
                cards.append("??")
            else:
                cards.append(f"{r}{s}")
        return "  ".join(cards)

    def new_hand(self):
        self.deck = self.fresh_deck()
        self.player = [self.deck.pop(), self.deck.pop()]
        self.dealer = [self.deck.pop(), self.deck.pop()]
        self.done = False
        self.status_lbl.config(text="")
        self.hit_btn.config(state="normal")
        self.stand_btn.config(state="normal")
        self.refresh(hide_dealer=True)

    def refresh(self, hide_dealer=False):
        self.dealer_lbl.config(text=f"Dealer: {self.fmt(self.dealer, hide_first=hide_dealer)}")
        self.player_lbl.config(text=f"You: {self.fmt(self.player)}   (value: {self.hand_value(self.player)})")

    def hit(self):
        if self.done:
            return
        self.player.append(self.deck.pop())
        if self.hand_value(self.player) > 21:
            self.end_hand("Bust! Dealer wins.")
        self.refresh(hide_dealer=True)

    def stand(self):
        if self.done:
            return
        while self.hand_value(self.dealer) < 17:
            self.dealer.append(self.deck.pop())
        pv, dv = self.hand_value(self.player), self.hand_value(self.dealer)
        if dv > 21 or pv > dv:
            self.end_hand("You win!")
        elif pv == dv:
            self.end_hand("Push.")
        else:
            self.end_hand("Dealer wins.")

    def end_hand(self, msg):
        self.done = True
        self.status_lbl.config(text=msg)
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")
        self.refresh(hide_dealer=False)



# ----------------------------------------------------------------------
# Extra games
# ----------------------------------------------------------------------
class TicTacToeGame(BaseFrame):
    def __init__(self, app):
        super().__init__(app.container, bg="#202020")
        self.app = app
        tk.Button(self, text="< Menu", command=lambda: app.show_frame("menu")).pack(anchor="w", padx=8, pady=8)
        self.status = tk.Label(self, fg="white", bg="#202020", font=("Segoe UI", 15, "bold"))
        self.status.pack(pady=8)
        board = tk.Frame(self, bg="#202020"); board.pack()
        self.buttons = []
        for i in range(9):
            b = tk.Button(board, text="", width=5, height=2, font=("Segoe UI", 24, "bold"),
                          command=lambda i=i: self.play(i))
            b.grid(row=i//3, column=i%3, padx=3, pady=3); self.buttons.append(b)
        tk.Button(self, text="New Game", command=self.new_game).pack(pady=15)
        self.new_game()

    def new_game(self):
        self.cells = [""] * 9; self.turn = "X"; self.over = False
        for b in self.buttons: b.config(text="", state="normal")
        self.status.config(text="Your turn: X")

    def play(self, i):
        if self.over or self.cells[i]: return
        self.cells[i] = self.turn; self.buttons[i].config(text=self.turn)
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        if any(self.cells[a] and self.cells[a] == self.cells[b] == self.cells[c] for a,b,c in wins):
            self.status.config(text=f"{self.turn} wins!"); self.over = True; return
        if all(self.cells):
            self.status.config(text="Draw!"); self.over = True; return
        self.turn = "O" if self.turn == "X" else "X"
        self.status.config(text=f"Turn: {self.turn}")


class PongGame(BaseFrame):
    W, H = 760, 460
    def __init__(self, app):
        super().__init__(app.container, bg="black"); self.app = app
        tk.Button(self, text="< Menu", command=lambda: app.show_frame("menu")).pack(anchor="w", padx=8, pady=5)
        self.score_lbl = tk.Label(self, text="", bg="black", fg="white", font=("Segoe UI", 13)); self.score_lbl.pack()
        self.canvas = tk.Canvas(self, width=self.W, height=self.H, bg="#111", highlightthickness=0); self.canvas.pack()
        self.bind("<Up>", lambda e: self.move_player(-30)); self.bind("<Down>", lambda e: self.move_player(30))
        self.running = False; self.new_game()

    def on_shown(self, visible):
        self.running = visible
        if visible: self.focus_set(); self.loop()

    def new_game(self):
        self.py = self.H//2-45; self.ay = self.H//2-45
        self.bx, self.by, self.dx, self.dy = self.W//2, self.H//2, 6, 4
        self.ps = self.ai = 0; self.draw()

    def move_player(self, d): self.py = max(0, min(self.H-90, self.py+d))

    def loop(self):
        if not self.running: return
        self.bx += self.dx; self.by += self.dy
        if self.by <= 8 or self.by >= self.H-8: self.dy *= -1
        self.ay += 5 if self.by > self.ay+45 else -5
        self.ay = max(0, min(self.H-90, self.ay))
        if self.dx < 0 and self.bx <= 35 and self.py <= self.by <= self.py+90: self.dx *= -1
        if self.dx > 0 and self.bx >= self.W-35 and self.ay <= self.by <= self.ay+90: self.dx *= -1
        if self.bx < 0: self.ai += 1; self.reset_ball(1)
        if self.bx > self.W: self.ps += 1; self.reset_ball(-1)
        self.draw(); self.after(20, self.loop)

    def reset_ball(self, direction):
        self.bx, self.by, self.dx, self.dy = self.W//2, self.H//2, 6*direction, random.choice([-4,4])

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_line(self.W//2,0,self.W//2,self.H,fill="#555",dash=(8,8))
        self.canvas.create_rectangle(20,self.py,35,self.py+90,fill="white",outline="")
        self.canvas.create_rectangle(self.W-35,self.ay,self.W-20,self.ay+90,fill="white",outline="")
        self.canvas.create_oval(self.bx-8,self.by-8,self.bx+8,self.by+8,fill="white",outline="")
        self.score_lbl.config(text=f"You {self.ps}   -   {self.ai} Computer   |   Up/Down arrows")


class MemoryGame(BaseFrame):
    def __init__(self, app):
        super().__init__(app.container, bg="#283747"); self.app = app
        tk.Button(self, text="< Menu", command=lambda: app.show_frame("menu")).pack(anchor="w", padx=8, pady=8)
        self.status = tk.Label(self, bg="#283747", fg="white", font=("Segoe UI", 14)); self.status.pack()
        f = tk.Frame(self, bg="#283747"); f.pack(pady=15)
        self.buttons=[]
        for i in range(16):
            b=tk.Button(f,text="?",width=6,height=3,font=("Segoe UI",16,"bold"),command=lambda i=i:self.flip(i))
            b.grid(row=i//4,column=i%4,padx=4,pady=4); self.buttons.append(b)
        tk.Button(self,text="New Game",command=self.new_game).pack()
        self.new_game()

    def new_game(self):
        self.values=list("AABBCCDDEEFFGGHH"); random.shuffle(self.values)
        self.open=[]; self.matched=set(); self.lock=False; self.moves=0
        for b in self.buttons:b.config(text="?",state="normal")
        self.status.config(text="Moves: 0")

    def flip(self,i):
        if self.lock or i in self.matched or i in self.open:return
        self.buttons[i].config(text=self.values[i]); self.open.append(i)
        if len(self.open)==2:
            self.moves+=1; self.status.config(text=f"Moves: {self.moves}")
            a,b=self.open
            if self.values[a]==self.values[b]:
                self.matched.update(self.open); self.open=[]
                if len(self.matched)==16:self.status.config(text=f"You won in {self.moves} moves!")
            else:self.lock=True; self.after(700,self.hide)

    def hide(self):
        for i in self.open:self.buttons[i].config(text="?")
        self.open=[];self.lock=False


class MinesweeperGame(BaseFrame):
    ROWS, COLS, MINES = 9, 12, 15
    def __init__(self, app):
        super().__init__(app.container,bg="#bbb");self.app=app
        tk.Button(self,text="< Menu",command=lambda:app.show_frame("menu")).pack(anchor="w",padx=8,pady=5)
        self.status=tk.Label(self,bg="#bbb",font=("Segoe UI",13,"bold"));self.status.pack()
        f=tk.Frame(self,bg="#bbb");f.pack(pady=8);self.buttons={}
        for r in range(self.ROWS):
            for c in range(self.COLS):
                b=tk.Button(f,text="",width=3,height=1,command=lambda r=r,c=c:self.reveal(r,c))
                b.bind("<Button-3>",lambda e,r=r,c=c:self.flag(r,c))
                b.grid(row=r,column=c);self.buttons[(r,c)]=b
        tk.Button(self,text="New Game",command=self.new_game).pack(pady=8);self.new_game()

    def new_game(self):
        cells=[(r,c) for r in range(self.ROWS) for c in range(self.COLS)]
        self.mines=set(random.sample(cells,self.MINES));self.shown=set();self.over=False
        for b in self.buttons.values():b.config(text="",state="normal",relief="raised")
        self.status.config(text=f"Mines: {self.MINES}  |  Right-click to flag")

    def near(self,r,c):
        return [(rr,cc) for rr in range(max(0,r-1),min(self.ROWS,r+2))
                for cc in range(max(0,c-1),min(self.COLS,c+2)) if (rr,cc)!=(r,c)]

    def reveal(self,r,c):
        if self.over or (r,c) in self.shown:return
        if (r,c) in self.mines:
            self.over=True;self.status.config(text="Boom! Game over.")
            for p in self.mines:self.buttons[p].config(text="*")
            return
        self.shown.add((r,c));n=sum(p in self.mines for p in self.near(r,c))
        self.buttons[(r,c)].config(text=str(n) if n else "",relief="sunken",state="disabled")
        if n==0:
            for p in self.near(r,c):self.reveal(*p)
        if len(self.shown)==self.ROWS*self.COLS-self.MINES:self.status.config(text="You cleared the field!");self.over=True

    def flag(self,r,c):
        if not self.over and (r,c) not in self.shown:
            b=self.buttons[(r,c)];b.config(text="" if b.cget("text")=="F" else "F")


class TypingGame(BaseFrame):
    WORDS=["python","report","analysis","database","office","project","dashboard","function",
           "variable","computer","keyboard","developer","analytics","spreadsheet","terminal"]
    def __init__(self,app):
        super().__init__(app.container,bg="#17202a");self.app=app
        tk.Button(self,text="< Menu",command=lambda:app.show_frame("menu")).pack(anchor="w",padx=8,pady=8)
        self.timer=tk.Label(self,bg="#17202a",fg="white",font=("Segoe UI",14));self.timer.pack(pady=8)
        self.word=tk.Label(self,bg="#17202a",fg="#39ff14",font=("Consolas",30,"bold"));self.word.pack(pady=25)
        self.entry=tk.Entry(self,font=("Consolas",20),justify="center");self.entry.pack()
        self.entry.bind("<Return>",self.check)
        tk.Button(self,text="Start / Restart",command=self.start).pack(pady=20)
        self.active=False;self.score=0;self.time=30;self.next_word()

    def next_word(self):self.current=random.choice(self.WORDS);self.word.config(text=self.current)
    def start(self):
        self.active=True;self.score=0;self.time=30;self.entry.delete(0,"end");self.entry.focus_set();self.next_word();self.tick()
    def tick(self):
        if not self.active:return
        self.timer.config(text=f"Time: {self.time}s   Score: {self.score}")
        if self.time<=0:self.active=False;self.word.config(text=f"Finished! Score: {self.score}");return
        self.time-=1;self.after(1000,self.tick)
    def check(self,e=None):
        if self.active and self.entry.get().strip().lower()==self.current:self.score+=1
        self.entry.delete(0,"end");self.next_word()


class RockPaperScissorsGame(BaseFrame):
    ITEMS=["Rock","Paper","Scissors"]
    def __init__(self,app):
        super().__init__(app.container,bg="#4a235a");self.app=app
        tk.Button(self,text="< Menu",command=lambda:app.show_frame("menu")).pack(anchor="w",padx=8,pady=8)
        self.result=tk.Label(self,text="Choose one",bg="#4a235a",fg="white",font=("Segoe UI",22,"bold"));self.result.pack(pady=50)
        f=tk.Frame(self,bg="#4a235a");f.pack()
        for x in self.ITEMS:tk.Button(f,text=x,width=12,height=2,command=lambda x=x:self.play(x)).pack(side="left",padx=8)
        self.score=tk.Label(self,bg="#4a235a",fg="white",font=("Segoe UI",14));self.score.pack(pady=35)
        self.you=self.cpu=0;self.update_score()
    def play(self,you):
        cpu=random.choice(self.ITEMS)
        if you==cpu:msg="Draw"
        elif (you,cpu) in [("Rock","Scissors"),("Paper","Rock"),("Scissors","Paper")]:msg="You win!";self.you+=1
        else:msg="Computer wins";self.cpu+=1
        self.result.config(text=f"You: {you}\nComputer: {cpu}\n{msg}");self.update_score()
    def update_score(self):self.score.config(text=f"Score — You {self.you} : {self.cpu} Computer")


class NumberGuessGame(BaseFrame):
    def __init__(self,app):
        super().__init__(app.container,bg="#154360");self.app=app
        tk.Button(self,text="< Menu",command=lambda:app.show_frame("menu")).pack(anchor="w",padx=8,pady=8)
        tk.Label(self,text="Guess a number from 1 to 100",bg="#154360",fg="white",font=("Segoe UI",20,"bold")).pack(pady=60)
        self.entry=tk.Entry(self,font=("Segoe UI",20),justify="center",width=10);self.entry.pack()
        self.entry.bind("<Return>",lambda e:self.guess())
        tk.Button(self,text="Guess",width=12,command=self.guess).pack(pady=15)
        self.status=tk.Label(self,bg="#154360",fg="white",font=("Segoe UI",15));self.status.pack()
        tk.Button(self,text="New Number",command=self.new_game).pack(pady=20);self.new_game()
    def new_game(self):self.answer=random.randint(1,100);self.tries=0;self.status.config(text="Good luck!");self.entry.delete(0,"end")
    def guess(self):
        try:n=int(self.entry.get())
        except ValueError:self.status.config(text="Enter a valid number.");return
        self.tries+=1
        if n<self.answer:self.status.config(text="Too low!")
        elif n>self.answer:self.status.config(text="Too high!")
        else:self.status.config(text=f"Correct! You found it in {self.tries} tries.")
        self.entry.delete(0,"end")


# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    OfficeGameApp(root)
    root.mainloop()
