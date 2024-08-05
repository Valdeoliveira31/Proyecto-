import csv
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
    self.crear_especies()
    self.asociar_especies_con_peliculas()
    self.crear_planetas()
    self.asociar_planetas_con_peliculas()
    ruta_residetes = "csv\planest.csv"
    self.asociar_planeta_con_residentes(ruta_residetes)
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
         for especie in self.especie_obj:
            especie.show()
      elif opcion == "3":
         for planeta in self.planeta_obj:
            planeta.show() 
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
  
       especies_pelicula = pelicula["species"]
       for especie_url in especies_pelicula:  #Obtener la URL de cada especie
          response_especie = requests.get(especie_url) 
          data_especie = response_especie.json()
          self.pelicula_obj[-1].especies.append(data_especie["name"])  # Porque fue el ultimo en insertarse
       
       planteas_pelicula = pelicula["planets"]
       for planeta_url in planteas_pelicula:
          response_planeta = requests.get(planeta_url)
          data_planeta = response_planeta.json()
          self.pelicula_obj[-1].planetas.append(data_planeta["name"])
 
  def crear_especies(self):
    url = "https://www.swapi.tech/api/species/"
    #while url:
    response = requests.get(url)
    data = response.json()
    for especie in data["results"]:   
        URL_especie = especie["url"]
        response_especie = requests.get(URL_especie)  #Obtener la URL de cada especie
        data_especie = response_especie.json()["result"]["properties"]
        homeworld_url = data_especie.get("homeworld")  #Se obtiene su planeta
        if homeworld_url:
            response_planeta_origen = requests.get(homeworld_url)
            data_planeta_origen = response_planeta_origen.json()["result"]["properties"]
            nombre_planeta_origen = data_planeta_origen["name"]   #Se obtiene el nombre del planeta
        else:
            nombre_planeta_origen = "Desconocido"  #si no tiene planeta es desconocido
        nueva_especie = Especie(data_especie["name"],data_especie["average_height"],data_especie["classification"],nombre_planeta_origen,data_especie["language"])
            
        for personaje_url in data_especie["people"]:
            response_personaje = requests.get(personaje_url).json()
            nombre_personaje = response_personaje["result"]["properties"]["name"]
            nueva_especie.personajes.append(nombre_personaje)  #Se ponen los nombres de todos los personajes de la especie    
            self.especie_obj.append(nueva_especie)
        #url = data["next"]

  def asociar_especies_con_peliculas(self):  #Se correlaciona las especies con su aparicion en las pelis
     for pelicula in self.pelicula_obj:
        for especie_name in pelicula.especies:  #Se obtiene los nombres de cada especie en cada peli
           for especie in self.especie_obj:
              if especie.nombre == especie_name:  #Se compara los nombres de especies en nuestra lista de especies con los nombres de las especies en cada peli
                 especie.episodios.append(pelicula.titulo)  

  def crear_planetas(self):
    url = "https://www.swapi.tech/api/planets/"
    #while url:
    response = requests.get(url)
    data = response.json()
    for planeta in data["results"]:
        URL_planeta = planeta["url"]
        response_planeta =requests.get(URL_planeta)
        data_planeta = response_planeta.json()["result"]["properties"]

        nuevo_planeta = Planeta(data_planeta["name"],data_planeta["orbital_period"],data_planeta["rotation_period"],data_planeta["population"],data_planeta["climate"])

       
        self.planeta_obj.append(nuevo_planeta)
        #url = data["next"] 

  def asociar_planetas_con_peliculas(self):
     for pelicula in self.pelicula_obj:
        for planeta_name in pelicula.planetas:
           for planeta in self.planeta_obj:
              if planeta.nombre == planeta_name:
                 planeta.episodios.append(pelicula.titulo)

  
  def asociar_planeta_con_residentes(self, csv_file):
     with open(csv_file, "r") as f:
        lineas = f.readlines()
        for linea in lineas[1:]:
           columnas = linea.strip().split(",")
           planeta_nombre = columnas[1]
           residents = [r.strip() for r in columnas[11].split(",")]
           for planeta in self.planeta_obj:
              if planeta.nombre == planeta_nombre:
                 planeta.residents.extend(planeta.residents)

      
                 
           
     

    
    