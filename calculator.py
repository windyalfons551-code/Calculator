import ast
import operator
import tkinter as tk

# Operator yang diizinkan (evaluasi aman, tanpa eval mentah)
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def normalisasi(teks: str):
    return teks.replace('÷', '/').replace('x', '*').replace('×', '*').replace(':', '/')

def hitung_aman(ekspresi: str):
    """Evaluasi ekspresi matematika sederhana secara aman."""
    ekspresi = normalisasi(ekspresi)

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Ekspresi tidak valid")

    return _eval(ast.parse(ekspresi, mode="eval"))


class Kalkulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")

        self.ekspresi = ""
        self.var_layar = tk.StringVar(value="0")

        self.buat_layar()
        self.buat_tombol()
        self.bind("<Key>", self.tekan_keyboard)

    def buat_layar(self):
        layar = tk.Entry(
            self,
            textvariable=self.var_layar,
            font=("Segoe UI", 28),
            justify="right",
            bd=0,
            bg="#2d2d2d",
            fg="white",
            state="readonly",
            readonlybackground="#2d2d2d",
        )
        layar.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=15, sticky="nsew")

    def buat_tombol(self):
        tombol = [
            ("C", 1, 0), ("⌫", 1, 1), ("%", 1, 2), ("÷", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("×", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("±", 5, 0), ("0", 5, 1), (".", 5, 2), ("=", 5, 3),
        ]
        for teks, baris, kolom in tombol:
            if teks == "=":
                warna = "#ff9500"
            elif teks in "÷×-+":
                warna = "#ff9500"
            elif teks in ("C", "⌫", "%", "±"):
                warna = "#505050"
            else:
                warna = "#333333"

            tk.Button(
                self,
                text=teks,
                font=("Segoe UI", 16),
                width=5,
                height=2,
                bd=0,
                bg=warna,
                fg="white",
                activebackground="#6e6e6e",
                activeforeground="white",
                command=lambda t=teks: self.klik(t),
            ).grid(row=baris, column=kolom, padx=4, pady=4)

        for i in range(4):
            self.columnconfigure(i, weight=1)

    def perbarui_layar(self):
        self.var_layar.set(self.ekspresi if self.ekspresi else "0")

    def klik(self, nilai):
        if nilai == "C":
            self.ekspresi = ""
        elif nilai == "⌫":
            self.ekspresi = self.ekspresi[:-1]
        elif nilai == "=":
            self.hitung()
            return
        elif nilai == "±":
            if self.ekspresi.startswith("-"):
                self.ekspresi = self.ekspresi[1:]
            elif self.ekspresi:
                self.ekspresi = "-" + self.ekspresi
        elif nilai == "%":
            try:
                self.ekspresi = self.format_angka(hitung_aman(self.ekspresi) / 100)
            except Exception:
                self.var_layar.set("Error")
                self.ekspresi = ""
                return
        else:
            self.ekspresi += nilai
        self.perbarui_layar()

    def hitung(self):
        try:
            hasil = hitung_aman(self.ekspresi)
            self.ekspresi = self.format_angka(hasil)
            self.perbarui_layar()
        except ZeroDivisionError:
            self.var_layar.set("Tidak bisa dibagi 0")
            self.ekspresi = ""
        except Exception:
            self.var_layar.set("Error")
            self.ekspresi = ""

    @staticmethod
    def format_angka(angka):
        if isinstance(angka, float) and angka.is_integer():
            angka = int(angka)
        return str(round(angka, 10) if isinstance(angka, float) else angka)

    def tekan_keyboard(self, event):
        if event.char in "0123456789.+-×÷":
            self.klik(event.char)
        elif event.keysym in ("Return", "KP_Enter") or event.char == "=":
            self.klik("=")
        elif event.keysym == "BackSpace":
            self.klik("⌫")
        elif event.keysym == "Escape":
            self.klik("C")
        elif event.char == "%":
            self.klik("%")


if __name__ == "__main__":
    Kalkulator().mainloop()
