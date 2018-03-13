$(function(){
    var search_box = $("#spotify-search");
    var delay = (function(){
        var timer = 0;
        return function(callback, ms){
            clearTimeout (timer);
            timer = setTimeout(callback, ms);
        };
    })();
    function spotify_update(){
        if (search_box.val()===""){
            return;
        }
        console.log(search_box.val());
        $.ajax({
            url: search_url,
            dataType: "json",
            data: {
                track: search_box.val()
            }
        }).done(function(data){
            var suggestions = data.tracks;
            $(".result").remove();
            if (suggestions) {
                for (var s in suggestions) {
                    var track = suggestions[s];
                    var container = $("#result--1").clone(true);
                    container.attr("id", "result-" + s);
                    container.attr("data-name", track.track_name);
                    container.attr("data-album", track.album);
                    container.attr("data-uri", track.spotify_uri);
                    container.attr("data-art", track.artwork_url);
                    container.attr("data-artist", track.artist);
                    container.addClass("result");
                    container.find(".result-head").text(track.track_name + " - " + track.artist);
                    container.find(".result-sub").text(track.album);
                    container.find(".result-img").attr("src", track.artwork_url);
                    container.find("#result--1").attr("id", "result-" +s);
                    container.removeClass("d-none");
                    $("#spotify-results").append(container);
                }
            } else {
                $("#spotify-results").append("<div class='result'>No results found</div>")
            }
        });
    }
    $("#result--1").on("click",function(e){
        var id_data_map = {"track_name": this.dataset.name,
                           "artist": this.dataset.artist,
                           "album": this.dataset.album,
                           "spotify_uri":this.dataset.uri,
                           "artwork_url": this.dataset.art};
        for (var attr in id_data_map) {
            var value = $("#id_"+attr);
            value.val(id_data_map[attr]);
            value.prop("disabled", true);
        }
        return false;
    });
    search_box.on("change", spotify_update);
    search_box.on("keypress", function(){delay(function(){spotify_update();},200)});
    $("#add-clear").on("click", function(){
        var inputs = $("#add-song-form").find("input");
        inputs.val("");
        inputs.prop("disabled", false)
    });
    $("#add-song-modal").on("show.bs.modal", function(){
        search_box.val(search_term);
        spotify_update();
    });
    $("#add-song-form").on("submit", function(e){
        e.preventDefault();
        var data = {};
        var inputs = $(e.target).find("input");
        inputs = inputs.each(function(a){
            var input = $(inputs[a]);
            data[input.attr("name")] =  input.val();
        });
        console.log(inputs);
        $.ajax({
            url: add_endpoint,
            data: data,
            type: "post",
            dataType: "text"
        }).done(function(data){
            $("#add-song-modal").modal("hide");
            alert("SAVED");
        })
    })
});
