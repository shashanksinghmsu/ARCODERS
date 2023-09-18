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



// may be for updating the data
$(".update").click(function () {

    console.log('function called!')
    var title, data

    title = $(this).parent().parent().children("td:first-child").text();
    data = $(this).parent().parent().children(".data").text();

    data = data.replace(/\s+/g, " ").replace(/^\s|\s$/g, "");

    if ($(this).parent().hasClass('experience-content')) {

        title = 'About'
        data = $('.education-description').text()

    }




    $("#newData").attr("placeholder", "Enter new " + title)
    $("#previousData").val(data)
    $(".modal-title").text(title);
    $('#newData').attr('name', title.toLowerCase())

    $('#newData').removeClass()
    $('#newData').addClass("form-control loginStyle")
    $('#newData').addClass(title.toLowerCase())
    $(".username-status").remove();

    $("#updateModal").modal()


    // updating url

    link = '/update/update_'.concat(title.toLowerCase())
    link = link.concat('/')
    $("#update").attr('action', link)
})

$('#previousData').keydown(function (e) {
    e.preventDefault();
    return false;
});





// profile info js

function privacy_check() {
    var privacy = document.getElementById('id_privacy')
    var privacy_value = !privacy.checked
    privacy.checked = privacy_value
    privacy_submit()
}



function privacy_submit() {
    var privacy = document.getElementById('id_privacy')
    var data = privacy.checked
    var form = document.getElementById('privacy_form')
    form.submit()
}

// calling the modal
$("#privacy_info").click(function () {
    $("#privacy_modal").modal()
})



// header js
// calling the modal
$("#image_upload").click(function () {
    $("#image_modal").modal()
})




