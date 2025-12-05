import tkinter as tk
from tkinter import ttk

class AmortizationSchedule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_results_frame()
        self._create_table_frame()

    def _create_results_frame(self):
        frame = ttk.LabelFrame(self, text="Resultados", padding=10)
        frame.grid(row=0, column=0, sticky="we", pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.installment_lbl = ttk.Label(frame, text="Cuota: $0.00", font=("Arial", 12, "bold"))
        self.installment_lbl.grid(row=0, column=0, sticky="w")

        self.interest_lbl = ttk.Label(frame, text="Intereses: $0.00")
        self.interest_lbl.grid(row=1, column=0, sticky="w")

        self.total_lbl = ttk.Label(frame, text="Total: $0.00")
        self.total_lbl.grid(row=2, column=0, sticky="w")

        self.monto_lbl = ttk.Label(frame, text="")
        self.monto_lbl.grid(row=0, column=1, sticky="e")

    def _create_table_frame(self):
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, sticky="nsew")

        columns = ("Periodo", "Cuota", "Interés", "Amortización", "Saldo")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def update_results(self, installment, total_interest, schedule, total_payment, periods, computed_amount=None):
        self.installment_lbl.config(text=f"Cuota: ${installment:,.2f}")
        self.interest_lbl.config(text=f"Intereses: ${total_interest:,.2f}")
        self.total_lbl.config(text=f"Total: ${total_payment:,.2f}")

        if computed_amount:
            self.monto_lbl.config(text=f"Monto calculado: ${computed_amount:,.2f}")
        else:
            self.monto_lbl.config(text="")

        self.clear_table()
        for row in schedule:
            self.tree.insert("", tk.END, values=(
                row["Periodo"],
                f"${row['Cuota']:,.2f}",
                f"${row['Interés']:,.2f}",
                f"${row['Amortización']:,.2f}",
                f"${row['Saldo']:,.2f}"
            ))

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)