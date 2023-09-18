
async function notify(title, text, redirect_url) {
    // create and show the notification
    // function showNotification(title, text) {
        const showNotification = () => {
            // var title = 'ARCODERS'
            // var text = 'This is a test notification'
            // var redirect_url = 'http://127.0.0.1:8000/contact/'
            var icon_link = 'http://127.0.0.1:8000/static/images/logo/test.png'

        // create a new notification
        const notification = new Notification(title, {
            body: text,
            icon: icon_link
        });

        // close the notification after 10 seconds
        setTimeout(() => {
            notification.close();
        }, 5 * 1000);

        // navigate to a URL when clicked
        notification.addEventListener('click', () => {

            window.open(redirect_url);
            // window.open(redirect_url, '_blank');
        });
    }

    // show an error message
    const showError = () => {
        const error = document.querySelector('.error');
        error.style.display = 'block';
        error.textContent = 'You blocked the notifications';
    }

    // check notification permission
    let granted = false;

    if (Notification.permission === 'granted') {
        granted = true;
    } else if (Notification.permission !== 'denied') {
        let permission = await Notification.requestPermission();
        granted = permission === 'granted' ? true : false;
    }

    // show notification or error
    granted ? showNotification() : showError();

};

// notify('ARCODERS', 'This is notification', 'http://127.0.0.1:8000/contact/')