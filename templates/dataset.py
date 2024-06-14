import csv
from campana_verde import CampanaVerde

def WKTaCoordenadas(WKT:str) -> tuple[float,float]:
    '''Requiere: WKT esté en el siguiente formato, donde "lat" y "lon" representan números decimales: "POINT (lat lon)".
       Devuelve: "lat" y "lon" convertidos a float en una tupla, en ese órden.
    '''
    xs_WKT:list[str] = WKT[7:-1].split(' ')
    return (float(xs_WKT[0]), float(xs_WKT[1]))

class DataSetCampanasVerdes:
    def __init__(self, archivo_csv:str):
        ''' completar docstring '''
        self.campanas_verdes:list[CampanaVerde] = []
        self.cantidad:int = 0

        f = open(archivo_csv)
        for c in csv.DictReader(f, delimiter=";"):
            campana:CampanaVerde = CampanaVerde(
                c["direccion"],
                c["barrio"],
                int(c["comuna"]),
                set(c["materiales"].split(' / ')),
    	        WKTaCoordenadas(c["WKT"])
            )
            self.campanas_verdes.append(campana)
            self.tamano += 1
        f.close()

    def tamano(self) -> int:
        ''' Requiere: Nada
            Devuelve: La cantidad de campanas verdes en el dataset d.
        '''
        return self.cantidad

    def barrios(self) -> set[str]:
        ''' Requiere: Nada
            Devuelve: El conjunto de todos los barrios existentes en el dataset d.
        '''
        barrios:set[str] = set()
        for campana in self.campanas_verdes:
            barrios.add(campana.barrio)
        return barrios 

    def campanas_del_barrio(self, barrio:str) -> list[CampanaVerde]:
        ''' Requiere: El nombre del barrio no tenga tilde
            Devuelve: Las instancias de CampanaVerde del dataset correspondientes al barrio indicado.
        '''
        barrio = barrio.upper()
        campanas_barrio:list[CampanaVerde] = []
        for campana in self.campanas_verdes:
            if campana.barrio == barrio:
                campanas_barrio.append(campana)
        return campanas_barrio

    def cantidad_por_barrio(self, material:str) -> dict[str, int]:
        ''' Requiere: La primera letra en mayúscula, y se usen tildes.
            Devuelve: La cantidad de campanas verdes en cada barrio en las que se puede depositar el material indicado.
        '''
        vr:dict[str,int] = {}
        for campana in self.campanas_verdes:
            if campana.barrio in vr:
                vr[campana.barrio] += 1
            else:
                vr[campana.barrio] = 1
        return vr

    def tres_campanas_cercanas(self, lat:float, lng:float) -> tuple[CampanaVerde, CampanaVerde, CampanaVerde]:
        ''' Requiere: Nada
            Devuelve: Las tres campanas verdes más cercanas al punto ingresado
        '''
        mas_cercanas:list[CampanaVerde] = []
        for campana in self.campanas_verdes:
            pass


    # def exportar_por_materiales(...) -> ...:
    #     ''' completar docstring '''
    #     pass

# c = DataSetCampanasVerdes("../campanas-verdes.csv")