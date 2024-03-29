let slideIndex = 0;


function showSlides() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
 
  slides[slideIndex-1].style.display = "block";  
  setTimeout(showSlides, 3000); // Change image every 3 seconds
}

// Run function when page loads
window.onload=showSlides;


$(document).ready(function() {



	//local storage for light-dark mode -auto load page settings
	if(localStorage.getItem("theme") == "light"){  
		$("body").removeClass("dark-mode");
		$(".login__logo").removeClass("logo-grayscale");

	}
	else if(localStorage.getItem("theme") == "dark"){ 
		$("body").addClass("dark-mode");
		$(".login__logo").addClass("logo-grayscale");
	}
	else{
		localStorage.setItem("theme", "light");
	}


	//Enable / Disbale login button when typing on text box

	$("#password_txtbox").keyup(function () {
		//Reference the Button.
		var btnLogin = $("#btnLogin");

		//Verify the TextBox value.
		if ($(this).val().trim() != "") {
			//Enable the TextBox when TextBox has value.
			btnLogin.removeAttr("status");
		} else {
			//Disable the TextBox when TextBox is empty.
			btnLogin.attr("status", "disabled");
		}
	});



});