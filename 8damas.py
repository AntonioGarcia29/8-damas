import tkinter as tk
from tkinter import messagebox


class Ndamas:
    def __init__(self, tamaño, primeraD):
        self.tamaño = tamaño
        self.primeraD = primeraD
        self.soluciones = []
        self.resuelve()

    #Coloca la primera dama indicada por el usuario e inicia el algoritmo
    def resuelve(self):
        tablero = [-1] * self.tamaño
        tablero[self.primeraD[0]]= self.primeraD[1]
        self.resuelveNDamas(tablero,0)

    def esSeguro(self, tablero, fila, columna):
        for i in range(fila):
            #verifica que no se coloque en la misma columna o diagonal, esto lo hace viendo si la diferencia de columnas y filas es igual
            if tablero[i] == columna or abs(tablero[i] - columna) == abs(i-fila):
                return False
        return True

#Algoritmo de backtracking
    def resuelveNDamas(self, tablero, fila):
        if fila == self.tamaño:
            self.soluciones.append(tablero[:])
            return

        for columna in range(self.tamaño):
            if fila == self.primeraD[0] and columna != self.primeraD[1]:
                continue
            if self.esSeguro(tablero, fila, columna):
                tablero[fila] = columna
                self.resuelveNDamas(tablero, fila+1)
                tablero[fila] = -1


class NdamasInterfaz:
#Interfaz
    def __init__(self,root):
        self.root = root
        self.root.title("Problema de las Damas")
        tk.Label(root, text="Tamaño del tablero:").grid(row=0, column=0)
        self.tamaño_entry = tk.Entry(root)
        self.tamaño_entry.grid(row=0, column=1)

        tk.Label(root, text="Fila de la primera dama:").grid(row=1, column=0)
        self.fila_entry = tk.Entry(root)
        self.fila_entry.grid(row=1, column=1)

        tk.Label(root, text="Columna de la primera dama:").grid(row=2, column=0)
        self.columna_entry = tk.Entry(root)
        self.columna_entry.grid(row=2, column=1)

        self.botonResolver = tk.Button(root, text="Resolver", command=self.resuelve)
        self.botonResolver.grid(row=3, columnspan=2)

        self.canvas = tk.Canvas(root, width = 700, height =700)
        self.canvas.grid(row=4, columnspan=2)

        self.solutions = []
        self.current_solution_index = 0
        
        self.next_button = tk.Button(root, text="Siguiente solución", command=self.mostrarSiguienteS)
        self.next_button.grid(row=5, columnspan=2)


    def resuelve(self):
        try:
            #Obtiene los valores de la interfaz
            tamaño = int(self.tamaño_entry.get())
            primeraFila = int(self.fila_entry.get()) - 1
            primeraColumna = int(self.columna_entry.get()) - 1

            #Valida que los valores ingresados sean validos
            if tamaño <= 0 or primeraFila < 0 or primeraColumna < 0 or primeraFila >= tamaño or primeraColumna >= tamaño:
                messagebox.showerror("Error", "Valores ingresados no válidos")
                return

            #ejecuta la clase Ndamas
            Resolver = Ndamas(tamaño, (primeraFila, primeraColumna))

            #mensaje en el que dice que no hay soluciones en el caso de que no se haya guardado nada en el array
            if not Resolver.soluciones:
                messagebox.showinfo("No existe solución", "No se encontró una solución.")
                return

            #Limitamos las soluciones para solo mostrar como maximo 10
            self.soluciones = Resolver.soluciones[:10]  
            #declaramos la variable solución actual para la paginación
            self.solucionActual = 0
            #llamamos el metodo mostrar soluciones para poder cambiar entre soluciones en la interfaz
            self.mostrarSolucion(self.soluciones[self.solucionActual])

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
    # Muestra las soluciones
    def mostrarSolucion(self, tablero):
        self.canvas.delete("all")
        #definimos el tamaño del tablero
        tamaño = len(tablero)
        #colocamos el tamaño que tendra cada recuadro, esto se divide entre el tamaño del tablero para que sea adaptable
        cell_size = 700 // tamaño  

        for i in range(tamaño):
            for j in range(tamaño):
                color = "white" if (i + j) % 2 == 0 else "black"
                self.canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)

        for i in range(tamaño):
            self.canvas.create_oval(tablero[i] * cell_size + 40, i * cell_size + 40,
                                    (tablero[i] + 1) * cell_size - 40, (i + 1) * cell_size - 40,
                                    fill="red")

    def mostrarSiguienteS(self):
        if self.soluciones:
            self.solucionActual = (self.solucionActual + 1) % len(self.soluciones)
            self.mostrarSolucion(self.soluciones[self.solucionActual])

if __name__ == "__main__":
    #Crea la ventana de la interfaz
    root = tk.Tk() 
    #instancia la clase para iniciar la interfaz
    app = NdamasInterfaz(root)
    #Sirve para mantener la ventana abierta
    root.mainloop()