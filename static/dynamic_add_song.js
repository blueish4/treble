var add_song_callback = function (data) {
    var input = $("li:has(#id_"+form_id+"_0)").clone();
    var new_input_id = "id_"+form_id+"_" + $("li:has(input)").length;
    input.find("#id_"+form_id+"_0").attr("id", new_input_id);
    input.find("label").attr("for", new_input_id);
    input.children()[0].childNodes[1].textContent = "\n " + data.song_name;
    var input_formval = input.find("input");
    input_formval.val(data.song_id);
    $("#id_"+form_id).append(input);
};
$("#add_song").on("click", function () {
    // Close the recommendations modal, and add opening it back up as a closing callback
    var rec_modal = $("#add-rec-modal");
    rec_modal.modal("hide");
    rec_modal.on("hidden.bs.modal", function () {
        var song_modal = $("#add-song-modal");
        song_modal.modal("show");
        rec_modal.off("hidden.bs.modal");
        song_modal.on("hidden.bs.modal", function () {
            // reload the form with the added song
            $("#add-rec-modal").modal("show");
        })
    });
});