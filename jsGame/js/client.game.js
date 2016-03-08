var chess = {};
var forfeitBtn = $('#forfeit-btn');

$(document).ready(function(event){
	var ws = new WebSocket("ws://127.0.0.1:8080/game/socket");
	var color = $('#color').text();

	var turn = (color == 'white' ? true: false);

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

		if(response.function ===  "success" && response.updated_board !== undefined){
			// todo: notify user it's opponent turn
			
		}
		if(response.state === "MATCH"){
			console.log("match");
			// Todo: parse the board
			var update_board = parseTable(response.updated_board);

			// update board
			chess.updateBoard(updated_board);

			// call the server to send possible moves
			ws.send(JSON.stringify({'function': 'get_moves'}));
		}


		if(response.function === "list_moves"){
			console.log("set possible moves");
			chess.setMoves(response.moves);
		}

		if(response.function === "game_over"){
			chess.setGameOver(true);

			if(response.reason === "DRAW"){
				chess.setGameStatus("draw");
			} else if (response.reason === "BLACK_WIN" && color === "black"
				|| response.reason === "WHITE_WIN" && color === "white"){
				chess.setGameStatus("win");
			} else {
				chess.setGameStatus("lose");
			}

			
			// pull up modal to notify that game is over

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

function parseTable(table){
	var result = {};
	for(var i =0; i < table.length; i++){
		var position = table[i].position;
		var piece = table[i].piece.name;
		result[position] = piece;
	}
	return result;
}
