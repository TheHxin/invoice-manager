authenticationForm.addEventListener("submit" , async (e) => {
    const data = {
      username : document.getElementById("username").value,
      password : document.getElementById("password").value
    };

    e.preventDefault();
    try{
      await fetch("http://127.0.0.1:8000/token_json" , {
        method : "POST",
        headers: { 
          'Content-Type': 'application/json'
         },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        localStorage.setItem("token", data.access_token);
      });

    } catch(err) {
      console.error("Login failed for some fucking reason", err);
    }
  });