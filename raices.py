import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --- CONFIGURACIÓN DE ESTILO ---
COLOR_BARRA_SUP = "#639dee"  
COLOR_CUERPO = "#040c18"
COLOR_BOTON = "#0056b3"

def cargar(frame, limpiar, tabla_datos, set_resultado, graficar):
    limpiar()
    frame.configure(bg=COLOR_CUERPO)

    # ================= LÓGICA MATEMÁTICA PRO =================
    def f_eval(x, expr):
        """Evalúa la función de forma segura y flexible."""
        # Limpieza de sintaxis para el usuario
        expr = expr.lower().replace("^", "**").replace("sen", "sin")
        contexto = {
            "x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "exp": math.exp, "log": math.log, "log10": math.log10,
            "sqrt": math.sqrt, "pi": math.pi, "e": math.e
        }
        try:
            return eval(expr, {"__builtins__": None}, contexto)
        except Exception as e:
            raise ValueError(f"Error en f(x): {e}")

    def derivada(x, expr):
        """Calcula la derivada numérica para Newton-Raphson."""
        h = 1e-7
        return (f_eval(x + h, expr) - f_eval(x - h, expr)) / (2 * h)

    def insertar_simbolo(simb):
        """Inserta texto en la posición actual del cursor."""
        entrada_f.insert(tk.INSERT, simb)
        entrada_f.focus_set()

    # ================= DISEÑO DE INTERFAZ (UI) =================
    
    # 1. BARRA DE TITULO (HEADER)
    header = tk.Frame(frame, bg=COLOR_BARRA_SUP, height=40)
    header.pack(side="top", fill="x")
    tk.Label(header, text="MÓDULO: RAÍCES DE ECUACIONES", fg="white", bg=COLOR_BARRA_SUP, 
             font=("Segoe UI", 12, "bold")).pack(side="left", padx=20)

    # 2. CINTA DE OPCIONES (RIBBON) - FUNCIONAL
    ribbon = tk.Frame(frame, bg="white", bd=1, relief="solid")
    ribbon.pack(side="top", fill="x", padx=10, pady=5)

    def crear_grupo_ribbon(titulo, simbolos):
        f = tk.Frame(ribbon, bg="white", padx=5)
        f.pack(side="left", fill="y", padx=2)
        grid = tk.Frame(f, bg="white")
        grid.pack()
        for i, (btn_text, val) in enumerate(simbolos.items()):
            tk.Button(grid, text=btn_text, width=4, relief="flat", bg="#f8f9fa",
                      command=lambda v=val: insertar_simbolo(v)).grid(row=i//3, column=i%3, padx=1, pady=1)
        tk.Label(f, text=titulo, font=("Arial", 7, "bold"), bg="#eeeeee").pack(side="bottom", fill="x")

    crear_grupo_ribbon("Básicos", {"√": "sqrt(", "π": "pi", "^": "^", "(": "(", ")": ")", "abs": "abs("})
    crear_grupo_ribbon("Trig", {"sin": "sin(", "cos": "cos(", "tan": "tan(", "asin": "asin(", "acos": "acos(", "atan": "atan("})
    crear_grupo_ribbon("Log/Exp", {"ln": "log(", "log10": "log10(", "exp": "exp(", "e": "e", "x": "x", "/": "/"})

    # 3. BARRA DE ENTRADA (FUNCION Y METODO)
    input_bar = tk.Frame(frame, bg=COLOR_CUERPO)
    input_bar.pack(fill="x", padx=20, pady=10)

    tk.Label(input_bar, text="f(x):", bg=COLOR_CUERPO, font=("Arial", 10, "bold")).pack(side="left")
    entrada_f = tk.Entry(input_bar, width=30, font=("Consolas", 12))
    entrada_f.insert(0, "x**2 - 4")
    entrada_f.pack(side="left", padx=5)

    metodo_cb = ttk.Combobox(input_bar, values=["Bisección", "Newton-Raphson", "Secante"], state="readonly", width=15)
    metodo_cb.current(0)
    metodo_cb.pack(side="left", padx=10)

    # Inputs dinámicos
    tk.Label(input_bar, text="Val 1:", bg=COLOR_CUERPO).pack(side="left")
    v1_ent = tk.Entry(input_bar, width=8); v1_ent.insert(0, "0"); v1_ent.pack(side="left", padx=2)
    tk.Label(input_bar, text="Val 2:", bg=COLOR_CUERPO).pack(side="left")
    v2_ent = tk.Entry(input_bar, width=8); v2_ent.insert(0, "3"); v2_ent.pack(side="left", padx=2)

    # 4. ÁREA DE RESULTADOS (GRÁFICA Y TABLA)
    display_frame = tk.Frame(frame, bg=COLOR_CUERPO)
    display_frame.pack(fill="both", expand=True, padx=20, pady=5)

    p_grafica = tk.Frame(display_frame, bg="white", bd=1, relief="solid")
    p_grafica.place(relx=0, rely=0, relwidth=0.48, relheight=1)

    p_tabla = tk.Frame(display_frame, bg="white", bd=1, relief="solid")
    p_tabla.place(relx=0.52, rely=0, relwidth=0.48, relheight=1)

    # ================= LÓGICA DE CÁLCULO =================
    def ejecutar_calculo():
        # Limpiar pantallas anteriores
        for w in p_grafica.winfo_children(): w.destroy()
        for w in p_tabla.winfo_children(): w.destroy()

        try:
            expr = entrada_f.get()
            metodo = metodo_cb.get()
            # Convertir constantes como pi
            a = float(v1_ent.get().replace("pi", str(math.pi)))
            b = float(v2_ent.get().replace("pi", str(math.pi)))
            
            datos = []
            raiz = 0

            # --- BISECCIÓN ---
            if metodo == "Bisección":
                if f_eval(a, expr) * f_eval(b, expr) >= 0:
                    messagebox.showerror("Error", "No hay cambio de signo en el intervalo.")
                    return
                for i in range(1, 15):
                    c = (a + b) / 2
                    err = abs(b - a)
                    datos.append((i, f"{a:.4f}", f"{b:.4f}", f"{c:.4f}", f"{err:.2e}"))
                    if f_eval(a, expr) * f_eval(c, expr) < 0: b = c
                    else: a = c
                    raiz = c

            # --- NEWTON RAPHSON ---
            elif metodo == "Newton-Raphson":
                x0 = a
                for i in range(1, 15):
                    fx = f_eval(x0, expr)
                    dfx = derivada(x0, expr)
                    if dfx == 0: break
                    x_new = x0 - fx/dfx
                    err = abs(x_new - x0)
                    datos.append((i, f"{x0:.4f}", f"{fx:.4f}", f"{x_new:.4f}", f"{err:.2e}"))
                    x0 = x_new
                    if err < 1e-6: break
                raiz = x0

            # --- RENDERIZAR TABLA ---
            cols = ("Iter", "A / Xn", "B / f(x)", "Raíz", "Error")
            tree = ttk.Treeview(p_tabla, columns=cols, show="headings")
            for col in cols: 
                tree.heading(col, text=col)
                tree.column(col, width=65, anchor="center")
            for d in datos: tree.insert("", "end", values=d)
            tree.pack(fill="both", expand=True)

            # --- RENDERIZAR GRÁFICA ---
            fig = Figure(figsize=(4, 4), dpi=90)
            ax = fig.add_subplot(111)
            # Rango inteligente de gráfica
            rango = b - a if b != a else 10
            x_vals = [ (a - rango) + (rango*3) * i/100 for i in range(101) ]
            y_vals = [ f_eval(x, expr) for x in x_vals ]
            
            ax.plot(x_vals, y_vals, color=COLOR_BARRA_SUP, lw=2)
            ax.axhline(0, color="black", lw=1)
            ax.axvline(0, color="black", lw=1)
            ax.plot(raiz, 0, 'go', markersize=8) # Punto de la raíz en verde
            ax.grid(True, alpha=0.3)
            
            canvas = FigureCanvasTkAgg(fig, master=p_grafica)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            set_resultado(f"Resultado: {raiz:.6f}")

        except Exception as e:
            messagebox.showerror("Error de Cálculo", str(e))

    # BOTÓN CALCULAR
    btn_calc = tk.Button(input_bar, text="Calcular", bg=COLOR_BOTON, fg="white", 
                        font=("Arial", 10, "bold"), width=15, relief="flat", command=ejecutar_calculo)
    btn_calc.pack(side="left", padx=20)
