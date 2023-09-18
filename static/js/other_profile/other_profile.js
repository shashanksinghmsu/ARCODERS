// if (window.screen.width <= 360){
var scwidth = window.screen.width / 4
$(".scroller").css("width", scwidth)
$(".scroller").css("overflow-x", "scroll")
// }
$(".headerscroll").css("width", "auto")

if ($(".languages").width() <= 112) {
    $(".headerscroll").css("max-width", "130px")
}
if (window.screen.width <= 360) {
    $(".header").css("padding-top", "50px")
}


