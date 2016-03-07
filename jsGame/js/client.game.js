var chess = {};
var forfeitBtn = $('#forfeit-btn');
$(document).ready(function(event){
	var ws = new WebSocket("ws://rpi.rawhat.net:8080/game/socket");
	chess = new GameLogic(ws);

	ws.onopen = function(evt){
		console.log("socket connected");

		// from alex -- remove if you want
		ws.send(JSON.stringify({'function': 'get_moves'}));
	};
	ws.onclose = function(evt){
		console.log("socket closed");
	};

	$(document).click(function(){
			ws.send(JSON.stringify({'function': 'update_board'}));
	});

	ws.onmessage = function(msg){
		var response = JSON.parse(msg.data);

		// other user forfeit
		if(response.function === "request_forfeit"){
			$('#statusModal').modal('show');
			$('.modal-body').empty();
			$('.modal-body').append("<h4> Congratulation, you won!</h4>");
			$('.modal-body').append("<p> Your opponent has forfeited.</p>");
			$('#statusModal').data('hideInterval', setTimeout(function(){
			            $('#statusModal').modal('hide');
			    }, 3000));
		}

		// from alex -- remove if you want
		if(response.function === "list_moves"){
			console.log(response.moves);
		}

		// from alex -- remove if you want
		if(response.state !== undefined){
			console.log("game state: " + response.state);
			console.log("board: " + response.board);
		}
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
});
