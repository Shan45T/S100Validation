$(document).ready(function(){
	var layerSwitcher = new ol.control.LayerSwitcher({
		tipLabel : 'Layers',
		target:'layers',
		})


	map.addControl(layerSwitcher);
});

ol.control.LayerSwitcher = function(opt_options) 
{	var options = opt_options || {};
	var self = this;
	this.dcount = 0;
	this.show_progress = options.show_progress;
	this.oninfo = (typeof (options.oninfo) == "function" ? options.oninfo: null);
	this.onextent = (typeof (options.onextent) == "function" ? options.onextent: null);
	this.hasextent = options.extent || options.onextent;
	this.hastrash = options.trash;
	this.reordering = (options.reordering!==false);

	var element;
	if (options.target) 
	{	element = $("<div>").addClass(options.switcherClass || "ol-layerswitcher");
	}
	else
	{	element = $("<div>").addClass((options.switcherClass || 'ol-layerswitcher') +' ol-unselectable ol-control ol-collapsed');
	
		this.button = $("<button>")
					.on("touchstart", function(e)
					{	element.toggleClass("ol-collapsed"); 
						e.preventDefault(); 
						self.overflow();
					})
					.click (function()
					{	element.toggleClass("ol-forceopen").addClass("ol-collapsed"); 
						self.overflow();
					})
					.appendTo(element);
		if (options.mouseover)
		{	$(element).mouseleave (function(){ element.addClass("ol-collapsed"); })
				.mouseover(function(){ element.removeClass("ol-collapsed"); });
		}
		this.topv = $("<div>").addClass("ol-switchertopdiv")
			.click(function(){ self.overflow("+50%"); })
			.appendTo(element);
		this.botv = $("<div>").addClass("ol-switcherbottomdiv")
			.click(function(){ self.overflow("-50%"); })
			.appendTo(element);
	}
	this.panel_ = $("<ul>").addClass("panel")
				.appendTo(element);
	ol.control.Control.call(this, 
	{	element: element.get(0),
		target: options.target
	});
	this.target = options.target;
};
ol.inherits(ol.control.LayerSwitcher, ol.control.Control);



/**
 * Set the map instance the control is associated with.
 * @param {ol.Map} map The map instance.
 */
ol.control.LayerSwitcher.prototype.setMap = function(map) 
{   ol.control.Control.prototype.setMap.call(this, map);
	this.drawPanel();
	
	if (this.map_)
	{	this.map_.getLayerGroup().un('change', this.drawPanel, this);
		this.map_.un('moveend', this.viewChange, this);
		//this.map.un('change:size', this.overflow, this);
		// console.log("remove");
	}

	this.map_ = map;
	// Get change (new layer added or removed)
	if (map) 
	{	map.getLayerGroup().on('change', this.drawPanel, this);
		map.on('moveend', this.viewChange, this);
		map.on('change:size', this.overflow, this);
	}
};

/** Calculate overflow and add scrolls
*	@param {-1|0|1|+50%|-50%} dir scroll direction
*/
ol.control.LayerSwitcher.prototype.overflow = function(dir)
{	
	if (this.button) 
	{	// Nothing to show
		if (this.panel_.css('display')=='none')
		{	$(this.element).css("height", "auto");
			return;
		}
		// Calculate offset
		var h = $(this.element).outerHeight();
		var hp = this.panel_.outerHeight();
		var dh = this.button.position().top + this.button.outerHeight(true);
		var top = this.panel_.position().top-dh;
		if (hp > h-dh)
		{	// Bug IE: need to have an height defined
			$(this.element).css("height", "100%");
			switch (dir)
			{	case 1: top += 2*$("li",this.panel_).height(); break;
				case -1: top -= 2*$("li",this.panel_).height(); break;
				case "+50%": top += Math.round(h/2); break;
				case "-50%": top -= Math.round(h/2); break;
				default: break;
			}
			// Scroll div
			if (top+hp <= h-3*dh/2) 
			{	top = h-3*dh/2-hp;
				this.botv.hide();
			}
			else
			{	this.botv.css("display","");//show();
			}
			if (top >= 0) 
			{	top = 0;
				this.topv.hide();
			}
			else
			{	this.topv.css("display","");
			}
			// Scroll ?
			this.panel_.css('top', top+"px");
		}
		else
		{	$(this.element).css("height", "auto");
			this.panel_.css('top', "0px");
			this.botv.hide();
			this.topv.hide();
		}
	}
}

/**
 * On view change hide layer depending on resolution / extent
 * @param {ol.event} map The map instance.
 * @private
 */
ol.control.LayerSwitcher.prototype.viewChange = function(e) 
{
	var map = this.map_;
	var res = this.map_.getView().getResolution();
	$("li", this.panel_).each(function()
	{	var l = $(this).data('layer');
		if (l)
		{	if (l.getMaxResolution()<=res || l.getMinResolution()>=res) $(this).addClass("ol-layer-hidden");
			else 
			{	var ex0 = l.getExtent();
				if (ex0)
				{	var ex = map.getView().calculateExtent(map.getSize());
					if (!ol.extent.intersects(ex, ex0)) 
					{	$(this).addClass("ol-layer-hidden");
					}
					else $(this).removeClass("ol-layer-hidden");
				}
				else $(this).removeClass("ol-layer-hidden");
			}
		}
	});
}

/**
 *	Draw the panel control (prevent multiple draw due to layers manipulation on the map with a delay function)
 */
ol.control.LayerSwitcher.prototype.drawPanel = function(e) 
{
	if (!this.getMap()) return;
	var self = this;
	// Multiple event simultaneously / draw once => put drawing in the event queue
	this.dcount++;
	setTimeout (function(){ self.drawPanel_(); }, 0);
}

/** Delayed draw panel control 
 * @private
 */
ol.control.LayerSwitcher.prototype.drawPanel_ = function(e) 
{
	if (--this.dcount || this.dragging_) return;
	this.panel_.html("");
	this.drawList (this.panel_, this.getMap().getLayers());
}

/** Change layer visibility according to the baselayer option
 * @param {ol.layer}
 * @param {Array{ol.layer}} related layers
 */
ol.control.LayerSwitcher.prototype.switchLayerVisibility = function(l, layers)
{
	if (!l.get('baseLayer')) {
		
		
		l.setVisible(!l.getVisible());
		
		 var mapLayers = map.getLayers().getArray();
			for (var i = 0; i < mapLayers.length; i++) {
				if(mapLayers[i].getLayers){
					if (mapLayers[i].getLayers().getArray().length > 0) {
						for (var k = 0; k < mapLayers[i].getLayers().getArray().length; k++) {
							if (mapLayers[i].getLayers().getArray()[k].get("type") == "wfs" && mapLayers[i].getLayers().getArray()[k].get("title") == l.get('title')) {
								mapLayers[i].getLayers().getArray()[k].setVisible(l.getVisible());								
							} 
						}
					}
				}
			 else if (mapLayers[i].get("type") == "wfs" && mapLayers[i].get("title") == l.get('title')) {
				 mapLayers[i].setVisible(l.getVisible());			
				 
				} 
			}
	}
	else 
	{	if (!l.getVisible()) l.setVisible(true);
		layers.forEach(function(li)
		{	if (l!==li && li.get('baseLayer') && li.getVisible()){
			
			li.setVisible(false);
		} 
		});
	}
}

/** Check if layer is on the map (depending on zoom and extent)
 * @param {ol.layer}
 * @return {boolean}
 */
ol.control.LayerSwitcher.prototype.testLayerVisibility = function(layer)
{
	if (this.map_)
	{	var res = this.map_.getView().getResolution();
		if (layer.getMaxResolution()<=res || layer.getMinResolution()>=res) return false;
		else 
		{	var ex0 = layer.getExtent();
			if (ex0)
			{	var ex = this.map_.getView().calculateExtent(this.map_.getSize());
				return ol.extent.intersects(ex, ex0);
			}
			return true;
		}
	}
	return true;
};


/** Start ordering the list
*	@param {event} e drag event
*	@private
*/
ol.control.LayerSwitcher.prototype.dragOrdering_ = function(e)
{	var drag = e.data;
	switch (e.type)
	{	// Start ordering
		case 'mousedown': 
		case 'touchstart':
		{	e.stopPropagation();
			//e.preventDefault();
			drag = 
				{	self: drag.self,
					elt: $(e.currentTarget), 
					start: true, 
					element: drag.self.element, 
					panel: drag.self.panel_, 
					pageY: e.pageY || e.originalEvent.touches[0].pageY 
				};
			drag.elt.parent().addClass('drag');
			$(document).on("mouseup mousemove touchend touchcancel touchmove", drag, drag.self.dragOrdering_);
			break;
		}
		// Stop ordering
		case 'touchcancel': 
		case 'touchend': 
		case 'mouseup':	
		{	if (drag.target) 
			{	// Get drag on parent
				var drop = drag.layer;
				var target = drag.target;
				if (drop && target) 
				{	var collection ;
					if (drag.group) collection = drag.group.getLayers();
					else collection = drag.self.getMap().getLayers();
					var layers = collection.getArray();
					// Switch layers
					for (var i=0; i<layers.length; i++) 
					{	if (layers[i]==drop) 
						{	collection.removeAt (i);
							break;
						}
					}
					for (var j=0; j<layers.length; j++) 
					{	if (layers[j]==target) 
						{	if (i>j) collection.insertAt (j,drop);
							else collection.insertAt (j+1,drop);
							break;
						}
					}
				}
			}
			
			$("li",drag.elt.parent()).removeClass("dropover");
			drag.elt.removeClass("drag");
			drag.elt.parent().removeClass("drag");
			$(drag.element).removeClass('drag');
			if (drag.div) drag.div.remove();

			$(document).off("mouseup mousemove touchend touchcancel touchmove", drag.self.dragOrdering_);
			break;
		}
		// Ordering
		default: 
		{	// First drag (more than 2 px) => show drag element (ghost)
			if (drag.start && Math.abs(drag.pageY - (e.pageY || e.originalEvent.touches[0].pageY)) > 2)
			{	drag.start = false;
				drag.elt.addClass("drag");
				drag.layer = drag.elt.data('layer');
				drag.target = false;
				drag.group = drag.elt.parent().parent().data('layer');
				// Ghost div
				drag.div = $("<li>").appendTo(drag.panel);
				drag.div.css ({ position: "absolute", "z-index":10000, left:drag.elt.position().left, opacity:0.5 })
						.html($(drag.elt).html())
						.addClass("ol-dragover")
						.width(drag.elt.width())
						.height(drag.elt.height());
				$(drag.element).addClass('drag');
			}
			if (!drag.start)
			{	e.preventDefault();
				e.stopPropagation();
				
				// Ghost div
				drag.div.css ({ top:(e.pageY || e.originalEvent.touches[0].pageY)-drag.panel.offset().top+5 });
				
				var li;
				if (e.pageX) li = $(e.target);
				else li = $(document.elementFromPoint(e.originalEvent.touches[0].clientX, e.originalEvent.touches[0].clientY)); 
				if (li.hasClass("ol-switcherbottomdiv")) 
				{	drag.self.overflow(-1);
				}
				else if (li.hasClass("ol-switchertopdiv")) 
				{	drag.self.overflow(1);
				}
				if (!li.is("li")) li = li.closest("li");
				if (!li.hasClass('dropover')) $("li", drag.elt.parent()).removeClass("dropover");
				if (li.parent().hasClass('drag') && li.get(0) !== drag.elt.get(0))
				{	var target = li.data("layer");
					// Don't mix layer level
					if (target && !target.get("allwaysOnTop") == !drag.layer.get("allwaysOnTop"))
					{	li.addClass("dropover");
						drag.target = target;
					}
					else
					{	drag.target = false;
					}
				} else drag.target = false;

				if (!drag.target) drag.div.hide();
				else drag.div.show();
			}
			break;
		}
	}
};


/** Change opacity on drag 
*	@param {event} e drag event
*	@private
*/
ol.control.LayerSwitcher.prototype.dragOpacity_ = function(e)
{	var drag = e.data;
	switch (e.type)
	{	// Start opacity
		case 'mousedown': 
		case 'touchstart':
		{	e.stopPropagation();
			e.preventDefault();
			drag.start = e.pageX || e.originalEvent.touches[0].pageX;
			drag.elt = $(e.target);
			drag.layer = drag.elt.closest("li").data('layer')
			drag.self.dragging_ = true;
			$(document).on("mouseup touchend mousemove touchmove touchcancel", drag, drag.self.dragOpacity_);
			break;
		}
		// Stop opacity
		case 'touchcancel': 
		case 'touchend': 
		case 'mouseup':	
		{	$(document).off("mouseup touchend mousemove touchmove touchcancel", drag.self.dragOpacity_);
			drag.layer.setOpacity(drag.opacity);
			drag.self.dragging_ = false;
			drag = false;
			break;
		}
		// Move opcaity
		default: 
		{	var x = e.pageX || e.originalEvent.touches[0].pageX;
			var dx = Math.max ( 0, Math.min( 1, (x - drag.elt.parent().offset().left) / drag.elt.parent().width() ));
			drag.elt.css("left", (dx*100)+"%");
			drag.opacity = dx;
			drag.layer.setOpacity(dx);
			break;
		}
	}
}


/** Render a list of layer
 * @param {elt} element to render
 * @layers {Array{ol.layer}} list of layer to show
 * @api stable
 */
ol.control.LayerSwitcher.prototype.drawList = function(ul, collection)
{	var self = this;
	var layers = collection.getArray();
	var setVisibility = function(e) 
	{	e.stopPropagation();
		e.preventDefault();
		var l = $(this).parent().data("layer");
		self.switchLayerVisibility(l,collection);
	};
	function moveLayer (l, layers, inc)
	{	
		for (var i=0; i<layers.getLength(); i++)
		{	if (layers.item(i) === l) 
			{	layers.remove(l);
				layers.insertAt(i+inc, l);
				return true;
			}
			if (layers.item(i).getLayers && moveLayer (l, layers.item(i).getLayers(), inc)) return true;
		}
		return false;
	};
	function moveLayerUp(e) 
	{	e.stopPropagation();
		e.preventDefault(); 
		moveLayer($(this).closest('li').data("layer"), self.map_.getLayers(), +1); 
	};
	function moveLayerDown(e) 
	{	e.stopPropagation();
		e.preventDefault(); 
		moveLayer($(this).closest('li').data("layer"), self.map_.getLayers(), -1); 
	};
	function onInfo(e) 
	{	e.stopPropagation();
		e.preventDefault(); 
		self.oninfo($(this).closest('li').data("layer")); 
	};
	function zoomExtent(e) 
	{	e.stopPropagation();
		e.preventDefault(); 
		if (self.onextent) self.onextent($(this).closest('li').data("layer")); 
		else self.map_.getView().fit ($(this).closest('li').data("layer").getExtent(), self.map_.getSize()); 
	};
	
	function showLegend(e){
		$(("#"+$(this).closest('li').data("layer").get("title")+"")).toggle();
	};
	
	function showOpacity(e){
		$(("#"+$(this).closest('li').data("layer").get("title")+"o")).toggle();
	}
	
	function removeLayer(e) 
	{	e.stopPropagation();
		e.preventDefault();
		var li = $(this).closest("ul").parent();
		if (li.data("layer")) 
		{	li.data("layer").getLayers().remove($(this).closest('li').data("layer"));
			if (li.data("layer").getLayers().getLength()==0) removeLayer.call($(".layerTrash", li), e);
		}
		else self.map_.removeLayer($(this).closest('li').data("layer"));
	};
	
	// Add the layer list

	for (var i=layers.length-1; i>=0; i--)
	{	var layer = layers[i];
		if(layers[i].get("title")==undefined || layers[i].get("title")=="undefined"){
			
		}else{
		if (layer.get("displayInLayerSwitcher")===false) continue;

		var d = $("<li>").addClass((layer.getVisible()?"visible ":" ")+(layer.get('baseLayer')?"baselayer":""))
						.data("layer",layer); //.appendTo(ul);
		if (this.reordering)
		{	d.on ("mousedown touchstart", {self:this}, this.dragOrdering_ );
		}
		if (!this.testLayerVisibility(layer)) d.addClass("ol-layer-hidden");
		
		var layer_buttons = $("<div>").addClass("ol-layerswitcher-buttons").appendTo(d);

		// Visibility
		$("<input>")
			.attr('type', layer.get('baseLayer') ? 'radio' : 'checkbox')
			.attr("checked",layer.getVisible())
			.on ('click', setVisibility)
			.appendTo(d);
	
		// Label
		$("<label>").text(layer.get("title") || layer.get("name"))
			.attr('title', layer.get("title") || layer.get("name"))
			.on ('click', setVisibility)
			.attr('unselectable', 'on')
			.css('user-select', 'none')
			.on('selectstart', false)
			.appendTo(d);

		// Layer group
		if (layer.getLayers)
		{	if (layer.get("openInLayerSwitcher")===true) 
			{	this.drawList ($("<ul>").appendTo(d), layer.getLayers());
			}
		}
		
		// Add to the list
		d.appendTo(ul);
	}
}

	if (ul==this.panel_) this.overflow();
};
