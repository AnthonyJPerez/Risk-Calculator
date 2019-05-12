const URL = "https://us-central1-risk-simulator-239019.cloudfunctions.net/simulate";

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
        num_simulations: parseInt(parameters.total_simulation_count),
        attacker_armies: parseInt(parameters.attacker_armies), 
        attack_until: 0,
        defender_armies: parseInt(parameters.defender_armies),
        defend_until: 0,
        ruleset: {
            attackerDice: parseInt(parameters.attacker_die_count),
            attackerDieSize: [1, parseInt(parameters.attacker_die_type)],
            minArmiesForAttack: 1,
            defenderDice: parseInt(parameters.defender_die_count),
            defenderDieSize: [1, parseInt(parameters.defender_die_type)],
            minArmiesForDefend: 0,
            tieBehavior: 0
        }
	};
		
	_Log("About to request: %s %O", URL, requestBody);
	$.ajax({
		url: URL,
		type: "POST",
		dataType: "json",
        data: JSON.stringify(requestBody, null, "\t"),
        contentType: 'application/json;charset=UTF-8'
	})
	.done(function(data) {
		_Log("Received response from server: %O", data);
		replyToPopup(data);
	})
	.fail(function() {
		alert("Ajax failed to fetch data.");
	});
	
	// True allows the replyToPopup reponse handler to stay alive
	// and allow its use in an asynchronous fashion.
	_InstrumentEnd();
	return true;
}


function main()
{
	_Instrument("Main");

	// Listen to messages from the popup
	chrome.runtime.onMessage.addListener(popupMessageHandler);

	_InstrumentEnd();
}
