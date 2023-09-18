
// handle custom message
var msgBox = document.getElementById('message-box')

function message(msg) {
    msgBox.classList.add("alert", "alert-danger", "mb-0", "alert-dismissible", "fade", "show", "message");

    msgBox.innerHTML = `<strong> Message: </strong> ${msg}
            <button type = "button" class= "close" id="close-msg-box" data - dismiss="alert" aria - label="Close">
        <span aria-hidden="true">×</span>
    </button>`

    var closeMsg = document.getElementById('close-msg-box')
    closeMsg.addEventListener('click', function () {
        msgBox.classList.remove("alert", "alert-danger", "mb-0", "alert-dismissible", "fade", "show", "message");
        msgBox.innerHTML = ''
    })
}



