
$(document).ready(function(event){

	var ws = new WebSocket("ws://http://192.168.1.238:8080/invite");

	$.ajax({
		method: "GET",
		url: "/users"
	}).done(function(data){

		var json = JSON.parse(data);
		console.log(json);
		for(var i = 0; i < json.users.length; i++){
			var user = json.users[i];			
			addRow(i, user.username, user.wins, user.losses, user.rating, ws);			
		}
	}).fail(function(){
		//To do
		// display error on screen
		console.log("get no data");
	});

});

function inviteHandler(button, socket){
	socket.onopen = function(){

		// send invitation to server
		socket.send(JSON.stringify({
			"function": "send",
			"target": button.value
		}));

		// retrieve message
		socket.onmessage = function(msg){
			console.log(msg);
		};
	};
	
}

function addRow(counter, username, win, loss, rate, fnc, socket){
	var that = this;
	var btn = createInviteButton(username, that.inviteHandler, socket);


	var index = createText("td", counter+1);
	var user = createText("td", username);
	var w = createText("td", win);
	var l = createText("td", loss);
	var r = createText("td", rate);

	$('#addr'+counter).append(index, user, w, l, r, btn);
	$('#lobby').append('<tr id="addr'+(counter+1)+'"></tr>');
}

function createText(element, text){
	var element = document.createElement(element);
	var textNode = document.createTextNode(text);
	element.appendChild(textNode);

	return element;
}

function createInviteButton(username, func, socket){
	var element = document.createElement("td");
    var button = document.createElement("button");
    var textNode = document.createTextNode("Invite");
    button.type = "button";
    button.value = username;
    button.appendChild(textNode);
    button.onclick = func(button, socket);

    element.appendChild(button);
    return element;
}

/*ws.onmessage = function(event){
          var response = $.parseJSON(event.data);
          console.log(response);
          if(response.function == "joining_game"){
            window.location.replace("/game/" + response.gameID);
          }
          else if(response.function == "create_game"){
            $.ajax({
              method: "PUT",
              url: "/game",
              data: {
                "player2": currentInvite,
              },
            }).done(function(data){
                window.location.replace("/game/" + $.parseJSON(data).gameID);
            });
          }
          if(response.status !== undefined){
            console.log(response.status);
          }
          if(response.request !== undefined){
            console.log(response.request);
          }

          if(response.sender !== undefined){
            $('#invite_area').show();
            $('#invitation_text_area').text(response.sender + " has invited you to play!");
            currentInvite = response.sender;
            inviteButtonListeners();
          }
      }*/
