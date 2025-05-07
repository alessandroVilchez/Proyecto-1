import mysql.connector
import requests
import pandas as pd


conn= mysql.connector.connect(
    host="localhost",
    user="root",
    password="", 

)

cursor= conn.cursor(buffered=True)



""" EJERCICIOS A REALIZAR:  
        - CONSUMIR LA API DE POKEMON 
        - CONVERTIR A UN DATAFRAME SOLAMENTE LOS NOMBRES Y LAS URL DE CADA POKEMON Y TOMAR DE LA URL
          EL ID DE CADA UNO DE ELLOS PARA LUEGO AÑADIRLA AL DATAFRAME EN UNA COLUMNA NUEVA. 
        - TRAER LA INFORMACION DE LAS HABILIDADES DE CADA POKEMON Y AÑADIRLA EN UNA COLUMNA NUEVA AL DF
        - CONECTARSE A LA BASE DE DATOS PARA GUARDAR LA DATA ACTUALIZADA.
"""


peticion= requests.get("https://pokeapi.co/api/v2/pokemon")
habilidades= requests.get("https://pokeapi.co/api/v2/ability").json()
respuesta=peticion.json()
lista=respuesta["results"]
df=pd.DataFrame(lista)

"""AQUI SE EXTRAE EL ID DE LA URL Y SE CREA UNA NUEVA COLUMNA CON EL ID DE CADA POKEMON PARA LUEGO AÑADIRLA AL DATAFRAME"""

id=[]
for x in df["url"]:
    z=x[31:]
    z=z[z.find("/")+1:]
    z=z[:z.find("/")]
    id.append(z)

df.insert(0, "id", id)

"""IMPORTANDO LA INFORMACION DE LAS HABILIDADES DE CADA POKEMON Y AÑADIRLA EN UNA COLUMNA NUEVA AL DF"""
a=[]
resultado=habilidades["results"]
for x in resultado:
    a.append(x["name"])

df.insert(2, "habilidades", a)   
df.rename(columns={"name":"nombre"}, inplace=True)

sql=cursor.execute("USE db")
cursor.execute("DELETE FROM practica")
conn.commit()
sql=cursor.execute("""CREATE TABLE practica(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   nombre VARCHAR (50), 
                   habilidades VARCHAR (50),
                   url VARCHAR (100)
                   
)                   """)

for i,v in df.iterrows():
     insertar="INSERT INTO practica (nombre, habilidades, url) VALUES (%s, %s, %s)"
     valores=(v["nombre"], v["habilidades"], v["url"])
     cursor.execute(insertar, valores)
conn.commit()

print("esta bien")


