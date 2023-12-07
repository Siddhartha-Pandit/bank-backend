url='http://127.0.0.1:8000/openacc/'
document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault();
    submit();
});

async function submit(){
    let email = document.getElementById('email').value;
    let accountType = document.getElementById('accountType').value;
    let pan = document.getElementById('pan').value;
    let aadhar = document.getElementById('aadhar').value;
    let occupation = document.getElementById('occupation').value;
    let incomesource = document.getElementById('incomesource').value;
    let grossAnnualIncome = document.getElementById('grossAnnualIncome').value;

    console.log("Email Received:", email);
    console.log("Account Type Received:", accountType);
    console.log("PAN Received:", pan);
    console.log("Aadhar Received:", aadhar);
    console.log("Occupation Received:", occupation);
    console.log("Income Source Received:", incomesource);
    console.log("Gross Annual Income Received:", grossAnnualIncome);

    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify({
            email: email,
            accountType: accountType,
            pan: pan,
            aadhar: aadhar,
            occupation: occupation,
            incomeSource: incomesource,
            grossAnnualIncome: grossAnnualIncome
        }),
        headers: {
            "Content-type": "application/json;"
        }
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
    // response()

