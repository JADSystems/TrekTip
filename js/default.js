var map = AmCharts.makeChart("mapdiv", {
	type: "map",

	balloon: {
		color: "#000000"
	},

	dataProvider: {
		map: "usa2Low",
		getAreasFromMap: true
	},

	theme : 'Dark',
	
	areasSettings: {
		autoZoom: true,
		selectedColor: "#CC0000",
		color : "#585858"
		
	},
	
	mouseWheelZoomEnabled: true,
	
	//backgroundAlpha: 100,
	
	smallMap: {	}
							
});

map.addListener("clickMapObject", function (event) {
	if (event.mapObject.id != undefined) {
	document.getElementById('clickData').innerHTML = "You clicked on: " + event.mapObject.title;
	}
	
});
			