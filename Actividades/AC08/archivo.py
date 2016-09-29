# AC08 - Isidora Vizcaya
import unittest
from main import PrograSU, Student, Verificador
from random import randint


class TesteoPUKE(unittest.TestCase):

    def setUp(self):
        self.mat = PrograSU("Matematicas")
        self.len = PrograSU("Lenguaje")

    def test_AlternativaCorrecta(self):
        # matematicas
        mat = open("Matematicas.txt")
        lineas = mat.readlines()
        self.assertEqual(self.mat.questions['1']['answer'],
                         lineas[0].split(",")[4].strip())
        self.assertEqual(self.mat.questions['2']['answer'],
                         lineas[1].split(",")[4].strip())
        self.assertEqual(self.mat.questions['6']['answer'],
                         lineas[5].split(",")[4].strip())

        mat.close()

        # matematicas
        leng = open("Lenguaje.txt")
        lineas = leng.readlines()
        self.assertEqual(self.leng.questions['1']['answer'],
                         lineas[0].split(",")[4].strip())
        self.assertEqual(self.leng.questions['2']['answer'],
                         lineas[1].split(",")[4].strip())
        self.assertEqual(self.leng.questions['5']['answer'],
                         lineas[4].split(",")[4].strip())

        leng.close()

    def test_SoloUnaCorrecta(self):
        # matematicas
        correctas = [x for x in ['a', 'b', 'c']
                     if x == self.mat.questions['1']['answer']]
        incorrectas = [x for x in ['a', 'b', 'c']
                       if x != self.mat.questions['6']['answer']]

        self.assertEqual(len(correctas), 1)
        self.assertEqual(len(incorrectas), 2)

        # lenguaje
        correctas = [x for x in ['a', 'b', 'c'] if
                     x == self.len.questions['1']['answer']]
        incorrectas = [x for x in ['a', 'b', 'c'] if
                       x != self.len.questions['5']['answer']]

        self.assertEqual(len(correctas), 1)
        self.assertEqual(len(incorrectas), 2)

    def test_CodigoVerificadorRUT(self):
        # RUT correcto
        self.assertTrue(Verificador("19246011-5"))

        # RUT incorrecto
        self.assertFalse(Verificador("19246011-8"))

    def test_Clave(self):
        aux = "".join(str(randint(0, 9)) for _ in range(8))
        random_rut = aux + "-{}".format(str(randint(0, 9)))
        student = Student("", 0, random_rut, "")
        print(student.rut)
        digitos = student.generar_codigo()

        self.assertEqual((int(aux) + digitos) % 97, 1)

    def test_CrearUsuario(self):
        fake = "Isidora"
        self.assertFalse(self.mat.register(fake))

        real = Student("Isidora", 20, "19246011-5", "cumbres")
        self.assertTrue(self.len.register(real))

    def test_RegistroExitoso(self):
        def random_students(n):
            return [Student("", 0, "", "") for _ in range(n)]

        # matematicas
        n = randint(1, 10)
        list(map(self.mat.register, random_students(n)))
        self.assertEqual(len(self.mat.students), n)

        # lenguaje
        n = randint(1, 10)
        list(map(self.len.register, random_students(n)))
        self.assertEqual(len(self.len.students), n)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TesteoPUKE)
    unittest.TextTestRunner().run(suite)
