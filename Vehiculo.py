class Vehiculo:
    def __init__(self, nombre, modelo, fabricante):
        self.nombre=nombre
        self.modelo=modelo
        self.fabricante=fabricante

    def show(self):
        print(f"El nombre de la nave es: {self.nombre}")
        print(f"El modelo es: {self.modelo}")
        print(f"El fabricante es: {self.fabricante}")