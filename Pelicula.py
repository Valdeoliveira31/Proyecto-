class Pelicula:
    def __init__(self, titulo, num_episodio, fecha_lanzamiento, texto_inicial, director):
        self.titulo=titulo
        self.num_episodio=num_episodio
        self.fecha_lanzamiento=fecha_lanzamiento
        self.texto_inicial=texto_inicial
        self.director=director
        self.especies=[]
        self.planetas=[]
        self.personajes=[]


    def show(self):
        print(f"El titulo de la pelicula es: {self.titulo}")
        print(f"El numero del episodio es: {self.num_episodio}")
        print(f"La fecha de lanzamiento es: {self.fecha_lanzamiento}")
        print(f"El Opening crawl es: {self.texto_inicial}")
        print(f"El director es: {self.director}")
        print("----------------------------------")

      

