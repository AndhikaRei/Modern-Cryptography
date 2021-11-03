import os
from flask import Flask, render_template, request, redirect, url_for


from ElGamal import ElGamal_Crypt, ElGamalKeygen
from ECEG import ECC, ECEG
from RSA import RSA_Crypt
from Paillier import Paillier_Crypt


# Flask Configuration.
app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'mysecret'



"""
--------------------------------------------------------------
# Default Route
--------------------------------------------------------------
"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
		return redirect(url_for('elgamal'))

	

"""
--------------------------------------------------------------
# Route for Generate Elgamal key
--------------------------------------------------------------
"""
# Index route.
@app.route('/elgamal-gen-key')
def elgamalKey():
	return render_template('pages/elgamalkey.html', random=True)

# Generate key route.
@app.route('/elgamal-gen-key/generate', methods=['POST', 'GET'])
def elgamalKeyGenerate():
	if request.method == 'POST':
		# Get the request payload.
		try:
			# Instantiation.
			elgamalKey = ElGamalKeygen()
			choice = request.form["randomizing"]

			if (choice == "random"):
				isRandom = True
				bitLength = int(request.form["bitLength"])
				
				# Key generation.
				elgamalKey.generateKey(is_random=True, key_size=bitLength)
			else:
				isRandom = False
				prime = int(request.form["prime"])

				# Key generation.
				elgamalKey.generateKey(is_random=False, p=prime)
			
			# Formatting the result.
			res_public = "{0} {1} {2}"
			result_public_key = res_public.format(elgamalKey.public_key[0], 
				elgamalKey.public_key[1], elgamalKey.public_key[2])
			res_private = "{0} {1}"
			result_private_key = res_private.format(elgamalKey.private_key[0], 
				elgamalKey.private_key[1] )

			return render_template('pages/elgamalkey.html', random=isRandom, form = request.form, 
				result_public_key=result_public_key, result_private_key = result_private_key)

		except (Exception) as e:
			# Render error webpage.
			return render_template('pages/elgamalkey.html', random=isRandom,
				error = e, form = request.form)
	else:
		# Render default webpage. 
		return redirect(url_for('elgamalKey'))


"""
--------------------------------------------------------------
# Route for Elgamal
--------------------------------------------------------------
"""
# Index route.
@app.route('/elgamal')
def elgamal():
	return render_template('pages/elgamal.html', encrypt=True)

# Encrypt route
@app.route('/elgamal/encrypt', methods=['POST', 'GET'])
def elgamalEncrypt():
	if request.method == 'POST':
		# Get the request payload.
		try:
			# Get the payload.
			plaintext = request.form['plaintext']
			public_key = request.form['key']

			# Create key.
			key = ElGamalKeygen()
			key.readKey(key=public_key, type="pub")

			# Create crypt object and encrypt the text.
			elGamal = ElGamal_Crypt()
			ciphertext = elGamal.encrypt(plaintext, key.public_key)

			return render_template('pages/elgamal.html', encrypt=True, form = request.form, 
				result_ciphertext=ciphertext)
		
		except (Exception) as e:
			# Render error webpage.
			return render_template('pages/elgamal.html', encrypt=True,
				error = e, form = request.form)
	else:
		# Render default webpage. 
		return redirect(url_for('elgamal'))

# Decrypt route.
@app.route('/elgamal/decrypt', methods=['POST', 'GET'])
def elgamalDecrypt():
	if request.method == 'POST':
	# Get the request payload.
		try:
			# Get the payload.
			ciphertextA = request.form['ciphertext']
			ciphertextB = request.form['ciphertext2']
			private_key = request.form['key']

			# Create key.
			key = ElGamalKeygen()
			key.readKey(key=private_key, type="pri")

			# Create crypt object and encrypt the text.
			elGamal = ElGamal_Crypt()
			plaintext = elGamal.decrypt((ciphertextA, ciphertextB), key.private_key)
			
			return render_template('pages/elgamal.html', encrypt=False, form = request.form, 
				result_plaintext=plaintext)
		
		except (Exception) as e:
			# Render error webpage.
			return render_template('pages/elgamal.html', encrypt=True,
				error = e, form = request.form)
	else:
		# Render default webpage. 
		return redirect(url_for('elgamal'))

"""
--------------------------------------------------------------
# Route for Generate ECEG key
--------------------------------------------------------------
"""
# Index route.
@app.route('/eceg-gen-key')
def ecegKey():
	return render_template('pages/ecegkey.html', random=True)

# Generate key route.
@app.route('/eceg-gen-key/generate', methods=['POST', 'GET'])
def ecegKeyGenerate():
	if request.method == 'POST':
		# Get the request payload.
		try:
			ecegKey = ECC()
			# Instantiation.
			choice = request.form["randomizing"]

			if (choice == "random"):
				isRandom = True
				bitLength = int(request.form["bitLength"])
				print(bitLength)
				ecegKey.fullyRandomizeAttribute(p_size=bitLength)
				
			else:
				isRandom = False
				# Get all payload.
				a = int(request.form["a"])
				b = int(request.form["b"])
				p = int(request.form["p"])
				Bx = int(request.form["Bx"])
				By = int(request.form["By"])
				B = (Bx, By)

				# Generate the key and curve parameter.
				ecegKey.generateEllipticCurve(is_random=False, a=a, b=b, p=p)
				ecegKey.generateGroup(is_random=True)
				ecegKey.generateBasis(is_random=False, B=B)
				ecegKey.generateKey(is_random=True)

			# Get the public and provate key in formatted string.
			ecegKey.printDetail()
			result_public_key = ecegKey.getKeyFormatted("pub")
			result_private_key = ecegKey.getKeyFormatted("pri")
			return render_template('pages/ecegkey.html', random=isRandom, form = request.form, 
				result_public_key=result_public_key, result_private_key = result_private_key)

		except (Exception) as e:
			# Render error webpage.
			return render_template('pages/ecegkey.html', random=isRandom,
				error = e, form = request.form)
	else:
		# Render default webpage. 
		return redirect(url_for('ecegKey'))

"""
--------------------------------------------------------------
# Route for RSA Keygen
--------------------------------------------------------------
"""
# Index route.
@app.route('/rsa-gen-key')
def rsaKey():
	return render_template('pages/rsakey.html', random=True)

# Generate key route.
@app.route('/rsa-gen-key/generate', methods=['POST', 'GET'])
def rsaKeyGenerate():
	if request.method == 'POST':
		# Get the request payload.
		try:
			# Instantiation.
			rsa = RSA_Crypt()
			choice = request.form["randomizing"]

			if (choice == "random"):
				isRandom = True
				keySize = int(request.form["keySize"])
				
				# Key generation.
				e, d, n = rsa.generate_rsa_key(keySize)
			else:
				isRandom = False
				p = int(request.form["p"])
				q = int(request.form["q"])
				e = int(request.form["e"])

				# Key generation.
				e, d, n = rsa.generate_rsa_key_manual(p, q, e)
			
			# Formatting the result.
			result_public_key = "{} {}".format(e, n)
			result_private_key = "{} {}".format(d, n)

			return render_template(
				'pages/rsakey.html', 
				random=isRandom, 
				form = request.form, 
				result_public_key=result_public_key, 
				result_private_key = result_private_key
			)

		except (Exception) as e:
			# Render error webpage.
			return render_template(
				'pages/rsakey.html', 
				random=isRandom,
				error = e, 
				form = request.form
			)
	else:
		# Render default webpage. 
		return redirect(url_for('rsaKey'))

"""
--------------------------------------------------------------
# Route for Paillier Keygen
--------------------------------------------------------------
"""
# Index route.
@app.route('/paillier-gen-key')
def paillierKey():
	return render_template('pages/paillierkey.html', random=True)

# Generate key route.
@app.route('/rsa-gen-key/generate', methods=['POST', 'GET'])
def paillierKeyGenerate():
	if request.method == 'POST':
		# Get the request payload.
		try:
			# Instantiation.
			paillier = Paillier_Crypt()
			choice = request.form["randomizing"]

			if (choice == "random"):
				isRandom = True
				keySize = int(request.form["keySize"])
				
				# Key generation.
				g, n, lmd, miu = paillier.generate_paillier_key(keySize)
			else:
				isRandom = False
				p = int(request.form["p"])
				q = int(request.form["q"])
				g = int(request.form["g"])

				# Key generation.
				g, n, lmd, miu = paillier.generate_paillier_key_manual(p, q, g)
			
			# Formatting the result.
			result_public_key = "{} {}".format(g, n)
			result_private_key = "{} {}".format(lmd, miu)

			return render_template(
				'pages/paillierkey.html', 
				random=isRandom, 
				form = request.form, 
				result_public_key=result_public_key, 
				result_private_key = result_private_key
			)

		except (Exception) as e:
			# Render error webpage.
			return render_template(
				'pages/paillierkey.html', 
				random=isRandom,
				error = e, 
				form = request.form
			)
	else:
		# Render default webpage. 
		return redirect(url_for('paillierKey'))

"""
--------------------------------------------------------------
# Route for RSA
--------------------------------------------------------------
"""
# Index route.
@app.route('/rsa')
def rsa():
	return render_template('pages/rsa.html', encrypt=True)

# Encrypt route
@app.route('/rsa/encrypt', methods=['POST', 'GET'])
def rsaEncrypt():
	if request.method == 'POST':
		# Get the request payload.
		try:
			# Get the payload.
			plaintext = request.form['plaintext']
			public_key = request.form['key'].split(' ')

			rsa = RSA_Crypt()
			ciphertext = rsa.encrypt(plaintext, int(public_key[0]), int(public_key[1]))

			return render_template(
				'pages/rsa.html', 
				encrypt=True, 
				form = request.form, 
				result_ciphertext=ciphertext
			)
		
		except (Exception) as e:
			# Render error webpage.
			return render_template('pages/rsa.html', encrypt=True,
				error = e, form = request.form)
	else:
		# Render default webpage. 
		return redirect(url_for('rsa'))

# Decrypt route.
@app.route('/rsa/decrypt', methods=['POST', 'GET'])
def rsaDecrypt():
	if request.method == 'POST':
	# Get the request payload.
		try:
			# Get the payload.
			ciphertext = request.form['ciphertext']
			private_key = request.form['key'].split(' ')

			rsa = RSA_Crypt()
			plain_text = rsa.decrypt(ciphertext, int(private_key[0]), int(private_key[1]))
			
			return render_template(
				'pages/rsa.html', 
				encrypt=False, 
				form = request.form, 
				result_plaintext=plain_text
			)
		
		except (Exception) as e:
			# Render error webpage.
			return render_template('pages/rsa.html', encrypt=True,
				error = e, form = request.form)
	else:
		# Render default webpage. 
		return redirect(url_for('rsa'))


"""
--------------------------------------------------------------
# Route for ECEG
--------------------------------------------------------------
"""
# Index route.
@app.route('/eceg')
def eceg():
	return render_template('pages/eceg.html', encrypt=True)

# Encrypt route
@app.route('/eceg/encrypt', methods=['POST', 'GET'])
def ecegEncrypt():
	if request.method == 'POST':
		# Get the request payload.
		try:
			# Get the payload.
			plaintext = request.form['plaintext']
			public_key = request.form['key']
			print("plaintext: ", plaintext)
			print("public key: ", public_key)

			# Create key.
			key = ECC()
			key.readKey(key=public_key, type="pub")
			print("Gonna encrypt with these params")
			key.printDetail()

			# Create crypt object and encrypt the text.
			eceg = ECEG(ecc=key)
			ciphertext = eceg.encrypt(plaintext)

			print("the result is")
			print(ciphertext)

			return render_template('pages/eceg.html', encrypt=True, form = request.form, 
				result_ciphertext=ciphertext)
		
		except (Exception) as e:
			# Render error webpage.
			return render_template('pages/eceg.html', encrypt=True,
				error = e, form = request.form)
	else:
		# Render default webpage. 
		return redirect(url_for('eceg'))

# Decrypt route.
@app.route('/eceg/decrypt', methods=['POST', 'GET'])
def ecegDecrypt():
	if request.method == 'POST':
	# Get the request payload.
		try:
			# Get the payload.
			ciphertextA = request.form['ciphertext']
			ciphertextB = request.form['ciphertext2']
			private_key = request.form['key']
			print("private key: ", private_key)
			print("ciphertext A: ", ciphertextA)
			print("Ciphertext B: ", ciphertextB)

			# Create key.
			key = ECC()
			key.readKey(key=private_key, type="pri")
			print("Gonna decrypt with these params")
			key.printDetail()

			# Create crypt object and encrypt the text.
			eceg = ECEG(ecc=key)
			
			plaintext = eceg.decrypt((ciphertextA, ciphertextB))
			print("the result is")
			print(plaintext)
			
			return render_template('pages/eceg.html', encrypt=False, form = request.form, 
				result_plaintext=plaintext)
		
		except (Exception) as e:
			# Render error webpage.
			return render_template('pages/eceg.html', encrypt=False,
				error = e, form = request.form)
	else:
		# Render default webpage. 
		return redirect(url_for('eceg'))


"""
--------------------------------------------------------------
# Flask Main Program
--------------------------------------------------------------
"""
if __name__ == '__main__':
	app.run(debug=True,threaded=True)

