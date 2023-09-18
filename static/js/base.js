$('article div .btn').each(function () {
    $(this).addClass('arbuttons')
    $(this).addClass('btn-small')
})


// function to prularize
function add_s(count) {
    if (count > 1) {
        return 's'
    }
    else {
        return ''
    }
}

// truncate to 10
function truncate(data) {
    return data.slice(0, 9)
}

function cap_first(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function round_off(number) {
    return parseFloat(number).toFixed(2);
}


function truncate_string(string, length){
    if (length > string.length) {
        return string;
    } else {
        string = string.substring(0, length);
        return string + "...";
    }
}