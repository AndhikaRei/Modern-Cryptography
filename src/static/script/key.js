/*--------------------------------------------------------------
# Capturing HTML element
--------------------------------------------------------------*/

// Capture the button for randomizing key or not.
const keyrandomInput = document.getElementById('keyrandom');
const keymanualInput = document.getElementById('keymanual');

// Capture input field for randomizing key or not.
const randomInput = document.getElementById('randomInput')
const manualInput = document.getElementById('manualInput')

// Const keyrelated value.
const resultPublic = document.getElementById('public-key')
const resultPrivate = document.getElementById('private-key')




/*--------------------------------------------------------------
# Event Listener.
--------------------------------------------------------------*/
// When onload.
if (keyrandomInput) {
    window.addEventListener('load', function () {
        if (keyrandomInput.checked) {
            randomInput.classList.remove("d-none");
            manualInput.classList.add("d-none");
        }

        if (keymanualInput.checked) {
            randomInput.classList.add("d-none");
            manualInput.classList.remove("d-none");
        }
    });
};


// Add event listener for randomizing key or not.
if (keyrandomInput) {
    keyrandomInput.addEventListener("click", () => {
        randomInput.classList.remove("d-none");
        manualInput.classList.add("d-none");
    });
    keymanualInput.addEventListener("click", () => {
        randomInput.classList.add("d-none");
        manualInput.classList.remove("d-none");
    });
};

/*--------------------------------------------------------------
# Function and Procedure declaration
--------------------------------------------------------------*/

// Function for downloading decrypted or encrypted data.
function downloadFile(data, type) {
    let filename = Date.now();

    if (type == "pri"){
        filename = document.getElementById('privateName').value || Date.now();
        filename += ".pri"
    } else {
        filename = document.getElementById('publicName').value || Date.now();
        filename += ".pub"
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