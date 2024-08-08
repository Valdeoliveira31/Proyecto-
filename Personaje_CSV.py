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

        