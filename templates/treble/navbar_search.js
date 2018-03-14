$(function() {
  document.getElementById("search_button").onclick = function search(request, response){
    var full_search = document.getElementById("search").value;

    for(i=0; i<2; i++){
          $.each(result[i]['label'], function(index, item) {
            if (full_search == item['track_name']){
              id = item['song_id'];
              $.ajax({
                  url: "/treble/song/"+id,
                  data: {
                      search_term: request.term
                  },
                  success: window.location.replace("/treble/song/"+id)
              });

            }
            else if (full_search == item['username']){
              slug = item['username_slug'];
              $.ajax({
                  url: "/treble/user/"+slug,
                  data: {
                      search_term: request.term
                  },
                  success: window.location.replace("/treble/user/"+slug)
              });
            }
          });
    }
  }

    $.widget("custom.catcomplete", $.ui.autocomplete, {
        _create: function() {
        this._super();
        this.widget().menu("option", "items", "> :not(.ui-autocomplete-category)");
    },
    _renderItemSong: function(ul, item){
        var newHtml = "<div class='ui-menu-item-wrapper'><div class='search-menu-song'>" + item.track_name + "</div><div class='search-menu-artist'>by " + item.artist + "</div></div>";
        return $("<li>").data("ui-autocomplete-item",{"label":item.track_name,"value":item.track_name}).append(newHtml).appendTo(ul);
    },
    _renderItemUser: function(ul, item){
        var newHtml = "<div class='ui-menu-item-wrapper'><div class='search-menu-song'>" + item.username;
        return $("<li>").data("ui-autocomplete-item",{"label":item.username,"value":item.username}).append(newHtml).appendTo(ul);
    },
    _renderMenu: function(ul, items) {
        var that = this,
        currentCategory = "";
        $.each(items, function(index, item) {
            var li;
            if (item.category != currentCategory) {
                ul.append("<li class='ui-autocomplete-category'>" + item.category + "</li>");
                currentCategory = item.category;
            }

            if (item.category) {
                if(item.category == "Song"){
                    $.each(item.label,function(key,value){
                        li = that._renderItemSong(ul, value);
                    })
                } else {
                    $.each(item.label,function(key,value){
                        li = that._renderItemUser(ul, value);
                    })
                }
            }
        });
    }
  });
  $("#search").catcomplete({
      delay: 0,
      source: function(request, response) {
        $.ajax({
            url: "{% url 'navbar_search' %}",
            data: {
                search_term: request.term
            },
            success: function(data) {
                result = data;
                response(data);
            },
        });
      },
      select: function(event, ui) {
      }
  });


});
