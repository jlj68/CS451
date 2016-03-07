
$(document).ready(function(event){
	var x = Cookies.get("username"); 

	$.ajax({
	  method: "GET",
	  url: "/users/asa/data",
	  data: "asa"
	}).done(function(data){
	  	console.log(data);
	});

});


