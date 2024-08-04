import requests
from Especie import Especie
from Nave import Nave
from Pelicula import Pelicula
from Personaje import Personaje
from Planeta import Planeta
from Vehiculo import Vehiculo

class APP:
  especie_obj=[]
  nave_obj=[]
  pelicula_obj=[]
  persona_obj=[]
  planeta_obj=[]
  vehiculo_obj=[]
  
  def start(self):
    self.crear_peliculas()
    while True:
      print("BIENVENIDOS A STAR WARS METROPEDIA")
      opcion=input("""
Ingrese una opcion del menú principal: 
    1.Lista de peliculas de la saga.
    2.Lista de las especies de seres vivos de la saga.
    3.Lista de planetas.
    4.Buscar personaje.
    5.Construir misión.
    6.Modificar misión.
    7.Visualizar misión.
    8.Guardar misiones.
    9.Cargar misiones. 
    10.Salir 
--->""")
      if opcion=="1":
         for pelicula in self.pelicula_obj:
            pelicula.show()
      elif opcion == "2":
        None
      elif opcion == "3":
         None
      elif opcion == "4":
         None
      elif opcion == "5":
         None
      elif opcion == "6":
         None
      elif opcion == "7":
        None
      elif opcion == "8":
        None
      elif opcion == "9":
        None
      elif opcion == "10":
        break
      else:
                print("Debe ingresar una opcion del menú.")

        # Funciones que premiten la creación de los objetos:
  def crear_peliculas(self):
        url = "https://swapi.dev/api/films/"
        response = requests.get(url)
        data = response.json()
        for pelicula in data["results"]:
            self.pelicula_obj.append(Pelicula(pelicula["title"], pelicula["episode_id"], pelicula["release_date"], pelicula["opening_crawl"], pelicula["director"],))
      
   

    
    