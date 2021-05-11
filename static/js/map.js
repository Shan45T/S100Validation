var map;
var OSM;
var satellitemap;
$(function(){
	var mousePositionControl = new ol.control.MousePosition({
        coordinateFormat: ol.coordinate.createStringXY(4),
        projection: 'EPSG:4326',
        className: 'custom-mouse-position',
        target: document.getElementById('mouse-position'),
        undefinedHTML: 'Mouse not hover on Map'
      });
	var scaleLineControl = new ol.control.ScaleLine();
	OSM = new ol.layer.Tile({
	source : new ol.source.OSM({
		crossOrigin : 'anonymous'
	})
	});
	satellitemap = new ol.layer.Tile({
	source : new ol.source.BingMaps(
	{
		key : 'AtRJu52pIf1CINdLfRGGJz27bXzXkGc8STzexLhnwtQecuzCnF-C_4RQI5KNKA88',
		crossOrigin : 'anonymous',
		imagerySet : 'Aerial',
		params : {
			'LAYERS' : "BingMaps"
		}
	})
	});
	map = new ol.Map({
        layers: [OSM],
        target: 'map',
        controls: ol.control.defaults({
          attributionOptions: {
            collapsible: false
          }
        }).extend([mousePositionControl,scaleLineControl]),
        view: new ol.View({
          center: ol.proj.transform([78.4786, 17.4656],'EPSG:4326','EPSG:3857'),
          zoom: 13
        })
      });
	var states = new ol.layer.Vector({
		title : 'States',
      source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson'
      }),
	  style: new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: 'blue',
            width: 2
          }),
          fill: new ol.style.Fill({
            color: 'transparent'
          })
        })
    });
	map.addLayer(states);
	
		var Districts = new ol.layer.Vector({
		title : 'Districts',
      source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'https://raw.githubusercontent.com/gggodhwani/telangana_boundaries/master/districts.json'
      }),
	  style: new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: 'green',
            width: 2
          }),
          fill: new ol.style.Fill({
            color: 'transparent'
          })
        })
    });
	map.addLayer(Districts);
});

function setOSM() {
	map.getLayers().setAt(0, OSM);
}

function setSatellite() {
	map.getLayers().setAt(0, satellitemap);
}