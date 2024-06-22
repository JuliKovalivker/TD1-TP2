import unittest
import csv
from dataset import *
from campana_verde import CampanaVerde

####################################################################

# Tests para el método __init__()
class TestInit(unittest.TestCase):

    # Crear un dataset con ninguna campana verde
    def test_ninguna_campana(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/empty.csv")
        output:list[CampanaVerde] = dataset.campanas_verdes
        expected_output:list[CampanaVerde] = []
        self.assertEqual(output, expected_output)

    # Crear un dataset con 1 campana verde
    def test_una_campana(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/una_campana.csv")
        output:list[CampanaVerde] = dataset.campanas_verdes
        expected_output:list[CampanaVerde] = [CampanaVerde("DIR","BAR",1,{"Papel"}, (1.0, 1.0))]
        self.assertEqual(output, expected_output)
        
    # Crear un dataset con varias campanas verde
    def test_varias_campanas(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        output:list[CampanaVerde] = dataset.campanas_verdes
        expected_campana:CampanaVerde = CampanaVerde("DIR","BAR",1,{"Papel"}, (1.0, 1.0))
        expected_output:list[CampanaVerde] = [expected_campana, expected_campana, expected_campana]
        self.assertEqual(output, expected_output)

####################################################################

# Tests para el método tamano()
class TestTamano(unittest.TestCase):

    # Tamaño de un dataset con ninguna campana verde
    def test_ninguna_campana(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/empty.csv")
        output:int = dataset.tamano()
        expected_output:int = 0
        self.assertEqual(output, expected_output)

    # Tamaño de un dataset con 1 campana verde
    def test_una_campana(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/una_campana.csv")
        output:int = dataset.tamano()
        expected_output:int = 1
        self.assertEqual(output, expected_output)
        
    # Tamaño de un dataset con varias campanas verde
    def test_varias_campanas(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        output:int = dataset.tamano()
        expected_output:int = 3
        self.assertEqual(output, expected_output)

####################################################################

# Tests para el método barrios()
class TestBarrios(unittest.TestCase):

    # Un dataset vacío, sin barrios
    def test_vacio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/empty.csv")
        output:set[str] = dataset.barrios()
        expected_output:set[str] = set()
        self.assertSetEqual(output, expected_output)

    # Varias campanas, todas con el mismo barrio
    def test_mismo_barrio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        output:set[str] = dataset.barrios()
        expected_output:set[str] = {"BAR"}
        self.assertSetEqual(output, expected_output)

    # Todas las campanas pertenecen a barrios distintos
    def test_varios_barrios(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_distintas.csv")
        output:set[str] = dataset.barrios()
        expected_output: set[str] = {"CHACARITA", "BOEDO", "MONTE CASTRO"}
        self.assertSetEqual(output, expected_output)

####################################################################

# Tests para el método campanas_del_barrio()
class TestCampanasDelBarrio(unittest.TestCase):

    # Ninguna CampanaVerde pertenece al barrio
    def test_ninguna_en_barrio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_distintas.csv")
        output:list[CampanaVerde] = dataset.campanas_del_barrio("TEST")
        expected_output:list[CampanaVerde] = []
        self.assertEqual(output, expected_output)

    # Una sola CampanaVerde pertenece al barrio
    def test_una_en_barrio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_distintas.csv")
        output:list[CampanaVerde] = dataset.campanas_del_barrio("CHACARITA")
        expected_output_len:int = 1
        expected_output_barrio:str = "CHACARITA"
        self.assertEqual(len(output), expected_output_len)
        self.assertEqual(output[0].barrio, expected_output_barrio)

    # Varias CampanaVerde pertenecen al barrio
    def test_varias_en_barrio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        output:set[str] = dataset.campanas_del_barrio("BAR")
        expected_output_len:int = 3
        expected_output_barrio:str = "BAR"
        self.assertEqual(len(output), expected_output_len)
        for campana in output:
            self.assertEqual(campana.barrio, expected_output_barrio)

####################################################################

# Tests para el método cantidad_por_barrio()
class TestCantidadPorBarrio(unittest.TestCase):
    
    # El material no se puede depositar en ningún barrio
    def test_ningun_barrio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        output:dict[str, int] = dataset.cantidad_por_barrio("Cartón")
        expected_output:dict[str, int] = {}
        self.assertDictEqual(output, expected_output)

    # El material se puede depositar en 1 campana en un solo barrio
    def test_una_campana_un_barrio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_distintas.csv")
        output:dict[str, int] = dataset.cantidad_por_barrio("Cartón")
        expected_output:dict[str, int] = {"CHACARITA": 1}
        self.assertDictEqual(output, expected_output)

    # El material se puede depositar en varias campanas en un solo barrio
    def test_varias_campana_un_barrio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        output:dict[str, int] = dataset.cantidad_por_barrio("Papel")
        expected_output:dict[str, int] = {"BAR": 3}
        self.assertDictEqual(output, expected_output)

    # El material se puede depositar en una campana en varios barrios
    def test_una_campana_varios_barrio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_distintas.csv")
        output:dict[str, int] = dataset.cantidad_por_barrio("Papel")
        expected_output:dict[str, int] = {"CHACARITA": 1, "BOEDO": 1, "MONTE CASTRO": 1}
        self.assertDictEqual(output, expected_output)

    # El material se puede depositar en varias campanas en varios barrios
    def test_varias_campana_varios_barrio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_mismos_materiales.csv")
        output:dict[str, int] = dataset.cantidad_por_barrio("Papel")
        expected_output:dict[str, int] = {"CHACARITA": 2, "BOEDO": 2}
        self.assertDictEqual(output, expected_output)

####################################################################

# Tests para el método tres_campanas_cercanas()
class TestTresCampanasCercanas(unittest.TestCase):
    
    # Las tres campanas más cercanas de un dataset con solo 3 campanas
    def test_tres_campanas(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        output:tuple[CampanaVerde, CampanaVerde, CampanaVerde] = dataset.tres_campanas_cercanas(0.0,0.0)
        expected_campana:CampanaVerde = CampanaVerde("DIR","BAR",1,{"Papel"}, (1.0, 1.0))
        expected_output:tuple[CampanaVerde, CampanaVerde, CampanaVerde] = (expected_campana, expected_campana, expected_campana)
        self.assertEqual(output, expected_output)

    # Tres CampanaVerdes en un mismo punto, y una en otro más cerca.
    def test_una_mas_cerca(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/distancia_una_mas_cerca.csv")
        output:tuple[CampanaVerde, CampanaVerde, CampanaVerde] = dataset.tres_campanas_cercanas(0.0,0.0)
        expected_closest:CampanaVerde = CampanaVerde("DIR","BAR",1,{"Papel"}, (0.5, 0.5)) # La campana más cercana
        self.assertIn(expected_closest, output)

    # Varias CampanasVerdes en distintos puntos y una en el mismo que se pide.
    def test_una_en_el_punto(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/distancias_distintas.csv")
        output:tuple[CampanaVerde, CampanaVerde, CampanaVerde] = dataset.tres_campanas_cercanas(0.2,0.2)
        output_distancias:tuple[float, float, float] = (output[0].distancia(0.2, 0.2), output[1].distancia(0.2, 0.2), output[2].distancia(0.2, 0.2))
        expected_distancia_cercana:float = 0.0
        self.assertIn(expected_distancia_cercana, output_distancias)
        
####################################################################

# Tests para el método exportar_por_materiales()
class TestExportarPorMateriales(unittest.TestCase):

    # Exportar por un material que no se puede depositar en ninguna CampanaVerde
    def test_export_ninguno(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        dataset.exportar_por_materiales("test", {"Legos"})
        f = open("test.csv", encoding='UTF-8')
        output:list[dict[str, str]] = list(csv.DictReader(f, delimiter=";"))
        f.close()
        expected_output:list[dict[str, str]] = []
        self.assertEqual(output, expected_output)

    # Exportar por material en un dataset vacio
    def test_export_vacio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/empty.csv")
        dataset.exportar_por_materiales("test", {"Papel"})
        f = open("test.csv", encoding='UTF-8')
        output:list[dict[str, str]] = list(csv.DictReader(f, delimiter=";"))
        f.close()
        expected_output:list[dict[str, str]] = []
        self.assertEqual(output, expected_output)

    # Exportar por un material que tengan todas las CampanaVerde
    def test_todas(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        dataset.exportar_por_materiales("test", {"Papel"})
        f = open("test.csv", encoding='UTF-8')
        output:list[dict[str, str]] = list(csv.DictReader(f, delimiter=";"))
        f.close()
        expected_data:dict[str, str] = {"DIRECCION": "DIR", "BARRIO": "BAR"}
        expected_output:list[dict[str, str]] = [expected_data, expected_data, expected_data]
        self.assertEqual(output, expected_output)

    # Exportar por un material que tenga solamente 1 CampanaVerde
    def test_una_sola(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_distintas.csv")
        dataset.exportar_por_materiales("test", {"Ladrillo"})
        f = open("test.csv", encoding='UTF-8')
        output:list[dict[str, str]] = list(csv.DictReader(f, delimiter=";"))
        f.close()
        expected_output:list[dict[str, str]] = [{"DIRECCION": "DIR", "BARRIO": "BOEDO"}]
        self.assertEqual(output, expected_output)

####################################################################
##################### FUNCIONES AUXILIARES #########################
####################################################################

# Tests para la función WKTaCoordenadas()
class TestWKTaCoordenadas(unittest.TestCase):

    # Latitud y longitud tienen solamente 1 punto decimal
    def test_un_decimal(self):
        output:tuple[float, float] = WKTaCoordenadas("POINT (0.0 0.0)")
        expected_output:tuple[float, float] = (0.0, 0.0)
        self.assertEqual(output, expected_output)

    # Latitud y longitud son números negativos
    def test_negativos(self):
        output:tuple[float, float] = WKTaCoordenadas("POINT (-5.0 -5.0)")
        expected_output:tuple[float, float] = (-5.0, -5.0)
        self.assertEqual(output, expected_output)

    # Uno es negativo y el otro no
    def test_uno_negativo(self):
        output:tuple[float, float] = WKTaCoordenadas("POINT (5.0 -5.0)")
        expected_output:tuple[float, float] = (5.0, -5.0)
        self.assertEqual(output, expected_output)

    # Latitud y longitud son números distintos
    def test_distintos(self):
        output:tuple[float, float] = WKTaCoordenadas("POINT (2.22 1.982)")
        expected_output:tuple[float, float] = (2.22, 1.982)
        self.assertEqual(output, expected_output)

####################################################################

# Tests para la función sortTresCampanas()
class TestSortTresCampanas(unittest.TestCase):

    # Una lista que ya está ordenada
    def test_ordenada(self):
        c1:CampanaVerde = CampanaVerde("D1","B", 1, set(), (1.0, 1.0))
        c2:CampanaVerde = CampanaVerde("D2","B", 1, set(), (2.0, 2.0))
        c3:CampanaVerde = CampanaVerde("D3","B", 1, set(), (3.0, 3.0))
        xs:list[CampanaVerde] = [c1, c2, c3]
        sortTresCampanas(xs, 0.0, 0.0)
        expected_output:list[CampanaVerde] = [c1, c2, c3]
        self.assertListEqual(xs, expected_output)

    # Una lista ordenada de mayor a menor
    def test_mayor_a_menor(self):
        c3:CampanaVerde = CampanaVerde("D3","B", 1, set(), (3.0, 3.0))
        c2:CampanaVerde = CampanaVerde("D2","B", 1, set(), (2.0, 2.0))
        c1:CampanaVerde = CampanaVerde("D1","B", 1, set(), (1.0, 1.0))
        xs:list[CampanaVerde] = [c3, c2, c1]
        sortTresCampanas(xs, 0.0, 0.0)
        expected_output = [c1, c2, c3]
        self.assertListEqual(xs, expected_output)

    # Una lista en el que el menor está en el medio
    def test_medio(self):
        c2:CampanaVerde = CampanaVerde("D2","B", 1, set(), (2.0, 2.0))
        c1:CampanaVerde = CampanaVerde("D1","B", 1, set(), (1.0, 1.0))
        c3:CampanaVerde = CampanaVerde("D3","B", 1, set(), (3.0, 3.0))
        xs:list[CampanaVerde] = [c2, c1, c3]
        sortTresCampanas(xs, 0.0, 0.0)
        expected_output:list[CampanaVerde] = [c1, c2, c3]
        self.assertListEqual(xs, expected_output)

####################################################################

# Tests para la función estaEnSet()
class TestEstaEnSet(unittest.TestCase):

    # set1 y set2 son iguales
    def test_iguales(self):
        set1:set[str] = {"P", "C"}
        set2:set[str] = {"P", "C"}
        output:bool = estaEnSet(set1, set2)
        expected_output:bool = True
        self.assertEqual(output, expected_output)

    # set1 y set2 están vacíos
    def test_vacios(self):
        set1:set[str] = set()
        set2:set[str] = set()
        output:bool = estaEnSet(set1, set2)
        expected_output:bool = True
        self.assertEqual(output, expected_output)

    # set1 y set2 están vacíos
    def test_vacios(self):
        set1:set[str] = set()
        set2:set[str] = set()
        output:bool = estaEnSet(set1, set2)
        expected_output:bool = True
        self.assertEqual(output, expected_output)

unittest.main()