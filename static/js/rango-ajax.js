$(document).ready(function() {

    $('#search-input').keyup(function() {
        var query;
        query = $(this).val();

        $.get('/rango/suggest',
              {'suggestion': query},
              function(data) {
                  $('#categories-listing').html(data);
              })
    });
    // add likes
    $('#likes').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/rango/like/', {category_id: catid}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });
    
    $("#likes").click(function(){
        $('#likes').hide();
    })
});