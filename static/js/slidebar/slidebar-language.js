var contact_button = `        
        <li>
            <a href="/contact/">
                <span class="fa fa-address-card icon-menu"></span>
                Contact
            </a>
        </li>`

function generate_language_buttons_slidebar() {
    var html_data = ''
    for (var i = 0; i < lang_all.length; i++) {
        html_data += `
            <li class="item-submenu" menu='${i}'>
                <a href="#">
                    <span class="fa fa-laptop-code icon-menu"></span>
                    ${lang_all[i].pk}
                    <span class="fa fa-chevron-right slidebar-arrow-icon"></span>
                </a>

                <!-- submenu starts -->
                <ul class="submenu" >
                    <li class="title-menu">
                        <span class="fa fa-laptop-code " style="color: dodgerblue; margin-right: 12px;"></span>
                        ${lang_all[i].pk}
                    </li>

                    <li class="go-back">
                        <span class="fas fa-caret-left"></span>
                        Back
                    </li>`

        var category_temp = lang_all[i].fields.category.split(',');
        for (var j = 0; j < category_temp.length; j++) {
            html_data += `
                    <li>
                        <a href="/${category_temp[j]}/${lang_all[i].pk}/">
                            <span class="fa fa-layer-group icon-menu"></span>
                            ${cap_first(category_temp[j])}
                        </a>
                    </li>
                `
        }
        html_data += '</ul></li>'
    }

    return html_data
}


var language_buttons_slidebar = generate_language_buttons_slidebar();
var sidebar_button_container = document.getElementById('sidebar_button_container');
sidebar_button_container.innerHTML += language_buttons_slidebar + contact_button;