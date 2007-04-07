import unittest
from Escenario import *

class EscenarioTest(unittest.TestCase):
	def testEscenario(self):
		e = Escenario(3)
		print e.bares


	def testEscenarioAttrs(self):
		e = Escenario(3)
		assert e.dineroAcumulado == 0, "dinero acumulado = 0"

if __name__=="__main__":
	unittest.main()
