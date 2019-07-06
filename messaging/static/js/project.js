/* Project specific Javascript goes here. */

var initializeControls = function ($form) {
	
	$form.find(".ui.dropdown").dropdown({ allowTab: true });
	$form.find(".ui.dropdown.disabled").dropdown({ allowTab: false });
	$form.find(".ui.checkbox").checkbox({});
	$form.find(".ui.search.dropdown").dropdown({
		allowTab: false,
		forceSelection: false,
		selectOnKeydown: false
	});

}

var stopDefaultFormSubmit = function($form) {

	if($form === undefined) {

		$(".ui.form").on("submit", function(event) {

			event.preventDefault();
			return false;

		});

	}

	else {

		$form.on("submit", function(event) {
			
			event.preventDefault();
			return false;

		});

	}

}

var submitForm = function() {

	$form = $("form.ui.form");
	stopDefaultFormSubmit($form)


}

var deleteComment = function() {

	$("div.messaging-wrapper").on("click", "a.delete.comment", function() {

		$self = $(this);

		$.ajax({
			type: "post",
			url: $self.attr("data-href"),
			data: {},
		}).done(function(response) {

			window.reload()

		}).fail(function(xhr, status, error) {
			alert(xhr.responseJSON)
		});
	})
}


// $(document).ready(function() {
// 	submitForm();
// });