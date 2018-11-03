document.getElementById("nav_bar_profile").addEventListener("click", RevealProfile);
document.getElementById("nav_bar_search").addEventListener("click", RevealSearchBar);
document.querySelector("#nav_bar_profile > img").addEventListener("mouseover", changeProfileLogo);
document.querySelector("#nav_bar_profile > img").addEventListener("mouseleave", changeProfileLogo);
document.querySelector("#nav_bar_profile > img").addEventListener("click", changeProfileLogo);
document.querySelector("#nav_bar_search > img").addEventListener("mouseover", changeSearchLogo);
document.querySelector("#nav_bar_search > img").addEventListener("mouseleave", changeSearchLogo);
document.querySelector("#nav_bar_search > img").addEventListener("click", changeSearchLogo);
document.querySelector("#nv_search_submit").addEventListener("mouseover", changeSearchArrow);
document.querySelector("#nv_search_submit").addEventListener("mouseleave", changeSearchArrow);


var checker = true;
var checker_s = true;
var checker_c_s = true;
var checker_c_p = true;
var checker_s_a = true;


function RevealProfile() {
  if(checker){
    document.getElementById("nv_profile_card").style.pointerEvents = "all";
    document.getElementById("nv_profile_card").style.top = "154px";
    document.getElementById("nv_profile_card").style.opacity = "1";
    checker = false;
  } else {
    document.getElementById("nv_profile_card").style.top = "0";
    document.getElementById("nv_profile_card").style.opacity = "0";
    document.getElementById("nv_profile_card").style.pointerEvents = "none";
    checker = true;
  }
}
function RevealSearchBar() {
  if(checker_s){
    document.getElementById("nv_search_input").style.width = "150px";
    document.getElementById("nv_search_input").style.opacity = "1";
    document.getElementById("nv_search_submit").style.width = "18pt";
    document.getElementById("nv_search_submit").style.opacity = "1";
    checker_s = false;
  } else {
    document.getElementById("nv_search_input").style.width = "0px";
    document.getElementById("nv_search_input").style.opacity = "0";
    document.getElementById("nv_search_submit").style.width = "0px";
    document.getElementById("nv_search_submit").style.opacity = "0";
    checker_s = true;
  }
}
function changeProfileLogo() {
  if(checker_c_s){
    document.querySelector("#nav_bar_profile > img").src="{% static 'profile_icon_black.png' %}";
    checker_c_s = false;
  } else {
      document.querySelector("#nav_bar_profile > img").src="{% static 'profile_icon_black.png' %}";
    checker_c_s = true;
  }
}
function changeSearchLogo() {
  if(checker_c_p){
    document.querySelector("#nav_bar_search > img").src="{% static 'search_icon.png' %}";
    checker_c_p = false;
  } else {
      document.querySelector("#nav_bar_search > img").src="{% static 'search_icon_black.png' %}";
    checker_c_p = true;
  }
}

function changeSearchArrow() {
  if(checker_s_a){
    document.querySelector("#nv_search_submit").src="{% static 'search_arrow_hover.png' %}";

    checker_s_a = false;
  } else {
      document.querySelector("#nv_search_submit").src="{% static 'search_arrow.png' %}";
    checker_s_a = true;
  }
}
