
function card(query, language, language_url, answer_count, query_url, is_edit = false, id = null) {
	if (is_edit == true) {
		edit_button = `<a href="/user/edit_program/${language}/${id}" class='edit_program' class='edit-button'>    
        <span class="fa fa-pencil-square-o text-muted p-1 my-1 mr-0 ml-0" aria-hidden="true" data-toggle="tooltip" data-placement="top" title="Edit Program" style="color:dodgerblue !important;"></span>Edit
        </a>`
	} else {
		edit_button = ''
	}


	var querybook_card_template = `
    <article class="search-result row ">
        <div class="col-xs-12 col-sm-12 col-md-7 excerpet program_card" style="margin: auto">

            <h3 title="query" class="program_title">
                ${query}    
            </h3>

            <hr style="border: 1px solid dodgerblue;">
            <a href="${language_url}" class="program_language_url">
                <span class="fa fa-laptop" aria-hidden="true" ></span>
                ${language}
            </a>


            <div class="lowerData">
                <p class="program_answer">
                    <span class="fa fa-code code_icon" aria-hidden="true" style="color: mintcream !important;"></span>
                    <span>
                        ${answer_count} Fixes
                    </span>
                </p>`

		+ edit_button +

		`<a type="button" href= "/${query_url} " class="btn btn-primary btn-sm arbuttons program_final_button">
                    &lt;/Fixes&gt;
                </a>
            </div>
        </div>

        <span class="clearfix borda"></span>
    </article>
    <hr class="program_hr col-xs-12 col-sm-12 col-md-9">
    `
	return querybook_card_template
}

