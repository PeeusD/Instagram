//This function is for CSRF processing....
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

$(document).ready(function () {

    // Ajax request for Deleting Current user's Post
    $(".fa-trash").on("click", function () {

        let id = $(this).attr("data-sid");  //current custom class or attribute
        const csrftoken = getCookie('csrftoken');
        $("#myModal" + id).css("display", "block");
        console.log("this is value >> "+ id);
        console.log("this is CSRF >> "+ csrftoken);
    
    });

    // When the user clicks on <span> (x), close the modal
    $(".no-btn").on("click", function () {
     
        let id = $(this).attr("data-sid");
        if (id) {
            $("#myModal" + id).css("display", "none"); 
        }

    });




});