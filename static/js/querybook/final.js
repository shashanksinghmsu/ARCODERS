function like_html(user_like, id, like_count) {
    if (user_like == true) {
        var like_data = `<div id="like${id}"><span class="fa fa-heart liked${id} solution_card_like" aria-hidden="true"></span><span
            class="like_count${id}" style = 'color: dodgerblue;font-weight: bold;font-family: monospace;'> ${like_count} like${add_s(like_count)}</span></div>`
        return like_data
    }
    else {
        var like_data = `<div id="like${id}" style = 'color:dodgerblue;'><span class="fa fa-heart liked${id}" aria-hidden="true"></span><span
            class="like_count${id}" style = 'color: dodgerblue;font-weight: bold;font-family: monospace;'> ${like_count} like${add_s(like_count)}</span></div>`
        return like_data
    }
}

