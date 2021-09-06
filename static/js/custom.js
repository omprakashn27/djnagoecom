$(document).ready(function () {

    
    $('.addToCartBtn').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('.product_data').find('input[name=csrfmiddlewaretoken]').val()

        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty' : product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                
                alertify.success(response.status);
            }
        });
    });

    $('.addToWishlistBtn').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('.product_data').find('input[name=csrfmiddlewaretoken]').val()

        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
            }
        });

    });

    $('.increment-btn').click(function (e) {
        e.preventDefault();

        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0 : value;
        if(value < 10)
        {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });

    $('.decrement-btn').click(function (e) {
        e.preventDefault();

        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if(value > 1)
        {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });

    $('.changeQuantity').click(function (e) {
        e.preventDefault();

        var prod_id = $(this).closest('.product_data').find('.prod_id').val();
        var qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('.product_data').find('input[name=csrfmiddlewaretoken]').val()

        data = {
            'product_id' : prod_id,
            'product_qty' : qty,
            csrfmiddlewaretoken: token
        }
        $.ajax({
            method: "POST",
            url: "update-cart",
            data: data,
            success: function (response) {
                window.location.reload();
            }
        });

    });

    $('.delete-cart-item').click(function (e) {
        e.preventDefault();

        var prod_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('.product_data').find('input[name=csrfmiddlewaretoken]').val()

        $.ajax({
            method: "POST",
            url: "delete-cart-item",
            data: {
                'product_id':prod_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
                setTimeout(
                    function() 
                    {
                        window.location.reload();
                    }, 2000);
            }
        });
    });

    
    $('.delete-wishlist-item').click(function (e) {
        e.preventDefault();

        var prod_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('.product_data').find('input[name=csrfmiddlewaretoken]').val()

        $.ajax({
            method: "POST",
            url: "/delete-wishlist-item",
            data: {
                'product_id':prod_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
                setTimeout(function(){
                    window.location.reload();
                }, 2000);
            }
        });
    });


});