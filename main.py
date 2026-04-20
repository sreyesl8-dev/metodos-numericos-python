import tkinter as tk
from config import *
from MODULOS import raices, interpolacion, sistemas

class PantallaBienvenida:
    """Pantalla de bienvenida con botones Iniciar y Salir"""
    def __init__(self, parent, on_iniciar):
        self.parent = parent
        self.on_iniciar = on_iniciar
        
        # Frame para la portada
        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True)
        
        # Contenido de la portada
        self.crear_portada()
    
    def crear_portada(self):
        # Título principal
        titulo = tk.Label(
            self.frame,
            text="App Métodos PRO",
            font=("Arial", 36, "bold"),
            bg=BG,
            fg="#639dee"
        )
        titulo.pack(pady=50)
        
        # Subtítulo
        subtitulo = tk.Label(
            self.frame,
            text="Métodos Numéricos para Ingeniería",
            font=("Arial", 16),
            bg=BG,
            fg="white"
        )
        subtitulo.pack(pady=10)
        
        # Línea decorativa
        linea = tk.Frame(self.frame, bg="#639dee", height=2, width=400)
        linea.pack(pady=20)
        linea.pack_propagate(False)
        
        # Icono o imagen (opcional - texto decorativo)
        icono = tk.Label(
            self.frame,
            text="📊📈🧮",
            font=("Arial", 48),
            bg=BG,
            fg="#639dee"
        )
        icono.pack(pady=30)
        
        # Descripción
        descripcion = tk.Label(
            self.frame,
            text="Resuelve problemas de:\n• Raíces de ecuaciones\n• Interpolación\n• Sistemas de ecuaciones\n• Y más...",
            font=("Arial", 12),
            bg=BG,
            fg="white",
            justify="center"
        )
        descripcion.pack(pady=20)
        
        # Frame para botones
        frame_botones = tk.Frame(self.frame, bg=BG)
        frame_botones.pack(pady=30)
        
        # Botón Iniciar
        btn_iniciar = tk.Button(
            frame_botones,
            text="▶ INICIAR",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.iniciar
        )
        btn_iniciar.pack(side="left", padx=10)
        
        # Botón Salir
        btn_salir = tk.Button(
            frame_botones,
            text="✖ SALIR",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.salir
        )
        btn_salir.pack(side="left", padx=10)
        
        # Efecto hover para botones
        def on_enter(btn, color):
            btn.config(bg=color)
        
        def on_leave(btn, color):
            btn.config(bg=color)
        
        btn_iniciar.bind("<Enter>", lambda e: on_enter(btn_iniciar, "#2ecc71"))
        btn_iniciar.bind("<Leave>", lambda e: on_leave(btn_iniciar, "#27ae60"))
        
        btn_salir.bind("<Enter>", lambda e: on_enter(btn_salir, "#c0392b"))
        btn_salir.bind("<Leave>", lambda e: on_leave(btn_salir, "#e74c3c"))
        
        # Versión
        version = tk.Label(
            self.frame,
            text="Versión 1.0",
            font=("Arial", 9),
            bg=BG,
            fg="#7f8c8d"
        )
        version.pack(side="bottom", pady=10)
    
    def iniciar(self):
        """Destruye la portada y ejecuta la app principal"""
        self.frame.destroy()
        self.on_iniciar()
    
    def salir(self):
        """Cierra la aplicación"""
        self.parent.quit()
        self.parent.destroy()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("App Métodos PRO")
        self.root.geometry("1200x700")
        self.root.configure(bg=BG)
        
        # Centrar la ventana en la pantalla
        self.centrar_ventana()
        
        # Mostrar pantalla de bienvenida primero
        self.mostrar_bienvenida()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        ancho = 1200
        alto = 700
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def mostrar_bienvenida(self):
        """Muestra la pantalla de bienvenida"""
        self.pantalla_bienvenida = PantallaBienvenida(self.root, self.iniciar_app)
    
    def iniciar_app(self):
        """Inicia la aplicación principal después de la bienvenida"""
        # -------- VARIABLES --------
        self.resultado = tk.StringVar()
        self.tabla_datos = []
        self.vista = "grafica"  # grafica o tabla
        self.modulo_actual = "raices"

        # -------- BARRA SUPERIOR --------
        barra = tk.Frame(self.root, bg="#639dee", height=50)
        barra.pack(fill="x")

        tk.Label(barra, text="App Métodos PRO",
                 bg="#639dee", fg="white",
                 font=("Arial", 14, "bold")).pack(side="left", padx=10)

        iconos = tk.Frame(barra, bg="#5387b5")
        iconos.pack(side="right", padx=10)

        tk.Button(iconos, text="📊", bg="#5387b5", fg="white",
                  border=0, command=self.mostrar_tabla).pack(side="left", padx=5)

        tk.Button(iconos, text="📈", bg="#5387b5", fg="white",
                  border=0, command=self.mostrar_grafica).pack(side="left", padx=5)

        tk.Button(iconos, text="🗑", bg="#5387b5", fg="white",
                  border=0, command=self.limpiar).pack(side="left", padx=5)

        # -------- CONTENEDOR --------
        contenedor = tk.Frame(self.root, bg=BG)
        contenedor.pack(fill="both", expand=True)

        # -------- MENÚ --------
        menu = tk.Frame(contenedor, bg="#2c3e50", width=200)
        menu.pack(side="left", fill="y")

        tk.Label(menu, text="MÓDULOS",
                 bg="#2c3e50", fg="white",
                 font=("Arial", 12, "bold")).pack(pady=10)

        def boton(texto, comando):
            tk.Button(menu, text=texto,
                      command=comando,
                      bg="#34495e", fg="white",
                      height=2).pack(fill="x", padx=5, pady=5)
            
        boton("Raíces", self.cargar_raices)
        boton("Interpolación", self.cargar_interpolacion)
        boton("Sistemas", self.cargar_sistemas)
        boton("Integración", self.cargar_integracion)
        boton("Diferenciales", self.cargar_diferenciales)
        
        # -------- CONTENIDO --------
        self.contenido = tk.Frame(contenedor, bg=BG)
        self.contenido.pack(side="left", fill="both", expand=True)

        # -------- PANEL RESULTADO --------
        self.panel_resultado = tk.Frame(contenedor, bg="#1e1e1e", width=300)
        self.panel_resultado.pack(side="right", fill="y")

        scroll = tk.Scrollbar(self.panel_resultado)
        scroll.pack(side="right", fill="y")

        self.txt_resultado = tk.Text(
            self.panel_resultado,
            wrap="word",
            yscrollcommand=scroll.set,
            bg="#1e1e1e",
            fg="#00ff88",
            font=("Consolas", 10)
        )
        self.txt_resultado.pack(fill="both", expand=True)

        scroll.config(command=self.txt_resultado.yview)

        # -------- INICIO --------
        self.cargar_raices()

    # -------- FUNCIONES GENERALES --------
    def limpiar(self):
        for w in self.contenido.winfo_children():
            w.destroy()
        self.txt_resultado.delete("1.0", tk.END)

    def set_resultado(self, txt):
        self.txt_resultado.insert(tk.END, txt + "\n")

    def mostrar_tabla(self):
        self.vista = "tabla"
        self.recargar_modulo()

    def mostrar_grafica(self):
        self.vista = "grafica"
        self.recargar_modulo()

    def recargar_modulo(self):
        if self.modulo_actual == "raices":
            self.cargar_raices()
        elif self.modulo_actual == "interpolacion":
            self.cargar_interpolacion()
        elif self.modulo_actual == "sistemas":
            self.cargar_sistemas()

    # -------- CARGA DE MÓDULOS --------
    def cargar_raices(self):
        self.modulo_actual = "raices"
        raices.cargar(self.contenido, self.limpiar,
                      self.tabla_datos, self.set_resultado, self.vista)

    def cargar_interpolacion(self):
        self.modulo_actual = "interpolacion"
        interpolacion.cargar(self.contenido, self.limpiar,
                             self.tabla_datos, self.set_resultado, self.vista)

    def cargar_sistemas(self):
        self.modulo_actual = "sistemas"
        sistemas.cargar(self.contenido, self.limpiar,
                        self.tabla_datos, self.set_resultado, self.vista)

    def cargar_integracion(self):
        self.modulo_actual = "integracion"
        self.limpiar()
        tk.Label(self.contenido,
                 text="Módulo Integración (en construcción)",
                 bg=BG, fg="white",
                 font=("Arial", 14)).pack(pady=20)

    def cargar_diferenciales(self):
        self.modulo_actual = "diferenciales"
        self.limpiar()
        tk.Label(self.contenido,
                 text="Módulo Diferenciales (en construcción)",
                 bg=BG, fg="white",
                 font=("Arial", 14)).pack(pady=20)

# -------- EJECUCIÓN --------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()