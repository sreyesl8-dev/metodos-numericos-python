import tkinter as tk
from tkinter import ttk
import re

def cargar(frame, limpiar, tabla_datos, set_resultado, graficar):
    limpiar()

    # -------- CONTENEDORES --------
    izquierda = tk.Frame(frame, bg=frame["bg"], width=300)
    izquierda.pack(side="left", fill="y", padx=10, pady=10)

    derecha = tk.Frame(frame, bg=frame["bg"])
    derecha.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    tabla_frame = tk.Frame(derecha, bg="white")
    tabla_frame.pack(fill="both", expand=True, pady=5)

    # -------- TÍTULO --------
    tk.Label(izquierda, text="MÓDULO 3: SISTEMAS",
             bg=frame["bg"], fg="white",
             font=("Arial", 14, "bold")).pack(pady=10)

    # -------- MÉTODO --------
    metodo = ttk.Combobox(izquierda, values=["Gauss-Seidel", "Factorización LU"])
    metodo.current(0)
    metodo.pack(pady=5)

    # -------- INPUT ECUACIONES --------
    tk.Label(izquierda, text="Ecuaciones (una por línea)",
             bg=frame["bg"], fg="white").pack()

    entrada_eq = tk.Text(izquierda, height=6, width=30)
    entrada_eq.insert("1.0", "4x+y=1\n2x+3y=2")
    entrada_eq.pack(pady=5)

    tk.Label(izquierda, text="Tolerancia",
             bg=frame["bg"], fg="white").pack()
    tol = tk.Entry(izquierda)
    tol.insert(0, "0.001")
    tol.pack(pady=3)

    tk.Label(izquierda, text="Iteraciones",
             bg=frame["bg"], fg="white").pack()
    max_iter = tk.Entry(izquierda)
    max_iter.insert(0, "20")
    max_iter.pack(pady=3)

    # -------- PARSEAR --------
    def parse_ecuaciones(texto):
        ecuaciones = texto.strip().split("\n")

        A = []
        b = []
        vars_orden = []

        for eq in ecuaciones:
            izquierda, derecha = eq.split("=")
            derecha = float(derecha.strip())

            terminos = re.findall(r'([+-]?\s*\d*)([a-z])', izquierda)

            fila = []
            for coef, var in terminos:
                if var not in vars_orden:
                    vars_orden.append(var)

            for var in vars_orden:
                match = re.search(rf'([+-]?\s*\d*){var}', izquierda)
                if match:
                    coef = match.group(1).replace(" ", "")
                    if coef in ["", "+"]:
                        fila.append(1)
                    elif coef == "-":
                        fila.append(-1)
                    else:
                        fila.append(float(coef))
                else:
                    fila.append(0)

            A.append(fila)
            b.append(derecha)

        return A, b, vars_orden

    # -------- TABLA --------
    def crear_tabla(datos, columnas):
        style = ttk.Style()

        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#2b2b2b")

        style.configure("Treeview.Heading",
                        background="#467dec",
                        foreground="black",
                        font=("Arial", 10, "bold"))

        tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
        tabla.pack(fill="both", expand=True)

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center")

        for fila in datos:
            tabla.insert("", "end", values=[round(v,6) for v in fila])

    # -------- GAUSS-SEIDEL CON FÓRMULAS --------
    def gauss_seidel(A, b, tol, max_iter, vars_):
        n = len(A)
        x = [0]*n
        datos = []
        pasos = "Paso 1: Despeje automático de variables\n"

        # Mostrar fórmulas
        for i in range(n):
            formula = f"{vars_[i]} = ( {b[i]}"
            for j in range(n):
                if j != i:
                    formula += f" - {A[i][j]}*{vars_[j]}"
            formula += f" ) / {A[i][i]}"
            pasos += formula + "\n"

        pasos += "\nPaso 2: Valores iniciales\n"
        for i in range(n):
            pasos += f"{vars_[i]}0 = 0\n"

        pasos += "\nPaso 3: Iteraciones\n"

        for k in range(max_iter):
            x_new = x.copy()
            pasos += f"\nIteración {k+1}\n"

            for i in range(n):
                suma = sum(A[i][j]*x_new[j] for j in range(n) if j != i)
                x_new[i] = (b[i] - suma) / A[i][i]

                pasos += f"{vars_[i]}{k+1} = {round(x_new[i],6)}\n"

            error = max(abs(x_new[i]-x[i]) for i in range(n))
            datos.append([k] + x_new + [error])

            pasos += f"Error = {round(error,6)}\n"

            if error < tol:
                break

            x = x_new

        return x_new, datos, pasos

    # -------- LU --------
    def LU(A):
        n = len(A)
        L = [[0]*n for _ in range(n)]
        U = [[0]*n for _ in range(n)]

        for i in range(n):
            L[i][i] = 1

        for j in range(n):
            for i in range(j+1):
                suma = sum(U[k][j]*L[i][k] for k in range(i))
                U[i][j] = A[i][j] - suma

            for i in range(j, n):
                suma = sum(U[k][j]*L[i][k] for k in range(j))
                L[i][j] = (A[i][j] - suma) / U[j][j]

        return L, U

    # -------- CALCULAR --------
    def calcular():
        try:
            texto = entrada_eq.get("1.0", "end")
            A, b, vars_ = parse_ecuaciones(texto)

            if len(A) != len(A[0]):
                set_resultado("La matriz debe ser cuadrada")
                return

            metodo_sel = metodo.get()

            if metodo_sel == "Gauss-Seidel":
                x, datos, pasos = gauss_seidel(
                    A, b,
                    float(tol.get()),
                    int(max_iter.get()),
                    vars_
                )

                columnas = ["Iter"] + vars_ + ["Error"]
                crear_tabla(datos, columnas)

                solucion = " | ".join([f"{vars_[i]} ≈ {round(v,6)}" for i,v in enumerate(x)])

                set_resultado(f"{pasos}\n\nResultado final:\n{solucion}")

            else:
                L, U = LU(A)

                texto_L = "\n".join([str([round(v,3) for v in fila]) for fila in L])
                texto_U = "\n".join([str([round(v,3) for v in fila]) for fila in U])

                set_resultado(f"L:\n{texto_L}\n\nU:\n{texto_U}")

        except Exception as e:
            set_resultado(f"Error: {e}")

    # -------- BOTÓN --------
    tk.Button(izquierda, text="Calcular",
              command=calcular,
              bg="#467dec", fg="white").pack(pady=10)