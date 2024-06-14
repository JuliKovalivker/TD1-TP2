from haversine import haversine, Unit

class CampanaVerde:
    def __init__(self, direccion:str, barrio:str, comuna:int, materiales:set[str], coord:tuple[float,float]):
        ''' completar docstring '''
        self.direccion:str = direccion
        self.barrio:str = barrio
        self.comuna:int = comuna
        self.materiales:set[str] = materiales
        self.latitud:float = coord[0]
        self.longitud:float = coord[1] 

    def distancia(self, lat:float, lng:float) -> float:
        ''' Requiere: Nada
            Devuelve: la distancia entre la CampanaVerde y el punto ingresado medida en metros 
        '''
        punto_campana:tuple[float ,float] = (self.latitud, self.longitud)
        punto_ingresado:tuple[float ,float] = (lat, lng)
        return haversine(punto_campana, punto_ingresado, unit=Unit.METERS)

    def __repr__(self) -> str:
        ''' Requiere: Nada
            Devuelve: La representación como string de la CampanaVerde en el siguiente formato: <dir@mater/iales@barrio>
        '''
        return "<" + self.direccion + "@" + "/".join(self.materiales) + "@" + self.barrio + ">"