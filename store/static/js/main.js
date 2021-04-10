const pesoSign = '₱' 
function updateCart(action, productId) {
  $.ajax({
    method: "POST",
    url: "/update_cart/" + productId,
    data: {
      // must be the input id
      action: action,
      quantity: 1,
      csrfmiddlewaretoken: csrftoken,
    },
    success: function (res) {
      cartItems = res[0]
      totalProductQty = res[1]
      cartTotal = res[2]

      $("#cartTotal").text(cartItems);
      $(`#processQty${productId}`).text(totalProductQty)
      $(".tmpAmount").text(pesoSign+cartTotal);
      
      if(totalProductQty <= 0 ){
        console.log(productId)
        $(`.product${productId}`).remove()
        console.log('Delete this list')
      }
    },
  });
}



$(document).ready(function () {
  
  $(".filter-category").click(function () {
    const value = $(this).attr("data-filter");
    if (value == "all") {
      $(".product").show("1000");
    } else {
      $(".product")
        .not("." + value)
        .hide("1000");
      $(".product")
        .filter("." + value)
        .show("1000");
    }
  });
  $(".filter-category").click(function () {
    $(this)
      .parent(".nav-item")
      .addClass("active")
      .siblings()
      .removeClass("active");
  });

  $("#addToCartForm").submit(function (e) {
    e.preventDefault();
    let qty = $("#addToCartQty").val();
    var productId = $(this).attr("data-product");

    var endpoint = "/add_to_cart/" + productId;
    $.ajax({
      method: "POST",
      url: endpoint,
      data: {
        // must be the input id
        quantity: qty,
        csrfmiddlewaretoken: csrftoken,
      },
      success: function (res) {
        $("#cartTotal").text(res);
        console.log("Successful post");
      },
    });
  });

  $(".iconshit").click(function () {
    var action = this.dataset.action;
    var productId = $(this).attr("id");
    console.log(action);
    updateCart(action, productId);

    // Check order status
    var order_stat = $(".track").attr("order-status")
    console.log(order_stat)

  });

  $("#checkoutForm").submit(function(e){
      e.preventDefault();
      $("#paypal-button-container").show(500)
      $("#checkoutBtn").hide()
     
  })
  



});
