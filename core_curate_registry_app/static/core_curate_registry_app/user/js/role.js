$(document).ready(function(){
    selectRole();
});

// map role to exact label used in template
const template_roles = {
    'organization': 'Organization',
    'datacollection': 'DataCollection',
    'repository': 'DataCollection',
    'projectarchive': 'DataCollection',
    'database': 'Dataset',
    'dataset': 'Dataset',
    'service': 'ServiceAPI',
    'informational': 'WebSite',
    'software': 'Software',
};

// map role to exact label used in template (when role is in a 2nd enumeration)
const template_sub_roles = {
    'organization': {'label': 'Organization', 'index': 3},
    'repository': {'label': 'Collection: Repository', 'index': 0},
    'projectarchive': {'label': 'Collection: Project Archive', 'index': 0},
    'database': {'label': 'Dataset: Database', 'index': 0},

}

var selectRole = function(){
    // get role from page
    var role = $("#role").html();
    // role is not undefined
    if(role != undefined){
        // role is in the map
        if (role in template_roles){
            // find the option that contains the role label
            var option = $("option:contains('" + template_roles[role] + "')")[0];
            // get the value of the option
            var value = option.value;
            // switch the select to the value corresponding to the role
            $(option).parent('select').val(value).change();
            // if the role has a value in the second select
            if (role in template_sub_roles){
                // find the option that contains the role label
                var option = $("option:contains('" + template_sub_roles[role]['label'] + "')")[template_sub_roles[role]['index']];
                // get the value of the option
                var value = option.value;
                // switch the select to the value corresponding to the role
                $(option).parent('select').val(value).change();
            }
        }
    }
}
