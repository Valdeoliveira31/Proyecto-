class Arma:
    def __init__(self,id,name,model,manufacturer,cost_in_credits,length,type,description,films):
        self.id=id
        self.name=name
        self.model=model
        self.manufacturer=manufacturer
        self.cost_in_credits=cost_in_credits
        self.length=length
        self.type=type
        self.description=description
        self.films=films

    def show_nombre(self):
        print(self.name)
    
    def show_datos(self):
        print(f"""
-----------------------------------DATOS DE {self.name}----------------------------------------
>ID:{self.id}
>Modelo:{self.model}
>Fabricante:{self.manufacturer}
>Cost in Credits: {self.cost_in_credits}
>Longitud:{self.length}    >Tipo:{self.type}
>Descripcion:{self.description}
>Episodios de aparicion:{self.films}
""")
    