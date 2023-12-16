url='http://127.0.0.1:8000/register/'


document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault();
    submit();
});

async function submit() {
    
    const formData = new FormData(document.getElementById('myForm'));
console.log(formData)
    const response = await fetch(url, {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        // Success - handle the response
        const responseData = await response.json();
        console.log("Response from server:", responseData);
    } else {
        // Error - handle the validation errors
        const errorData = await response.json();
        console.error("Validation errors:", errorData);
    }
}

