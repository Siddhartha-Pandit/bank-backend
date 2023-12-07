
url='http://127.0.0.1:8000/login/'

async function submit(){
    mail=document.getElementById('email')
    console.log("Email Recived",mail)
    email=document.getElementById("email")
  
    

}

document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault();
    submit();
  });
  
  async function submit(){
      let email = document.getElementById('email').value;
      let password = document.getElementById('password').value;
      console.log("Email Received:", email);
      console.log("Password Received:", password);
      const response=await fetch(url,{
        method:"POST",
        body:JSON.stringify({
            email:email,
            password:password

        }),
        headers:{
            "Content-type":"application/json; charset=UTF-8"
        }
    
    })
    .then(response=>response.json())
    .then(json=>localStorage.setItem('token',json.token))
    var data=localStorage.getItem('token');
    document.cookie='token='+data;
  }
  