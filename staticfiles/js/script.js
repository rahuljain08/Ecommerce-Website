var slideIndex = 0;
// showSlides();

$.ajaxSetup({"headers": {
            "X-CSRFToken": getCookie('csrftoken')     
          }});

(function showSlides() {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1;}
  if(slideIndex<=slides.length){
    slides[slideIndex-1].style.display = "block";
  }
  setTimeout(showSlides, 5000); // Change image every 2 seconds
})();


function getCookie(name) {
    let cookieValue = null;
    // console.log(document.cookie);
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


function cart(productID, qty=null){
  // console.log("Reached");
  // console.log(getCookie('csrftoken'));

  if(!qty){
    qty = $("#qty").val();
  }
  
  if(qty > 5){
    alert("You can only buy a maximum of 5 products at once!");
    return;
  }

  $.post(
    "/products/buy/" + productID,
    {
      "qty": qty,
    },
    ()=>{
      $(".add_alert").css("display", "table"); 
    }
  )

};

function remove(itemID){

  $.post("/cart/remove/" + itemID,
          () => {
            window.location.reload();
          },
        )

}

function empty() {
  
  $.post("/cart/remove", 
        () => {
          window.location.reload()
        }
        )

}

$(".btn-close").click(() => {
  $(".add_alert").css("display", "none")
})



function buy(key = null){

  $.post(window.location.href, {"key": key}, () => {
    console.log("Successfully bought!");
  })

}


function cancelOrder(itemID){

  $.ajax({
    method: "DELETE",
    url: window.location.href,
    data: {
      "key": itemID
    }
  }).done(()=>{
      window.location.reload()
    })

}