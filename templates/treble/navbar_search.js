$(function() {
    $.widget("custom.catcomplete", $.ui.autocomplete, {
        _create: function() {
        this._super();
        this.widget().menu("option", "items", "> :not(.ui-autocomplete-category)");
    },
    _renderItemSong: function(ul, item){
        var newHtml = "<div class='ui-menu-item-wrapper'><div class='search-menu-song'>" + item.track_name + "</div><div class='search-menu-artist'>by " + item.artist + "</div></div>";
        return $("<li>").data("ui-autocomplete-item",{"label":item.track_name,"value":item.track_name}).append(newHtml).appendTo(ul);
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
                    li = that._renderItemData(ul, item);
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
                response(data);
            },
        });
      },
      select: function(event, ui) {
      }
  });
});
