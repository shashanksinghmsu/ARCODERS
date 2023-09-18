var navbar = document.getElementById('navbar')
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

// var csrf_token = getCookie("csrftoken");
// console.log("csrf_token");
// console.log(csrf_token);

var contact_button = `
        <a href="/contact/" class="btn my-2 my-sm-0 arbuttons ml-2" type="button">
            <span class="fa fa-address-card"></span> 
            Contact Us
        </a>`

var search_button = `
        <button class="btn my-2 my-sm-0 arbuttons ml-2" type="button" id="search">
            <span class="fa fa-search "></span>
            Search
        </button>`

var home_button = `
        <a href="/" class="btn my-2 my-sm-0 arbuttons ml-2" type="button">
            <span class="fa fa-home"></span>
            Home
        </a>`

var category_list = lang_all[0].fields.category.split(',')
function category_options(category_list) {
    var final_value = '';
    for (var i = 0; i < category_list.length; i++) {
        final_value += `<a href="/${category_list[i]}/?next=${pathname}">${category_list[i][0].toUpperCase() + category_list[i].slice(1)}</a>`
    }
    return final_value;
}
var category_button = `
        <div class="dropdown ml-2 py-1 my-1">
            <button class="dropbtn arbuttons">
                <span class='fa fa-layer-group mr-1'></span>
                Category
                <span class="fa fa-sort-down float-right"></span>
            </button>

            <div class="dropdown-content">
                ${category_options(category_list)}
            </div>
        </div>`


function change_csharp_slug(language) {
    if (language == 'C#') {
        return 'C%23'
    }
    return language
}
function language_options() {
    var final_value = '';
    for (var i = 0; i < lang_all.length; i++) {
        final_value += `<a href="/${change_csharp_slug(lang_all[i].pk)}/?next=${pathname}">
                ${lang_all[i].pk}
            </a>`
    }
    return final_value;
}
var language_button = `    
        <div class="dropdown ml-2 pl-1 py-1 my-1">
            <button class="dropbtn arbuttons">
                <span class='fa fa-laptop-code mr-1'></span>
                Language
                <span class="fa fa-sort-down float-right"></span>
            </button>

            <div class="dropdown-content">
                ${language_options()}
            </div>
        </div>`


function category_value_search_modal(category) {
    dropdown_list = document.getElementById('category-dropdown-SB');
    dropdown_list.innerHTML = category + `<span class='fa fa-sort-down float-right'><span>`;
    category_element = document.getElementById('category-sb');
    category_element.value = category;
}
function category_option_search_modal(category_list) {
    var final_value = '';
    for (var i = 0; i < category_list.length; i++) {
        final_value += `<button class="dropdown-item" type="button" onclick='category_value_search_modal("${cap_first(category_list[i])}")'> ${cap_first(category_list[i])}</button>`
    }
    return final_value;
}
var category_search_modal = `
        <div class="dropdown" style='width:100%'>
            <button class="btn btn-secondary dropdown-toggle arbuttons dropbtn search-box-field" type="button" id="category-dropdown-SB" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style='color:dodgerblue !important;'>
                Category
                <span class='fa fa-sort-down float-right'><span>
            </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenu2">
            ${category_option_search_modal(category_list)}
        </div>
        </div>`

function language_value_search_modal(language_name) {
    dropdown_list = document.getElementById('language-dropdown-SB');
    dropdown_list.innerHTML = language_name + `<span class='fa fa-sort-down float-right'><span>`;
    language_element = document.getElementById('language-sb');
    language_element.value = language_name;
}
function language_option_search_modal() {
    var final_value = '';
    for (var i = 0; i < lang_all.length; i++) {
        final_value += `<button class="dropdown-item" type="button" onclick='language_value_search_modal("${lang_all[i].pk}")'> ${lang_all[i].pk}</button>`
    }
    return final_value;
}
var language_search_modal = `
    <div class="dropdown" style="width:100%">
        <button class="btn btn-secondary dropdown-toggle arbuttons dropbtn search-box-field" type="button" id="language-dropdown-SB" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style='color:dodgerblue !important;'>
        Language
        <span class='fa fa-sort-down float-right'><span>
        </button>
    <div class="dropdown-menu" aria-labelledby="dropdownMenu2">
        <button class="dropdown-item" type="button" onclick='language_value_search_modal("All")'> All</button>
        ${language_option_search_modal()}
    </div>
    </div>`

function submit_search_box() {
    category_field = document.getElementById('category-sb');
    language_field = document.getElementById('language-sb');
    error_box = document.getElementById('sb-error');
    error_box.classList.add('sb-error');
    error_box.classList.add('arbuttons');
    if (category_field.value == '' && language_field.value == '') {
        error_box.innerHTML = 'Please select Language and Category';
    } else if (language_field.value == '') {
        error_box.innerHTML = 'Please select Language';
    } else if (category_field.value == '') {
        error_box.innerHTML = 'Please select Category';
    } else {
        error_box.classList.remove('sb-error');
        error_box.classList.remove('arbuttons');
        error_box.innerHTML = '';
    }
}



var log_in_modal = `
        <div class="modal fade" id="loginModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
        aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Login</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true" style="color: dodgerblue">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <form method="post" action="/login/?next=${pathname}">
                            <div style="display:none;">${csrf_token}</div>
                            <div class="form-group">
                                <label for="Username" class="mt-1 form-label"> 
                                    <span class="fas fa-id-card sb-icon"></span>
                                </label>
                                    
                                <input type="text" class='form-control arbuttons search-box-field' id="Username" aria-describedby="UsernameHelp" placeholder="Username" readonly
                                    onfocus="this.removeAttribute('readonly');" name="username">
                            </div>
                            <div class="form-group">
                                <label for="Password" class="mt-1 form-label">
                                    <span class="fas fa-key sb-icon"></span>
                                </label>
                                <input type="password" class='form-control arbuttons search-box-field' name="password" placeholder="Password">
                            </div>
                            <div class="modal-footer">
                                <button type="submit" class="btn arbuttons">Login</button>

                                <button type="button" class="btn arbuttons" data-dismiss="modal">Close</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>`

var search_modal = `
        <div class="modal fade" id="searchModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
            aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel-2">Search</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true" style="color: dodgerblue !important;">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body" style="width: 100%;">
                        <form method="get" name="searchBox" action="/search/?next=${pathname} ">
                            ${csrf_token}
                            <div class="form-group">
                                <label for="query" class="mt-1 form-label">
                                    <span class='fa fa-search sb-icon'></span> 
                                </label>
                                <input type="text" class="form-control arbuttons search-box-field" id="query" aria-describedby="UsernameHelp" placeholder="Query " readonly
                                    onfocus="this.removeAttribute('readonly');" name="search" required>
                            </div>

                            <div class="form-group">
                                <label for="language" class="mt-1 form-label">
                                    <span class='fa fa-laptop-code sb-icon'></span> 
                                </label>
                                ${language_search_modal}     
                                <input name="language" type='text' class='form-control' id='language-sb' hidden required>
                            </div>

                            <div class="form-group">
                                <label for="category" class="mt-1 form-label"> 
                                    <span class='fa fa-layer-group sb-icon'></span>
                                </label>
                                ${category_search_modal}     
                                <input name="category" type='text' class='form-control' id='category-sb' hidden required>
                            </div>
                            <div id='sb-error'>
                            </div>
                            <div class="modal-footer">
                                <button type="submit" class="btn arbuttons" onclick='submit_search_box()'>Search</button>
                                <button type="button" class="btn arbuttons" data-dismiss="modal">Close</button>
                                                
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>`


function nav_data_1(auth, username) {
    if (auth == true) {

        return contact_button
    }
    else {

        return search_button
    }

}

function nav_data_2(auth, username) {
    if (auth == true) {
        var user_button = `
                <div class="dropdown ml-0 ph-1 py-1">
                    <button class="dropbtn arbuttons" style="width:150px">
                        <span class="fas fa-user-tie mr-1"></span>
                        ${username}
                        <span class="fa fa-sort-down float-right"></span>
                    </button>

                    <div class="dropdown-content">
                        <a href="/user/?next=${pathname}">
                            <span class="fas fa-id-badge mr-1"></span>
                            My Profile
                        </a>
                        <a href="/logout/?next=${pathname}">
                            <span class="fas fa-sign-out-alt mr-1"></span>
                            Log Out
                        </a>
                    </div>
                </div>`

        var return_value = search_button + user_button
        return return_value

    }
    else {
        var login_button = `
                <button class="btn my-2 my-sm-0 arbuttons ml-2" type="button" id="login">
                    <span class="fas fa-sign-in-alt"></span>
                    Login
                </button>`
        var sign_up_button = `
                <a href="/signup/" class="btn my-2 my-sm-0 arbuttons ml-2" id="createAccount" type="button">
                    <span class="fas fa-user-plus"></span>
                    Create Account
                </a>`

        var return_value = sign_up_button + login_button
        return return_value
    }

}

var nav_script = document.createElement('script')
nav_script.type = 'text/javascript'

$.ajax({
    url: '/navbar/',
    type: 'GET',
    data: {}
}).done(function (response) {
    var data = home_button + nav_data_1(response.auth, response.username) + category_button + language_button + nav_data_2(response.auth, response.username) + log_in_modal + search_modal

    navbar.innerHTML = data
})
    .fail(function () {
        console.log("failed");
    })


$(document).ready(function () {
    // nav_script.innerHTML = `
    $("#login").click(function () {
        $("#loginModal").modal()
    })

    $("#search").click(function () {
        $("#searchModal").modal()
    })


})
