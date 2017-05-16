var chess = {};
var forfeitBtn = $('#forfeit-btn');
var gameState = $('#game_state');

$(document).ready(function(event){
	var ws = new WebSocket("ws://enjoychess.rawhat.net/game/socket");
	var color = $('#color').text();
	setColor(color);
	var turn = (color == 'white' ? true: false);

	chess = new GameLogic(ws, turn, color);

	//initialize game state
	if(!turn){
		gameState.text("Opponent's Turn");
	}

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
			var message = "<h5> Congratulation, you won!</h5><h6> Your opponent has forfeited.</h6>";
			showStatusModal(message);
		}

		if(response.function ===  "success"){
			// todo: notify user it's opponent turn
			gameState.text("Opponent's Turn");
			if(response.state !== undefined && response.state.match("CHECK"))
				gameState.append(' : ' + response.state);
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
				var message = "<h5> This game is a draw. Good luck next time!<h5>";
				showStatusModal(message);

			} else if (response.reason === "BLACK_WIN" && color === "black"
				|| response.reason === "WHITE_WIN" && color === "white"){
				chess.setGameStatus("win");
				var message = "<h5> Congratulation! You won :)<h5>";
				showStatusModal(message);

			} else {
				chess.setGameStatus("lose");
				var message = "<h5> Too bad you lost! Good luck next time.<h5>";
				showStatusModal(message);
			}


			// pull up modal to notify that game is over
			window.location.href = "/lobby";
		}

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


function showStatusModal(message){

	$('#statusModal').modal('show');
	$('.modal-body').empty();
	$('.modal-body').append(message);
	$('#statusModal').data('hideInterval', setTimeout(function(){
	            $('#statusModal').modal('hide');
							window.location.href = "/lobby";
	    }, 3000));
}

function setColor(color){
	var opColor = $('#colorOp');
	if(color === "white"){
		opColor.text("black");
	} else {
		opColor.text("white");
	}
}
