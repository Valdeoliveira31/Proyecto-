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
from Personaje_CSV import Personaje_CSV
from Planeta_CSV import Planeta_CSV
from Arma import Arma
from Mision import Mision
import json


class APP:
  especie_obj=[]
  nave_obj=[]
  pelicula_obj=[]
  persona_obj=[]
  planeta_obj=[]
  vehiculo_obj=[]
  lista_planetas_csv=[]
  lista_naves=[]
  lista_personajes_csv=[]
  lista_misiones=[]
  lista_armas=[]
  i=1
  def start(self):
    self.crear_peliculas()
    self.crear_especies()
    self.asociar_especies_con_peliculas()
    self.crear_planetas()
    self.asociar_planetas_con_peliculas()
    ruta_residetes = "csv/planets.csv"
    self.asociar_planeta_con_residentes(ruta_residetes)
    self.agregar_personajes()
    self.cargar_datos()
    self.cargar_mision()
    
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
    14.Salir  
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
         self.crear_mision()
      elif opcion == "12":
        self.modificar_mision()
      elif opcion == "13":
        self.visualizar_mision()
      elif opcion=="14":
         self.guardar_mision()
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

  def cargar_datos(self):
      #Agregar planetas a la lista
      planetas=pd.read_csv("csv/planets.csv") #Lectura del Csv de los planetas
      planetas=planetas.drop_duplicates(subset=["name"]) #Eliminar Duplicados
      for index, planeta in planetas.iterrows():   #Bucle para recorrer cada fila y cada atributo
         self.lista_planetas_csv.append(Planeta_CSV(planeta["id"],planeta["name"],planeta["population"],planeta["climate"],planeta["residents"],planeta["films"]))
      
      #Agregar Naves a la lista
      naves=pd.read_csv("csv/starships.csv") #Lectura del Csv de las naves
      naves=naves.drop_duplicates(subset=["name"]) #Eliminar repetidos
      for index,nave in naves.iterrows():
         self.lista_naves.append(Nave(nave["id"],nave["name"],nave["model"],nave["manufacturer"],nave["cost_in_credits"],nave["length"],nave["max_atmosphering_speed"],nave["crew"],nave["passengers"],nave["cargo_capacity"],nave["consumables"],nave["hyperdrive_rating"],nave["MGLT"],nave["starship_class"],nave["pilots"],nave["films"]))
     
      #Agregar armas a la lista
      armas=pd.read_csv("csv/weapons.csv") #Lectura del Csv de las armas
      armas=armas.drop_duplicates(subset=["name"]) #Eliminar repetidos
      for index,arma in armas.iterrows():
         self.lista_armas.append(Arma(arma["id"],arma["name"],arma["model"],arma["manufacturer"],arma["cost_in_credits"],arma["length"],arma["type"],arma["description"],arma["films"]))
      
      #Agregar personajes a la lista
      personajes=pd.read_csv("csv/characters.csv") #Lectura del Csv de los personajes
      personajes=personajes.drop_duplicates(subset=["name"])  #Eliminar repetidos
      for index,per in personajes.iterrows():
         self.lista_personajes_csv.append(Personaje_CSV(per["id"],per["name"],per["species"],per["gender"],per["height"],per["weight"],per["hair_color"],per["eye_color"],per["skin_color"],per["year_born"],per["homeworld"],per["year_died"],per["description"]))

  def cargar_mision(self):
     try:
         with open("guardado_misiones/misiones_guardadas.txt","r") as f:
             lista_de_dict_misiones=json.loads(f.read())
             for mision in lista_de_dict_misiones:
                 #Se agarra el nombre
                 nombre_mision=mision["nombre_mision"]
                 #Buscar el planeta
                 p_mision=None
                 for planeta in self.lista_planetas_csv:
                     if planeta.id==mision["planeta_destino"]:
                         p_mision=planeta
                         p_mision:Planeta_CSV
                 #Buscar Nave
                 n_mision=None
                 for nave in self.lista_naves:
                     if nave.id==mision["nave"]:
                         n_mision=nave
                         n_mision:Nave
                 #Buscar Integrantes
                 i_mision=[]
                 for ids in mision["integrantes"]:
                     for integrante in self.lista_personajes_csv:
                         if ids==integrante.id:
                             i_mision.append(integrante)
                             i_mision:Personaje_CSV
                 #Buscar Armas
                 a_mision=[]
                 for datos in mision["armas"]:
                     for arma in self.lista_armas:
                         if datos==arma.id:
                             a_mision.append(arma)
                             a_mision:Arma

                 #Agregamos a la lista de misiones como objeto de mision
                 self.lista_misiones.append(Mision(nombre_mision,p_mision,n_mision,i_mision,a_mision))
     except:
         archivo=open("guardado_misiones/misiones_guardadas.txt", "w")
         archivo.close()
   
  def crear_mision(self):
      #Bucle While para crear las misiones
      while self.i<=5:
         print(f"-------------------------INICIANDO CREACION DE MISION------------------- \nMisiones Disponibles para crear:{6-self.i}")
         nombre_mision=input("Ingrese el nombre para su mision: ") #Nombre de la mision
         for n in self.lista_planetas_csv:
             n.show_nombre()
         while True:
             try:   #Validador de escojer planeta
                 ingreso_planeta=int(input("Escoja el planeta a donde desea realizar la mision: "))
                 planeta_escogido=self.lista_planetas_csv[ingreso_planeta-1] #Planeta Escogido
                 break
             except:
                 print("Ingrese una opcion valida")

         contador_nave=1
         for n in self.lista_naves:
             print(f"{contador_nave}.-{n.name}")
             contador_nave+=1
         while True:
             try: #Validador de escojer nave
                 ingreso_nave=int(input("Indique el numero de la nave que desea para la mision: "))
                 nave_escogida=self.lista_naves[ingreso_nave-1] #Nave escogida
                 break
             except:
                 print("Ingrese una opcion valida")

         personajes_mision=[]#Lista para personajes de la mision
         contador_personaje=1
         restantes_personajes=7
         print("Lista de personajes")
         for n in self.lista_personajes_csv: #Mostrar los personajes
             print(f"{contador_personaje}.-{n.name}")
             contador_personaje+=1
         while len(personajes_mision)<=7: #Asegurarse de que la lista puede tener maximo 7 personajes
             try:
                 ingreso_personaje=int(input(f"Seleccione los integrantes para su mision (Restantes: {restantes_personajes}) \nIngrese el numero del personaje--> "))
                 personaje_escogido=self.lista_personajes_csv[ingreso_personaje-1]
                 if personaje_escogido in personajes_mision:
                     print(f"{personaje_escogido.name} ya se encuentra en la mision") #Asegurarse de no repetir integrantes
                 else:
                     personajes_mision.append(personaje_escogido) #Agregar personaje a la lista
                     restantes_personajes-=1
                 while True:
                     continuar=input("Desea agregar otro personaje? \nsi \nno \n--> ")
                     if continuar=="si":
                         break
                     elif continuar=="no":
                         break
                     else:
                         print("Ingrese si o no")
                 if continuar=="no":
                     break
             except:
                 print("Ingrese una opcion valida")

         armas_mision=[] #Lista de armas para la mision
         contador_armas=1
         restantes_armas=7
         print("Lista de armas")
         for n in self.lista_armas: #Mostrar armas 
             print(f"{contador_armas}.-{n.name}")
             contador_armas+=1
         while len(armas_mision)<=7: #Asegurarse de cumplir el maximo de 7 armas
             try:
                 ingreso_arma=int(input(f"Seleccione las armas para su mision (Restantes: {restantes_armas}) \nIngrese el numero del arma---> "))
                 arma_escogida=self.lista_armas[ingreso_arma-1]
                 armas_mision.append(arma_escogida) #Agregar el arma, si pueden haber armas repetidas por ser armas
                 restantes_armas-=1
                 while True:
                     continuar=input("Desea agregar otra arma? \nsi \nno \n--> ")
                     if continuar=="si" or continuar=="no":
                         break
                     else:
                         print("Ingrese si o no")
             
                 if continuar=="no":
                     break
             except:
                 print("Ingrese una opcion valida")
         
         self.lista_misiones.append(Mision(nombre_mision,planeta_escogido,nave_escogida,personajes_mision,armas_mision)) #Agregar mision a la lista de misiones
         otra_mision=input("Desea crear una nueva mision? \nsi \nno \n---> ") 
         if otra_mision=="no":
             print("QUE LA FUERZA TE ACOMPAÑE")
             break
         elif otra_mision=="si":
             self.i+=1
         else:
             print("Ingrese si o no")
         

  def modificar_mision(self):
     contador=1
     print("----------------------LISTA DE MISIONES-------------")
     for n in self.lista_misiones: #Mostrar las listas presentes en la base de datos
         print(f"{contador}.Mision {n.nombre} Planeta DEstino-->{n.planeta_destino.name}")
         contador+=1
     print("-----------------------------------------------------")
     seleccion=int(input("Seleccione la mision a modificar: "))
     mision_seleccionada=self.lista_misiones[seleccion-1]
     mision_seleccionada.show_datos()

     while True:
         print("-----------MODIFICANDO LA MISION-------------")
         cambiar=int(input("Que aspecto desea modificar \n1.--->Nombre de la mision \n2.--->Planeta de la mision \n3.--->Nave del planeta \n4.--->Integrantes de la mision \n5.--->Armas de la mision \n---> "))
         
         if cambiar==1: #Opcion para cambiar nombre de la mision
             nuevo_nombre=input("Ingrese el nuevo nombre de la mision: ")
             mision_seleccionada.nombre=nuevo_nombre

         elif cambiar==2: #Opcion para cambiar el planeta de la mision
             for n in self.lista_planetas_csv:
                 n.show_nombre() #Mostrar la lista de planetas
             escoger_planeta=int(input("Ingrese el numero del nuevo planeta destino de la mision: ")) 
             nuevo_planeta=self.lista_planetas_csv[escoger_planeta-1]
             if nuevo_planeta.name==mision_seleccionada.planeta_destino.name: #En caso de que se escoja el mismo planeta
                 print("Ya se tiene ese planeta de destino configurado")
             else:
                 mision_seleccionada.planeta_destino=nuevo_planeta #Cambiar el nuevo planeta

         elif cambiar==3: #Opcion para cambiar la nave
             contador=1
             print("Lista de Naves:")
             for n in self.lista_naves:
                 print(f"{contador}.{n.name}") #Mostrar las naves
                 contador+=1
             escoger_nave=int(input("Ingrese el numero de la nueva nave: ")) #Escoger la nave
             nueva_nave=self.lista_naves[escoger_nave-1]
             if nueva_nave.name==mision_seleccionada.nave.name: #En caso de que se escoja la misma nave
                 print("Ya se tiene esta nave para la mision")
             else:
                 mision_seleccionada.nave=nueva_nave 

         elif cambiar==4: #Opcion para modificar los integrantes
             modificar=int(input("Que accion desea realizar \n1-->Agregar Integrante \n2-->Eliminar Integrante \n3-->Cambiar Integrante \n-->"))
             contador=1
             for n in mision_seleccionada.integrantes: #Mostrar los integrantes de la mision seleccionada
                 print(f"{contador}.{n.name}")
                 contador+=1
             if modificar==1: #En caso de que se desee agregar un nuevo integrante
                 contador_1=1
                 if len(mision_seleccionada.integrantes)<7:
                     print("Lista de Personajes")
                     for n in self.lista_personajes_csv:
                         print(f"{contador_1}.{n.name}") #Mostrar lista de personajes
                         contador_1+=1
                     try:
                         agregar_personaje=int(input("Seleccione el numero del personaje que desea agregar: "))
                         personaje_agregar=self.lista_personajes_csv[agregar_personaje-1]
                         if personaje_agregar in mision_seleccionada.integrantes: #En caso de que ya se tenga el personaje
                             print("Ya se tiene a este integrante en la mision")
                         else:
                             mision_seleccionada.integrantes.append(personaje_agregar)
                     except ValueError:
                         print("Ingrese un numero porfavor") 
                 else:
                     print("Ya tiene el maximo de integrantes posibles") #En caso de que ya se tengan siete integrantes

             elif modificar==2:  #En caso de que se desee eliminar un integrante
                 escoger_eliminar=int(input("Ingrese el numero del personaje que desee eliminar"))
                 mision_seleccionada.integrantes.pop(escoger_eliminar-1)
        
             elif modificar==3:  #En caso de que se desee cambiar un integrante
                 escoger_cambio=int(input("Ingrese el numero del personaje que desea cambiar: "))
                 contador_2=1
                 print("Lista de Personajes")
                 for n in self.lista_personajes_csv: 
                     print(f"{contador_2}.{n.name}")        #Mostrar los personajes
                     contador_2+=1
                 escoger_nuevo=int(input("Ingrese el numero del personaje nuevo para el cambio: "))
                 personaje_cambiar=self.lista_personajes_csv[escoger_nuevo-1]
                 if personaje_cambiar in mision_seleccionada.integrantes:      #En caso de que ya se tenga el personaje en la mision
                     print("Ya se tiene este personaje en la mision")
                 else:
                     mision_seleccionada.integrantes[escoger_cambio-1]=personaje_cambiar
             
         elif cambiar==5:   #Opcion para modificar armas
             modificar=int(input("Que accion desea realizar \n1-->Agregar Arma \n2-->Eliminar Arma \n3-->Cambiar Arma \n-->"))
             contador=1
             for n in mision_seleccionada.armas:  #Mostrar armas de la mision
                 print(f"{contador}.{n.name}")
                 contador+=1

             if modificar==1: #En caso de que se desee agregar un arma
                 contador_1=1
                 if len(mision_seleccionada.armas)<7:
                     print("Lista de Armas")
                     contador_1=1
                     for n in self.lista_armas:   #Mostrar armas
                         print(f"{contador_1}.{n.name}")
                         contador_1+=1
                     escoger_arma=int(input("Seleccione el numero del arma que desea agregar: "))
                     agregar_arma=self.lista_armas[escoger_arma-1]
                     mision_seleccionada.armas.append(agregar_arma)
                 else:
                     print("Ya tiene el maximo de armas posibles")  #En caso de ya tener el limite de armas

             elif modificar==2: #En caso que se desee eliminar un arma
                 escoger_eliminar=int(input("Ingrese el numero del arma que desee eliminar"))
                 mision_seleccionada.armas.pop(escoger_eliminar-1)
        
             elif modificar==3: #En caso de que se desee cambiar un arma
                 escoger_cambio=int(input("Ingrese el numero del arma que desea cambiar: "))
                 contador_2=1
                 for n in self.lista_armas:
                     print(f"{contador_2}.{n.name}")
                     contador_2+=1
                 escoger_nuevo=int(input("Ingrese el numero del arma nueva para el cambio: "))
                 arma_cambiar=self.lista_armas[escoger_nuevo-1]
                 mision_seleccionada.armas[escoger_cambio-1]=arma_cambiar

         continuar=input("Desea modificar otra aspecto de la mision? \nsi \nno \n---> ")
         if continuar=="no":
            break
  
  def visualizar_mision(self):
     print("--------------------------LISTA DE MISIONES----------------------")
     contador=1
     for n in self.lista_misiones:
         print(f"-------------------------MISION {contador}--------------------------")
         n.show_datos()
         contador+=1
     print("-------------------------------------------------------------------------------")
     while True:
         try:
             escoger=int(input("Seleccione la mision que desee visualizar a detalle: "))
             mision_escogida=self.lista_misiones[escoger-1]
             while True:
                 ver=int(input("Que elemento deseas ver a detalle \n1-->Planeta Destino \n2-->Detalle de integrantes \n3-->Detalle Armas \n4-->Detalle Nave \n--> "))
                 if ver==1:
                     mision_escogida.planeta_destino.show_datos()
                     break
                 elif ver==2:
                     for i in mision_escogida.integrantes:
                         i.show_datos()
                     print("-----------------------------------------------------------------------------------------------------")
                     break
                 elif ver==3:
                     for i in mision_escogida.armas:
                         i.show_datos()
                     print("-------------------------------------------------------------------------------------------------------")
                     break
                 elif ver==4:
                     mision_escogida.nave.show_datos()
                     break
                 else:
                         print("ingrese una opcion valida")
             continuar=input("Desea ver de nuevo los detalles de una mision? \nsi \nno \n---> ")
             if continuar=="no":
                 break
         except:
             print("Ingrese una opcion valida")

  def guardar_mision(self):
     lista_dic_misiones=[]
     for n in self.lista_misiones:
         ids_integrantes=[]
         ids_armas=[]
         for i in n.integrantes:
             ids_integrantes.append(i.id)
         for i in n.armas:
             ids_armas.append(i.id)
         diccionario_mision={}
         diccionario_mision["nombre_mision"]=n.nombre
         diccionario_mision["planeta_destino"]=n.planeta_destino.id
         diccionario_mision["nave"]=n.nave.id
         diccionario_mision["integrantes"]=ids_integrantes
         diccionario_mision["armas"]=ids_armas
         lista_dic_misiones.append(diccionario_mision)
    
     with open("guardado_misiones/misiones_guardadas.txt","w") as f:
         f.write(json.dumps(lista_dic_misiones, indent=3))






       

    
    