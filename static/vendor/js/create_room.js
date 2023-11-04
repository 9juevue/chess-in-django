$(document).ready(function () {
    $('#create_room').on('click', function () {
        $.ajax({
            data: {
                'type': 'create_room',
                'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
            },
            type: 'POST',
            url: '',
            success: function (response) {
                if (response) {
                    let room_url = window.location.href + response['unique_string'];
                    $('<a href="' + room_url + '">' + room_url + '</a>').appendTo('#room_list');
                    console.log(room_url);
                }
            }
        });
    })
});