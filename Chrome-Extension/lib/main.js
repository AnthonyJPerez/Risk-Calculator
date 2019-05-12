const URL = "https://id5qu1pl4a.execute-api.us-east-2.amazonaws.com/Production/simulation";

//// 
// Globals
////
var dom_loaded = new $.Deferred();

// Register the main routine to fire when our
// dependencies have loaded:
$.when(dom_loaded).then(main);


(function()
{    
	dom_loaded.resolve();
	console.info("DOM is ready");
})();


// Callback function to handle messages received from the popup. The
// popup will send simulation parameters submitted by the user.
function popupMessageHandler (parameters, sender, replyToPopup)
{
	_Instrument("popupMessageHandler");
	_Log("Received message from popup -- parameters: %O, sender: %O, replyToPopup: %O", parameters, sender, replyToPopup);
	
	// Perform an AJAX request here to the server. 
	//
	// POST to create/submit the initial request,
	// GET using the ID returned by the server.
	//
	var requestBody = {
		initialAttackerArmies: parameters.attacker_armies, 
		numAttackerDice: parameters.attacker_die_count,
		attackerDiceType: parameters.attacker_die_type,
		initialDefenderArmies: parameters.defender_armies,
		numDefenderDice: parameters.defender_die_count,
		defenderDiceType: parameters.defender_die_type
	};
		
	_Log("About to request: %s %O", URL, requestBody);
	$.ajax({
		url: URL,
		type: "POST",
		dataType: "json",
		data: JSON.stringify(requestBody)
	})
	.done(function(data) {
		_Log("Received response from server: %O", data);
		getSimulationResource(data, replyToPopup);
	})
	.fail(function() {
		alert("Ajax failed to fetch data.");
	});
	
	// True allows the replyToPopup reponse handler to stay alive
	// and allow its use in an asynchronous fashion.
	_InstrumentEnd();
	return true;
}


function getSimulationResource(serverResponse, replyToPopup)
{
	_Instrument("getSimulationResource");
	_Log("serverResponse: %O", serverResponse);
	
	var url = URL + "?id=" + serverResponse.id;
	_Log("About to request: %O", url);
	$.ajax({
		url: url,
	})
	.done(function(newResponse) {
		_Log("Received response from server: %O", newResponse);
		if (null != newResponse.status && newResponse.status === "processing")
		{
			// Try the next request in 500ms
			setTimeout(function() 
			{
				getSimulationResource(newResponse, replyToPopup);
			}, 1000);
		}
		else
		{	
			replyToPopup(newResponse);
		}
	})
	.fail(function() {
		alert("Ajax failed to fetch data.");
	});
	
	_InstrumentEnd();
}


function main()
{
	_Instrument("Main");

	// Listen to messages from the popup
	chrome.runtime.onMessage.addListener(popupMessageHandler);

	_InstrumentEnd();
}
