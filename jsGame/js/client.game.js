var game = {};

window.onload = function(){
	
	var ws = new WebSocket("ws://subsonic.rawhat.net:8080/game/socket");
	game = new GameLogic(ws);



};