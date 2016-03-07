var chess = {};

window.onload = function(){
	
	var ws = new WebSocket("ws://subsonic.rawhat.net:8080/game/socket");
	chess = new GameLogic(ws);



};