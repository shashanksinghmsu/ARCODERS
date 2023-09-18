$("#halfstarsReview").rating({
    "half": true,
    "click": function (e) {
        console.log(e);
        $("#halfstarsInput").val(e.stars);
    }
});



var rate = $('#halfstarsInput').val()

for (var i = 1; i <= rate; i++) {
    var str1 = "#halfstarsReview i:nth-child(".concat(i)
    var str = str1.concat(')')
    $(str).removeClass('far')
    $(str).addClass('fas')

}
if (rate - (i - 1) == 0.5) {
    var str1 = "#halfstarsReview i:nth-child(".concat(i)
    var str = str1.concat(')')
    $(str).removeClass('far fa-star')
    $(str).addClass('fas fa-star-half-alt')

}



// console.log('Rating.js is loaded')
