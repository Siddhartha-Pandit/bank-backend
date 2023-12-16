document.getElementById("myForm").addEventListener("submit",function(event){
    event.preventDefault();
    submit()
    
})
function register(){
    const formdata=new FormData('myForm')
    const data=Object.fromEntries(FormData)
    const jsonData=JSON.stringify(formData)
}

async function submit(){
    const formElement = document.getElementById('myForm');
    const formData = new FormData(formElement);
    console.log(formData);
    const response = await fetch('http://127.0.0.1:8000/register/',{
        method:'POST',
        body:formData
    });
    if(response.ok){
        const responseData = await response.json();
        console.log("Response from server", responseData);
    }  
    else{
        const errorData = await response.json();
        console.error("Validation errors", errorData);
    }
}

