//ADDS CLASSES TO INPUT BOXES
document.getElementById("id_username").className = "input_textbox";
document.getElementById("id_first_name").className = "input_textbox";
document.getElementById("id_last_name").className = "input_textbox";
document.getElementById("id_email").className = "input_textbox";
document.getElementById("id_ORCID").className = "input_textbox";
document.getElementById("id_scientific_area").className = "input_textbox";
document.getElementById("id_password1").className = "input_textbox";
document.getElementById("id_password2").className = "input_textbox";

document.querySelector("#id_password1").parentElement.nextElementSibling.id = "password1_description";

//PLACES UL INSIDE CORRECT <p> ELEMENT
var password_info = document.getElementById("password1_description");
document.getElementById("id_password1").nextElementSibling.appendChild(password_info);


//  CHANGES THE LABELS OF THE INPUT BOXES
document.querySelector('label[for="id_username"]').innerHTML = "Username";
document.querySelector('label[for="id_first_name"]').innerHTML = "First name";
document.querySelector('label[for="id_last_name"]').innerHTML = "Last name";
document.querySelector('label[for="id_email"]').innerHTML = "E-mail";
document.querySelector('label[for="id_ORCID"]').innerHTML = "ORCID";
document.querySelector('label[for="id_scientific_area"]').innerHTML = "Research Interests";
document.querySelector('label[for="id_password1"]').innerHTML = "Password";
document.querySelector('label[for="id_password2"]').innerHTML = "Repeat Password";
