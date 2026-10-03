import math
import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ValidacionParametrica:
    def __init__(self, media_teorica, tamaño, media_muestral, desviacion):
        self.mu_0 = media_teorica
        self.n = tamaño
        self.media = media_muestral
        self.std = desviacion

    def calcular_t(self):
        error_estandar = self.std / math.sqrt(self.n)
        if error_estandar == 0:
            return 0
        t_stat = (self.media - self.mu_0) / error_estandar
        return t_stat

class InterfazValidacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Validación Paramétrica (Prueba t de Student)")
        self.root.geometry("900x620")
        self.root.configure(bg="#11111b")

        self.estilos()
        self.crear_widgets()

    def estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#11111b")
        style.configure("TLabel", background="#11111b", foreground="#cdd6f4", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground="#f38ba8")
        style.configure("TButton", background="#f38ba8", foreground="#11111b", font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[("active", "#f5e0dc")])

    def crear_widgets(self):
        panel_top = ttk.Frame(self.root, padding=15)
        panel_top.pack(fill=tk.X)

        lbl_titulo = ttk.Label(panel_top, text="Prueba t de Student - Validación de Simulador", style="Title.TLabel")
        lbl_titulo.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        ttk.Label(panel_top, text="Media Teórica (μ₀):").grid(row=1, column=0, sticky="w", padx=5)
        self.ent_mu = ttk.Entry(panel_top, width=12)
        self.ent_mu.insert(0, "50.0")
        self.ent_mu.grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(panel_top, text="Tamaño Muestra (n):").grid(row=1, column=2, sticky="w", padx=5)
        self.ent_n = ttk.Entry(panel_top, width=12)
        self.ent_n.insert(0, "30")
        self.ent_n.grid(row=1, column=3, sticky="w", padx=5)

        ttk.Label(panel_top, text="Media Obtenida (x̄):").grid(row=2, column=0, sticky="w", padx=5, pady=10)
        self.ent_media = ttk.Entry(panel_top, width=12)
        self.ent_media.insert(0, "51.2")
        self.ent_media.grid(row=2, column=1, sticky="w", padx=5, pady=10)

        ttk.Label(panel_top, text="Desv. Estándar (s):").grid(row=2, column=2, sticky="w", padx=5, pady=10)
        self.ent_std = ttk.Entry(panel_top, width=12)
        self.ent_std.insert(0, "3.5")
        self.ent_std.grid(row=2, column=3, sticky="w", padx=5, pady=10)

        btn_evaluar = ttk.Button(panel_top, text="Realizar Prueba t", command=self.evaluar)
        btn_evaluar.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

        panel_contenido = ttk.Frame(self.root, padding=10)
        panel_contenido.pack(fill=tk.BOTH, expand=True)

        self.txt_res = tk.Text(panel_contenido, width=32, bg="#1e1e2e", fg="#cdd6f4", insertbackground="white", font=("Consolas", 9), bd=0)
        self.txt_res.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.panel_grafica = ttk.Frame(panel_contenido)
        self.panel_grafica.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def evaluar(self):
        try:
            mu0 = float(self.ent_mu.get())
            n = int(self.ent_n.get())
            media = float(self.ent_media.get())
            std = float(self.ent_std.get())

            val = ValidacionParametrica(mu0, n, media, std)
            t_calc = val.calcular_t()

            t_critico = 2.045
            pasa_prueba = abs(t_calc) <= t_critico

            self.txt_res.delete("1.0", tk.END)
            res_str = f"=== EVALUACIÓN ===\n\n"
            res_str += f"Valor t Calculado: {t_calc:.3f}\n"
            res_str += f"Valor t Crítico: ±{t_critico}\n\n"
            res_str += "--- DICTAMEN ---\n"
            if pasa_prueba:
                res_str += "RESULTADO: ACEPTADO\n"
                res_str += "El simulador es confiable y no presenta diferencias significativas."
            else:
                res_str += "RESULTADO: RECHAZADO\n"
                res_str += "El simulador difiere de la media teórica esperada."

            self.txt_res.insert(tk.END, res_str)
            self.graficar(mu0, media, std, n)

        except ValueError:
            self.txt_res.delete("1.0", tk.END)
            self.txt_res.insert(tk.END, "Error: Ingrese datos válidos.")

    def graficar(self, mu0, media, std, n):
        for widget in self.panel_grafica.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4), facecolor="#1e1e2e")
        ax.set_facecolor("#1e1e2e")

        datos = [random.gauss(media, std) for _ in range(n)]
        
        ax.scatter(range(1, n + 1), datos, color="#f38ba8", alpha=0.7, label="Muestras")
        ax.axhline(mu0, color="#89b4fa", linestyle="--", linewidth=2, label=f"Media Teórica ({mu0})")

        ax.set_title("Distribución de Muestras vs Valor Teórico", color="#cdd6f4", fontsize=10)
        ax.set_xlabel("Número de Muestra", color="#cdd6f4", fontsize=9)
        ax.set_ylabel("Valor Generado", color="#cdd6f4", fontsize=9)
        ax.tick_params(colors="#cdd6f4", labelsize=8)
        ax.legend(facecolor="#181825", edgecolor="none", labelcolor="#cdd6f4", fontsize=8)

        for spine in ax.spines.values():
            spine.set_color("#45475a")

        canvas = FigureCanvasTkAgg(fig, master=self.panel_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazValidacion(root)
    root.mainloop()