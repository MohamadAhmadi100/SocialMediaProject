$('#following_btn').click(function () {

    // function getCookie(name) {
    //     let cookieValue = null;
    //     if (document.cookie && document.cookie !== '') {
    //         const cookies = document.cookie.split(';');
    //         for (let i = 0; i < cookies.length; i++) {
    //             const cookie = cookies[i].trim();
    //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
    //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    //                 break;
    //             }
    //         }
    //     }
    //     return cookieValue;
    // }

    // function csrfSafeMethod(method) {
    //     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    // }
    //
    // $.ajaxSetup({
    //     beforeSend: function (xhr, settings) {
    //         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
    //             xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //         }
    //     }
    // });
    //
    // const csrftoken = getCookie('csrftoken');
    //
    //
    /////////////////////////////////
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });


    let user_id = $('#following_btn').attr('data-id')
    let follow = $('#following_btn').text()

    if (follow === 'follow') {
        var url = '/account/follow/'
        var btn_text = 'unfollow'
    } else {
        var url = '/account/unfollow/'
        var btn_text = 'follow'
    }

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'user_id': user_id,
        },
        success: function (data) {
            if (data['status'] === 'OK') {
                $('#following_btn').text(btn_text)
            }
        }
    });
});