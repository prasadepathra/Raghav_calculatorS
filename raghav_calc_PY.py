"""Raghav Calculator: a Tkinter conversion of raghav_calculator.html."""

import ast
import operator
import re
import tkinter as tk
from tkinter import messagebox


class SafeCalculator:
    """Evaluate only numeric arithmetic expressions."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def evaluate(cls, expression: str) -> float:
        tree = ast.parse(expression, mode="eval")
        return cls._evaluate_node(tree.body)

    @classmethod
    def _evaluate_node(cls, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.UnaryOp) and type(node.op) in cls.OPERATORS:
            return cls.OPERATORS[type(node.op)](cls._evaluate_node(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in cls.OPERATORS:
            left = cls._evaluate_node(node.left)
            right = cls._evaluate_node(node.right)
            return cls.OPERATORS[type(node.op)](left, right)
        raise ValueError("Only numeric arithmetic is supported")


class RaghavCalculator(tk.Tk):
    """Desktop calculator window."""

    BUTTONS = (
        ("AC", "clear"), ("⌫", "backspace"), ("÷", "/"), ("×", "*"),
        ("7", "7"), ("8", "8"), ("9", "9"), ("−", "-"),
        ("4", "4"), ("5", "5"), ("6", "6"), ("+", "+"),
        ("1", "1"), ("2", "2"), ("3", "3"), ("=", "equals"),
        ("0", "0"), (".", "."),
    )

    def __init__(self) -> None:
        super().__init__()
        self.title("Raghav Calculator")
        self.configure(bg="#111827")
        self.geometry("360x500")
        self.resizable(False, False)
        self.expression = ""
        self.display = tk.StringVar(value="0")
        self._build_ui()
        self.bind("<Key>", self._handle_key)

    def _build_ui(self) -> None:
        frame = tk.Frame(self, bg="#1f2937", padx=22, pady=22)
        frame.pack(fill="both", expand=True, padx=12, pady=12)
        tk.Label(
            frame, text="Raghav Calculator", bg="#1f2937", fg="#93c5fd",
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(0, 16))
        tk.Entry(
            frame, textvariable=self.display, justify="right", state="readonly",
            readonlybackground="#0b1220", fg="#f9fafb", font=("Segoe UI", 24),
            relief="flat", width=15,
        ).pack(fill="x", ipady=10, pady=(0, 14))
        keys = tk.Frame(frame, bg="#1f2937")
        keys.pack(fill="both", expand=True)
        for index, (label, value) in enumerate(self.BUTTONS):
            row, column = divmod(index, 4)
            if label == "0":
                column = 0
            button = tk.Button(
                keys, text=label, command=lambda item=value: self._press(item),
                bg="#374151", fg="#f9fafb", activebackground="#4b5563",
                activeforeground="#ffffff", relief="flat", font=("Segoe UI", 14),
                width=4, height=2,
            )
            if label in {"÷", "×", "−", "+"}:
                button.configure(bg="#2563eb", activebackground="#3b82f6")
            elif label == "AC":
                button.configure(bg="#b91c1c", activebackground="#dc2626")
            elif label == "=":
                button.configure(bg="#059669", activebackground="#10b981")
            button.grid(row=row, column=column, columnspan=2 if label == "0" else 1,
                        sticky="nsew", padx=5, pady=5)
        for row in range(5):
            keys.rowconfigure(row, weight=1)
        for column in range(4):
            keys.columnconfigure(column, weight=1)

    def _press(self, value: str) -> None:
        if value == "clear":
            self.expression = ""
        elif value == "backspace":
            self.expression = self.expression[:-1]
        elif value == "equals":
            self._calculate()
            return
        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += value
        self.display.set(self.expression or "0")

    def _calculate(self) -> None:
        if not self.expression or not re.fullmatch(r"[0-9+*/().\s-]+", self.expression):
            return
        try:
            result = SafeCalculator.evaluate(self.expression)
            if not result == result or result in (float("inf"), float("-inf")):
                raise ValueError("Invalid result")
            self.expression = str(int(result)) if result.is_integer() else str(result)
        except (ArithmeticError, SyntaxError, ValueError):
            self.expression = "Error"
            messagebox.showerror("Raghav Calculator", "Invalid calculation")
        self.display.set(self.expression)

    def _handle_key(self, event: tk.Event) -> None:
        if event.char and re.fullmatch(r"[0-9.+*/()-]", event.char):
            self._press(event.char)
        elif event.keysym in ("Return", "equal"):
            self._press("equals")
        elif event.keysym == "BackSpace":
            self._press("backspace")
        elif event.keysym == "Escape":
            self._press("clear")


if __name__ == "__main__":
    RaghavCalculator().mainloop()
