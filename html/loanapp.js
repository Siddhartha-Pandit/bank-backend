const url = 'http://127.0.0.1:8000/loan/';

document.getElementById('loanForm').addEventListener('submit', function(event) {
    event.preventDefault();
    submit();
});

async function submit() {
    const formData = new FormData(document.getElementById('loanForm'));

    const response = await fetch(url, {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        // Success - handle the response
        console.log("Form data successfully submitted!");
    } else {
        // Error - handle the validation errors
        console.error("Error submitting form data!");
    }
}
