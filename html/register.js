
document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault();
    submitForm();
});
// async function submitForm() {
   
//     const name = document.getElementById("name").value;
//     const email = document.getElementById("email").value;
//     const password = document.getElementById("password").value;
//     const phone = document.getElementById("phone").value;
//     const pan = document.getElementById("pantxt").value;
//     const aadhar = document.getElementById("aadhartxt").value;

//     // Debugging logs
//     console.log("Name:", name);
//     console.log("Email:", email);
//     console.log("Password:", password);
//     console.log("Phone:", phone);
//     console.log("PAN:", pan);

//     const aadharFile = document.getElementById("aadharfile").files[0];
//     const panFile = document.getElementById("panfile").files[0];
//     const photoFile = document.getElementById("photo").files[0];

//     // const pdfFile = document.getElementById("pdf").files; // New line

//     const formData = new FormData();
//     formData.append("aadharimg", aadharFile);
//     formData.append("panimg", panFile);
//     formData.append("photo", photoFile);
//     // formData.append("pdf_file", pdfFile); // New line

//     const data = {
//         name:name,
//         email:email,
//         password:phone,
//         phone:phone,
//         pan:pan,
//         aadhar:aadhar
//     };

//     formData.append("data", new Blob([JSON.stringify(data)], { type: "application/json" }));
//     console.log("form data",data)

//     try {
//         const response = await fetch('http://127.0.0.1:8000/register/', {
//             method: 'POST',
//             body: formData,
//         });

//         if (response.ok) {
//             const responseData = await response.json();
//             console.log("Response from server", responseData);
//         } else {
//             const errorData = await response.json();
//             console.error("Validation errors", errorData);
//         }
//     } catch (error) {
//         console.error("Error during the fetch operation", error);
//     }
// }
async function submitForm() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const phone = document.getElementById("phone").value;
    const pan = document.getElementById("pantxt").value;
    const aadhar = document.getElementById("aadhartxt").value;

    const aadharFile = document.getElementById("aadharfile").files[0];
    const panFile = document.getElementById("panfile").files[0];
    const photoFile = document.getElementById("photo").files[0];

    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("phone", phone);
    formData.append("pan", pan);
    formData.append("aadhar", aadhar);
    formData.append("aadharimg", aadharFile);
    formData.append("panimg", panFile);
    formData.append("photo", photoFile);

    try {
        const response = await fetch('http://127.0.0.1:8000/register/', {
            method: 'POST',
            body: formData,
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
