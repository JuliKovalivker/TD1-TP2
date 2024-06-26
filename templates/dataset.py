import csv
from campana_verde import CampanaVerde

def WKTaCoordenadas(WKT:str) -> tuple[float,float]:
    '''Requiere: WKT esté en el siguiente formato, donde "lat" y "lon" representan números decimales: "POINT (lat lon)".
       Devuelve: "lat" y "lon" convertidos a float, en una tupla, en ese órden.
    '''
    xs_WKT:list[str] = WKT[7:-1].split(' ') # -> Esta línea lo convierte al siguiente formáto: ["lat", "lon"]
    return (float(xs_WKT[0]), float(xs_WKT[1]))

def sortTresCampanas(xs:list[CampanaVerde], lat: float, lng: float) -> None:
    '''Requiere: len(xs) sea 3.
       Devuelve: Nada.
       Modifica: xs de tal manera que ordena las campanas de menor a mayor con respecto a su distancia de la coord ingresada.
    '''
    for _ in range(2):
        for j in range(2):
            if xs[j].distancia(lat, lng) > xs[j+1].distancia(lat, lng):
                (xs[j], xs[j+1]) = (xs[j+1], xs[j])

def estaEnSet(set1: set[str], set2: set[str]) -> bool:
    '''Requiere: Nada.
       Devuelve: True si todos los elementos de set1 se encuentran en set2. False si no.
    '''
    return len(set1 - set2) == 0

class DataSetCampanasVerdes:
    def __init__(self, archivo_csv:str) -> None:
        ''' Requiere: archivo_csv exista y sea del tipo .csv.
                      Debe contar con las siguientes columnas: WKT;direccion;barrio;comuna;materiales
                      Los datos en la columna WKT deben estar en el siguiente formato, donde "lat" y "lon" representan números decimales: "POINT (lat lon)".
                      Los datos en la columna materiales deben estar en el siguiente formato, donde "mat1" y "mat2" representan texto plano: "mat1 / mat2"
            Devuelve: Nada.
        '''
        self.campanas_verdes:list[CampanaVerde] = []
        self.cantidad:int = 0

        f = open(archivo_csv, encoding='utf8')
        for c in csv.DictReader(f, delimiter=";"):
            campana:CampanaVerde = CampanaVerde(
                c["direccion"],
                c["barrio"],
                int(c["comuna"]),
                set(c["materiales"].split(' / ')),
    	        WKTaCoordenadas(c["WKT"])
            )
            self.campanas_verdes.append(campana)
            self.cantidad += 1
        f.close()

    def tamano(self) -> int:
        ''' Requiere: Nada.
            Devuelve: La cantidad de campanas verdes en el dataset d.
        '''
        return self.cantidad

    def barrios(self) -> set[str]:
        ''' Requiere: Nada.
            Devuelve: El conjunto de todos los barrios existentes en el dataset d.
        '''
        barrios:set[str] = set()
        for campana in self.campanas_verdes:
            barrios.add(campana.barrio)
        return barrios 

    def campanas_del_barrio(self, barrio:str) -> list[CampanaVerde]:
        ''' Requiere: El nombre del barrio esté en el mismo formato que en el archivo .csv ingresado.
            Devuelve: Las instancias de CampanaVerde del dataset correspondientes al barrio indicado.
        '''
        campanas_barrio:list[CampanaVerde] = []
        for campana in self.campanas_verdes:
            if campana.barrio == barrio:
                campanas_barrio.append(campana)
        return campanas_barrio

    def cantidad_por_barrio(self, material:str) -> dict[str, int]:
        ''' Requiere: El nombre del material esté en el mismo formato que en el archivo .csv ingresado.
            Devuelve: La cantidad de campanas verdes en cada barrio en las que se puede depositar el material indicado.
        '''
        vr:dict[str,int] = {}
        for campana in self.campanas_verdes:
            if material in campana.materiales:
                if campana.barrio in vr:
                    vr[campana.barrio] += 1
                else:
                    vr[campana.barrio] = 1
        return vr

    def tres_campanas_cercanas(self, lat:float, lng:float) -> tuple[CampanaVerde, CampanaVerde, CampanaVerde]:
        ''' Requiere: self.tamano() >= 3.
            Devuelve: Las tres campanas verdes más cercanas al punto ingresado.
        '''
        tres_mas_cercanas:list[CampanaVerde] = [self.campanas_verdes[0], self.campanas_verdes[1], self.campanas_verdes[2]]
        sortTresCampanas(tres_mas_cercanas, lat, lng)
        for campana in self.campanas_verdes[3:]:
            if campana.distancia(lat, lng) < tres_mas_cercanas[2].distancia(lat, lng):
                tres_mas_cercanas.pop()
                tres_mas_cercanas.append(campana)
                sortTresCampanas(tres_mas_cercanas, lat, lng)
        return tuple(tres_mas_cercanas)

    def exportar_por_materiales(self, archivo_csv:str, materiales:set[str]) -> None:
        '''Requiere: Nada.
           Devuelve: Nada.
           Modifica: Si es que existe previamente un archivo bajo el nombre archivo_csv, se sobreescribe por 
                     la cantidad de campanas verdes en las que se pueda depositar todos los materiales del 
                     conjunto materiales según dirección y barrio.
        '''
        f = open(archivo_csv + ".csv", mode='w', encoding='UTF-8')
        f.write(';'.join(['DIRECCION','BARRIO']) + '\n')
        for campana in self.campanas_verdes:
            if estaEnSet(materiales, campana.materiales):
                f.write(';'.join([campana.direccion, campana.barrio])+ '\n')
        f.close()