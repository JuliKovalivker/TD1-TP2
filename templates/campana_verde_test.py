import unittest
from campana_verde import CampanaVerde
from haversine import haversine, Unit

#############################################################################################
# Tests para el método __init__()
class TestInit(unittest.TestCase):

    # Crear una campana estándar y verificar sus atributos
    def test_crear_campana(self):
        output:CampanaVerde = CampanaVerde("AGUIRRE 1447","CHACARITA", 15, {"PAPEL", "CARTON"}, (-58.4, -34.5))
        self.assertEqual(output.direccion, "AGUIRRE 1447")
        self.assertEqual(output.barrio, "CHACARITA")
        self.assertEqual(output.comuna, 15)
        self.assertEqual(output.materiales, {"PAPEL", "CARTON"})
        self.assertAlmostEqual(output.latitud, -58.4)
        self.assertAlmostEqual(output.longitud, -34.5)

    # Crear una campana sin materiales
    def test_sin_materiales(self):
        output:CampanaVerde = CampanaVerde("AGUIRRE 1447","CHACARITA", 15, set(), (-58.4, -34.5))
        self.assertEqual(output.materiales, set())

#############################################################################################
# Tests para el método distancia()
class TestDistancia(unittest.TestCase):

    # Punto y campana están en la misma coordenada
    def test_distancia_cero(self):
        campana:CampanaVerde = CampanaVerde("","", 1, {"PAPEL"}, (0.0, 0.0))

        output:float = campana.distancia(0.0,0.0)
        expected_output:float = 0.0
        self.assertAlmostEqual(output, expected_output)

    # Un solo punto es igual, el otro es distinto
    def test_uno_igual(self):
        campana:CampanaVerde = CampanaVerde("","", 1, {"PAPEL"}, (0.0, 0.0))

        output:float = campana.distancia(1.0,0.0)
        expected_output:float = haversine((1.0, 0.0), (0.0, 0.0), unit=Unit.METERS)
        self.assertAlmostEqual(output, expected_output)     

    # Punto tiene coordenadas negativas, y campana positivas
    def test_coord_negativa(self):
        campana:CampanaVerde = CampanaVerde("","", 1, {"PAPEL"}, (1.0, 1.0))

        output:float = campana.distancia(-1.0,-1.0)
        expected_output:float = haversine((-1.0, -1.0), (1.0, 1.0), unit=Unit.METERS)
        self.assertAlmostEqual(output, expected_output)

#############################################################################################
# Tests para el método __repr__()
class TestRepr(unittest.TestCase):

    # Datos de barrio y dirección reales
    def test_campana_real(self):
        campana:CampanaVerde = CampanaVerde("AGUIRRE 1447","CHACARITA", 1, {"PAPEL"}, (0.0, 0.0))
        output:str = str(campana) # -> Invoca el método __repr__()
        expected_output:str = "<AGUIRRE 1447@PAPEL@CHACARITA>"
        self.assertEqual(output, expected_output)

    # Campana sin materiales
    def test_sin_mat(self):
        campana:CampanaVerde = CampanaVerde("D","B", 1, set(), (0.0, 0.0))
        output:str = str(campana)
        expected_output:str = "<D@@B>"
        self.assertEqual(output, expected_output)

    # Campana un solo material
    def test_un_mat(self):
        campana:CampanaVerde = CampanaVerde("D","B", 1, {"PAPEL"}, (0.0, 0.0))
        output:str = str(campana)
        expected_output:str = "<D@PAPEL@B>"
        self.assertEqual(output, expected_output)

    # Campana más de un material
    def test_varios_mat(self):
        campana:CampanaVerde = CampanaVerde("D","B", 1, {"PAPEL", "CARTON"}, (0.0, 0.0))
        output:str = str(campana)
        # 2 outputs possibles pués el set no está ordenado
        possible_output1:str = "<D@PAPEL/CARTON@B>"
        possible_output2:str = "<D@CARTON/PAPEL@B>"
        error_message:str = output + " no es igual a " + possible_output1 + " o " + possible_output2
        self.assertTrue((output == possible_output1) or (output == possible_output2), error_message)

#############################################################################################
# Tests para el método __eq__()
class TestEq(unittest.TestCase):
    
    # Dos instancias de CampanaVerde con los mismos atributos
    def test_mismos_atributos(self):
        campana1:CampanaVerde = CampanaVerde("D","B", 1, {"Papel"}, (0.0, 0.0))
        campana2:CampanaVerde = CampanaVerde("D","B", 1, {"Papel"}, (0.0, 0.0))
        output:bool = campana1 == campana2
        expected_output:bool = True
        self.assertEqual(output, expected_output)

    # Dos instancias de CampanaVerde con todos los atributos distintos
    def test_distintos_atributos(self):
        campana1:CampanaVerde = CampanaVerde("D","B", 1, {"Papel"}, (0.0, 0.0))
        campana2:CampanaVerde = CampanaVerde("D2","B2", 2, {"Cartón"}, (1.0, 1.0))
        output:bool = campana1 == campana2
        expected_output:bool = False
        self.assertEqual(output, expected_output)

    # Dos instancias de CampanaVerde con la mitad de sus atributos iguales
    def test_algunos_distintos_atributos(self):
        campana1:CampanaVerde = CampanaVerde("D","B", 2, {"Papel", "Cartón"}, (1.0, 0.0))
        campana2:CampanaVerde = CampanaVerde("D2","B", 2, {"Cartón"}, (1.0, 1.0))
        output:bool = campana1 == campana2
        expected_output:bool = False
        self.assertEqual(output, expected_output)

unittest.main()