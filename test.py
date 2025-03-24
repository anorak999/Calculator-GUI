import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=10, font=('Helvetica', 12))
        
        # Display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display = ttk.Entry(
            root,
            textvariable=self.display_var,
            justify="right",
            font=('Helvetica', 20),
            state='readonly'
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        # Calculator state
        self.current_number = ""
        self.first_number = None
        self.operation = None
        self.should_reset = False
        
        # Buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('←', 5, 1), ('±', 5, 2), ('√', 5, 3),
        ]
        
        for (text, row, col) in buttons:
            button = ttk.Button(
                root,
                text=text,
                command=lambda t=text: self.button_click(t)
            )
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # Configure grid weights
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def button_click(self, value):
        if value.isdigit() or value == '.':
            if self.should_reset:
                self.current_number = value
                self.should_reset = False
            else:
                self.current_number += value
            self.display_var.set(self.current_number)
            
        elif value in ['+', '-', '*', '/']:
            if self.first_number is None:
                self.first_number = float(self.current_number or '0')
            elif not self.should_reset:
                self.calculate()
            self.operation = value
            self.should_reset = True
            
        elif value == '=':
            self.calculate()
            self.first_number = None
            self.operation = None
            
        elif value == 'C':
            self.clear()
            
        elif value == '←':
            self.current_number = self.current_number[:-1] or '0'
            self.display_var.set(self.current_number)
            
        elif value == '±':
            if self.current_number and self.current_number != '0':
                if self.current_number[0] == '-':
                    self.current_number = self.current_number[1:]
                else:
                    self.current_number = '-' + self.current_number
                self.display_var.set(self.current_number)
                
        elif value == '√':
            try:
                num = float(self.current_number or '0')
                if num < 0:
                    self.display_var.set("Error")
                else:
                    result = math.sqrt(num)
                    self.current_number = str(result)
                    self.display_var.set(self.current_number)
            except ValueError:
                self.display_var.set("Error")

    def calculate(self):
        if not self.operation:
            return
        
        try:
            second_number = float(self.current_number or '0')
            if self.operation == '+':
                result = self.first_number + second_number
            elif self.operation == '-':
                result = self.first_number - second_number
            elif self.operation == '*':
                result = self.first_number * second_number
            elif self.operation == '/':
                if second_number == 0:
                    self.display_var.set("Error")
                    return
                result = self.first_number / second_number
                
            self.current_number = str(result)
            self.display_var.set(self.current_number)
            self.first_number = result
            
        except Exception:
            self.display_var.set("Error")
            self.clear()

    def clear(self):
        self.current_number = ""
        self.first_number = None
        self.operation = None
        self.should_reset = False
        self.display_var.set("0")

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
