
var Piece = (function(piece, position){
	var name;
	var position;
	var possibleMove;

	function Piece(piece, position){
		this.name = piece;
		this.position = position
		this.possibleMove = [];
	}

	Piece.prototype = {
		getPosition: function(){
			return this.position;
		},
		getName: function(){
			return this.name;
		},
		setPosition: function(position){
			this.position = position;
		},
		getPossibleMoves: function(){
			return this.possibleMove;
		},
		setPossibleMoves: function(data){
			this.possibleMove = data;
		}

	};
	return Piece;

})();


var Game = (function(turn){
	var color, turn;
	var status, end;


	var possibleMoves;


	function Game(color, turn){
		this.turn = turn;
		this.color = color;
		this.status = "";
		this.end = false;
		this.possibleMoves = [];
	}

	Game.prototype = {
		flipTurn: function(){
			if(this.turn === true)
				this.turn = false;
			else
				this.turn = true;
		},
		isTurn: function(){
			return this.turn;
		},
		getColor: function(){
			return this.color;
		},
		isGameOver: function(){
			return this.end;
		},
		setGameOver: function(bool){
			this.end = bool;
		},
		setStatus: function(status){
			this.status = status;
		},
		setPossibleMoves: function(list){

			for(var i =0; i < list.length; i++){
				var piece = new Piece(list[i].name, list[i].position);
				piece.setPossibleMoves(list[i].moves);
				this.possibleMoves.push(piece);

			}
		},
		getPossibleMove: function(piece, position){

			for(var i = 0; i < this.possibleMoves.length; i++){
				var p = this.possibleMoves[i];
				if(p.getName() === piece && p.getPosition() === position)
					return p.getPossibleMoves();
			}

			return [];
		},
		resetPossibleMove: function(){
			this.possibleMoves = [];
		}

	};

	return Game;
})();



var GameLogic = (function(socket, turn, color){
	var board = {};
	var game;
	var ws;

	function GameLogic (socket, turn, color){
		var that = this;
			game = new Game(color, turn);
			ws = socket;

		var config_board = {
			orientation: 'white',
			position: 'start',
			draggable: true,
			dropOffBoard: 'snapback',
			//onChange: that.onChangeMove,
			onDragStart: that.onDragStart,
			onDrop: that.onDrop,
			highlightMove: that.highlightMove,
			removeHighlight: that.removeHighlight,
			onMouseoverSquare: that.onMouseOver,
			onMouseoutSquare: that.onMouseOut,
			setMoves: that.setMoves,
			resetMoves: that.resetMoves,
			updateBoard: that.updateBoard,
			sendMove: that.sendMove,
			isTurn: that.isTurn,
			setGameOver: that.setGameOver,
			isGameOver: that.isGameOver,
			setGameStatus: that.setGameStatus
			//position: that.updateBoard

		};

		board = that.init(config_board, color);
	}

	GameLogic.prototype = {
		init: function(config, color){
			var board_init =  ChessBoard('board', config);
			board_init.orientation(color);
			return board_init;
		},
		/*// fired when there is a change in move
		onChangeMove : function(oldMove, newMove){
			game.flipTurn();
		},*/
		//fired when piece is picked up. Returns false to prevent the pick up
		onDragStart : function(source, piece, position, orientation){

			if(game.isGameOver() === true || !game.isTurn() ||
				(game.getColor() === 'white' && piece.search(/^b/) !== -1) ||
      			(game.getColor() === 'black' && piece.search(/^w/) !== -1)){
				return false;
			}
		},
		onDrop : function(source, target, piece){
			this.removeHighlight();

			var possibleMoves = game.getPossibleMove(piece, source);

			for(var i = 0; i<possibleMoves.length; i++){
				if(possibleMoves[i].move === target){
					//reste the possible move list of game
					game.resetPossibleMove();
					game.flipTurn();
					this.sendMove(source, target)
					return;
				}
			}

			//if illegal move, snapback to original place
			return 'snapback';
		},
		highlightMove: function(square){
			var squareE = $('#board .square-' + square);

			var background = '#00B18C';
			if(squareE.hasClass('black-3c85d') === true){
				background = '#77C699';
			}

			squareE.css('background', background);
		},
		removeHighlight: function() {
		  	$('#board .square-55d63').css('background', '');
		},
		onMouseOver: function(square, piece){

			if(game.isTurn()){
				// get a list of possible move for this piece
				var moves = game.getPossibleMove(piece, square);
				// no valid moves
				if(moves.length === 0) return;

				// highlight the possible squares
				for(var i = 0; i < moves.length; i++){
					this.highlightMove(moves[i].move);
				}
			}


		},
		onMouseOut: function(){
			this.removeHighlight();
		},
		setMoves: function(data){
			game.setPossibleMoves(data);
		},
		resetMoves: function(){
			game.resetPossibleMove();
		},
		updateBoard: function(data){
			board.position(data);
			game.flipTurn();

		},
		sendMove: function(oldPos, newPos){
			console.log("send move");
			ws.send(JSON.stringify(
				{'function': 'make_move',
				'move': {
					'fromPos':{
						'rowcol': oldPos
					},
					'toPos': {
						'rowcol': newPos
					}
				}
			}));
		},
		isTurn: function(){
			return game.isTurn();
		},
		setGameOver: function(bool){
			game.setGameOver(bool);
			
		},
		isGameOver: function(){
			return game.isGameOver();
		},
		setGameStatus: function(status){
			game.setGameStatus(status);
		}


	};

	return GameLogic;

})();
