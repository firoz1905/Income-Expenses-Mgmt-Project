console.log("login is working")

const passwordField=document.querySelector("#passwordField");
const showPasswordToggle=document.querySelector(".showPasswordToggle");



//show password
const handleToggleInput=(e)=> {
    console.log('99999',99999);
    if (showPasswordToggle.textContent==="SHOW"){
        showPasswordToggle.textContent='HIDE';
        passwordField.setAttribute("type","text");
    }else{
        showPasswordToggle.textContent="SHOW";
        passwordField.setAttribute("type","password");
    }
}
showPasswordToggle.addEventListener("click",handleToggleInput); // This is like writing to another function where this function brings the event



