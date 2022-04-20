function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }



  $(document).ready(function() {
// Logout ajax request


  $(".corner-avatar").click(function () {
    $(".settings-menu").toggleClass("settings-menu-height");
  
  });
  
  $(".dark-btn").click(function () {
    $(".dark-btn").toggleClass("dark-btn-on");
    $("body").toggleClass("dark-mode");
    $(".navigation__column:first-child img").toggleClass("logo-grayscale");
    // $(".dark-btn span").toggleClass("bckgd-color");
    if(localStorage.getItem("theme") == "light"){ 
      localStorage.setItem("theme", "dark");
     }
     else{
      localStorage.setItem("theme", "light");
     }

  });

//local storage for light-dark mode
if(localStorage.getItem("theme") == "light"){  
  $(".dark-btn").removeClass("dark-btn-on");
  $("body").removeClass("dark-mode");
  $(".navigation__column:first-child img").removeClass("logo-grayscale");
}
else if(localStorage.getItem("theme") == "dark"){ 
  $(".dark-btn").addClass("dark-btn-on");
  $("body").addClass("dark-mode");
  $(".navigation__column:first-child img").addClass("logo-grayscale");
}
else{
  localStorage.setItem("theme", "light");
}



  // $(".log-out").on("click", function () {
   
  //   const csrftoken = getCookie('csrftoken');

  //   $.ajax({
  //     url:   "/logout/",
  //     method: "POST",
  //     headers: {'X-CSRFToken': csrftoken},
  //     dataType: "json",
  //     success: (data) => {
      
  //     },


  //     error: (error) => {
  //       console.log(error);
  //     },
  
  //   });
  // });


});


//screeen Dark/Light Mode
// function toggle(){
//   document.body.classList.toggle('dark');
//   }

// let darkBtn = document.getElementById("dark-btn");
// darkBtn.onclick = function(){
//   darkBtn.classList.toggle("dark-btn-on")
// }
