import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage

# Clase para simular una cuenta bancaria
class CuentaBancaria:
    def __init__(self, num_cuenta, titular, saldo, tipo_cuenta):
        self.num_cuenta = num_cuenta
        self.titular = titular
        self.saldo = saldo
        self.tipo_cuenta = tipo_cuenta
        self.historial = []

    def consultar_saldo(self):
        return self.saldo

    def depositar(self, monto):
        if monto > 0:
            self.saldo += monto
            self.historial.append(f"Depósito: {monto}")
            return True
        return False

    def retirar(self, monto):
        if monto > 0 and self.saldo >= monto:
            self.saldo -= monto
            self.historial.append(f"Retiro: {monto}")
            return True
        return False

    def transferir(self, cuenta_destino, monto):
        if monto > 0 and self.saldo >= monto:
            self.saldo -= monto
            cuenta_destino.saldo += monto
            self.historial.append(f"Transferencia a {cuenta_destino.num_cuenta}: {monto}")
            cuenta_destino.historial.append(f"Transferencia de {self.num_cuenta}: {monto}")
            return True
        return False

# Diccionario para almacenar las cuentas bancarias
cuentas = {}

# Funciones para interactuar con la interfaz
def crear_cuenta():
    num_cuenta = entry_num_cuenta.get()
    titular = entry_titular.get()
    try:
        saldo_inicial = float(entry_saldo.get())
        tipo_cuenta = tipo_cuenta_var.get()

        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")

        # Crear la cuenta bancaria
        cuenta = CuentaBancaria(num_cuenta, titular, saldo_inicial, tipo_cuenta)
        cuentas[num_cuenta] = cuenta

        # Mensaje de éxito
        messagebox.showinfo("Cuenta creada", f"Cuenta {num_cuenta} creada exitosamente.")
        limpiar_campos()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def consultar_saldo():
    num_cuenta = entry_num_cuenta.get()

    if num_cuenta in cuentas:
        cuenta = cuentas[num_cuenta]
        saldo = cuenta.consultar_saldo()
        label_resultado.config(text=f"Saldo: {saldo}", fg="yellow")
    else:
        messagebox.showerror("Error", "Cuenta no encontrada.")
    limpiar_campos()

def depositar_dinero():
    num_cuenta = entry_num_cuenta.get()

    if num_cuenta in cuentas:
        try:
            monto = float(entry_monto.get())
            if monto <= 0:
                raise ValueError("El monto debe ser positivo.")
            cuenta = cuentas[num_cuenta]
            if cuenta.depositar(monto):
                messagebox.showinfo("Depósito", f"Depósito de {monto} realizado exitosamente.")
                label_resultado.config(text=f"Saldo actual: {cuenta.consultar_saldo()}", fg="yellow")
            else:
                raise ValueError("No se pudo realizar el depósito.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Cuenta no encontrada.")
    limpiar_campos()

def retirar_dinero():
    num_cuenta = entry_num_cuenta.get()

    if num_cuenta in cuentas:
        try:
            monto = float(entry_monto.get())
            if monto <= 0:
                raise ValueError("El monto debe ser positivo.")
            cuenta = cuentas[num_cuenta]
            if cuenta.retirar(monto):
                messagebox.showinfo("Retiro", f"Retiro de {monto} realizado exitosamente.")
                label_resultado.config(text=f"Saldo actual: {cuenta.consultar_saldo()}", fg="yellow")
            else:
                raise ValueError("Saldo insuficiente para realizar el retiro.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Cuenta no encontrada.")
    limpiar_campos()

def transferir_dinero():
    num_cuenta = entry_num_cuenta.get()

    if num_cuenta in cuentas:
        try:
            monto = float(entry_monto.get())
            num_cuenta_destino = entry_num_cuenta_destino.get()

            if num_cuenta_destino not in cuentas:
                raise ValueError("Cuenta de destino no encontrada.")
            if monto <= 0:
                raise ValueError("El monto debe ser positivo.")
            cuenta_origen = cuentas[num_cuenta]
            cuenta_destino = cuentas[num_cuenta_destino]
            if cuenta_origen.transferir(cuenta_destino, monto):
                messagebox.showinfo("Transferencia", f"Transferencia de {monto} realizada a {num_cuenta_destino}.")
                label_resultado.config(text=f"Saldo actual: {cuenta_origen.consultar_saldo()}", fg="yellow")
            else:
                raise ValueError("Saldo insuficiente para realizar la transferencia.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Cuenta no encontrada.")
    limpiar_campos()

# Función para limpiar los campos
def limpiar_campos():
    entry_num_cuenta.delete(0, tk.END)
    entry_titular.delete(0, tk.END)
    entry_saldo.delete(0, tk.END)
    entry_monto.delete(0, tk.END)
    entry_num_cuenta_destino.delete(0, tk.END)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Simulación de Cuenta Bancaria")
ventana.geometry("500x600")
ventana.configure(bg="black")  # Fondo de ventana negro

# Etiquetas y campos de entrada
label_num_cuenta = tk.Label(ventana, text="Número de cuenta:", bg="black", fg="white")
label_num_cuenta.pack(pady=5)
entry_num_cuenta = tk.Entry(ventana)
entry_num_cuenta.pack(pady=5)

label_titular = tk.Label(ventana, text="Titular de la cuenta:", bg="black", fg="white")
label_titular.pack(pady=5)
entry_titular = tk.Entry(ventana)
entry_titular.pack(pady=5)

label_saldo = tk.Label(ventana, text="Saldo inicial:", bg="black", fg="white")
label_saldo.pack(pady=5)
entry_saldo = tk.Entry(ventana)
entry_saldo.pack(pady=5)

label_tipo_cuenta = tk.Label(ventana, text="Tipo de cuenta:", bg="black", fg="white")
label_tipo_cuenta.pack(pady=5)
tipo_cuenta_var = tk.StringVar(value="Ahorros")
radio_ahorros = tk.Radiobutton(ventana, text="Ahorros", variable=tipo_cuenta_var, value="Ahorros", bg="black", fg="white")
radio_ahorros.pack(pady=5)
radio_corriente = tk.Radiobutton(ventana, text="Corriente", variable=tipo_cuenta_var, value="Corriente", bg="black", fg="white")
radio_corriente.pack(pady=5)

# Botones para las operaciones con colores
btn_crear_cuenta = tk.Button(ventana, text="Crear Cuenta", bg="#4CAF50", fg="white", command=crear_cuenta)
btn_crear_cuenta.pack(pady=5)

label_monto = tk.Label(ventana, text="Monto:", bg="black", fg="white")
label_monto.pack(pady=5)
entry_monto = tk.Entry(ventana)
entry_monto.pack(pady=5)

btn_depositar = tk.Button(ventana, text="Depositar Dinero", bg="#32CD32", fg="white", command=depositar_dinero)
btn_depositar.pack(pady=5)

btn_retirar = tk.Button(ventana, text="Retirar Dinero", bg="#FF6347", fg="white", command=retirar_dinero)
btn_retirar.pack(pady=5)

label_num_cuenta_destino = tk.Label(ventana, text="Número de cuenta destino:", bg="black", fg="white")
label_num_cuenta_destino.pack(pady=5)
entry_num_cuenta_destino = tk.Entry(ventana)
entry_num_cuenta_destino.pack(pady=5)

btn_transferir = tk.Button(ventana, text="Transferir Dinero", bg="#FFD700", fg="white", command=transferir_dinero)
btn_transferir.pack(pady=5)

# Etiqueta para mostrar el resultado
label_resultado = tk.Label(ventana, text="Resultado:", font=("Arial", 14), bg="black", fg="white")
label_resultado.pack(pady=10)

# Ejecutar la aplicación
ventana.mainloop()

