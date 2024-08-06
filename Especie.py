class Especie:
    def __init__(self, nombre, altura, clasificacion, planeta_origen, lengua_materna):
        self.nombre=nombre
        self.altura=altura
        self.clasificacion=clasificacion
        self.planeta_origen=planeta_origen
        self.lengua_materna=lengua_materna
        self.episodios=[]
        self.personajes=[]
    
    def show(self):
        print(f"El nombre de la especie es: {self.nombre}")
        print(f"Su altura es de: {self.altura}")
        print(f"Su clasificacion es: {self.clasificacion}")
        print(f"El planeta de origen es: {self.planeta_origen}")
        print(f"Su lengua materna es: {self.lengua_materna}")
        print("Los episodios en que aparecen son:")
        for episodio in self.episodios:
            print(f"-{episodio}")
        print("Los personajes de esta especie son:")
        for personaje in self.personajes:
            print(f"-{personaje}")
        print("----------------------------------")
