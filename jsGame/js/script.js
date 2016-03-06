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
				$('#usernameCheck').html("User successfully created");
				ws.send(JSON.stringify({'function': 'register', 'name': uname}));
				$btn.button('reset');
			},
			409: function(){
				$('#usernameCheck').html("User already exists.  Please try again.");
				$btn.button('reset');
			}
		}
	});*/

	$toLobbyBtn.show();

	
});

