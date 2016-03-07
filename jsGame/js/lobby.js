
$(document).ready(function(event){
	

	$.ajax({
		method: "GET",
		url: "/users"
	}).done(function(data){

		var json = JSON.parse(data);
		var ws = new WebSocket("ws://192.168.1.238:8080/invite");

		for(var i = 0; i < json.users.length; i++){
			var user = json.users[i];			
			addRow(i, user.username, user.wins, user.losses, user.rating);			
		}

		ws.onopen = function(evt){
			console.log("socket connected");
		};

		ws.onmessage = function(evt){
			var status = JSON.parse(evt.data);
			console.log("server: " + status.status);

			// if failed to invite
			if(status.status === "failed" &&
				($('#myModal').data('bs.modal') || {isShown: false}).isShown ){

				$(".modal-body p").replaceWith("<p> Error sending invitation...</p>");

				//todo: cancel invitation check

				$('#sendInviteBtn').addClass('hide');
				
			}

			// if sending is success
			if(status.status === "success" &&
				($('#myModal').data('bs.modal') || {isShown: false}).isShown ){

				$(".modal-body p").replaceWith("<p> Invitation sent!</p>");
				$(".modal-body").append("<p> Waiting for response... </p>");
				// Todo: set a timer for waiting
				$('#sendInviteBtn').addClass('hide');
				
			}
		};



		ws.onclose = function(evt){
			//To do
			// cancel the invitation
			alert("connection closed");
			if(($('#myModal').data('bs.modal') || {isShown: false}).isShown){
				console.log("plz close modal");
			}
		};

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

			$('#sendInviteBtn').click(function(evt){

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
			});
			
	
		});



	}).fail(function(){
		//To do
		// display error on screen
		console.log("get no data");
	});

	


});

$.clearInput = function () {
        $('form').find('input[type=text], input[type=password], input[type=number], input[type=email], textarea').val('');
};



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
