function messages_system(game_id) {
	
	var obj = {};
	
	obj.messages_types = {
		'say' : function(msg) {
			var div = document.createElement("div");
			div.innerText = msg.msg;
			$("history").insertBefore(div, $("history").firstChild);
		},
		'set_rabbit' : function(msg) {
			map.set_rabbit(msg.x, msg.y, msg.color)
		},
		'set_map' : function(msg) {
			map.set_map(msg.x, msg.y, msg.color)
		}/*,
		'set_round' : function(msg) {
			game_turn = msg.color
		}*/
	};
	
	obj.send_msg = function(msg) {
		Ajax().post( '/send_command/' + game_id,
				JSON.stringify(msg),
				{
					onerror:function(r) {
						alert('error');
					}
				}
		);
	};
	
	obj.process_message = function(msg) {
		var type = msg.action;
		func = this.messages_types[type];
		if (typeof func == 'function') {
			var div = document.createElement("div");
			div.innerText = "# Action: " + JSON.stringify(msg);
			$("history").insertBefore(div, $("history").firstChild);
			func(msg);
		}
		else
			alert('Exception: unknown message type');
	};
	
	obj.messages_loop = function() {
		var next_id = 0;
		function request_next_part() {
			Ajax().get("/commands/" + game_id  + "/" + next_id,
					{
						onerror: function (r) {
						},
						onload: function(r) {
							var data = JSON.parse(r.responseText);
							for (x in data) {
								obj.process_message(data[x]);
								next_id = next_id + 1;
							}
							obj.make_callbacks();
						},
						onfinish: function(r) {
							request_next_part();
						}
						// todo ON_ERROR reaction!
					}
			); // ajax.get()
		};// function request_next_part
		
		request_next_part();
	};
	
	obj.make_callbacks = function () {
		map.display();
	}
	
	return obj;
}
	