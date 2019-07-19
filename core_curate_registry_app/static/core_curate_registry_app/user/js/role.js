$(document).ready(function(){
    selectRole();
});

var selectRole = function(){
    // get role from page
    var role_choice = $("#role_choice").html();
    var role_type = $("#role_type").html();
    // role is not undefined
    if(role_choice && role_type){
        // find the option that contains the role label
        var option = $('option').filter(function () { return $(this).html() == role_choice; })[0];
        // get the value of the option
        var value = $(option).val();
        // switch the select to the value corresponding to the role
        $(option).parent('select').val(value).change();
        // find the option that contains the role label
        var option = $('option[value="'+ role_type +'"]')[0];
        // get the value of the option
        var value = $(option).val();
        // switch the select to the value corresponding to the role
        $(option).parent('select').val(value).change();

    }
}
