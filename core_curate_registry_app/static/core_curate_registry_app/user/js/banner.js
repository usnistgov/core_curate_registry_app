$(document).ready(function(){
    $("#icons_banner div").each(function(){
        $(this).on("click", action_click);
    }) ;
});

var action_click = function(event){
    var $td = $(event.target).closest('div');
    var slug = $td.attr("id").replace('cnt_','');
    var link_id = slug+"_link"
    window.location = $("#" + link_id).attr("href");
}