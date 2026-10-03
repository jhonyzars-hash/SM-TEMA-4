import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimulacionInventario:
    def __init__(self, inicial, reorden, pedido, dias):
        self.inicial = inicial
        self.reorden = reorden
        self.pedido = pedido
        self.dias = dias

    def ejecutar(self):
        niveles = []
        stock = self.inicial
        dias_entrega = -1

        for _ in range(self.dias):
            if dias_entrega == 0:
                stock += self.pedido
                dias_entrega = -1
            elif dias_entrega > 0:
                dias_entrega -= 1

            demanda = random.randint(0, 9)
            stock = max(0, stock - demanda)

            if stock <= self.reorden and dias_entrega == -1:
                dias_entrega = 2

            niveles.append(stock)

        return niveles

class InterfazInventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Control de Inventarios")
        self.root.geometry("900x620")
        self.root.configure(bg="#181825")

        self.estilos()
        self.crear_widgets()

    def estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#181825")
        style.configure("TLabel", background="#181825", foreground="#cdd6f4", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground="#a6e3a1")
        style.configure("TButton", background="#a6e3a1", foreground="#11111b", font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[("active", "#94e2d5")])

    def crear_widgets(self):
        panel_top = ttk.Frame(self.root, padding=15)
        panel_top.pack(fill=tk.X)

        lbl_titulo = ttk.Label(panel_top, text="Simulación de Control de Inventario", style="Title.TLabel")
        lbl_titulo.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        ttk.Label(panel_top, text="Stock Inicial:").grid(row=1, column=0, sticky="w", padx=5)
        self.ent_inicial = ttk.Entry(panel_top, width=12)
        self.ent_inicial.insert(0, "50")
        self.ent_inicial.grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(panel_top, text="Punto Reorden:").grid(row=1, column=2, sticky="w", padx=5)
        self.ent_reorden = ttk.Entry(panel_top, width=12)
        self.ent_reorden.insert(0, "15")
        self.ent_reorden.grid(row=1, column=3, sticky="w", padx=5)

        ttk.Label(panel_top, text="Cant. Pedido:").grid(row=2, column=0, sticky="w", padx=5, pady=10)
        self.ent_pedido = ttk.Entry(panel_top, width=12)
        self.ent_pedido.insert(0, "30")
        self.ent_pedido.grid(row=2, column=1, sticky="w", padx=5, pady=10)

        ttk.Label(panel_top, text="Días Simulación:").grid(row=2, column=2, sticky="w", padx=5, pady=10)
        self.ent_dias = ttk.Entry(panel_top, width=12)
        self.ent_dias.insert(0, "30")
        self.ent_dias.grid(row=2, column=3, sticky="w", padx=5, pady=10)

        btn_simular = ttk.Button(panel_top, text="Generar Simulación", command=self.simular)
        btn_simular.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

        panel_contenido = ttk.Frame(self.root, padding=10)
        panel_contenido.pack(fill=tk.BOTH, expand=True)

        self.txt_res = tk.Text(panel_contenido, width=30, bg="#1e1e2e", fg="#cdd6f4", insertbackground="white", font=("Consolas", 9), bd=0)
        self.txt_res.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.panel_grafica = ttk.Frame(panel_contenido)
        self.panel_grafica.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def simular(self):
        try:
            ini = int(self.ent_inicial.get())
            reo = int(self.ent_reorden.get())
            ped = int(self.ent_pedido.get())
            dias = int(self.ent_dias.get())

            sim = SimulacionInventario(ini, reo, ped, dias)
            niveles = sim.ejecutar()

            self.txt_res.delete("1.0", tk.END)
            res_str = f"=== RESUMEN ===\n\n"
            res_str += f"Días: {dias}\n"
            res_str += f"Stock Mín: {min(niveles)}\n"
            res_str += f"Stock Máx: {max(niveles)}\n"
            res_str += f"Stock Prom: {sum(niveles)/len(niveles):.1f}\n\n"
            res_str += "--- DETALLE DIARIO ---\n"
            for i in range(min(15, len(niveles))):
                res_str += f"Día {i+1}: {niveles[i]} unid.\n"

            self.txt_res.insert(tk.END, res_str)
            self.graficar(niveles)

        except ValueError:
            self.txt_res.delete("1.0", tk.END)
            self.txt_res.insert(tk.END, "Error: Ingrese números enteros válidos.")

    def graficar(self, niveles):
        for widget in self.panel_grafica.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4), facecolor="#1e1e2e")
        ax.set_facecolor("#1e1e2e")

        dias = range(1, len(niveles) + 1)
        ax.plot(dias, niveles, color="#a6e3a1", linewidth=2, marker='o', markersize=4)

        ax.set_title("Evolución del Stock Diario", color="#cdd6f4", fontsize=10)
        ax.set_xlabel("Día", color="#cdd6f4", fontsize=9)
        ax.set_ylabel("Unidades", color="#cdd6f4", fontsize=9)
        ax.tick_params(colors="#cdd6f4", labelsize=8)
        ax.grid(True, color="#313244", linestyle="--", alpha=0.5)

        for spine in ax.spines.values():
            spine.set_color("#45475a")

        canvas = FigureCanvasTkAgg(fig, master=self.panel_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazInventario(root)
    root.mainloop()