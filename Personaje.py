class Personaje:
    def __init__(self, nombre, planeta_origen, genero, nombre_nave, episodios, nombre_vehiculo, especie):
        self.nombre=nombre
        self.planeta_origen=planeta_origen
        self.genero=genero
        self.nombre_nave=nombre_nave
        self.episodios=episodios
        self.nombre_vehiculo= nombre_vehiculo
        self.especie= especie


    def show(self):
        print(f"El nombre del personaje es: {self.nombre}")
        print(f"El plantea de origen es: {self.planeta_origen}")
        print(f"Su genero es: {self.genero}")
        print(f"El nombre de las naves que utiliza son: {self.nombre_nave}")
        print(f"Los episodios en los que aparece son: {self.episodios}")
        print(f"El nombre de los vehiculos que utiliza son: {self.nombre_vehiculo}")
        print(f"Su especie es: {self.especie}")
        