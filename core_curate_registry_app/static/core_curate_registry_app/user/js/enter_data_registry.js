/**
 * Display the save form modal
 */
var sendSaveRequest = function() {
    $("#save-form-modal").modal("hide");
    var objectID = $("#curate_data_structure_id").html();
    $.ajax({
        url: saveFormUrl,
        type: 'POST',
        data: {
            'id': objectID
        },
        dataType: 'json',
        success: function(data) {
            $.notify(data.message, { style: data.tags });
        },
    });
};

/**
 * Notify the download
 */
var downloadMessage = function() {
    $.notify("Download in progress", "info");
};

/**
 * Shows the review data dialog
 */
var reviewDataDialog = function() {
    $("#xml-valid-registry-modal").modal("show");
};

$(document).on('click', '.btn.save-form-registry', sendSaveRequest);
$(document).on('click', '.btn.download-registry', downloadMessage);


