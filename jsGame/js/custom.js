var main = function() {
    'use strict';

    var createUserName = function() {
        var urname = $('#username').val();
        $.ajax({
            method: 'PUT',
            url: '/users',
            data: { username:uname },
            statusCode: {
                201: function() {
                    $('#result_area').html('User successfully created.');
                },
                409: function() {
                    $('#result_area').html('user already exists. Please try again.');
                }
            }
        }
    }

    $('#username').on('click', function(event) {
        createUserName();
    });

    $('#username').on('click', function(event) {
        // when user press enter
        if(event.keyCode === 13) {
            createUserName();
        }
    });
}

