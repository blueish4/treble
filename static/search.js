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
                // TODO disable the manual inputs, but set their values on select
                for (var s in suggestions) {
                    var track = suggestions[s];
                    var container = $("#result--1").clone();
                    container.attr("id", "result-" + s);
                    container.addClass("result");
                    container.find(".result-head").text(track.track_name + " - " + track.artist);
                    container.find(".result-sub").text(track.album);
                    container.find(".result-img").attr("src", track.artwork_url);
                    container.removeClass("d-none");
                    $("#spotify-results").append(container);
                }
            } else {
                $("#spotify-results").append("<div class='result'>No results found</div>")
            }
        });
    }
    search_box.on("change", spotify_update);
    search_box.on("keypress", function(){delay(function(){spotify_update();},200)});
    $("#add-song-modal").on("show.bs.modal", function(){
        search_box.val(search_term);
        spotify_update();
    })
});
