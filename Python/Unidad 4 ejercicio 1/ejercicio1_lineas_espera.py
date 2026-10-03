import math
import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimulaciónColas:
    def __init__(self, lambda_rate, mu_rate, clientes):
        self.lambda_rate = lambda_rate
        self.mu_rate = mu_rate
        self.clientes = clientes

    def ejecutar(self):
        tiempos_llegada = []
        tiempos_servicio = []
        tiempos_espera = []
        
        tiempo_actual = 0
        tiempo_salida_anterior = 0
        
        for _ in range(self.clientes):
            llegada = -math.log(1 - random.random()) / self.lambda_rate
            servicio = -math.log(1 - random.random()) / self.mu_rate
            
            tiempo_actual += llegada
            inicio_servicio = max(tiempo_actual, tiempo_salida_anterior)
            espera = inicio_servicio - tiempo_actual
            
            tiempos_espera.append(espera)
            tiempo_salida_anterior = inicio_servicio + servicio
            
        return tiempos_espera

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Colas M/M/1")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2e")
        
        self.estilos()
        self.crear_widgets()

    def estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e2e")
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground="#89b4fa")
        style.configure("TButton", background="#89b4fa", foreground="#11111b", font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[("active", "#b4befe")])

    def crear_widgets(self):
        panel_top = ttk.Frame(self.root, padding=15)
        panel_top.pack(fill=tk.X)

        lbl_titulo = ttk.Label(panel_top, text="Simulación de Líneas de Espera (M/M/1)", style="Title.TLabel")
        lbl_titulo.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        ttk.Label(panel_top, text="Tasa Llegada (λ):").grid(row=1, column=0, sticky="w", padx=5)
        self.ent_lambda = ttk.Entry(panel_top, width=12)
        self.ent_lambda.insert(0, "2.5")
        self.ent_lambda.grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(panel_top, text="Tasa Servicio (μ):").grid(row=1, column=2, sticky="w", padx=5)
        self.ent_mu = ttk.Entry(panel_top, width=12)
        self.ent_mu.insert(0, "3.0")
        self.ent_mu.grid(row=1, column=3, sticky="w", padx=5)

        ttk.Label(panel_top, text="Total Clientes:").grid(row=2, column=0, sticky="w", padx=5, pady=10)
        self.ent_clientes = ttk.Entry(panel_top, width=12)
        self.ent_clientes.insert(0, "100")
        self.ent_clientes.grid(row=2, column=1, sticky="w", padx=5, pady=10)

        btn_simular = ttk.Button(panel_top, text="Iniciar Simulación", command=self.simular)
        btn_simular.grid(row=2, column=2, columnspan=2, sticky="ew", padx=5, pady=10)

        panel_contenido = ttk.Frame(self.root, padding=10)
        panel_contenido.pack(fill=tk.BOTH, expand=True)

        self.txt_res = tk.Text(panel_contenido, width=32, bg="#181825", fg="#cdd6f4", insertbackground="white", font=("Consolas", 9), bd=0)
        self.txt_res.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.panel_grafica = ttk.Frame(panel_contenido)
        self.panel_grafica.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def simular(self):
        try:
            lam = float(self.ent_lambda.get())
            mu = float(self.ent_mu.get())
            num_c = int(self.ent_clientes.get())

            if lam >= mu:
                self.txt_res.delete("1.0", tk.END)
                self.txt_res.insert(tk.END, "Error:\nLa tasa λ debe ser menor a μ para evitar que la cola crezca al infinito.")
                return

            sim = SimulaciónColas(lam, mu, num_c)
            tiempos = sim.ejecutar()

            promedio_espera = sum(tiempos) / len(tiempos)
            utilizacion = (lam / mu) * 100

            self.txt_res.delete("1.0", tk.END)
            res_str = f"=== RESULTADOS ===\n\n"
            res_str += f"Clientes: {num_c}\n"
            res_str += f"Uso Servidor: {utilizacion:.1f}%\n"
            res_str += f"Espera Prom.: {promedio_espera:.2f} min\n"
            res_str += f"Max Espera: {max(tiempos):.2f} min\n\n"
            res_str += "--- MUESTRA (10 Clientes) ---\n"
            for i in range(min(10, len(tiempos))):
                res_str += f"C{i+1}: {tiempos[i]:.2f} min\n"

            self.txt_res.insert(tk.END, res_str)
            self.graficar(tiempos)

        except ValueError:
            self.txt_res.delete("1.0", tk.END)
            self.txt_res.insert(tk.END, "Error: Ingrese valores numéricos válidos.")

    def graficar(self, tiempos):
        for widget in self.panel_grafica.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4), facecolor="#181825")
        ax.set_facecolor("#181825")

        muestras = tiempos[:25]
        ax.bar(range(1, len(muestras) + 1), muestras, color="#89b4fa", alpha=0.85)

        ax.set_title("Tiempo de Espera por Cliente (Primeros 25)", color="#cdd6f4", fontsize=10)
        ax.set_xlabel("Cliente", color="#cdd6f4", fontsize=9)
        ax.set_ylabel("Tiempo (min)", color="#cdd6f4", fontsize=9)
        ax.tick_params(colors="#cdd6f4", labelsize=8)
        
        for spine in ax.spines.values():
            spine.set_color("#45475a")

        canvas = FigureCanvasTkAgg(fig, master=self.panel_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()