$(document).ready(function() {
    $('main #form_submit').submit(function() { // On form submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(data) { // on success..
            $('#refresh').html(data)// update the DIV
            },
            error: function(e) { // on error..
                $('#error_div').html(e); // update the DIV
            }
        });
        return false;
    });
    $('.my_form').submit(function() { // On form submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(data) { // on success..
            $('#refresh').html(data)// update the DIV
            },
            error: function(e, x, r) { // on error..
                $('#error_div').html(e); // update the DIV
            }
        });
        return false;
    });
    $(".submit_form").click(function(){
    $(".my_form").submit();
  });
  $('.my_form_order').submit(function() { // On form submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(data) { // on success..
            $('#refresh').html(data)// update the DIV
            },
            error: function(e, x, r) { // on error..
                $('#error_div').html(e); // update the DIV
            }
        });
        return false;
    });
    $('.my_form_order_shop').submit(function() { // On form submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(data) { // on success..
            $('#refresh').html(data)// update the DIV
            },
            error: function(e, x, r) { // on error..
                $('#error_div').html(e); // update the DIV
            }
        });
        return false;
    });
    $(".submit_form_shop").click(function(){
    $(".my_form_order_shop").submit();
  });
  $('.my_form_orders').submit(function() { // On form submit event
    $.ajax({ // create an AJAX call...
        data: $(this).serialize(), // get the form data
        type: $(this).attr('method'), // GET or POST
        url: $(this).attr('action'), // the file to call
        success: function(data) { // on success..
        $('#refresh').html(data)// update the DIV
        },
        error: function(e, x, r) { // on error..
            $('#error_div').html(e); // update the DIV
        }
    });
    return false;
});
$(".submit_form_orders").click(function(){
$(".my_form_orders").submit();
});
})