class Mision:
    def __init__(self, nombre, planeta_destino, nave, integrantes, armas):
        self.nombre=nombre
        self.planeta_destino=planeta_destino
        self.nave=nave
        self.integrantes=integrantes
        self.armas=armas

    def show_datos(self):
        print(f"""
Nombre de la mision: {self.nombre}
Planeta Destino: {self.planeta_destino.name}
Nave a utilizar: {self.nave.name}
""")
        print("Integrantes de la mision:")
        self.mostrar_integrantes()
        print("Armas de la mision:")
        self.mostrar_armas()

    def mostrar_integrantes(self):
        contador=1
        for i in self.integrantes:
            print(f"{contador}.{i.name}")
            contador+=1

    def mostrar_armas(self):
        contador=1
        for i in self.armas:
            print(f"{contador}.{i.name}")
            contador+=1

    