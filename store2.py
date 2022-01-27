from pymongo import MongoClient
from prettytable import PrettyTable
import sys, signal, os

# Mongo server direction, host
MONGO_URI = "mongodb://localhost"

# DB connection
client = MongoClient(MONGO_URI)

# Db creation
db = client["mystore"]


# Create collection
collection = db["products"]

#collection.insert_one({"_id": 1, "Nombre": "Camiseta", "Color": "Negro", "Unidades": 50})
#collection.delete_many({})
#collection.update_one({"Nombre": "Pantalón"}, {"$set": {"Precio": 100000}})
#producto_3 = {"_id": 3, "Nombre": "Gorra", "Color": "Rojo", "Unidades": 100, "Precio": 80000}
#producto_4 = {"_id": 4, "Nombre": "Tenis", "Color": "Azul", "Unidades": 121, "Precio": 250000}
#collection.insert_many([producto_3, producto_4])

#Manipula ctrl C
def manipulador_signal(signal, frame):
    sys.exit("\nHasta Luego")
signal.signal(signal.SIGINT, manipulador_signal)

#results = collection.find({})

def mostrarCantidad():
    #Variables no Globales para que se puedan actualizar
    results = collection.find({})
    Tnames = collection.find_one({}).keys()

    tabla = PrettyTable(Tnames)

    for result in results:
        #print(result.values())
        tabla.add_row(result.values())
    print(f"{tabla}\n")


print("Bienvenido a 'my store', \n Para abandonar la tienda pulse ctrl + C")
print("\nEstán disponibles los siguientes productos:")
mostrarCantidad()

#Lista de los IDs
IDs = collection.find({}, {"_id": 1}) #Devuelve un diccionario
lista_Ids = []
for id in IDs:
     lista_Ids.append(id["_id"])

while True:
    try:
        ID = int(input("Inserte el _id del producto que desea comprar: "))
    
    except ValueError:
        print("El id no existe")
        continue
    
    if ID not in lista_Ids:
        print("El id no existe")
        continue
    
    else:
        break

# Buscando producto por ID
producto = collection.find_one({"_id": ID})


class Almacen:
    def __init__(self, producto):
        self.producto = producto

    def seleccion(self):
        print("\nHa elegido el producto:", self.producto["Nombre"], "\n")

    def comprar(self):
        while True:
            try:
                budget = int(input("Inserte la cantidad de dinero en pesos con la que va a pagar: "))
            
            except ValueError:
                print("Debe ser un entero")
                continue
            
            if budget < self.producto["Precio"]:
                sys.exit("No tiene dinero suficiente")
            
            else:
                break

        cambio =  budget - self.producto["Precio"]
        print(f"\nSu cambio es de: {cambio}")
        self.actualizar_cantidad()

    def actualizar_cantidad(self):
        collection.update_one({"Nombre": self.producto["Nombre"]}, {"$inc": {"Unidades": -1}})
        print("\nLa tabla se ha actualizado")

    def mostrar_cantidad(self):
        mostrarCantidad()

    def continuar(self):
        request = input("Desea continuar comprando [S/n]: ")
        if request == "S" or request == "s":
            os.system(f"python3 {__file__}")
        else:
            sys.exit("Hasta la próxima")

miProducto = Almacen(producto)
miProducto.seleccion()
miProducto.comprar()
#miProducto.actualizar_cantidad()
miProducto.mostrar_cantidad()
miProducto.continuar()
