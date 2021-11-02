// Utility for client-side.

/*--------------------------------------------------------------
# Capturing HTML element
--------------------------------------------------------------*/

// Capture the uploading ciphertext/plaintext related element with dom manipulation.
const fileCiphertext = document.getElementById('file-ciphertext');
const filePlaintext = document.getElementById('file-plaintext');
const plainText = document.getElementById('plaintext');
const cipherText = document.getElementById('ciphertext');

const filePublicKey = document.getElementById('file-public-key');
const filePrivateKey = document.getElementById('file-private-key');
const publicKey = document.getElementById('key-encrypt');
const privateKey = document.getElementById('key-decrypt');

// Capture additional element in elgamal or ECEG.
const cipherText2 = document.getElementById('ciphertext2');
const fileCiphertext2 = document.getElementById('file-ciphertext2');
const resultCipher2 = document.getElementById('result-ciphertext2');

// Capture the downloading ciphertext/plaintext related element with dom manipulation.
const btnDownloadCipher = document.getElementById('download-ciphertext');
const btnDownloadPlain = document.getElementById('download-plaintext');
const resultCipher = document.getElementById('result-ciphertext');
const resultPlain = document.getElementById('result-plaintext');

/*--------------------------------------------------------------
# Function and Procedure declaration
--------------------------------------------------------------*/

// Function to download encrypted pr decrypted  data.
function downloadData(data, type) {
    let filename = Date.now();

    if (type == "cip") {
        filename = document.getElementById('ciphertextName').value || Date.now();
    } else if (type == "cip2") {
        filename = document.getElementById('ciphertextName2').value || Date.now();
    } else {
        filename = document.getElementById('plaintextName').value || Date.now();
    }

    const filetype = "text/plain";
    const filecontent = [data]

    var file = new Blob(filecontent, {
        filetype
    });

    // Handling unsupported browser.
    if (window.navigator.msSaveOrOpenBlob)
        window.navigator.msSaveOrOpenBlob(file, filename);
    else {

        var a = document.createElement("a")
        var url = URL.createObjectURL(file);

        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();

        setTimeout(function () {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}

let readtext = (event, text) => {
    const fileList = event.target.files;
    const fr = new FileReader();
    fr.onload = function () {
        text.value = fr.result;
    }
    fr.readAsText(fileList[0]);
};

/*--------------------------------------------------------------
# Event Listener.
--------------------------------------------------------------*/

// Add event listener for loading plaintext file, so it will automaticaly change 
// plaintext textarea value.
if (filePlaintext){
    filePlaintext.addEventListener('change', (event) => readtext(event, plainText));
}

// Add event listener for loading ciphertext file, so it will automaticaly change 
// ciphertext textarea value.
if (fileCiphertext){
    fileCiphertext.addEventListener('change', (event) => readtext(event, cipherText));
}

// Add event listener for loading key file, so it will automaticaly change 
// public or private key textarea value.
if (filePublicKey){
    filePublicKey.addEventListener('change', (event) => readtext(event, publicKey));
}

if (filePrivateKey) {
    filePrivateKey.addEventListener('change', (event) => readtext(event, privateKey));
}

// Only in elgamal and ECEG
if (fileCiphertext2) {
    fileCiphertext2.addEventListener('change', (event) => readtext(event, cipherText2));
}



