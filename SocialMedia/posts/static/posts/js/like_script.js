$(document).ready(function () {
    $("body").on("click", "#comments", function () {
        // $("#comments").click(function () {
        $('#all_comments').toggle();
    });

    var total_likes;
    // $("body").on("click", "#like", function () {
    // $('#like').click(function () {
    $('body').delegate('#like', 'click', function () {
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
        let post_id = $('#like').attr('data-id');
        $.ajax({
            url: '/like/',
            method: 'POST',
            data: {
                'post_id': post_id,
            },

            success: function (data) {
                total_likes = data['total_likes']
                $("#like_count").text(total_likes);
                if (data['status'] === 'unliked') {
                    $('#heart').removeAttr("class");
                    $('#heart').addClass('bi-heart')

                } else if (data['status'] === 'liked') {
                    $('#heart').removeAttr("class");
                    $('#heart').addClass('bi-heart-fill')

                }
            }
        });
    });
});