$( function(){

    // Initially the form should not be visible
    $("#review-form").hide();
    $("#submit-review").hide();

    $("#add-review").on("click", function(){
        $.ajax({
            url: "{% url 'review' %}",
            data: {
                submit:false,
                url:window.location.pathname // So the view can look up reviews for the song
            },
            success: function(data) {
                //Fill the review form with the original review (for editing)
                $("#review-message").val(data.prev_comment.message);

                // Add all possible options (may have changed since last review)
                $.each(data.reactions, function(i,choice){
                    $("#review-reaction").append($("<option>",{
                        value: choice[0],
                        text: choice[1]
                    }));
                });
                // Preselect the prev. reaction
                $("#review-reaction").val(data.prev_comment.reaction);
            },
        })

        $("#submit-review").show();
        $("#review-form").show(400,"swing");
        $("#add-review").hide();
    })

    $("#submit-review").on("click", function(){
        console.log({review:{message:$("#review-message").val(),reaction:$("#review-reaction").val()}});
        $.ajax({
            url: "{% url 'review' %}",
            data: {
                submit:true,
                url:window.location.pathname,
                message:$("#review-message").val(),
                reaction:$("#review-reaction").val()
            },
            success: function(data) {

            }
        })
    })

})
