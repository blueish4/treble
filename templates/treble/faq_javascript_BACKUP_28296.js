$(function(){
    $(".info").hide();
<<<<<<< HEAD
    $(".title").click( function () {
=======
    $(".title").on("click", function(){
>>>>>>> b6280b8584aca870f5cbf58951c3b076232004be

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

<<<<<<< HEAD
        $(this).find('.info').slideToggle();
=======
      $(this).find('.info').toggle('slide', {
        duration: 1000,
        direction: 'up'
      });
>>>>>>> b6280b8584aca870f5cbf58951c3b076232004be

    });
})
