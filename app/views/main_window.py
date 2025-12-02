import tkinter as tk
from tkinter import ttk, messagebox

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Calculadora de Créditos Bancarios")
        self.geometry("800x600")
        
        self._create_widgets()

    def _create_widgets(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self, text="Datos del Crédito", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)

        # Amount
        ttk.Label(input_frame, text="Monto del Préstamo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.amount_var = tk.DoubleVar()
        ttk.Entry(input_frame, textvariable=self.amount_var).grid(row=0, column=1, padx=5, pady=5)

        # Rate
        ttk.Label(input_frame, text="Tasa de Interés Anual (%):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.rate_var = tk.DoubleVar()
        ttk.Entry(input_frame, textvariable=self.rate_var).grid(row=0, column=3, padx=5, pady=5)

        # Years
        ttk.Label(input_frame, text="Plazo (Años):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.years_var = tk.IntVar()
        ttk.Entry(input_frame, textvariable=self.years_var).grid(row=1, column=1, padx=5, pady=5)

        # Periodicity
        ttk.Label(input_frame, text="Periodicidad:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.periodicity_var = tk.StringVar()
        self.periodicity_combo = ttk.Combobox(input_frame, textvariable=self.periodicity_var, state="readonly")
        self.periodicity_combo['values'] = ("Mensual", "Trimestral", "Semestral", "Anual")
        self.periodicity_combo.current(0)
        self.periodicity_combo.grid(row=1, column=3, padx=5, pady=5)

        # Calculate Button
        ttk.Button(input_frame, text="Calcular", command=self.on_calculate).grid(row=2, column=0, columnspan=4, pady=10)

        # Results Frame
        results_frame = ttk.LabelFrame(self, text="Resultados", padding="10")
        results_frame.pack(fill="x", padx=10, pady=5)

        self.installment_label = ttk.Label(results_frame, text="Cuota: $0.00", font=("Helvetica", 12, "bold"))
        self.installment_label.pack(side="left", padx=20)
        
        self.total_interest_label = ttk.Label(results_frame, text="Total Intereses: $0.00")
        self.total_interest_label.pack(side="left", padx=20)

        # Table Frame
        table_frame = ttk.Frame(self, padding="10")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Periodo", "Cuota", "Interés", "Amortización", "Saldo")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def on_calculate(self):
        try:
            amount = self.amount_var.get()
            rate = self.rate_var.get()
            years = self.years_var.get()
            periodicity = self.periodicity_var.get()

            if amount <= 0 or rate <= 0 or years <= 0:
                messagebox.showerror("Error", "Por favor ingrese valores positivos mayores a 0.")
                return

            self.controller.calculate(amount, rate, years, periodicity)
        except tk.TclError:
            messagebox.showerror("Error", "Por favor verifique que los datos sean numéricos.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_results(self, installment, total_interest, schedule_df):
        self.installment_label.config(text=f"Cuota: ${installment:,.2f}")
        self.total_interest_label.config(text=f"Total Intereses: ${total_interest:,.2f}")
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add new items
        for row in schedule_df:
            self.tree.insert("", "end", values=(
                row['Periodo'],
                f"${row['Cuota']:,.2f}",
                f"${row['Interés']:,.2f}",
                f"${row['Amortización']:,.2f}",
                f"${row['Saldo']:,.2f}"
            ))
