
$(document).ready(function(event){

	Cookies.remove('player_color', {path: '/'});
	Cookies.remove('gameID', {path: '/'});

	var ws = new WebSocket("ws://127.0.0.1:8080/invite");

	ws.onopen = function(evt){
		console.log("socket connected");
	};

	ws.onmessage = function(evt){
		var response = JSON.parse(evt.data);

		if(response.function === "joining_game"){
			window.location.replace("/game/" + response.gameID);
		}

		if(response.function === "create_game"){
			$.ajax({
				method: "PUT",
				url: "/game",
				data: {
					"player2": response.target,
				},
			}).done(function(data){
					window.location.replace("/game/" + $.parseJSON(data).gameID);
			});
		}


		// if failed to invite
		if(response.status === "failed" &&
			($('#myModal').data('bs.modal') || {isShown: false}).isShown ){
			$('.modal-body').empty();
			$('.modal-body').append("<p> Error sending invitation...</p>");

			//todo: cancel invitation check

			$('#sendInviteBtn').addClass('hide');

		}
		// if sending is success
		if(response.status === "success" &&
			($('#myModal').data('bs.modal') || {isShown: false}).isShown ){
			$('.modal-body').empty();
			$('.modal-body').append("<p> Invitation sent!</p>");
			$('.modal-body').append("<p> Waiting for response... </p>");
			// Todo: set a timer for waiting
			$('#sendInviteBtn').addClass('hide');

		}

		// if invitation is cancelled
		if(response.status === "cancelled"){
			if(($("#myModal").data('bs.modal') || {isShown: false}).isShown){
				cancelModal("#myModal", "Invitation is cancelled!");
			}

			if(($('#inviteModal').data('bs.modal') || {isShown: false}).isShown){
				cancelModal("#inviteModal", "Invitation is cancelled!");
			}
		}


		if(response.status === "declined" &&
			($('#myModal').data('bs.modal') || {isShown: false}).isShown ){

			cancelModal("#myModal","Invitation is declined!");

		}

		// if receive invitation
		if(response.sender && !($('#myModal').data('bs.modal') || {isShown: false}).isShown){

			$('#inviteModal').modal('show');
			$('.modal-body').empty();
			$('.modal-body').append("<p> You have received an invitation from" + status.sender + "</p>");
			$('#acceptInviteBtn').val(response.sender);
			$('#declineInviteBtn').val(response.sender);
		}



	};

	ws.onclose = function(evt){
		console.log("connection closed");
		if(($("#myModal").data('bs.modal') || {isShown: false}).isShown){
			cancelModal("#myModal", "Invitation is cancelled!");
		}

		if(($('#inviteModal').data('bs.modal') || {isShown: false}).isShown){
			cancelModal("#inviteModal", "Invitation is cancelled!");
		}
	};

	$.ajax({
		method: "GET",
		url: "/users"
	}).done(function(data){

		var json = JSON.parse(data);


		for(var i = 0; i < json.users.length; i++){
			var user = json.users[i];
			addRow(i, user.username, user.wins, user.losses, user.rating);
		}

		// reset modal
		$('#myModal').on('hidden.bs.modal', function () {
		        $('.modal-body').empty();
		        $('#sendInviteBtn').removeClass('hide');
		});
		$('#inviteModal').on('hidden.bs.modal', function () {
		        $('.modal-body').empty();
		});


		$('.invite-btn').click(function(evt){
			evt.preventDefault();
			var target = this.value;

			// show modal
			$('<p>Send invitation to ' + target + '? </p>').appendTo('.modal-body');
			$('#myModal').modal('show');

			$('#sendInviteBtn').click(function(){

				console.log("send invite!");
				ws.send(JSON.stringify({
	                'function': 'send',
	                'target': target
	            }));

			});

			$('#cancelInviteBtn').click(function(evt){
				console.log("cancel invite!");
				ws.send(JSON.stringify({
	                'function': 'cancel',
	                'target': target
	            }));
			});


		});

		$('#declineInviteBtn').click(function(evt){
			console.log("decline invitation");
			ws.send(JSON.stringify({
	                'function': 'decline',
	                'target' : this.value
	            }));
		});

		$('#acceptInviteBtn').click(function(evt){
			console.log("accept invitation");
			// todo create new game
			ws.send(JSON.stringify({
				'function': 'accept',
				'target': this.value
			}));
		});



	}).fail(function(){
		//To do
		// display error on screen
		console.log("get no data");
	});




});

function cancelModal(modalid, text){

	$('.modal-body').empty();
	$('.modal-body').append("<p>" + text +"</p>");
	$('#sendInviteBtn').addClass('hide');
	$('#cancelInviteBtn').addClass('hide');
	$(modalid).data('hideInterval', setTimeout(function(){
	            $(modalid).modal('hide');
	    }, 2000));
}



function addRow(counter, username, win, loss, rate){
	var that = this;
	var btn = createInviteButton(username);


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

function createInviteButton(username){
	var element = document.createElement("td");
    var button = document.createElement("button");
    var textNode = document.createTextNode("Invite");
    button.type = "button";
    button.value = username;
    button.appendChild(textNode);
    $(button).addClass("invite-btn");

    element.appendChild(button);
    return element;
}
