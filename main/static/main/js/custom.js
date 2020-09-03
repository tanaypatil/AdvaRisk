function highlight_search(sterm) {
    let review_boxes = $("#review_boxes");
    let src_str = review_boxes.html();
    let term = sterm;
    term = term.replace(/(\s+)/, "(<[^>]+>)*$1(<[^>]+>)*");
    let pattern = new RegExp("(" + term + ")", "gi");

    src_str = src_str.replace(pattern, "<mark>$1</mark>");
    src_str = src_str.replace(/(<mark>[^<>]*)((<[^>]+>)+)([^<>]*<\/mark>)/, "$1</mark>$2<mark>$4");

    review_boxes.html(src_str);
}

$('#searchbar').keyup(function () {
    if ($(this).val().length >= 3) {
        search($(this).val());
    } else if ($(this).val().length === 0) {
        search("");
    }
});

function search(term) {
    $.ajax({
        type: 'POST',
        url: '/search/',
        data: {'term': term},
        success: function (data) {
            $('#pages').html(data['pages']);
            $('#review_boxes').html(data['reviews']);
            if (data["term"] !== "") {
                highlight_search(data['term']);
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}