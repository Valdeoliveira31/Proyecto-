class Personaje_CSV:
    def __init__(self, id, name, species, gender, height, weight, hair_color, eye_color, skin_color, year_born, homeworld, year_died, description):
        self.id=id
        self.name=name
        self.species=species
        self.gender=gender
        self.height=height
        self.weight=weight
        self.hair_color=hair_color
        self.eye_color=eye_color
        self.skin_color=skin_color
        self.year_born=year_born
        self.homeworld=homeworld
        self.year_died=year_died
        self.description=description
    
    def show_nombre(self):
        print(self.name)

    def show_datos(self):
        print(f"""
-----------------------------------DATOS DE {self.name}----------------------------------------
>ID:{self.id}
>Especie:{self.species}
>Genero:{self.gender}     
>Altura:{self.height}    >Peso:{self.weight}
>Color de Pelo:{self.hair_color}    >Color de Ojos:{self.eye_color}     >Color de piel:{self.skin_color}
>Nacimiento:{self.year_born}       >Pais de origen: {self.homeworld}    >Fallecimiento: {self.year_died}
>Descripcion: {self.description}
""")