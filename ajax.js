var $ = function (id) {
	return document.getElementById(id);
};

function Ajax() {
	var obj = new Object();

	obj.init = function() {
		var requester;
		if (window.XMLHttpRequest) {
			// Mozilla, Safari, Opera ...
			requester = new XMLHttpRequest();
		} else if (window.ActiveXObject) {
			// Internet Explorer
			requester = new ActiveXObject("Microsoft.XMLHTTP");
		}
		return requester;
	}

	function state_changed(req,obj){
		return function() {
			// Completed
			if ((req.readyState == 4)) {
				if (req.status == 200) {
					if (obj.onload) obj.onload(req);
				}
				else {
					if (obj.onerror) obj.onerror(req);
				}
				
				if (obj.onfinish)
					obj.onfinish(req);
			}
			return true;
		};
	}

	obj.get = function(uri, obj) {
		var req = this.init();
		req.onreadystatechange = state_changed(req,obj); //function() { state_changed(); };
		req.open("GET", uri);
		req.send(null);
	}

	obj.post = function(uri, data, obj) {
		var req = this.init();
		req.open("POST", uri);
		req.onreadystatechange = state_changed(req,obj); //function() { state_changed(); };
		req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		req.setRequestHeader("Content-length", data.length);
		req.setRequestHeader("Connection", "close");
		req.send(data);
	}

	obj.init();

	return obj;
};

