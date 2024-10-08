class Planeta:
    def __init__(self, nombre, periodo_orbita, periodo_rotacion, cantidad_habitantes, clima,episodios, residentes):
        self.nombre=nombre
        self.periodo_orbita=periodo_orbita
        self.periodo_rotacion=periodo_rotacion
        self.cantidad_habitantes=cantidad_habitantes
        self.clima=clima
        self.episodios=episodios
        self.residentes=residentes
    
    def show(self):
        print("-----------------------------------------------------------------")
        print(f"El nombre del planeta es: {self.nombre}")
        print(f"Su período de orbita es: {self.periodo_orbita}")
        print(f"Su período de rotación es: {self.periodo_rotacion}")
        print(f"La cantidad de habitantes son: {self.cantidad_habitantes}")
        print(f"El clima es: {self.clima}")
        print("Los episodios en que aparecen son:")
        for episodio in self.episodios:
            print(f"-{episodio}")
        print("Los personajes originarios del planeta son:")
        for personaje in self.residentes:
            print(f"-{personaje}")
        print("----------------------------------")
       
        
