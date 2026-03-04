window.dash_clientside = Object.assign({}, window.dash_clientside, {
	utils: {
		getDevicePixelRatio: function(_) {
			return window.devicePixelRatio || 1;
		}
	}
});