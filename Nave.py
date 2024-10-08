class Nave:
    def __init__(self, id,name,model,manufacturer,cost_in_credits,length,max_atmosphering_speed,crew,passengers,cargo_capacity,consumables,hyperdrive_rating,MGLT,starship_class,pilots,films):
        self.id=id
        self.name=name
        self.model=model
        self.manufacturer=manufacturer
        self.cost_int_credits=cost_in_credits
        self.length=length
        self.max_atmosphering_speed=max_atmosphering_speed
        self.crew=crew
        self.passengers=passengers
        self.cargo_capacity=cargo_capacity
        self.consumables=consumables
        self.hyperdrive_rating=hyperdrive_rating
        self.MGLT=MGLT
        self.starship_class=starship_class
        self.pilots=pilots
        self.films=films

    def show_nombre(self):
        print(self.name)

    def show_datos(self):
        print(f"""
-------------DETALLES DE LA NAVE {self.name}-------------------------------------
>ID: {self.id}
>Modelo:{self.model}      >Fabricante:{self.manufacturer}
>Cost in Credits:{self.cost_int_credits}
>Longitud:{self.length}   >Maxima velocidad atmosferica:{self.max_atmosphering_speed}
>Tripulacion en Episodios:{self.crew}    >Pasajeros en episodios:{self.passengers}
>Capacidad de Carga:{self.cargo_capacity}    >Consumibles:{self.consumables}
>Hyperdrive Rating:{self.hyperdrive_rating}    <MGLT:{self.MGLT}
>Clase: {self.starship_class}   >Pilotos en episodios:{self.pilots}
>Episodios de aparicion:{self.films}
""")