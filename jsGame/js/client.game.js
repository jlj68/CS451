var chess = {};
var forfeitBtn = $('#forfeit-btn');

$(document).ready(function(event){
	var ws = new WebSocket("ws://192.168.1.238:8080/game/socket");
	var color = $('#color').text();

	var turn = (color == 'white' ? true: false);

	chess = new GameLogic(ws, turn, color);

	ws.onopen = function(evt){
		console.log("socket connected");

		if(chess.isTurn()){
			ws.send(JSON.stringify({'function': 'get_moves'}));
		}


	};

	ws.onclose = function(evt){
		Cookies.remove('player_color', {path: '/'});
		Cookies.remove('gameID', {path: '/'});
		console.log("socket closed");
		window.location.href = '/lobby';
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
									window.location.href = "/lobby";
			    }, 3000));
		}

		if(response.function ===  "success"){
			// todo: notify user it's opponent turn
			$('#game_state').html("Opponent's Turn");
			if(response.state !== undefined && response.state.match("CHECK"))
				$('#game_state').append(' : ' + response.state);
		}

		if(response.state === "MATCH"){
			console.log("match");
			// Todo: parse the board
			var update_board = parseTable(response.updated_board);

			// update board
			chess.updateBoard(update_board);

			// call the server to send possible moves
			//ws.send(JSON.stringify({'function': 'get_moves'}));
		}


		if(response.function === "list_moves"){
			var update_board = parseTable(response.updated_board);

			// update board
			chess.updateBoard(update_board);
			console.log("set possible moves");

			chess.flipTurn(response.moves.length !== 0);
			if(response.moves.length !== 0){
				$('#game_state').html('Your turn.');
				if(response.state !== undefined && response.state.match("CHECK"))
					$('#game_state').append(' : ' + response.state);
			}
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
			window.location.href = "/lobby";
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
					window.location.href = "/lobby";
		});

	});
});

function parseTable(table){
	console.log(table);
	var result = {};
	for(var i =0; i < table.length; i++){
		if(table[i].piece != null){
			var position = table[i].position;
			var piece = table[i].piece.name;
			result[position] = piece;
		}
	}
	return result;
}
