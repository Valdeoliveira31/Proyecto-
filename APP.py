import csv
import requests
import pandas as pd 
import matplotlib.pyplot as plt
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
    ruta_residetes = "csv/planets.csv"
    self.asociar_planeta_con_residentes(ruta_residetes)
    self.agregar_personajes()
    
    while True:
      print("BIENVENIDOS A STAR WARS METROPEDIA")
      opcion=input("""
Ingrese una opcion del menú principal: 
    1.Lista de peliculas de la saga.
    2.Lista de las especies de seres vivos de la saga.
    3.Lista de planetas.
    4.Buscar personaje.
    5.Grafico cantidad de personajes nacidos en cada planeta
    6.Grafico longitud de las naves
    7.Grafico capacidad de carga de las naves
    8.Grafico clasificacion de hiperimpulsor de las naves
    9.Grafico MGLT (Modern Galactic Light Time) de las naves
    10.Estadisticas sobre naves                                            
    11.Construir misión.
    12.Modificar misión.
    13.Visualizar misión.
    14.Guardar misiones.
    15.Cargar misiones. 
    16.Salir 
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
         self.buscar_personaje()
      elif opcion == "5":
         self.grafico_personas_nacidas()
      elif opcion == "6":
         self.grafico_longitud_naves()
      elif opcion == "7":
         self.grafico_carga_naves()
      elif opcion == "8":
         self.grafico_hiperimpulsor_naves()
      elif opcion == "9":
         self.grafico_mglt_naves()
      elif opcion == "10":
         self.estadisticas_naves()
      elif opcion == "11":
        None
      elif opcion == "12":
        None
      elif opcion == "16":
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
    while url:
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
       url = data["next"]

  def asociar_especies_con_peliculas(self):  #Se correlaciona las especies con su aparicion en las pelis
     for pelicula in self.pelicula_obj:
        for especie_name in pelicula.especies:  #Se obtiene los nombres de cada especie en cada peli
           for especie in self.especie_obj:
              if especie.nombre == especie_name:  #Se compara los nombres de especies en nuestra lista de especies con los nombres de las especies en cada peli
                 especie.episodios.append(pelicula.titulo)  

  def crear_planetas(self):
    url = "https://www.swapi.tech/api/planets/"
    response = requests.get(url)
    data = response.json()
    for planeta in data["results"]:
        URL_planeta = planeta["url"]
        response_planeta =requests.get(URL_planeta)
        data_planeta = response_planeta.json()["result"]["properties"]

        nuevo_planeta = Planeta(data_planeta["name"],data_planeta["orbital_period"],data_planeta["rotation_period"],data_planeta["population"],data_planeta["climate"])

        self.planeta_obj.append(nuevo_planeta)
      
  def asociar_planetas_con_peliculas(self):
     for pelicula in self.pelicula_obj:
        for planeta_name in pelicula.planetas:
           for planeta in self.planeta_obj:
              if planeta.nombre == planeta_name:
                 planeta.episodios.append(pelicula.titulo)

  
  def asociar_planeta_con_residentes(self, csv_file):
     with open(csv_file, newline= "", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
           planeta_nombre = row["name"]
           residents = row["residents"].strip().split(", ")
           for planeta in self.planeta_obj:
              if planeta.nombre == planeta_nombre:
                 planeta.residentes.extend(residents)
        
  def agregar_personajes(self):
     url= 'https://www.swapi.tech/api/people/'
     while url: 
        response= requests.get(url)
        data = response.json()
        for personaje in data["results"]:
           url_personaje= personaje["url"]
           response_personaje= requests.get(url_personaje)
           data_personaje= response_personaje.json()["result"]["properties"]
           nombre_personaje= data_personaje["name"]
           genero_personaje= data_personaje["gender"]
           homeworld_url= data_personaje["homeworld"]
           if homeworld_url:
             response_homeworld= requests.get(homeworld_url)
             data_homeworld= response_homeworld.json()["result"]["properties"]
             planeta_personaje= data_homeworld["name"]
           else:
              planeta_personaje="Desconocido"
           lista_naves=[]
           response_naves= requests.get('https://www.swapi.tech/api/starships/')
           data_naves= response_naves.json()["results"]
           for nave in data_naves:
               url_nave= nave["url"]
               response_nave= requests.get(url_nave)
               data_nave= response_nave.json()["result"]["properties"]
               for piloto in data_nave["pilots"]:
                  if url_personaje ==piloto:
                     lista_naves.append(data_nave["name"])
           lista_espisodios=[]
           response_espisodios= requests.get("https://www.swapi.tech/api/films/")
           data_espisodios= response_espisodios.json()["result"]
           for n in data_espisodios:
              for personaje in n["properties"]["characters"]:
                 if personaje ==url_personaje:
                    lista_espisodios.append(n["properties"]["title"])
           lista_vehiculos=[]
           response_vehiculos= requests.get('https://www.swapi.tech/api/vehicles/')
           data_vehiculos= response_vehiculos.json()["results"]
           for vehiculo in data_vehiculos:
             url_vehiculo= vehiculo["url"]
             response_vehiculo= requests.get(url_vehiculo)
             data_vehiculo= response_vehiculo.json()["result"]["properties"]
             for conductor in data_vehiculo["pilots"]:
                if conductor ==url_personaje:
                   lista_vehiculos.append(data_vehiculo["name"])
           especie_personaje="Desconocido"
           for especie in self.especie_obj:
              for persona in especie.personajes:
                  if persona==nombre_personaje:
                      especie_personaje=especie.nombre
           self.persona_obj.append(Personaje(nombre_personaje,planeta_personaje,genero_personaje,lista_naves,lista_espisodios,lista_vehiculos, especie_personaje))
        url=data["next"]

  def buscar_personaje(self):
     nombre = input("Introduzca los caracteres del personaje que desea buscar: ")
     contador =1
     lista_coinciden=[]
     print("Lista de personajes que coinciden con la busqueda")
     for personaje in self.persona_obj:
        if nombre in personaje.nombre:
           lista_coinciden.append(personaje)
           print(f"{contador}.{personaje.nombre}")
           contador+=1
     if len(lista_coinciden)==0:
         print("Ningun personaje coincide con su busqueda")
     else:
      escoger_personaje=int(input("Seleccione el personaje"))
      personaje_escogido=lista_coinciden[escoger_personaje-1]
      personaje_escogido.show()

 #Funciones que muestran los graficos 
  def grafico_personas_nacidas(self):
      df = pd.read_csv("csv/planets.csv") #Leer archivo csv de planetas
      planeta= df['name'] #Seleccionar datos para el graficos
      poblacion= df['population']
      plt.figure(figsize=(14,10)) #Crear diagrama de barras vertical
      plt.bar(planeta,poblacion)
      plt.title('Personajes nacidos en cada planeta') #Añadir titulo y nombre de los ejes
      plt.xlabel('Nombre del plantea')
      plt.ylabel('Personajes nacidos')
      plt.show() #Mostrar la grafica
          
  def grafico_longitud_naves(self):
      ships= pd.read_csv("csv/starships.csv") #Leer archivo csv de starships
      ships = ships.drop_duplicates(subset=['name']) # Eliminar duplicados
      nave= ships['name'] #Seleccionar datos para el graficos
      longitud= ships['length']
      plt.figure(figsize=(14,10)) #Crear diagrama de barras horizontal
      plt.barh(nave,longitud)
      plt.xscale('log') # Aplicar escala logarítmica en el eje x para mejorar la visibilidad
      plt.title('Longitud de las Naves (Escala Logarítmica)') #Añadir titulo y nombre de los ejes
      plt.xlabel('Longitud')
      plt.ylabel('Nombre de la nave')
      plt.show() #Mostrar la grafica   

  def grafico_carga_naves(self):
      ships= pd.read_csv("csv/starships.csv") #Leer archivo csv de starships
      ships = ships.drop_duplicates(subset=['name']) # Eliminar duplicados
      nave= ships['name'] #Seleccionar datos para el graficos
      carga= ships['cargo_capacity']
      plt.figure(figsize=(14,10)) #Crear diagrama de barras horizontal
      plt.barh(nave,carga)
      plt.xscale('log') # Aplicar escala logarítmica en el eje x para mejorar la visibilidad
      plt.title('Carga de las Naves (Escala Logarítmica)') #Añadir titulo y nombre de los ejes
      plt.xlabel('Carga')
      plt.ylabel('Nombre de la nave')
      plt.show() #Mostrar la grafica     

  def grafico_hiperimpulsor_naves(self):
      ships= pd.read_csv("csv/starships.csv") #Leer archivo csv de starships
      ships = ships.drop_duplicates(subset=['name']) # Eliminar duplicados
      nave= ships['name'] #Seleccionar datos para el graficos
      hiperimpulsor= ships['hyperdrive_rating']
      plt.figure(figsize=(14,10)) #Crear diagrama de barras horizontal
      plt.barh(nave,hiperimpulsor)
      plt.title('Clasificacion del hiperimpulsor') #Añadir titulo y nombre de los ejes
      plt.xlabel('Hiperimpulsor')
      plt.ylabel('Nombre de la nave')
      plt.show() #Mostrar la grafica   

  def grafico_mglt_naves(self):
      ships= pd.read_csv("csv/starships.csv") #Leer archivo csv de starships
      ships = ships.drop_duplicates(subset=['name']) # Eliminar duplicados
      nave= ships['name'] #Seleccionar datos para el graficos
      mglt= ships['MGLT']
      plt.figure(figsize=(14,10)) #Crear diagrama de barras horizontal
      plt.barh(nave,mglt)
      plt.title('MGLT(Modern Galactic Light Time)') #Añadir titulo y nombre de los ejes
      plt.xlabel('MGLT')
      plt.ylabel('Nombre de la nave')
      plt.show() #Mostrar la grafica  
        
  def estadisticas_naves(self):
     ships = pd.read_csv("csv/starships.csv") #Leer archivo csv de starships
     ships = ships.drop_duplicates(subset=['name']) # Eliminar duplicados
     ships = ships.replace(["NaN"],pd.NA) # Para valores faltantes
     ships['hyperdrive_rating'] = pd.to_numeric(ships['hyperdrive_rating'], errors='coerce') #Pasar columnas a vlores numericos
     ships['MGLT'] = pd.to_numeric(ships['MGLT'], errors='coerce')
     ships['max_atmosphering_speed'] = pd.to_numeric(ships['max_atmosphering_speed'], errors='coerce')
     ships['cost_in_credits'] = pd.to_numeric(ships['cost_in_credits'], errors='coerce')
      
     def mode_series(series):  #Funcion para calcular modas
        mode_values = series.mode()
        if len(mode_values) == 1:
           return mode_values[0]
        else:
           return mode_values.tolist()
        
      #Agrupar por clase de nave y calcular las estadisticas
     estadisticas = ships.groupby('starship_class').agg({
         'hyperdrive_rating':['mean','max','min',mode_series],
         'MGLT':['mean','max','min',mode_series],
         'max_atmosphering_speed':['mean','max','min',mode_series],
         'cost_in_credits':['mean','max','min',mode_series]
      }).reset_index()
     
     #Renombrar columnas
     estadisticas.columns= ['Clase de nave',
                            'Hiperimpulsor (Promedio)', 'Hiperimpulsor (Máx)', 'Hiperimpulsor (Mín)', 'Hiperimpulsor (Moda)',
                            'MGLT (Promedio)', 'MGLT (Máx)', 'MGLT (Mín)', 'MGLT (Moda)', 
                            'Velocidad Máxima en Atmósfera (Promedio)', 'Velocidad Máxima en Atmósfera (Máx)', 'Velocidad Máxima en Atmósfera (Mín)', 'Velocidad Máxima en Atmósfera (Moda)',
                            'Costo en Créditos (Promedio)', 'Costo en Créditos (Máx)', 'Costo en Créditos (Mín)', 'Costo en Créditos (Moda)']
     estadisticas= estadisticas.round(2) #redondear
     #Mostrar tabla
     with pd.option_context('display.max_rows',None,'display.max_columns', None):
        print(estadisticas)
     
        







       

    
    