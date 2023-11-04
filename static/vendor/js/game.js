$(document).ready(function () {
    let unique_string = window.location.pathname.replace(/\/$/, '').split("/").pop();
    let url = `ws://${window.location.host}/ws/socket-server/` + unique_string + `/`;
    const chessSocket = new WebSocket(url);

    chessSocket.onopen = function (e) {


        chessSocket.send(JSON.stringify({
            'type': 'init_game',
            'id': unique_string,
            'white_player': 'Ruslan',
            'black_player': 'Vladimir'
        }));
    }

    chessSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);

        console.log(data);

        if (data.type === 'chat') {
            let messages = document.getElementById('messages');

            messages.insertAdjacentHTML('beforeend', `<div><p>${data.message}</p></div>`)
        }

        // if (data.type === 'init_current_field') {
        //     let coordinates,
        //         color,
        //         name,
        //         start_coordinates,
        //         figureId;
        //     Object.entries(data.field).forEach(
        //         (key, value) => {
        //             if (key[1] != null) {
        //                 coordinates = key[0];
        //                 color = key[1]['color'];
        //                 name = key[1]['name'];
        //                 start_coordinates = key[1]['start_coordinates']
        //                 figureId = start_coordinates + name[0];
        //                 $('#' + figureId).appendTo($('#' + coordinates));
        //             }
        //         }
        //     )
        // }

        if (data.type === 'figure_move') {
            let figure = $('#' + data['figure_id']);

            if (data.status) {
                let coordinatesNew = $('#' + data['coordinates_new']);

                coordinatesNew.empty();
                figure.attr('id', data['coordinates_new'] + data['figure_id'].substring(2)).appendTo(coordinatesNew);
                figure.css({'top': data['original_position_top'], 'left': data['original_position_left']})
            } else {
                figure.css({'top': data['original_position_top'], 'left': data['original_position_left']})
            }
        }
    }

    let form = document.getElementById('form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let message = e.target.message.value;
        chessSocket.send(JSON.stringify({
            'type': 'message',
            'message': message
        }));
        form.reset();
    })

    $('td > img').draggable({
        containment: '.chess-board',
        grid: [85, 85],
        zIndex: 100,
        stop: function (event, ui) {
            let left = ui.offset.left,
                top = ui.offset.top,
                elements = document.elementsFromPoint(left, top);

            Object.entries(elements).forEach(
                ([key, value]) => {
                    if (value.tagName === 'TD') {
                        let coordinatesOld = ui.helper[0].id.substring(0, 2),
                            coordinatesNew = value.id;

                        chessSocket.send(JSON.stringify({
                            'type': 'figure_move',
                            'coordinates_old': coordinatesOld,
                            'coordinates_new': coordinatesNew,
                            'figure_id': ui.helper[0].id,
                            'original_position_left': ui.originalPosition['left'],
                            'original_position_top': ui.originalPosition['top'],
                            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
                        }));
                    }
                }
            );
        }
    });
});