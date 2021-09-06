$(document).ready(function () {

    $('.razorpay_btn').click(function (e) { 
        e.preventDefault();

        var fname =  $("[name='fname']").val();   
        var lname =  $("[name='lname']").val();   
        var email =  $("[name='email']").val();   
        var phone =  $("[name='phone']").val();   
        var address1 =  $("[name='address1']").val();    
        var address2 =  $("[name='address2']").val();    
        var city =  $("[name='city']").val();    
        var state =  $("[name='state']").val();   
        var country =  $("[name='country']").val(); 
        var pincode =  $("[name='pincode']").val(); 
        var payment_mode =  "PayPal";
        var token = $('.container').find('input[name=csrfmiddlewaretoken]').val()
        data = {
            'fname':fname,
            'lname':lname,
            'email':email,
            'phone':phone,
            'address1':address1,
            'address2':address2,
            'city':city,
            'state':state,
            'country':country,
            'pincode':pincode,
            'payment_mode':payment_mode,
            csrfmiddlewaretoken: token
        }

        $.ajax({
            method: "POST",
            url: "/proceed-to-pay",
            data: data,
            success: function (response) {
                // alert(response.cart_total_price)
                var options = {
                    "key": "rzp_test_oRfSzsSGPgUAwU", // Enter the Key ID generated from the Dashboard
                    "amount": 1*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": response.fname+' '+response.lname,
                    "description": "Testing my Django Ecom Website",
                    "image": "https://example.com/your_logo",
                    // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (responsea){
                        // alert(responsea.razorpay_payment_id);
                        $.ajax({
                            method: "POST",
                            url: "/place-order",
                            data: {
                                'fname': response.fname,
                                'lname': response.lname,
                                'email': response.email,
                                'phone': response.phone,
                                'address1': response.address1,
                                'address2': response.address2,
                                'city': response.city,
                                'state': response.state,
                                'country': response.country,
                                'pincode': response.pincode,
                                'payment_mode': "Paid by Razorpay",
                                'payment_id':responsea.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                            },
                            success: function (response) {
                                window.location.href = "/orders"
                            }
                        });
                    },
                    "prefill": {
                        "name":  response.fname+' '+response.lname,
                        "email": response.email,
                        "contact": response.phone
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.open();
            }
        });
        

        
    });


});