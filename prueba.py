import pandas as pd
from  Planeta_CSV import Planeta_CSV
from Nave import Nave
from Arma import Arma
from Personaje_CSV import Personaje_CSV
from Mision import Mision
import json



lista_planetas=[]
lista_naves=[]
lista_armas=[]
lista_personajes=[]
lista_misiones=[]

def cargar_datos():
      #Agregar planetas a la lista
      planetas=pd.read_csv("csv/planets.csv") #Lectura del Csv de los planetas
      planetas=planetas.drop_duplicates(subset=["name"]) #Eliminar Duplicados
      for index, planeta in planetas.iterrows():   #Bucle para recorrer cada fila y cada atributo
         lista_planetas.append(Planeta_CSV(planeta["id"],planeta["name"],planeta["population"],planeta["climate"],planeta["residents"],planeta["films"]))
      
      #Agregar Naves a la lista
      naves=pd.read_csv("csv/starships.csv") #Lectura del Csv de las naves
      naves=naves.drop_duplicates(subset=["name"]) #Eliminar repetidos
      for index,nave in naves.iterrows():
         lista_naves.append(Nave(nave["id"],nave["name"],nave["model"],nave["manufacturer"],nave["cost_in_credits"],nave["length"],nave["max_atmosphering_speed"],nave["crew"],nave["passengers"],nave["cargo_capacity"],nave["consumables"],nave["hyperdrive_rating"],nave["MGLT"],nave["starship_class"],nave["pilots"],nave["films"]))
     
      #Agregar armas a la lista
      armas=pd.read_csv("csv/weapons.csv") #Lectura del Csv de las armas
      armas=armas.drop_duplicates(subset=["name"]) #Eliminar repetidos
      for index,arma in armas.iterrows():
         lista_armas.append(Arma(arma["id"],arma["name"],arma["model"],arma["manufacturer"],arma["cost_in_credits"],arma["length"],arma["type"],arma["description"],arma["films"]))
      
      #Agregar personajes a la lista
      personajes=pd.read_csv("csv/characters.csv") #Lectura del Csv de los personajes
      personajes=personajes.drop_duplicates(subset=["name"])  #Eliminar repetidos
      for index,per in personajes.iterrows():
         lista_personajes.append(Personaje_CSV(per["id"],per["name"],per["species"],per["gender"],per["height"],per["weight"],per["hair_color"],per["eye_color"],per["skin_color"],per["year_born"],per["homeworld"],per["year_died"],per["description"]))

cargar_datos()

def cargar_mision():
     try:
         with open("guardado_misiones/misiones_guardadas.txt","r") as f:
             lista_de_dict_misiones=json.loads(f.read())
             for mision in lista_de_dict_misiones:
                 #Se agarra el nombre
                 nombre_mision=mision["nombre_mision"]
                 #Buscar el planeta
                 p_mision=None
                 for planeta in lista_planetas:
                     if planeta.id==mision["planeta_destino"]:
                         p_mision=planeta
                         p_mision:Planeta_CSV
                 #Buscar Nave
                 n_mision=None
                 for nave in lista_naves:
                     if nave.id==mision["nave"]:
                         n_mision=nave
                         n_mision:Nave
                 #Buscar Integrantes
                 i_mision=[]
                 for ids in mision["integrantes"]:
                     for integrante in lista_personajes:
                         if ids==integrante.id:
                             i_mision.append(integrante)
                             i_mision:Personaje_CSV
                 #Buscar Armas
                 a_mision=[]
                 for datos in mision["armas"]:
                     for arma in lista_armas:
                         if datos==arma.id:
                             a_mision.append(arma)
                             a_mision:Arma

                 #Agregamos a la lista de misiones como objeto de mision
                 lista_misiones.append(Mision(nombre_mision,p_mision,n_mision,i_mision,a_mision))
     except:
         archivo=open("guardado_misiones/misiones_guardadas.txt", "w")
         archivo.close()
             
             
cargar_mision()

def crear_mision():
      #Bucle While para crear las misiones
      i=1
      while i<=5:
         print(f"-------------------------INICIANDO CREACION DE MISION------------------- \nMisiones Disponibles para crear:{6-i}")
         nombre_mision=input("Ingrese el nombre para su mision: ") #Nombre de la mision
         for n in lista_planetas:
             n.show_nombre()
         ingreso_planeta=int(input("Escoja el planeta a donde desea realizar la mision: "))
         planeta_escogido=lista_planetas[ingreso_planeta-1] #Planeta Escogido

         contador_nave=1
         for n in lista_naves:
             print(f"{contador_nave}.-{n.name}")
             contador_nave+=1
         ingreso_nave=int(input("Indique el numero de la nave que desea para la mision: "))
         nave_escogida=lista_naves[ingreso_nave-1] #Nave escogida

         personajes_mision=[]#Lista para personajes de la mision
         contador_personaje=1
         restantes_personajes=7
         print("Lista de personajes")
         for n in lista_personajes: #Mostrar los personajes
             print(f"{contador_personaje}.-{n.name}")
             contador_personaje+=1
         while len(personajes_mision)<=7: #Asegurarse de que la lista puede tener maximo 7 personajes
             ingreso_personaje=int(input(f"Seleccione los integrantes para su mision (Restantes: {restantes_personajes}) \nIngrese el numero del personaje--> "))
             personaje_escogido=lista_personajes[ingreso_personaje-1]
             if personaje_escogido in personajes_mision:
                 print(f"{personaje_escogido.name} ya se encuentra en la mision") #Asegurarse de no repetir integrantes
             else:
                 personajes_mision.append(personaje_escogido) #Agregar personaje a la lista
                 continuar=input("Desea agregar otro personaje? \nsi \nno \n--> ")
                 restantes_personajes-=1
            
             if continuar=="no":
                 break

         armas_mision=[] #Lista de armas para la mision
         contador_armas=1
         restantes_armas=7
         print("Lista de armas")
         for n in lista_armas: #Mostrar armas 
             print(f"{contador_armas}.-{n.name}")
             contador_armas+=1
         while len(armas_mision)<=7: #Asegurarse de cumplir el maximo de 7 armas
             ingreso_arma=int(input(f"Seleccione las armas para su mision (Restantes: {restantes_armas}) \nIngrese el numero del arma---> "))
             arma_escogida=lista_armas[ingreso_arma-1]
             armas_mision.append(arma_escogida) #Agregar el arma, si pueden haber armas repetidas por ser armas
             continuar=input("Desea agregar otra arma? \nsi \nno \n--> ")
             restantes_armas-=1
             if continuar=="no":
                 break
         
         lista_misiones.append(Mision(nombre_mision,planeta_escogido,nave_escogida,personajes_mision,armas_mision)) #Agregar mision a la lista de misiones

         otra_mision=input("Desea crear una nueva mision? \nsi \nno \n---> ") 
         if otra_mision=="no":
             print("QUE LA FUERZA TE ACOMPAÑE")
             break
         else:
             i+=1

crear_mision()

def modificar_mision():
     contador=1
     print("----------------------LISTA DE MISIONES-------------")
     for n in lista_misiones: #Mostrar las listas presentes en la base de datos
         print(f"{contador}.Mision {n.nombre} Planeta DEstino-->{n.planeta_destino.name}")
         contador+=1
     print("-----------------------------------------------------")
     seleccion=int(input("Seleccione la mision a modificar: "))
     mision_seleccionada=lista_misiones[seleccion-1]
     mision_seleccionada.show_datos()

     while True:
         print("-----------MODIFICANDO LA MISION-------------")
         cambiar=int(input("Que aspecto desea modificar \n1.--->Nombre de la mision \n2.--->Planeta de la mision \n3.--->Nave del planeta \n4.--->Integrantes de la mision \n5.--->Armas de la mision \n---> "))
         
         if cambiar==1: #Opcion para cambiar nombre de la mision
             nuevo_nombre=input("Ingrese el nuevo nombre de la mision: ")
             mision_seleccionada.nombre=nuevo_nombre

         elif cambiar==2: #Opcion para cambiar el planeta de la mision
             for n in lista_planetas:
                 n.show_nombre() #Mostrar la lista de planetas
             escoger_planeta=int(input("Ingrese el numero del nuevo planeta destino de la mision: ")) 
             nuevo_planeta=lista_planetas[escoger_planeta-1]
             if nuevo_planeta.name==mision_seleccionada.planeta_destino.name: #En caso de que se escoja el mismo planeta
                 print("Ya se tiene ese planeta de destino configurado")
             else:
                 mision_seleccionada.planeta_destino=nuevo_planeta #Cambiar el nuevo planeta

         elif cambiar==3: #Opcion para cambiar la nave
             contador=1
             print("Lista de Naves:")
             for n in lista_naves:
                 print(f"{contador}.{n.name}") #Mostrar las naves
                 contador+=1
             escoger_nave=int(input("Ingrese el numero de la nueva nave: ")) #Escoger la nave
             nueva_nave=lista_naves[escoger_nave-1]
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
                     for n in lista_personajes:
                         print(f"{contador_1}.{n.name}") #Mostrar lista de personajes
                         contador_1+=1
                     try:
                         agregar_personaje=int(input("Seleccione el numero del personaje que desea agregar: "))
                         personaje_agregar=lista_personajes[agregar_personaje-1]
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
                 for n in lista_personajes: 
                     print(f"{contador_2}.{n.name}")        #Mostrar los personajes
                     contador_2+=1
                 escoger_nuevo=int(input("Ingrese el numero del personaje nuevo para el cambio: "))
                 personaje_cambiar=lista_personajes[escoger_nuevo-1]
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
                     for n in lista_armas:   #Mostrar armas
                         print(f"{contador_1}.{n.name}")
                         contador_1+=1
                     escoger_arma=int(input("Seleccione el numero del arma que desea agregar: "))
                     agregar_arma=lista_armas[escoger_arma-1]
                     mision_seleccionada.armas.append(agregar_arma)
                 else:
                     print("Ya tiene el maximo de armas posibles")  #En caso de ya tener el limite de armas

             elif modificar==2: #En caso que se desee eliminar un arma
                 escoger_eliminar=int(input("Ingrese el numero del arma que desee eliminar"))
                 mision_seleccionada.armas.pop(escoger_eliminar-1)
        
             elif modificar==3: #En caso de que se desee cambiar un arma
                 escoger_cambio=int(input("Ingrese el numero del arma que desea cambiar: "))
                 contador_2=1
                 for n in lista_armas:
                     print(f"{contador_2}.{n.name}")
                     contador_2+=1
                 escoger_nuevo=int(input("Ingrese el numero del arma nueva para el cambio: "))
                 arma_cambiar=lista_personajes[escoger_nuevo-1]
                 mision_seleccionada.integrantes[escoger_cambio-1]=arma_cambiar

         continuar=input("Desea modificar otra aspecto de la mision? \nsi \nno \n---> ")
         if continuar=="no":
            break

modificar_mision()

def visualizar_mision():
     print("--------------------------LISTA DE MISIONES----------------------")
     contador=1
     for n in lista_misiones:
         print(f"-------------------------MISION {contador}--------------------------")
         n.show_datos()
         contador+=1
     print("-------------------------------------------------------------------------------")

visualizar_mision()

def guardar_mision():
     lista_dic_misiones=[]
     for n in lista_misiones:
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

guardar_mision()
