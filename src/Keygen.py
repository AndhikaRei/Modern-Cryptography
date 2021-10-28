import os
from Crypto.Util import number
from Crypto.Random import get_random_bytes
from datetime import date, datetime
from typing import Tuple

from Utility import *


class RSAKeygen:
	"""
	A class used for generating public and private key from RSA algorithm.
	
	Attributes.
	-----------
	public_key 	: tuple(int, int)
		Public key of RSA
	private_key	: tuple(int, int)
		Private key of RSA
	"""

	def __init__(self, public_key:Tuple[int,int]=(0,0), private_key:Tuple[int,int]=(0,0)) -> None:
		"""
		Constructor for RSAKeygen class.
		
		Attributes.
		-----------
		public_key 	: tuple(int, int)
			Public key of RSA
		private_key	: tuple(int, int)
			Private key of RSA
		"""
		self.public_key = public_key
		self.private_key = private_key

	def generateKey(self, is_random:bool=True, key_size:int=5, p:int=0, q:int=0, e:int=0) -> None:
		"""
		Generate public and private key from parameter given. 
		
		Parameter.
		----------
		is_random : bool
			randomize key or not
		key_size: int
			length of key (bit) of randomized key
		p, q : int
			two prime number
		e : int 
			part of public key
		"""
		# If generate random key. 
		if (is_random):
			# Get the requirement element.
			p = number.getPrime(key_size, randfunc=get_random_bytes)
			q = number.getPrime(key_size, randfunc=get_random_bytes)
			n = p * q
			totient = (p-1) * (q-1)
			e = self.generateE(totient, key_size)
			d = modularInverse(e, totient)

			# Validation
			if (d==0):
				raise Exception("Modular inverse not found")
		else:
			# Validation.
			if (not (isPrime(p))):
				raise Exception("P must be a prime number")
			if (not (isPrime(q))):
				raise Exception("Q must be a prime number")
			
			# Get the requirement element.
			n = p * q
			totient = (p-1) * (q-1)
			
			# Validation.
			if (gcd(e, totient) != 1):
				raise Exception("E must be relative prime with totient")

			d = modularInverse(e, totient)
			
		self.public_key = (e, n)
		self.private_key= (d, n)

	def generateE(self, totient:int, key_size:int) -> int:
		"""
		Generate public key e, from provided parameter. e must be relative prime with totient.
		
		Parameter.
		----------
		totient: int
			totient value of key
		key_size: int
			length of key (bit) of randomized e
		"""
		E = number.getPrime(key_size, randfunc=get_random_bytes)
		while (gcd(E, totient) != 1):
			E = number.getPrime(key_size, randfunc=get_random_bytes)
		return E
	
	def loadKey(self, filename:str) -> None:
		"""
		Load key from .pri and .pub file.
		
		Parameter.
		----------
		filename: str
			name of the file
		"""
		try:
			# Read the file.
			f = open(filename, "r")
			res = f.read()

			# Modify the key based on file extension.
			if (os.path.splitext(filename)[1].lower() == ".pub"):
				self.public_key = (int(res.split(" ")[0]), int(res.split(" ")[1]))
			elif (os.path.splitext(filename)[1].lower() == ".pri"):
				self.private_key = (int(res.split(" ")[0]), int(res.split(" ")[1]))
			else :
				raise Exception("Invalid filename extension")
			
		except :
			raise Exception("Failed when opening file")

	def saveKey(self, is_public: bool = True, filename:str= str(datetime.now())) -> None:
		"""
		Write key to file .pri and .pub .
		
		Parameter.
		----------
		is_public: bool
			totient value of key
		filename: str
			name of the file
		"""
		# Filling filename and content.
		# Default case.
		ext = ".pub"
		content = str(self.public_key[0]) + " " + str(self.public_key[1])
		
		# Private case.
		if (not is_public):
			ext = ".pri"
			content = str(self.private_key[0]) + " " + str(self.private_key[1])
		
		# Writing file to directory.
		filename += ext
		
		try:
			f = open(filename, "w")
			f.write(content)
		except :
			raise Exception("Failed when writing file")

# Main Program.
def main():
	# Test loadfile.
	test = RSAKeygen()
	test.loadKey("yamet.pub")
	print("Loading pub")
	print("Public: ", end="")
	print(test.public_key)
	print("Private: ", end="")
	print(test.private_key)
	test.loadKey("yamet.pri")
	print("Loading pri")
	print("Public: ", end="")
	print(test.public_key)
	print("Private: ", end="")
	print(test.private_key)

	# Test generate random key.
	test = RSAKeygen()
	test.generateKey(is_random=True, key_size=10)
	print("Random key")
	print("Public: ", end="")
	print(test.public_key)
	print("Private: ", end="")
	print(test.private_key)

	# Test generate key.
	test = RSAKeygen()
	test.generateKey(is_random=False, p=47, q=71, e=79)
	print("Filled key")
	print("Public: ", end="")
	print(test.public_key)
	print("Private: ", end="")
	print(test.private_key)

# If module is being runned.
if __name__ == "__main__":
    main()