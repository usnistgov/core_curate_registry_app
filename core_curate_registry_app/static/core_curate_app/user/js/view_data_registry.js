/**
 * Load controllers for view data
 */
$(document).ready(function(){
    $('.btn.save-to-repo-registry').on('click', saveToRepositoryRegistry);
    $('.btn.publish').on('click', publish);
});

/**
 * AJAX, to start form save
 */
var displaySaveForm = function(){
    $("#save-form-registry-modal").modal({
            show: true,
    		backdrop: 'static',
    		keyboard: false
		});
    $(".close").hide();
    $("#save-form-registry-modal").modal("show");
};

/**
 * Saves the data.
 */
var saveToRepositoryRegistry = function(){
   var objectID = $("#curate_data_structure_id").html();
   $.ajax({
        url : saveDataUrl,
        type: 'POST',
        data: {
          'id': objectID
        },
        dataType: 'json',
        success : function(data) {
        $("#data_id").html(data.data_id);

        displaySaveForm();
        },
        error: function(data){
            XMLDataSavedError(data.responseText);
        }
    });
};

/**
 * Saved XML data to DB error message.
 * @param errors
 */
var XMLDataSavedError = function(errors){
    var $saved_error_modal = $("#save-error-modal");
    $("#saveErrorMessage").html(errors);
    $saved_error_modal.modal("show");
};

/**
 * Publish the data
 */
function publish(){
   var objectID = $("#data_id").html() ;

    $.ajax({
        url : publishUrl,
        type : "POST",
        dataType: "json",
        data : {
            "data_id": objectID
        },
        success: function(data){
            window.location = curateIndexUrl;
        },
        error:function(data){
            var myArr = JSON.parse(data.responseText);
            $.notify(myArr.message, {style: myArr.tags });
        }
    });
}
