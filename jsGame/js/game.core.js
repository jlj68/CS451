
var Piece = (function(piece, xCor, yCor){
	var name;
	var x, y;
	var possibleMove;

	function Piece(piece, xCor, yCor){
		name = piece;
		x = xCor;
		y = yCor;
		possibleMove = [];
	}

	Piece.prototype = {
		getCordinate: function(){
			return {'x': this.x, 'y', thix.y};
		},
		getName: function(){
			return this.name;
		},
		setX: function(x){
			this.x = x;
		},
		setY: function(y){
			this.y = y;
		},
		setCordinate: function(x, y){
			this.x = x;
			this.y = y;
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


var Game = (function(){
	var turn;
	var win;
	var pieceList = {
		King: 'k',
		Queen: 'q',
		Bishop: 'b',
		Rock: 'r',
		Knight: 'n',
		Pawn: 'p'
	};

	var possibleMoves = {};


	function Game(){
		turn = 'white';
		win = false;		
	}

	Game.prototype = {
		flipTurn: function(){
			if(turn === 'white')
				turn = 'black';
			else
				turn = 'white';
		},
		getTurn: function(){
			return turn;
		},
		isGameOver: function(){
			return win;
		},
		setWin: function(isWin){
			win = isWin;
		},
		setPossibleMoves: function(data){

			var list = JSON.parse(data);
			for(var i =0; i < list.length; i++){
				var piece = new Piece(list[i].name, list[i].row, list[i].col);
				piece.setPossibleMoves(list[i].moves);
				this.possibleMoves.push(piece);
			}
		}, 
		getPossibleMove: function(piece){

			var piece = $.grep(this.possibleMoves, function(e){
				return e.getName() === piece;
			});

			return piece.getPossibleMoves();
		}

	};

	return Game;
})();



var GameLogic = (function(socket){	
	var board = {};	
	var game = new Game();

	function GameLogic (socket){
		var that = this;

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
			onMouseoutSquare: that.onMouseOut

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
		onDrop : function(source, target, piece, newPos, oldPos, orientation){
			this.removeHighlight();
			// need logic from server



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
			/*
				move object
				move : {
					color: 'b',
					piece: 'b',
					from: 'h6',
					to: 'h7'
				}
			*/
			var moves; // Todo: get possible move

			// no valid moves
			if(moves.length === 0) return;

			// highlight the possible squares
			for(var i = 0; i < moves.length; i++){
				this.highlightMove(moves[i].to);
			}
		},
		onMouseOut: function(){
			this.removeHighlight();
		}

	};

	return GameLogic;

})();




	