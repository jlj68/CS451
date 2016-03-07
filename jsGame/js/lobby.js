
$(document).ready(function(event){
	
	$.ajax({
		method: "GET",
		url: "/users"
	}).done(function(data){

		var json = JSON.parse(data);
		console.log(json);
		for(var i = 0; i < json.users.length; i++){
			var user = json.users[i];			
			addRow(i, user.username, user.wins, user.losses, user.rating);			
		}
	}).fail(function(){
		console.log("get no data");
	});

});

function addRow(counter, username, win, loss, rate){
	var that = this;
	var btn = createInviteButton(username, function(button){
		console.log(button.value);
	});
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

function createInviteButton(username, func){
	var element = document.createElement("td");
    var button = document.createElement("button");
    var textNode = document.createTextNode("Invite");
    button.type = "button";
    button.value = username;
    button.appendChild(textNode);
    button.onclick = func(button);

    element.appendChild(button);
    return element;
}

