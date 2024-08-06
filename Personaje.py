class Personaje:
    def __init__(self, nombre, planeta_origen, episodios, genero, especie, nombre_nave, nombre_vehiculo):
        self.nombre=nombre
        self.planeta_origen=planeta_origen
        self.episodios=episodios
        self.genero=genero
        self.especie=especie
        self.nombre_nave=[]
        self.nombre_vehiculo=[]

    def show(self):
        print(f"El nombre del personaje es: {self.nombre}")
        print(f"El plantea de origen es: {self.planeta_origen}")
        print(f"Los episodios que interviene son: {self.episodios}")
        print(f"Su genero es: {self.genero}")
        print(f"Su especie es: {self.especie}")
        print(f"El nombre de las naves que utiliza son: {self.nombre_nave}")
        print(f"El nombre de los vehiculos que utiliza son: {self.nombre_vehiculo}")