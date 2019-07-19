$(document).ready(function(){
    $("#icons_table td").each(function(){
        $(this).on("click", action_click);
    }) ;
});

var action_click = function(event){
    var $td = $(event.target).closest('td');
    var slug = $td.attr("id").replace('td_','');
    var link_id = slug+"_link"
    window.location = $("#" + link_id).attr("href");
}