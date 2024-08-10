function loadSignUp(){
    fetch("/signup-content")
    .then(response => response.json())
    .then(data => {
        document.getElementById("DynamicContent").innerHTML = data.html;
    });
}
function loadSignIn(){
    fetch("/signin-content")
    .then(response => response.json())
    .then(data => {
        document.getElementById("DynamicContent").innerHTML = data.html;
    });
}