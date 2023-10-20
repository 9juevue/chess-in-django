$(document).ready(function () {
    let coordinates,
        figure;

    $.ajax({
        data: {
            'status': true,
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
        },
        type: 'POST',
        url: '/game/chess',
        success: function (response) {

        }
    })

    $('td > img').draggable({
        containment: '.chess-board',
        grid: [85, 85],
        stop: function (event, ui) {
            let left = ui.offset.left,
                top = ui.offset.top,
                elements = document.elementsFromPoint(left, top),
                figure = $(this);

            Object.entries(elements).forEach(
                ([key, value]) => {
                    if (value.tagName === 'TD') {
                        let coordinatesOld = ui.helper[0].id.substring(0, 2),
                            coordinatesNew = value.id;

                        $('#' + ui.helper[0].id).attr('id', coordinatesNew + ui.helper[0].id.substring(2));

                        $.ajax({
                            data: {
                                'coordinates_old': coordinatesOld,
                                'coordinates_new': coordinatesNew,
                                'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
                            },
                            type: 'POST',
                            url: '/game/chess',
                            success: function (response) {
                                if (!response.status) {
                                    figure.css({'top': ui.originalPosition['top'], 'left': ui.originalPosition['left']})
                                }
                            }
                        });
                    }
                }
            );
        }
    });
});