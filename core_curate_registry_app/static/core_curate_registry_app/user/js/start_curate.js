$(document).ready(function(){
    load_start_form($("#template_id").html());
    $('#btn-display-data').on('click', function(){
        // start regular form processing
        displayTemplateProcess($("#btn-display-data > i"));

    });
    var MAX_INTERVAL_ITER = 5000;
    var iteration = 0;

    var interval = setInterval(function() {
        iteration++;
        if (iteration >= MAX_INTERVAL_ITER) clearInterval(interval);
        if ($("#form_start_content").text().length> 1) {
            clearInterval(interval);
            displayRoleTitle();
            }
    }, 100);

});

var displayRoleTitle = function() {
if ($("#role_title").text() != "")
    {
        role_title = "Create a new " + $("#role_title").text() + ":";
        $("#form_role_title").text(role_title);
    }
else
    {
        $("#form_role_title").text("Create a new resource :");
    }
}