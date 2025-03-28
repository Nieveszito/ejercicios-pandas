import tkinter as tk
from tkinter import messagebox
import pandas as pd

USUARIOS = {}
with open("usuarios.txt", "r") as f:
    for linea in f:
        usuario, contrasena = linea.strip().split(",")
        USUARIOS[usuario] = contrasena
        
datos = pd.read_excel("Sacramentorealestatetransactions.xlsx")

#inicio de sesión
def validar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    
    if usuario in USUARIOS and USUARIOS[usuario] == contrasena:
        abrir_consultas()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

#consultas
def ejecutar_consulta(consulta):
    resultado = ""
    if consulta == "Casas con más de 3 habitaciones y precio mayor a 100,000":
        resultado = datos[(datos["beds"] > 3) & (datos["price"] > 100000)].to_string()
        
        
    elif consulta == "Propiedades en Sacramento con más de 2 baños":
        resultado = datos[(datos["city"] == "SACRAMENTO") & (datos["baths"] > 2)].to_string()
        
    elif consulta == "Precio promedio de casas con más de 2 habitaciones":
        resultado = f"Promedio de precio: {datos[datos['beds'] > 2]['price'].mean()}"
        
    elif consulta == "Propiedades con más de 1000 sqft y menos de 3 habitaciones":
        resultado = datos[(datos["sq__ft"] > 1000) & (datos["beds"] < 3)].to_string()
        
    elif consulta == "Top 5 propiedades más caras":
        resultado = datos.nlargest(5, "price").to_string()
        
    elif consulta == "Ciudades con el mayor número de propiedades":
        resultado = datos["city"].value_counts().head(5).to_string()
        
    elif consulta == "Precio promedio por ciudad":
        resultado = datos.groupby("city")["price"].mean().to_string()
        
    elif consulta == "Total de sqft en propiedades residenciales":
        resultado = f"Total de sqft: {datos[datos['type'] == 'Residential']['sq__ft'].sum()}"
        
    elif consulta == "Propiedad más grande por ciudad":
        resultado = datos.loc[datos.groupby("city")["sq__ft"].idxmax()].to_string()
        
    elif consulta == "Cantidad de propiedades con precio mayor al promedio":
        resultado = f"Cantidad: {(datos['price'] > datos['price'].mean()).sum()}"
    
    text_resultado.delete("1.0", tk.END)
    text_resultado.insert(tk.END, resultado)

# Función para abrir la ventana de consultas
def abrir_consultas():
    ventana_login.destroy()
    global ventana_consultas, text_resultado
    
    ventana_consultas = tk.Tk()
    ventana_consultas.title("Consultas Complejas")
    
    consultas = [
        "Casas con más de 3 habitaciones y precio mayor a 100,000", 
        "Propiedades en Sacramento con más de 2 baños", 
        "Precio promedio de casas con más de 2 habitaciones",
        "Propiedades con más de 1000 sqft y menos de 3 habitaciones",
        "Top 5 propiedades más caras",
        "Ciudades con el mayor número de propiedades",
        "Precio promedio por ciudad",
        "Total de sqft en propiedades residenciales",
        "Propiedad más grande por ciudad",
        "Cantidad de propiedades con precio mayor al promedio"
    ]
    
    frame_consultas = tk.Frame(ventana_consultas)
    frame_consultas.pack(side=tk.LEFT, padx=50, pady=50)
    
    for consulta in consultas:
        tk.Button(frame_consultas, text=consulta, command=lambda c=consulta: ejecutar_consulta(c)).pack(pady=5)
    
    frame_resultado = tk.Frame(ventana_consultas)
    frame_resultado.pack(side=tk.RIGHT, padx=50, pady=50)
    
    text_resultado = tk.Text(frame_resultado, width=180, height=100)
    text_resultado.pack()
    
    ventana_consultas.mainloop()

# ventana para el inicio de sesión
ventana_login = tk.Tk()
ventana_login.title("Inicio de Sesión")
tk.Label(ventana_login, text="NIEVES SANDOVAL ROBERTO GAEL").pack()

tk.Label(ventana_login, text="Usuario:").pack()
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack()

tk.Label(ventana_login, text="Contraseña:").pack()
entry_contrasena = tk.Entry(ventana_login, show="*")
entry_contrasena.pack()

tk.Button(ventana_login, text="Iniciar Sesión", command=validar_login).pack()

ventana_login.mainloop()

