$(document).ready(function() {
    $(".dropdown-content a").click(function(){
        var songName = this.innerHTML;
        document.getElementById("drop").innerText = songName;
        });
});
