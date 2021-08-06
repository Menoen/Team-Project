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
        var catname;
        catname = $(this).attr("data-catname");
        $.get('/rango/like/', {category_catname: catname}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });
});