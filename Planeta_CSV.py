class Planeta_CSV:
    def __init__(self, id, name, population, climate, residents, films):
        self.id=id
        self.name=name
        self.population=population
        self.climate=climate
        self.residents=residents
        self.films=films

    def show_nombre(self):
        print(f"{self.id}.{self.name}")
    
    def show_datos(self):
        print(f"""
------------------Datos del planeta {self.name}--------------------
>ID:{self.id}
>Poblacion:{self.population} habitantes
>Clima:{self.climate}
>Residentes:{self.residents}
>Episodios en los que aparece:{self.films}
--------------------------------------------------------------------
""")