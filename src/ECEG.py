import os
import random

from sympy.core.basic import as_Basic
import utils
import math

from Crypto.Util import number
from Crypto.Random import get_random_bytes
from datetime import datetime
from typing import Tuple, List
from utils.blockText import ciphertextToArrTupleInt


class ECC:
	"""
	A class used for generating elliptic curve cryptography parameter/key.
	Also used for basic method in ECC.

	Attributes
	----------
	a,b,p: int
		parameter persamaan kurva eliptik, p haruslah bilangan prima.
	group: List[Tuple[int,int]]
		grup eliptik yang dihitung dari persamaan kurva eliptik
	B: Tuple[int,int]
		Titik basis (base point) (xb,yb), dipilih dari grup eliptik untuk operasi kriptografi.
	N: int
		banyaknya anggota grup yang dimiliki.
	x: int
		kunci privat, dipilih dari selang [1, p-1]
	Q: Tuple[int,int] 
		kunci publik, adalah hasil kali antara x dan titik basis B: Q = x.B
	"""

	def __init__(self, a:int=0, b:int=0, p:int=0, N:int=0, B:Tuple[int, int]=(0,0), group:List[Tuple[int, int]]=None, x:int=0, Q:Tuple[int,int]=(0,0)) -> None:
		"""
		Constructor for ECEGKeygen class.
		"""

		self.a = a
		self.b = b
		self.p = p
		self.group = group
		self.N = N
		self.B = B
		self.x = x
		self.Q = Q
		self.math = utils.Math()
	
	def fullyRandomizeAttribute(self, p_size:int = 14):
		"""
		Fully randomized attribute.
		"""

		self.generateEllipticCurve(is_random=True, p_size=p_size)
		self.generateGroup(is_random=True)
		self.generateBasis(is_random=True)
		self.generateKey(is_random=True)
				
	def generateEllipticCurve(self, a:int=0, b:int=0, p:int=0, is_random:bool=True, p_size:int=12)->None:
		"""
		Generate Elliptic Curve basic parameter
		"""
		# Randomized case.
		if (is_random):
			p = number.getPrime(p_size, randfunc=get_random_bytes)
			a = random.randint(2, p-1)
			b = random.randint(1, p-1)
			while (4*(a**3) + 27*(b**2) == 0):
				a = random.randint(2, p-1)
				b = random.randint(1, p-1)

		# Validation.
		if (not self.math.isPrime(p)):
			raise Exception("P must be a prime number")
		if(4*(a**3) + 27*(b**2) == 0):
			raise Exception("Invalid a and b value (4a^3 + 27b^2 != 0)")
		
		# Fill the value.
		self.a = a
		self.b = b
		self.p = p
	
	def generateGroup(self, is_random:bool=True, group:List[Tuple[int, int]]=None,  N:int=0) -> None:
		"""
		Generate elliptic curve group.
		"""
		# Randomized case.
		if (is_random):
			group = []
			# Enumerate all possible x and y values.
			for x in range(self.p):
				right_side = (pow(x,3, self.p) + self.a*x + self.b) % self.p
				for y in range(self.p):
					left_side = pow(y,2,self.p)
					# If matching then (x,y) is part of the group.
					if (right_side == left_side):
						group.append((x,y))
			
			# Get the length.
			N = len(group)
		# Validation.
		if(N < 256):
			raise Exception("Group size must be atleast 256 point")
		# Fill the value.
		self.group = group
		self.N = N
	
	def generateBasis(self, is_random:bool=True, B:Tuple[int,int]=(0,0))-> None:
		"""
		Generate basis for elliptic curve.
		"""
		# Randomized case.
		if (is_random):
			B = self.group[random.randrange(0, len(self.group))]
		
		# Fill the value.
		self.B = B
	
	def generateKey(self, is_random:bool=True, d:int=2, Q:Tuple[int,int]=(0,0)):
		"""
		Generate public key and private key.
		"""
		if (is_random):
			# Generate private key
			d = random.randint(2, self.p-1)

			# Generate public key.
			Q = self.perkalianTitik(d, self.B)
			while ((Q[0]==math.inf and Q[1]==math.inf)):
				# Generate private key
				d = random.randint(2, self.p-2)

				# Generate public key.
				Q = self.perkalianTitik(d, self.B)

		# Validation.
		if (d <= 1 or d >= self.p):
			raise Exception("d must be between 1 and p")
		if(Q[0]==math.inf and Q[1]==math.inf):
			raise Exception("Q cant be an identity point")
		
		# Fill the value.
		self.d = d
		self.Q = Q
	
	def penjumlahanTitik(self, titik1:Tuple[int,int], titik2:Tuple[int,int]) ->Tuple[int,int]:
		"""
		Melakukan penjumlahan dua titik pada elliptic curve.
		"""

		# Variable naming.
		xp, yp = titik1
		xq, yq = titik2

		# Sifat elemen netral pada abelian.
		if (xp == math.inf and yp == math.inf):
			return (xq, yq)
		if (xq == math.inf and yq == math.inf):
			return (xp, yp)
		
		# If ditambah dengan inverse
		if (xp == xq and yp == (-1*yq) % self.p):
			return (math.inf, math.inf)

		# If equal checking (penggandaan).
		if (xp == xq and yp == yq):
			# Jika ordinat 0 maka tangen berpotongan di infinity.
			if (yp == 0):
				return (math.inf, math.inf)
			else:
				# Rumus gradien pada penggandaan.
				m = ((3*(xp**2) + self.a) * self.math.modinv2(2*yp, self.p)) % self.p

				# Rumus xr dan yr pada penggandaan.
				xr = (m**2 - 2*xp) % self.p
				yr = (m*(xp-xr)-yp) % self.p
				return (xr, yr)
		else:
			# Gradien infinity.
			if (xp - yp) == 0:
				return  (math.inf, math.inf)
			else:
				# Rumus gradien biasa.
				
				m = ((yp -yq) * self.math.modinv2(xp - xq, self.p)) % self.p
				# Rumus xr dan yr pada penggandaan.
				xr = (m**2 - xp - xq) % self.p
				yr = (m*(xp-xr)-yp) % self.p
				return (xr, yr)
	
	def perkalianTitik(self, k:int, titik:Tuple[int,int]):
		"""
		Melakukan perkalian titik secara rekursif.
		"""
		res = (math.inf, math.inf)
		for i in range(k):
			res = self.penjumlahanTitik(res, titik)
		
		return res
	
	def negative(self, titik:Tuple[int,int]):
		"""
		Melakukan negasi titik.
		"""
		return (titik[0], -1* titik[1] % self.p)
	
	def readKey(self, key:str, type:str):
		"""
		Read key from string in file.
		"""

		# Read the string.
		res = key

		# Modify the key based on file extension.
		if (type =="pub"):
			# .pub
			# a b p Bx By Qx Qy
			a = int(res.split(" ")[0])
			b = int(res.split(" ")[1])
			p = int(res.split(" ")[2])
			Bx = int(res.split(" ")[3])
			By = int(res.split(" ")[4])
			B = (Bx, By)
			Qx = int(res.split(" ")[5])
			Qy = int(res.split(" ")[6])
			Q = (Qx, Qy)

			self.generateEllipticCurve(a=a, b=b, p=p, is_random=False)
			self.generateGroup(is_random=True)
			self.generateBasis(is_random=False, B = B)
			self.generateKey(is_random=False, Q = Q)
			
		else:
			# .pri
			# a b p Bx By d
			a = int(res.split(" ")[0])
			b = int(res.split(" ")[1])
			p = int(res.split(" ")[2])
			Bx =int(res.split(" ")[3])
			By = int(res.split(" ")[4])
			B = (Bx, By)
			d = int(res.split(" ")[5])

			self.generateEllipticCurve(a=a, b=b, p=p, is_random=False)
			self.generateGroup(is_random=True)
			self.generateBasis(is_random=False, B = B)
			self.generateKey(is_random=False, d = d)


		
	def loadKey(self, filename:str) -> None:
		"""
		Load key from .pri and .pub file.
		"""
		try:
			# Read the file.
			f = open(filename, "r")
			res = f.read()

			# Modify the key based on file extension.
			if (os.path.splitext(filename)[1].lower() == ".pub"):
				# .pub
        		# a b p Bx By Qx Qy
				a = int(res.split(" ")[0])
				b = int(res.split(" ")[1])
				p = int(res.split(" ")[2])
				Bx = int(res.split(" ")[3])
				By = int(res.split(" ")[4])
				B = (Bx, By)
				Qx = int(res.split(" ")[5])
				Qy = int(res.split(" ")[6])
				Q = (Qx, Qy)

				self.generateEllipticCurve(a=a, b=b, p=p, is_random=False)
				self.generateGroup(is_random=True)
				self.generateBasis(is_random=False, B = B)
				self.generateKey(is_random=False, Q = Q)

			elif (os.path.splitext(filename)[1].lower() == ".pri"):
				# .pri
				# a b p Bx By d
				a = int(res.split(" ")[0])
				b = int(res.split(" ")[1])
				p = int(res.split(" ")[2])
				Bx = int(res.split(" ")[3])
				By = int(res.split(" ")[4])
				B = (Bx, By)
				d = int(res.split(" ")[5])

				self.generateEllipticCurve(a=a, b=b, p=p, is_random=False)
				self.generateGroup(is_random=True)
				self.generateBasis(is_random=False, B = B)
				self.generateKey(is_random=False, d = d)

			else :
				raise Exception("Invalid filename extension")
			
		except :
			raise Exception("Failed when opening file")

	def saveKey(self, is_public: bool = True, filename:str= str(datetime.now())) -> None:
		"""
		Write key to file .pri and .pub .
		"""
		# .pri
        # a b p Bx By d

        # .pub
        # a b p Bx By Qx Qy
		# Filling filename and content.
		
		# Default case.
		if (is_public):
			ext = ".pub"
			content = str(self.a) + " " + str(self.b) + " " + str(self.p) + " "
			content = content + str(self.B[0]) + " " + str(self.B[1]) + " "
			content = content + str(self.Q[0]) + " " + str(self.Q[1]) 

		# Private case.
		if (not is_public):
			ext = ".pri"
			content = str(self.a) + " " + str(self.b) + " " + str(self.p) + " "
			content = content + str(self.B[0]) + " " + str(self.B[1]) + " "
			content = content + str(self.d)
		
		# Writing file to directory.
		filename += ext
		
		try:
			f = open(filename, "w")
			f.write(content)
		except :
			raise Exception("Failed when writing file")

	def getKeyFormatted(self, type:str):
		"""
		Formatted key for file.
		"""
		content = str(self.a) + " " + str(self.b) + " " + str(self.p) + " "
		content = content + str(self.B[0]) + " " + str(self.B[1]) + " "
		if (type == "pub"):
			content = content + str(self.Q[0]) + " " + str(self.Q[1]) 
		else:
			content = content + str(self.d)

		return content
	

	def printDetail(self):
		"""
		Print the detail of the curve
		"""
		print("Elliptic Curve parameter")
		print("a: ", self.a)
		print("b: ", self.b)
		print("p: ", self.p)
		print("N -> Group size: ", self.N)
		print("B -> Titik basis: ", end="")
		print(self.B)
		print("d -> private key: ", self.d)
		print("Q -> Public key: ", end="")
		print(self.Q)

class ECEG:
	"""
	A class used for representing ECC with elgamal algorithm.
	"""
	def __init__(self, ecc:ECC=None) -> None:
		"""
		Constructor for ECEG class.
		"""
		# if (ecc is None):
		# 	ecc = ECC()
		# 	ecc.fullyRandomizeAttribute()
		self.ecc = ecc
	
	def encrypt(self, plain_text: str) -> Tuple[str,str]:
		"""
		Encrypt the plaintext using ECEG algorithm. Return tuple containing two ciphertext.
		"""

		# Encrypt using ECEG algorithm.
		complete_a =[]
		complete_b =[]

		for char in plain_text:
			# Encrypt.
			pm = self.ecc.group[ord(char)]
			k = random.randint(2, self.ecc.p - 2)
			a = self.ecc.perkalianTitik(k, self.ecc.B)
			b = self.ecc.penjumlahanTitik(pm, self.ecc.perkalianTitik(k, self.ecc.Q))

			# Append to tuple result.
			a1 = str(a[0]).rjust(len(str(self.ecc.p)), "0")
			a2 = str(a[1]).rjust(len(str(self.ecc.p)), "0")
			complete_a.append(a1+a2)

			b1 = str(b[0]).rjust(len(str(self.ecc.p)), "0")
			b2 = str(b[1]).rjust(len(str(self.ecc.p)), "0")
			complete_b.append(b1+b2)
		
		# print("=======================")
		# print("Before combined")
		# print("a: ", end="")
		# print(complete_a)
		# print("b: ", end="")
		# print(complete_b)
		# print("=======================")
		
		# Combine a to one string and b to one string.
		complete_a = "".join(complete_a)
		complete_b = "".join(complete_b)
		return (complete_a, complete_b)
		
	def decrypt(self, cipher_text: Tuple[str, str]) -> str:
		"""
		Decrypt the ciphertext using ECEG algorithm. 
		Ciphertext must be a tuple of two string (a and b). Return plaintext.
		"""

		# Prepare for decrypting.
		max_length = len(str(self.ecc.p))
		num_alphabet = 1
		list_a = cipher_text[0]
		list_int_a = ciphertextToArrTupleInt(list_a, max_length)
		list_b = cipher_text[1]
		list_int_b = ciphertextToArrTupleInt(list_b, max_length)

		print("a: ", end="")
		print(list_int_a)
		print("b: ", end="")
		print(list_int_b)


		# Decrypting using elgamal algorithm.
		plaintext = ""
		for a, b in zip(list_int_a, list_int_b):
			first_equation = self.ecc.perkalianTitik(self.ecc.d, a)
			pm = self.ecc.penjumlahanTitik(b, self.ecc.negative(first_equation))
			ascii = self.ecc.group.index(pm)
			plaintext += chr(ascii)

		return plaintext

# Testing ecc.
def testECC():
	Ecc = ECC()
	Ecc.fullyRandomizeAttribute()
	Ecc.printDetail()
	Ecc.saveKey(True, "yamet")
	Ecc.saveKey(False, "yamet")

def testECEG():
	print("ECEG without loading")
	# Generating elliptic curve.
	Ecc = ECC()
	Ecc.fullyRandomizeAttribute(p_size=12)
	Ecc.printDetail()

	# Encrypt the message.
	Ecg = ECEG(Ecc)
	print("Encrypting the plaintext")
	plaintext = '''reihan 
	karel'''
	print("The plaintext is ",  plaintext)
	ciphertext = Ecg.encrypt(plaintext)
	print("The ciphertext is")
	print("a: ", end="")
	print(ciphertext[0])
	print("b: ", end="")
	print(ciphertext[1])

	# Decrypt the message.
	print("Decrypting the ciphertext")
	a = ciphertext[0]
	b = ciphertext[1]
	plaintext = Ecg.decrypt((a,b))
	print("The plaintext is ", plaintext)

	# # Saving the key.
	Ecc.saveKey(True, "ECEG") 
	Ecc.saveKey(False, "ECEG")

def TestLoad():
	print("ECEG with loading")
	# Generating elliptic curve.
	Ecc = ECC()
	Ecc.loadKey("ECEG.pub")
	Ecc.printDetail()

	# Encrypt the message.
	Ecg = ECEG(Ecc)
	print("Encrypting the plaintext")
	plaintext = '''karel
	reihan'''
	print("The plaintext is ",  plaintext)
	ciphertext = Ecg.encrypt(plaintext)
	print("The ciphertext is")
	print("a: ", end="")
	print(ciphertext[0])
	print("b: ", end="")
	print(ciphertext[1])

	# Decrypt the message.
	print("Decrypting the ciphertext")
	Ecc.loadKey("ECEG.pri")
	Ecc.printDetail()
	Ecg = ECEG(Ecc)
	a = ciphertext[0]
	b = ciphertext[1]
	plaintext = Ecg.decrypt((a,b))
	print("The plaintext is ", plaintext)

# If module is being runned.
if __name__ == "__main__":
	# testECC()
	testECEG()
	TestLoad()