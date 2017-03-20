$(function(){
	$('#btnSignUp').click(function(){
        var name = $('#txtname').val();
        var email = $('#txtemail').val();
		var pass = $('#txtPassword').val();
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});