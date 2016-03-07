
$(document).ready(function(event){
	var ws = new WebSocket("ws://subsonic.rawhat.net:8080/invite");

	ws.onopen = function(evt){
		console.log("socket connected");
	};

	ws.onmessage = function(evt){
		var status = JSON.parse(evt.data);
		console.log("server: " + status.sender);

		// if failed to invite
		if(status.status === "failed" &&
			($('#myModal').data('bs.modal') || {isShown: false}).isShown ){
			$('.modal-body').empty();
			$('.modal-body').append("<p> Error sending invitation...</p>");

			//todo: cancel invitation check

			$('#sendInviteBtn').addClass('hide');

		}
		// if sending is success
		if(status.status === "success" &&
			($('#myModal').data('bs.modal') || {isShown: false}).isShown ){
			$('.modal-body').empty();
			$('.modal-body').append("<p> Invitation sent!</p>");
			$('.modal-body').append("<p> Waiting for response... </p>");
			// Todo: set a timer for waiting
			$('#sendInviteBtn').addClass('hide');

		}

		// if invitation is cancelled
		if(status.status === "cancelled" &&
			($('#myModal').data('bs.modal') || {isShown: false}).isShown ){

			cancelModal();

		}
	};

	ws.onclose = function(evt){
		console.log("connection closed");
		if(($('#myModal').data('bs.modal') || {isShown: false}).isShown){
			cancelModal();
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

		$('#myModal').on('hidden.bs.modal', function () {
		        $('.modal-body').empty();
		        $('#sendInviteBtn').removeClass('hide');
		});


		$('.invite-btn').click(function(evt){
			evt.preventDefault();
			var target = this.value;

			// show modal
			$('<p>Send invitation to ' + target + '? </p>').appendTo('.modal-body');
			$('#myModal').modal('show');

			$('#sendInviteBtn').click(function(){

				// todo
				// waiting for server response

				console.log("send invite!");
				ws.send(JSON.stringify({
	                'function': 'send',
	                'target': target
	            }));

			});

			$('#cancelInviteBtn').click(function(evt){
				//Todo
				// send cancel to the invitation
				console.log("cancel invite!");
				ws.send(JSON.stringify({
	                'function': 'cancel',
	                'target': target
	            }));
			});


		});



	}).fail(function(){
		//To do
		// display error on screen
		console.log("get no data");
	});




});

function cancelModal(){
	$('.modal-body').empty();
	$('.modal-body').append("<p> Invitation is canceled!</p>");
	$('#sendInviteBtn').addClass('hide');
	$('#cancelInviteBtn').addClass('hide');
	$('#myModal').data('hideInterval', setTimeout(function(){
	            $('#myModal').modal('hide');
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
