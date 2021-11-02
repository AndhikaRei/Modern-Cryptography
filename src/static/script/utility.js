// Utility for client-side.

/*--------------------------------------------------------------
# Capturing HTML element
--------------------------------------------------------------*/

// Capture the uploading ciphertext/plaintext related element with dom manipulation.
const fileCiphertext = document.getElementById('file-ciphertext');
const filePlaintext = document.getElementById('file-plaintext');
const plainText = document.getElementById('plaintext');
const cipherText = document.getElementById('ciphertext');

// Capture the downloading ciphertext/plaintext related element with dom manipulation.
const btnDownloadCipher = document.getElementById('download-ciphertext');
const btnDownloadPlain = document.getElementById('download-plaintext');
const resultCipher = document.getElementById('result-ciphertext');
const resultPlain = document.getElementById('result-plaintext');


/*--------------------------------------------------------------
# Function and Procedure declaration
--------------------------------------------------------------*/


// Function for downloading decrypted or encrypted data.
function downloadFile(data) {
    const filename = Date.now();
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
    if (fileList[0].type != "text/plain") {
        return;
    }
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
    // filePlaintext.addEventListener('change', (event) => {
    //     const fileList = event.target.files;
    //     if (fileList[0].type != "text/plain") {
    //         return;
    //     }
    //     const fr = new FileReader();
    //     fr.onload = function () {
    //         plainText.value = fr.result;
    //     }
    //     fr.readAsText(fileList[0]);
    // });
    filePlaintext.addEventListener('change', readtext(event, plainText));
}


// Add event listener for loading ciphertext file, so it will automaticaly change 
// ciphertext textarea value.
if (fileCiphertext){
    fileCiphertext.addEventListener('change', (event) => {
        const fileList = event.target.files;
        if (fileList[0].type != "text/plain") {
            return;
        }
        const fr = new FileReader();
        fr.onload = function () {
            cipherText.value = fr.result;
        }
        fr.readAsText(fileList[0]);
    });
}




