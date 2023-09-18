function category_language() {
    var final_value = '';
    for (var i = 0; i < lang_all.length; i++) {
        final_value += `<a class="dropdown-item" type="button" href='${change_langauge_url}${change_csharp_slug(lang_all[i].pk)}/?next=${pathname}'> ${lang_all[i].pk}</a>`
    }
    return final_value;
}

function language_selected(category_language_selected) {
    if (category_language_selected == '') {
        return 'All';
    } else {
        return category_language_selected;
    }
}

var language_select_title = `            
        <h5 style="color: dodgerblue;">
            Select the Language:
        </h5>`
var langauge_select = `
        <div class="dropdown" style="min-width:140px;width:300px;">
            <button class="btn btn-secondary dropdown-toggle arbuttons dropbtn search-box-field" type="button" data-toggle="dropdown" aria-haspopup="true" id='category_language_button' aria-expanded="false" style='color:dodgerblue !important;'>
                ${language_selected(category_language_selected)}
        <span class='fa fa-sort-down float-right'><span>
        </button>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenu2">
                        <a class="dropdown-item" type="button" href='${change_langauge_url}?next=${pathname}'> All</a>
        ${category_language()}
                    </div>
    </div>`

var category_language_select_container = document.getElementById('category_language_select_container');
category_language_select_container.innerHTML = language_select_title + langauge_select;
