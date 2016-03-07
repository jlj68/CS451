var chess = {};
var forfeitBtn = $('#forfeit-btn');

window.onload = function(){
	
	var ws = new WebSocket("ws://subsonic.rawhat.net:8080/game/socket");
	chess = new GameLogic(ws);
	
	ws.onopen = function(evt){
		console.log("socket connected");
	};
	ws.onclose = function(evt){
		console.log("socket closed");
	};

	ws.onmessage = function(msg){
		
	};

	forfeitBtn.click(function(){
		// show modal to ask for forfeit
		$('#forfeitModal').modal('show');

		$('#forfeitConfirmBtn').click(function(){
			ws.send(JSON.stringify({
	                'function': 'forfeit'
	        }));
		});
		
	});



};