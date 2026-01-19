import tkinter as tk
from tkinter import messagebox
import random

# -----------------------------
# MINIMAX (Khó che_do)
# -----------------------------
def minimax(ban_co, do_sau, isMaximizing):
    win = doi_thang(ban_co)
    if win == "X": return -1
    if win == "O": return 1
    if ban_co_full(ban_co): return 0

    if isMaximizing:
        toi_da = -999
        for i in range(3):
            for j in range(3):
                if ban_co[i][j] == "":
                    ban_co[i][j] = "O"
                    toi_da = max(toi_da, minimax(ban_co, do_sau+1, False))
                    ban_co[i][j] = ""
        return toi_da
    else:
        toi_da = 999
        for i in range(3):
            for j in range(3):
                if ban_co[i][j] == "":
                    ban_co[i][j] = "X"
                    toi_da = min(toi_da, minimax(ban_co, do_sau+1, True))
                    ban_co[i][j] = ""
        return toi_da

def may_danh(ban_co, che_do="Trung bình"):
    o_trong = [(i,j) for i in range(3) for j in range(3) if ban_co[i][j] == ""]

    if che_do == "Dễ":
        return random.choice(o_trong)

    if che_do == "Trung bình":
        # 70% random, 30% minimax → "Trung bình"
        if random.random() < 0.7:
            return random.choice(o_trong)

    # Khó che_do — full minimax
    toi_da_diem = -999
    di_chuyen = None
    for i, j in o_trong:
        ban_co[i][j] = "O"
        diem = minimax(ban_co, 0, False)
        ban_co[i][j] = ""
        if diem > toi_da_diem:
            toi_da_diem = diem
            di_chuyen = (i, j)
    return di_chuyen

# -----------------------------
# CHECK win
# -----------------------------
def doi_thang(ban_co):
    cac_dong = []
    # Hàng và cột
    for i in range(3):
        cac_dong.append(ban_co[i])
        cac_dong.append([ban_co[0][i], ban_co[1][i], ban_co[2][i]])

    # Đường chéo
    cac_dong.append([ban_co[0][0], ban_co[1][1], ban_co[2][2]])
    cac_dong.append([ban_co[0][2], ban_co[1][1], ban_co[2][0]])

    for duong_ke in cac_dong:
        if duong_ke == ["X","X","X"]:
            return "X"
        if duong_ke == ["O","O","O"]:
            return "O"
    return None

def ban_co_full(ban_co):
    return all(ban_co[i][j] != "" for i in range(3) for j in range(3))

# -----------------------------
# GUI CLASS
# -----------------------------
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        root.title("Tic Tac Toe - AI")

        self.ban_co = [["" for _ in range(3)] for _ in range(3)]
        self.che_do = tk.StringVar(value="pve")
        self.difficulty = tk.StringVar(value="Trung bình")

        self.turn = "X"
        self.buttons = [[None]*3 for _ in range(3)]

        # khung chọn chế độ
        che_do = tk.Frame(root)
        che_do.pack()

        tk.Label(che_do, text="Chế độ: ").pack(side=tk.LEFT)
        tk.Radiobutton(che_do, text="Người vs Máy", variable=self.che_do, value="pve").pack(side=tk.LEFT)
        tk.Radiobutton(che_do, text="Người vs Người", variable=self.che_do, value="pvp").pack(side=tk.LEFT)

        tk.Label(che_do, text="   Độ khó AI: ").pack(side=tk.LEFT)
        tk.OptionMenu(che_do, self.difficulty, "Dễ", "Trung bình", "Khó").pack(side=tk.LEFT)

        tk.Button(che_do, text="Chơi lại", command=self.choi_lai).pack(side=tk.LEFT)

        # Bàn cờ
        khung = tk.Frame(root)
        khung.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    khung, text="", font=("Arial", 28), width=4, height=1,
                    command=lambda r=i, c=j: self.click(r, c)
                )
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def click(self, r, c):
        if self.ban_co[r][c] != "":
            return

        self.ban_co[r][c] = self.turn
        self.buttons[r][c].config(text=self.turn)

        win = doi_thang(self.ban_co)
        if win:
            self.kiem_tra_ket_qua(win)
            messagebox.showinfo("Kết quả", f"{win} thắng!")
            return

        if ban_co_full(self.ban_co):
            messagebox.showinfo("Kết quả", "Hòa!")
            return

        if self.che_do.get() == "pve":
            self.turn = "O"
            self.root.after(200, self.may_quay_lai)
        else:
            self.turn = "O" if self.turn == "X" else "X"

    def may_quay_lai(self):
        che_do = self.difficulty.get()
        r, c = may_danh(self.ban_co, che_do)
        self.ban_co[r][c] = "O"
        self.buttons[r][c].config(text="O")

        win = doi_thang(self.ban_co)
        if win:
            self.kiem_tra_ket_qua(win)
            messagebox.showinfo("Kết quả", "Máy thắng!")
            return

        if ban_co_full(self.ban_co):
            messagebox.showinfo("Kết quả", "Hòa!")
            return

        self.turn = "X"

    def kiem_tra_ket_qua(self, win):
        # kiểm tra 8 đường thắng và highlight
        mau_chien_thang = [
            [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],  # hàng
            [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],  # cột
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]                        # chéo
        ]
        for mau in mau_chien_thang:
            if all(self.ban_co[r][c] == win for r,c in mau):
                for r,c in mau:
                    self.buttons[r][c].config(bg="yellow")

    def choi_lai(self):
        self.turn = "X"
        self.ban_co = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="SystemButtonFace")

# -----------------------------
# RUN APP
# -----------------------------
root = tk.Tk()
app = TicTacToeGUI(root)
root.mainloop()
