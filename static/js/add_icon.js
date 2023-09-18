$('.add_program').hover(
    function () {
        $(this).addClass("add_program_hover"); //Add an active class to the anchor
        $('.test').text('ADD PROGRAM '); //Add an active class to the anchor
    },
    function () {
        $('.test').text(''); //Add an active class to the anchor
        $(this).removeClass("add_program_hover"); //Add an active class to the anchor
    });


$('.add_query').hover(
    function () {
        $(this).addClass("add_query_hover"); //Add an active class to the anchor
        $('.test').text('ADD QUERY '); //Add an active class to the anchor
    },
    function () {
        $('.test').text(''); //Add an active class to the anchor
        $(this).removeClass("add_query_hover"); //Add an active class to the anchor
    });
