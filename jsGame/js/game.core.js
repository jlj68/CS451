
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
	var turn;
	var win;
	

	var possibleMoves;


	function Game(turn){
		this.turn = turn;
		this.win = false;
		this.possibleMoves = [];		
	}

	Game.prototype = {
		flipTurn: function(){
			if(this.turn === 'white')
				this.turn = 'black';
			else
				this.turn = 'white';
		},
		getTurn: function(){
			return this.turn;
		},
		isGameOver: function(){
			return this.win;
		},
		setWin: function(isWin){
			this.win = isWin;
		},
		setPossibleMoves: function(data){

			var list = JSON.parse(data);
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



var GameLogic = (function(socket, turn){	
	var board = {};	
	var game;

	function GameLogic (socket, turn){
		var that = this;
			game = new Game(turn);

		var config_board = {
			orientation: 'white',
			position: 'start',
			draggable: true,
			dropOffBoard: 'snapback',
			onChange: that.onChangeMove,
			onDragStart: that.onDragStart,
			onDrop: that.onDrop,
			highlightMove: that.highlightMove,
			removeHighlight: that.removeHighlight,
			onMouseoverSquare: that.onMouseOver,
			onMouseoutSquare: that.onMouseOut,
			setMoves: that.setMoves,
			resetMoves: that.resetMoves

		};

		board = that.init(config_board);
	}	

	GameLogic.prototype = {	
		init: function(config){
			return ChessBoard('board', config);		
		},
		// fired when there is a change in move
		onChangeMove : function(oldMove, newMove){
			game.flipTurn();
			console.log("Flip side. Now turn is: " + game.getTurn());
		},
		//fired when piece is picked up. Returns false to prevent the pick up
		onDragStart : function(source, piece, position, orientation){
			if(game.isGameOver() === true ||
				(game.getTurn() === 'white' && piece.search(/^b/) !== -1) ||
      			(game.getTurn() === 'black' && piece.search(/^w/) !== -1)){
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
			
			// get a list of possible move for this piece
			var moves = game.getPossibleMove(piece, square);
			// no valid moves
			if(moves.length === 0) return;

			// highlight the possible squares
			for(var i = 0; i < moves.length; i++){
				this.highlightMove(moves[i].move);
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
		}

	};

	return GameLogic;

})();




	