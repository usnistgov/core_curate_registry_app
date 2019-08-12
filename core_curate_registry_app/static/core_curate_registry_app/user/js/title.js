$(document).ready(function(){
    if (dataElements != "" )
    {
        getResourceName(dataElements);
    }
});

/**
Put the value of title into the resourceName field
@param dataElements jquery_selector of the resourceName
**/
var getResourceName = function(dataElements) {
    resourceName = $(dataElements)
    resourceName = $(resourceName.children().filter(":input"))
    title = $("#data_title").html();
    resourceName.val(title.trim());
    saveTitle(resourceName);
};

/**
Saves the input associated to the jquery selector
@param jquery_selector
**/
var saveTitle = function(jquery_selector) {

    var $input = $(jquery_selector);
    var inputId = $input.attr('id');

    console.log('Saving element ' + inputId + '...');
    $.ajax({
        'url': dataStructureElementUrl,
        'type': 'POST',
        'dataType': 'json',
        'data': {
            'id': inputId,
            'value': $input.val()
        },
        success: function() {
            console.log('Element ' + inputId + ' saved');
        },
        error: function() {
            console.error('An error occurred when saving element ' + inputId);
        }
    });
};
