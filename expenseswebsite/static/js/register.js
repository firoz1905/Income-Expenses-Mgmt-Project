console.log("register is working")
const usernameFeedBackArea=document.querySelector(".usernameFeedbackArea");
const usernameField=document.querySelector("#usernameField");

const emailField=document.querySelector("#emailField");
const emailFeedbackArea=document.querySelector(".emailFeedbackArea");

const usernameSuccessOutput=document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");

const passwordField=document.querySelector("#passwordField");
const showPasswordToggle=document.querySelector(".showPasswordToggle");

const submitBtn=document.querySelector("#submitbtn");

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

// emailfield
emailField.addEventListener("keyup", (e) => {
    // This is like writing an anonymous function
    console.log('88888',88888);
    const emailVal=e.target.value;
    console.log(emailVal);

    emailSuccessOutput.style.display = "block";
    emailSuccessOutput.textContent = `Checking ${emailVal}`;
    
    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display = "none";

    if(emailVal.length>0){
        fetch("/authenticationapp/validate-email",{
        body:JSON.stringify({email:emailVal}),
        method:"POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data",data);
            emailSuccessOutput.style.display = "none";
            if(data.email_error){
                //is-invalid is a bootstrap class
                submitBtn.setAttribute('disabled','disabled');
                emailField.classList.add('is-invalid');
                emailFeedbackArea.style.display="block";
                emailFeedbackArea.innerHTML=`<p>${data.email_error}</p>`;
                //submitBtn.disabled = true;
            }
            else{
                submitBtn.removeAttribute("disabled");
            }
        });
    }
});

// Username field
usernameField.addEventListener('keyup',(e) => {
    console.log('777777',77777);
    const usernameVal=e.target.value; // STORING WHAT the user typed out
    console.log(usernameVal);

    // To say we are checking the username.Keep track of what user is entering
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;
    

    // resetts when the user made a mistake and start wiping it off
    usernameField.classList.remove('is-invalid');
    usernameFeedBackArea.style.display = "none";


    if(usernameVal.length>0){
        // JS has built in API called fetch
        fetch("/authenticationapp/validate-username",{
            // This would make an api call to the url with input as body and method POST
            // Json.stringify - turns JS object to a json so we can send over network
            body:JSON.stringify({username:usernameVal}),
            method:"POST",
            //fetch returns a promise so we write .then
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data",data);
            usernameSuccessOutput.style.display="none"; // we are hiding when it is correct
            if(data.username_error){
                //is-invalid is a bootstrap class that turns red
                submitBtn.setAttribute('disabled','disabled');
                usernameField.classList.add('is-invalid');
                usernameFeedBackArea.style.display = "block";
                usernameFeedBackArea.innerHTML = `<p>${data.username_error}</p>`; //Javascript way of template
                //submitBtn.disabled = true;
                
            }
            else{
                submitBtn.removeAttribute("disabled");
            }
        });
    }
    
});