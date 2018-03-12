$(function(){
    $("#spotify-search").on("change", function(){
        $.ajax({
            url: search_url,
            dataType: "json",
            data: {
                track: $("#spotify-search").val()
            }
        }).done(function(data){
            console.log(data);
            var suggestions = data.tracks;
            console.log(suggestions);
            for(var s in suggestions){
                var track = suggestions[s];
                console.log(track.track_name);
                var container = $("#result--1").clone();
                container.attr("id","result-"+s);
                container.find(".result-head").text(track.track_name + " - " +track.artist);
                container.find(".result-sub").text(track.album);
                container.find(".result-img").attr("src", track.artwork_url);
                container.removeClass("d-none");
                $("#spotify-results").append(container);
            }
        });
    });
});
