$(function() {
  $.widget("custom.catcomplete", $.ui.autocomplete, {
    _create: function() {
      this._super();
      this.widget().menu("option", "items", "> :not(.ui-autocomplete-category)");
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
        li = that._renderItemData(ul, item);
        if (item.category) {
          li.attr("aria-label", item.category + " : " + item.label);

        }
      });
    }
  });


  $("#search").catcomplete({
      delay: 0,
      source: function(request, response) {
        $.ajax({
          url: "{% url 'navbar_search' %}",
          dataType: "jsonp",
          data: {
            search_term: request.term
          },
          success: function(data) {
            response(data);
          }
        });
      },
      select: function(event, ui) {
        log("Selected: " + ui.item.value + " aka " + ui.item.id);
      }

  });
});
