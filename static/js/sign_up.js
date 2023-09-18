$(".neon").mouseover(function () {
    $(".neon").css("color", "#122647");
});
$(".neon").mouseout(function () {
    $(".neon").css("color", "dodgerblue");
});
$("#email").on('input', function () {
    if ($("#email").val().length != 0) {
        $("#spanEmail").css("transform", "translateY(-24px)");
        $("#spanEmail").css("color", " #1bfaad");

    }
    else {
        $("#spanEmail").css("transform", "translateY(0px)");
        $("#spanEmail").css("color", "rgba(255,255,255,0.5)");

    }
})
$(".contactForm").submit(function (e) {
    var form = this;
    e.preventDefault();
    setTimeout(function () {
        form.submit()
    }, 1200)
})





// username checker
$("#username").keyup(function () {
    var username = $(this).val();
    if (username != "") {
        $.ajax({
            url: '/username/',
            type: 'POST',
            data: { username: username }
        }).done(function (response) {
            // console.log(response);
            if (response == "True") {
                $(".username-status").remove();
                $("<small class='username-status'>Not Available</small>").insertAfter("#username-label");
            }
            else {
                $(".username-status").remove();
                $("<small class='username-status'>Available</small>").insertAfter("#username-label");
            }
        })
            .fail(function () {
                console.log("failed");
            })
    }
    else {
        $(".username-status").remove();
        console.log("done")
    }
});
