import unittest
from dataset import DataSetCampanasVerdes
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

        expected_campana = CampanaVerde("DIR","BAR",1,{"Papel"}, (1.0, 1.0))
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
    
    # Las tres campanas más cercanas de un dataset vacío
    def test_vacio(self):
        dataset:DataSetCampanasVerdes = DataSetCampanasVerdes("./dataset_test_files/varias_campanas_iguales.csv")
        output:tuple[CampanaVerde, CampanaVerde, CampanaVerde] = dataset.tres_campanas_cercanas(0.0,0.0)
        print(output)

unittest.main()