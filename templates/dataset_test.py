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

unittest.main()
