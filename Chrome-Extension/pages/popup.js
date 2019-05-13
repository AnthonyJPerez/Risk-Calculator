var dom_loaded = new $.Deferred();
var PROCESSING_IMG = "images/gears.gif";
var ERROR_IMG = "images/error.png";

// Register the main routine to fire when our
// dependencies have loaded:
$.when(dom_loaded).then(main);


function convertFormToJson(form)
{
	var json = {};
    
    jQuery.each(form, function() {
        json[this.name] = this.value || '';
    });
    
    return json;
}


function showResponse(response)
{
	var status = $("#status");
	if (response.status === "error")
	{
		status.fadeOut(function() {
			setStatusImage(ERROR_IMG);
			status.fadeIn();
		});
	}
	else
	{
		var sim = $('#simulationResponse');
		for (fieldName in response) {
			$('#'+fieldName, sim).text(response[fieldName].toFixed(2));
			console.log("%O: %O", fieldName, response[fieldName]);
		}

		status.fadeOut(function() {
			sim.fadeIn();
		});
	}
}


function assertValidParameters(form)
{
    var valid = true;
	
    jQuery.each(form, function() {
		console.log("element: ", this.name, this.value)
		var elem = $('input[name='+this.name+']');
		var value = elem.val();
		console.log("value: ", value);
        if (!value)
		{
			elem.addClass('error');
			valid = false;
			console.log("field", this.name, "is not set");
		}
		else
		{
			elem.removeClass('error');
		}
    });
    
    return valid;
}


function runSimulation()
{
	console.log("Running the simulation");
	setStatusImage(PROCESSING_IMG);
	
	// Clear any previous results
	$("#simulationResponse").fadeOut("fast", function() {
		$("#status").fadeIn(function() {
			// Grab the form parameters
			var formArray = $("#simulationForm").serializeArray();
			if (assertValidParameters(formArray))
			{
				var simParams = convertFormToJson(formArray);
				console.log("form JSON:", simParams);

				chrome.runtime.sendMessage(
					simParams,
					function(response) {
						console.log("Background returned %O to popup.", response);
						showResponse(response);
					});
			}
			else
			{
				$("#status").fadeOut();
			}
		})
	});

	// Don't reset the form.
	return false;
}


function setStatusImage(imgUrl)
{
	var status = $("#status");
	status.attr("src", chrome.extension.getURL(imgUrl));
}


function main()
{
	console.log("Main started.");
	
	// Setup the onclick handler for our simulate button
	$("#simulate").click(runSimulation);
	$("#simulationResponse").hide();
	
	setStatusImage(PROCESSING_IMG);
	var status = $("#status");
	status.hide();
}


$(document).ready(function(){
	dom_loaded.resolve();
});