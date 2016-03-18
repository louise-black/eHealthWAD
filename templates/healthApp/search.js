/*

{% extends "populate_healthApp.py" %}



$('#savePageModal')).click(function() {
	add_page(cat={{ category.name }},
        title={{ result.title }},
        url={{ result.link }})
}*/
<script>
$('.reserve-button').click(function(){

    var book_id = $(this).parent().data('id');

    $.ajax
    ({ 
        url: 'reservebook.php',
        data: {"bookID": book_id},
        type: 'post',
        success: function(result)
        {
            $('.modal-box').text(result).fadeIn(700, function() 
            {
                setTimeout(function() 
                {
                    $('.modal-box').fadeOut();
                }, 2000);
            });
        }
    });
});
</script>

$( '#savePageModal' ).click(function( event ) {
  event.preventDefault();

  var savePageModal = $( this );

  $.ajax({
    type: 'POST',
	cat={{ category.name }},
    title={{ result.title }},
    url={{ result.link }}

    dataType: 'json',
    success: function( resp ) {
      console.log( resp );
    }
  });
});