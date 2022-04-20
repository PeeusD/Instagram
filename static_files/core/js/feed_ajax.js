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
// Ajax request for opening modals for specific post
  $(".seeComments").on("click", function () {
   
    let id = $(this).attr("data-sid");  //current custom class or attribute
    const csrftoken = getCookie('csrftoken');
    $("#myModal"+id).css("display", "block");
    // console.log("this is value >> "+ id);
    mydata = { pid: id,};

    $.ajax({
      url:   "comment/" + id + "/",
      method: "POST",
      headers: {'X-CSRFToken': csrftoken},
      dataType: "json",
      data: "mydata",
      success: (data) => {
        //converting json objects to js obj 
        data = JSON.parse(data);
        // console.log(data);
        $("#post_" + id).show(function () { //setting obj to HTML
          // console.log(data)
          for (i = 0; i < data.length; i++) {
        
            // username = "<span class='photo__author-username'>" + data[i]["model"] + ":</span> ";
            obj = " <span class='photo__author-comment'>" +'<b>User:</b>'+ data[i]["fields"]["user"] + data[i]["fields"]["text"] + "</span><br/> ";
            $("#post_" + id).append(obj);
          }

        });

      },

      error: (error) => {
        console.log(error);
      },


    });
  });



  //Modal Section

  // When the user clicks on <span> (x), close the modal
  $(".closeModal").on("click", function () {
    
    let id = $(this).attr("data-sid");
    if(id){
      $("#myModal"+id).css("display", "none");
      $("#post_" + id).html("");   //making blank every time user click close btn
    }
     
  });

 
  //Ajax request for comment box posting  .fa-paper-plane
  $(".send-cmt").on("click", function () {
    let id = $(this).attr("data-sid");  //current custom class or attribute
    // let csr = $("#myModal"+id).find("input[name='csrfmiddlewaretoken']").attr("value");
    
    const csrftoken = getCookie('csrftoken');
    let txt = $("#myModal"+id).find('textarea').val();
    
    // console.log("this is value >> "+ csrftoken);
    // console.log("this is value >> "+ txt);
    // console.log("this is value >> "+ id);
    
    if (txt){  //checks if there is any comment send request
      $("#post_" + id).html("");   //making blank every time user sends req
      $.ajax({
        url:   "comment/" + id + "/", //"{% url 'post_comment_view' %}",
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        dataType: "json",
        data:{"myData":txt},
        success: (data) => {
          //converting json objects to js obj 
          data = JSON.parse(data);
          // console.log(data);
          $("#post_" + id).show( function () { //setting obj to HTML
            // console.log(data)
            for (i = 0; i < data.length; i++) {
              // username = "<span class='photo__author-username'>" + data[i]["model"] + ":</span> ";
              obj = " <span class='photo__author-comment'>" + data[i]["fields"]["user"] + data[i]["fields"]["text"] + "</span><br/> ";
              $("#post_" + id).append(obj);
            }

          });

        },
        error: function (request, status, error) {
          alert(request.responseText);
        }

      }); 
      $("#myModal"+id).find('textarea').val("");  //clean txtarea after sending ajax request
    };
    
  });



// Ajax request for adding likes/dislikes
$(".fa-heart").on("click", function () {
   
  let id = $(this).attr("data-sid");  //current custom class or attribute
  const csrftoken = getCookie('csrftoken');

  $.ajax({
    url:   "post/like/" + id + "/",
    method: "POST",
    headers: {'X-CSRFToken': csrftoken},
    dataType: "json",

    success: (data) => {

      // console.log(data["Exists"])
      if (data["Exists"]){
        console.log("liked exists");
      }
      else {
        $("#photo__likes"+id).text(data["Created"]+" likes")
        console.log("liked created");
      }
      
    },

    error: (error) => {
      console.log(error);
    },

  });
});

});




