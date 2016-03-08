var chess = {};
var forfeitBtn = $('#forfeit-btn');

$(document).ready(function(event){
	var ws = new WebSocket("ws://127.0.0.1:8080/game/socket");
	var color = $('#color').text();

	var turn = (color == 'white ' ? false: true);

	chess = new GameLogic(ws, turn, color);

	ws.onopen = function(evt){
		console.log("socket connected");

		// from alex -- remove if you want
		if(chess.isTurn()){
			ws.send(JSON.stringify({'function': 'get_moves'}));
		}
		
	};

	ws.onclose = function(evt){
		Cookies.remove('player_color', {path: '/'});
		Cookies.remove('gameID', {path: '/'});
		console.log("socket closed");
		Cookies.remove('player_color'); 
		Cookies.remove('gameID');
	};


	ws.onmessage = function(msg){
		var response = JSON.parse(msg.data);
		console.log(response);

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

		if(response.state !==  undefined && response.function === "success"){
			var board = JSON.parse(response.updated_board);
			console.log(board);
		}
		if(response.state !==  undefined && response.board_state !== undefined){
			var board = JSON.parse(response.updated_board);
			console.log(board);
		}

		if(response.function === "list_moves"){
			console.log("set possible moves");
			chess.setMoves(response.moves);
		}

		// from alex -- remove if you want
		/*if(response.function === "list_moves"){
			console.log(response.moves);
			//chess.testing();
		}

		// from alex -- remove if you want
		if(response.state !== undefined){
			console.log("game state: " + response.state);
			//chess.testing();
		}*/
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
