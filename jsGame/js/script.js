var $submitUserNameBtn = $('#submitUserName');
var $usernameCheckText = $('#usernameCheck');
var $toLobbyBtn = $('#toLobby');
//var ws = new WebSocket("ws://subsonic.rawhat.net:8080/invite");

$submitUserNameBtn.on('click', function (event) {
    var $btn = $(this).button('loading');
    var uname = $('#userName').val();
    

	/*$.ajax({
		method: "PUT",
		url: "/users",	
		data: {username: uname},
		statusCode: {
			201: function(){
				$usernameCheckText.html("User successfully created");
				ws.send(JSON.stringify({'function': 'register', 'name': uname}));
				$toLobbyBtn.removeClass('hide');
				$toLobbyBtn.addClass('btn-margin-left');
				$submitUserNameBtn.addClass('hide');
			},
			409: function(){
				$usernameCheckText.html("User already exists.  Please try again.");
				$btn.button('reset');
			}
		}
	});*/

$usernameCheckText.html("User successfully created");
//ws.send(JSON.stringify({'function': 'register', 'name': uname}));
$toLobbyBtn.removeClass('hide');
$toLobbyBtn.addClass('btn-margin-left');
$submitUserNameBtn.addClass('hide');
	
});

$toLobbyBtn.on('click', function(){
	window.location.href = "../html/lobby.html";
});

