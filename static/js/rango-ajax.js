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

    $('#likes').click(function(){
        var catname;
        catname = $(this).attr("data-catname");
        $.get('/rango/like/', {category_name: catname}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });
});