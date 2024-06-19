import unittest
from campana_verde import CampanaVerde
from haversine import haversine, Unit

class TestInit(unittest.TestCase):
    # Test crear una campana normal
    def test_crear_campana(self):
        output:CampanaVerde = CampanaVerde("AGUIRRE 1447","CHACARITA", 15, {"PAPEL", "CARTON"}, (-58.4, -34.5))
        self.assertEqual(output.direccion, "AGUIRRE 1447")
        self.assertEqual(output.barrio, "CHACARITA")
        self.assertEqual(output.comuna, 15)
        self.assertEqual(output.materiales, {"PAPEL", "CARTON"})
        self.assertAlmostEqual(output.latitud, -58.4)
        self.assertAlmostEqual(output.longitud, -34.5)

    # Test crear una sin materiales
    def test_sin_materiales(self):
        output:CampanaVerde = CampanaVerde("AGUIRRE 1447","CHACARITA", 15, set(), (-58.4, -34.5))
        self.assertEqual(output.materiales, set())

class TestDistancia(unittest.TestCase):
    # Test punto y campana están en la misma coordenada
    def test_distancia_cero(self):
        campana:CampanaVerde = CampanaVerde("","", 1, {"PAPEL"}, (0.0, 0.0))

        output:float = campana.distancia(0.0,0.0)
        expected_output:float = 0.0
        self.assertAlmostEqual(output, expected_output)

    # Test punto tiene coordenadas negativa, y campana positiva
    def test_coord_negativa(self):
        campana:CampanaVerde = CampanaVerde("","", 1, {"PAPEL"}, (1.0, 1.0))

        output:float = campana.distancia(-1.0,-1.0)
        expected_output:float = haversine((-1.0, -1.0), (1.0, 1.0), unit=Unit.METERS)
        self.assertAlmostEqual(output, expected_output)


unittest.main()