$(function(){
    $(".info").hide();
    $(".title").on("click", function(){

      var end = $(this).find(".title-text").text().slice(-3);
      var rest_of_text = $(this).find(".title-text").text().slice(0,-3);
      var replace;
      if (end == "[+]"){
        replace = rest_of_text + "[-]";
      }
      else{
        replace = rest_of_text + "[+]"
      }
      $(this).find(".title-text").text(replace);

      $(this).find('.info').toggle('slide', {
        duration: 1000,
        direction: 'up'
      });

    });
})
