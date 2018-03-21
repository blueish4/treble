$( function(){
    $("#edit-comment-row").hide();
    $("#edit-comment").on("click", function(){
        $("#edit-comment-row").show(200);
        $("html, body").animate({
            scrollTop: $("#reviews").offset().top
            }, 200);
    })
})
