document.getElementById("myForm").addEventListener("submit", function (event) {
    event.preventDefault();
    submit();
});

async function submit() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("password", password);

    try {
        const response = await fetch('http://127.0.0.1:8000/register/', {
            method: 'POST',
            body: formData,
            // Note: Do not manually set Content-Type when using FormData
        });

        if (response.ok) {
            const responseData = await response.json();
            console.log("Response from server", responseData);
        } else {
            const errorData = await response.json();
            console.error("Validation errors", errorData);
        }
    } catch (error) {
        console.error("Error during the fetch operation", error);
    }
}
