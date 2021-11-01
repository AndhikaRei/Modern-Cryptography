import os
import random
from Crypto.Util import number
from Crypto.Random import get_random_bytes
from datetime import date, datetime
from typing import Tuple


from Utility import *

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