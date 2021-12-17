/*
 * TODO:
 * 1. create a clear polygons button
 * 2. integrate the properties clicks, round values, int(rent).
 */


import "ol/ol.css";
import Draw from "ol/interaction/Draw";
import Map from "ol/Map";
import Overlay from "ol/Overlay";
import View from "ol/View";
import {Circle as CircleStyle, Fill, Stroke, Style} from "ol/style";
import {LineString, Polygon} from "ol/geom";
import {OSM, Vector as VectorSource, ImageWMS} from "ol/source";
import {Tile as TileLayer, Vector as VectorLayer, Image} from "ol/layer";
import {getArea, getLength} from "ol/sphere";
import {unByKey} from "ol/Observable";
import {Control, defaults, ScaleLine, MousePosition, ZoomToExtent} from "ol/control";
// import * as olCoordinate from "ol/coordinate";
import {createStringXY} from "ol/coordinate";
import {transform} from "ol/proj";

var measuring = 0;

var style1 = new Style({fill: new Fill({
                            color: "rgba(255, 255, 255, 0.2)",
                        }),
                        stroke: new Stroke({
                            color: "#C800FF",
                            width: 2,
                        }),
                        image: new CircleStyle({
                            radius: 7,
                            fill: new Fill({
                                color: "#C800FF",
                            }),
                        }),
});

var view1 = new View({center: transform([13.199195, 55.70331], "EPSG:4326", "EPSG:3857"), zoom: 13});

class measureButton extends Control {
    /**
    * Docs:
    * @param {Object} [opt_options] Control options.
    */
    constructor(opt_options) {
        const options = opt_options || {};

        const button = document.createElement("button");
        button.innerHTML = "M";
        var buttonTipLabel = options.buttonTipLabel ? options.buttonTipLabel : "Open Measuring Tool";
        button.title = buttonTipLabel;
        const element = document.createElement("div");
        element.className = "measure ol-unselectable ol-control";
        element.appendChild(button);

        super({
            element: element,
            target: options.target,
        });

        button.addEventListener("click", this.enableMeasuring.bind(this), false);
    }

    enableMeasuring() {
        if (measuring == 0) {
            alert("Measuring Tool Enabled");
            measuring = 1;
            map.on("pointermove", pointerMoveHandler);
            addInteraction();
            map.getViewport().addEventListener("mouseout", hideMeasureTooptip);


        } else {
            alert("measuring tool disabled");
            measuring = 0;
            map.un("pointermove", pointerMoveHandler);
            map.removeInteraction(draw);
            map.getViewport().removeEventListener("mouseout", hideMeasureTooptip);
            map.removeOverlay(helpTooltip);
        }
    }
};


class clearButton extends Control {
    /**
    * @param {Object} [opt_options] Control options.
    */
    constructor(opt_options) {
        const options = opt_options || {};

        const button = document.createElement("button");
        button.innerHTML = "C";
        var buttonTipLabel = options.buttonTipLabel ? options.buttonTipLabel : "Clear Map";
        button.title = buttonTipLabel;
        const element = document.createElement("div");
        element.className = "clear ol-unselectable ol-control";
        element.appendChild(button);

        super({
            element: element,
            target: options.target,
        });

        button.addEventListener("click", this.clearAll.bind(this), false);
    }

    clearAll() {
        location.reload();
        /*
        for (var i = 0, length = vectorCount.length; i < length; i++) {
            document.getElementsByClassName("v"+vectorCount)[i].style.display = "none";
        }

        map.removeLayer(vectors["v" + vectorCount]);
        const vector = new VectorLayer({
            source: new VectorSource(),
            style: style1
        });
        vectorCount += 1;
        vectors["v" + vectorCount] = vector;
        map.addLayer(vectors["v" + vectorCount]);
        */
    }
};


function hideMeasureTooptip(){
    helpTooltipElement.classList.add("hidden");
}


const raster = new TileLayer({
  source: new OSM(),
});

const source = new VectorSource();

const vector = new VectorLayer({
  source: source,
  style: style1
});

var vectors = {};
var vectorCount = 1;
vectors["v" + vectorCount] = vector;

/**
 * Currently drawn feature.
 * @type {import("../src/ol/Feature.js").default}
 */
let sketch;

/**
 * The help tooltip element.
 * @type {HTMLElement}
 */
let helpTooltipElement;

/**
 * Overlay to show the help messages.
 * @type {Overlay}
 */
let helpTooltip;

/**
 * The measure tooltip element.
 * @type {HTMLElement}
 */
let measureTooltipElement;

/**
 * Overlay to show the measurement.
 * @type {Overlay}
 */
let measureTooltip;

/**
 * Message to show when the user is drawing a polygon.
 * @type {string}
 */
const continuePolygonMsg = "Click to continue drawing the polygon";

/**
 * Message to show when the user is drawing a line.
 * @type {string}
 */
const continueLineMsg = "Click to continue drawing the line";

/**
 * Handle pointer move.
 * @param {import("../src/ol/MapBrowserEvent").default} evt The event.
 */
const pointerMoveHandler = function (evt) {
  if (evt.dragging) {
    return;
  }
  /** @type {string} */
  let helpMsg = "Click to start drawing";

  if (sketch) {
    const geom = sketch.getGeometry();
    if (geom instanceof Polygon) {
      helpMsg = continuePolygonMsg;
    } else if (geom instanceof LineString) {
      helpMsg = continueLineMsg;
    }
  }

  helpTooltipElement.innerHTML = helpMsg;
  helpTooltip.setPosition(evt.coordinate);

  helpTooltipElement.classList.remove("hidden");
};


/* ----- map definition ------- */


var housingLayer = new ImageWMS({
    url: "https://geoserver.gis.lu.se/geoserver/wms",
    params: {
    "LAYERS": "salvazin_dummy_data", // ,salvazin_landmarks
    "TILED": true
    },
    serverType: "geoserver"
});

//OpenStreetMap background + layers handling

var salvazin = new Image({source: housingLayer});

var layers = {};
var layersCount = 1;
layers["salvazin" + layersCount] = salvazin;


const map = new Map({
  controls: defaults().extend([ // {attributionOptions:({collapsible: false})}

        //Control for displaying a scale line
        new ScaleLine({
            units: "metric",
            bar: true,
            steps: 4,
            text: false,
            minWidth: 140,
        }),

        //Extra functionality of the map
        //Control for displaying coordinates
        new MousePosition({
            coordinateFormat: createStringXY(4),
            projection: "EPSG:4326",
            target: document.getElementById("mouse-position")
        }),
        new ZoomToExtent({
            extent: transform([13.199195,13.199195, 55.70331,55.70331], "EPSG:4326", "EPSG:3857")
        }),

        new measureButton(),
        new clearButton()

    ]),
  layers: [raster, vectors["v" + vectorCount], layers["salvazin" + layersCount]],
  target: "map",
  view: view1
});

const typeSelect = document.getElementById("type");

let draw; // global so we can remove it later

/**
 * Format length output.
 * @param {LineString} line The line.
 * @return {string} The formatted length.
 */
const formatLength = function (line) {
  const length = getLength(line);
  let output;
  if (length > 100) {
    output = Math.round((length / 1000) * 100) / 100 + " " + "km";
  } else {
    output = Math.round(length * 100) / 100 + " " + "m";
  }
  return output;
};

/**
 * Format area output.
 * @param {Polygon} polygon The polygon.
 * @return {string} Formatted area.
 */
const formatArea = function (polygon) {
  const area = getArea(polygon);
  let output;
  if (area > 10000) {
    output = Math.round((area / 1000000) * 100) / 100 + " " + "km<sup>2</sup>";
  } else {
    output = Math.round(area * 100) / 100 + " " + "m<sup>2</sup>";
  }
  return output;
};

function addInteraction() {
  const type = typeSelect.value == "area" ? "Polygon" : "LineString";
  draw = new Draw({
    source: source,
    type: type,
    style: new Style({
      fill: new Fill({
        color: "rgba(255, 255, 255, 0.2)",
      }),
      stroke: new Stroke({
        color: "rgba(0, 0, 0, 0.5)",
        lineDash: [10, 10],
        width: 2,
      }),
      image: new CircleStyle({
        radius: 5,
        stroke: new Stroke({
          color: "rgba(0, 0, 0, 0.7)",
        }),
        fill: new Fill({
          color: "rgba(255, 255, 255, 0.2)",
        }),
      }),
    }),
  });
  map.addInteraction(draw);

  createMeasureTooltip();
  createHelpTooltip();

  let listener;
  draw.on("drawstart", function (evt) {
    // set sketch
    sketch = evt.feature;

    /** @type {import("../src/ol/coordinate.js").Coordinate|undefined} */
    let tooltipCoord = evt.coordinate;

    listener = sketch.getGeometry().on("change", function (evt) {
      const geom = evt.target;
      let output;
      if (geom instanceof Polygon) {
        output = formatArea(geom);
        tooltipCoord = geom.getInteriorPoint().getCoordinates();
      } else if (geom instanceof LineString) {
        output = formatLength(geom);
        tooltipCoord = geom.getLastCoordinate();
      }
      measureTooltipElement.innerHTML = output;
      measureTooltip.setPosition(tooltipCoord);
    });
  });

  draw.on("drawend", function () {
    measureTooltipElement.className = "ol-tooltip ol-tooltip-static";
    measureTooltip.setOffset([0, -7]);
    // unset sketch
    sketch = null;
    // unset tooltip so that a new one can be created
    measureTooltipElement = null;
    createMeasureTooltip();
    unByKey(listener);
  });
}

// Creates a new help tooltip

function createHelpTooltip() {
  if (helpTooltipElement) {
    helpTooltipElement.parentNode.removeChild(helpTooltipElement);
  }
  helpTooltipElement = document.createElement("div");
  helpTooltipElement.className = "ol-tooltip hidden";
  helpTooltip = new Overlay({
    element: helpTooltipElement,
    offset: [15, 0],
    positioning: "center-left",
  });
  map.addOverlay(helpTooltip);
}

// Creates a new measure tooltip

function createMeasureTooltip() {
  if (measureTooltipElement) {
    measureTooltipElement.parentNode.removeChild(measureTooltipElement);
  }
  measureTooltipElement = document.createElement("div");
  measureTooltipElement.className = "ol-tooltip ol-tooltip-measure v"+vectorCount;
  measureTooltip = new Overlay({
    element: measureTooltipElement,
    offset: [0, -15],
    positioning: "bottom-center",
    stopEvent: false,
    insertFirst: false,
  });
  map.addOverlay(measureTooltip);
};


// Let user change the geometry type:

function changeMeasureType() {
    map.removeInteraction(draw);
}

typeSelect.addEventListener("change", changeMeasureType);

/* ---- housing filtering ----- */

map.on("singleclick", function (evt) {
    if (measuring == 0){
        var viewResolution = /** @type {number} */ (view1.getResolution());
        var url = housingLayer.getFeatureInfoUrl(
            evt.coordinate,
            viewResolution,
            "EPSG:3857",
            { "INFO_FORMAT": "application/json" });
        // JQuery HTTP GET request
        $.get(url, function (resp) {
            var features = resp.features;
            if (features.length > 0) {
            var properties = features[0].properties;
                fillInfoPanel(properties)
            }
        });
    }
});


function fillInfoPanel(props) {
    var infoPanel = document.getElementById("infoContent");
    var content = "";
    var listItems = "";
    for (var prop in props) {
        // skip loop if the property is from prototype
        if (!props.hasOwnProperty(prop)) continue;
        if (prop != "bbox") {
        listItems += "<li>" + "<b>" + prop + "</b>: " + props[prop] + "</li>";
        }
    }
    content = "<ul>" + listItems + "</ul>";
    infoPanel.innerHTML = content;
};


function toggleInfo() {
    var checkBox = document.getElementById("infoToggle");
    var checked = checkBox.checked;
    var display = ""
    if (checked) {
        display = "block"
    } else {
        display = "none"
    }
    document.getElementById("info").style.display = display
};
function toggleFilters() {
    var checkBox = document.getElementById("filtersToggle");
    var checked = checkBox.checked;
    var display = ""
    if (checked) {
        display = "block"
    } else {
        display = "none"
    }
    document.getElementById("filters").style.display = display
};

// Filters handling
// docs: https://docs.geoserver.org/stable/en/user/styling/sld/reference/filters.html

function updateMap() {
    map.removeLayer(layers["salvazin" + layersCount]);

    var filters = "";
    if (document.filtersForm.rentMax.value != "") {
        filters += "<PropertyIsLessThan><PropertyName>rent</PropertyName><Literal>" + document.filtersForm.rentMax.value + "</Literal></PropertyIsLessThan>"
    };

    if (document.filtersForm.rentMin.value != "") {
        filters += "<PropertyIsGreaterThan><PropertyName>rent</PropertyName><Literal>" + document.filtersForm.rentMin.value + "</Literal></PropertyIsGreaterThan>"
    };

    if (document.filtersForm.userRank.value != "") {
        filters += "<PropertyIsLessThan><PropertyName>rank</PropertyName><Literal>" + document.filtersForm.userRank.value + "</Literal></PropertyIsLessThan>"
    };

    var trailer = document.getElementById("trailer").checked;
    var house = document.getElementById("house").checked;
    var apartment = document.getElementById("apartment").checked;

    if(!trailer){
        filters += "<PropertyIsNotEqualTo><PropertyName>type</PropertyName><Literal>trailer</Literal></PropertyIsNotEqualTo>"
    }
    if(!house){
        filters += "<PropertyIsNotEqualTo><PropertyName>type</PropertyName><Literal>house</Literal></PropertyIsNotEqualTo>"
    }
    if(!apartment){
        filters += "<PropertyIsNotEqualTo><PropertyName>type</PropertyName><Literal>apartment</Literal></PropertyIsNotEqualTo>"
    }

    var housingLayer = new ImageWMS({
        url: "https://geoserver.gis.lu.se/geoserver/wms",
        params: {
        "LAYERS": "salvazin_dummy_data", // ,salvazin_landmarks
        "FILTER": "(<Filter><And>" + filters + "</And></Filter>)()"
        },
        serverType: "geoserver"
    });

    var salvazin = new Image({source: housingLayer});
    layersCount += 1;
    layers["salvazin" + layersCount] = salvazin;
    map.addLayer(layers["salvazin" + layersCount]);
};

function clearFilters() {
    document.getElementById("trailer").checked = true;
    document.getElementById("house").checked = true;
    document.getElementById("apartment").checked = true;
    document.filtersForm.rentMax.value = "";
    document.filtersForm.rentMin.value = "";
    document.filtersForm.userRank.value = "";

    map.removeLayer(layers["salvazin" + layersCount]);

    var housingLayer = new ImageWMS({
        url: "https://geoserver.gis.lu.se/geoserver/wms",
        params: {
        "LAYERS": "salvazin_dummy_data" // ,salvazin_landmarks
        },
        serverType: "geoserver"
    });

    var salvazin = new Image({source: housingLayer});
    layersCount += 1;
    layers["salvazin" + layersCount] = salvazin;
    map.addLayer(layers["salvazin" + layersCount]);
};


document.getElementById("infoToggle").addEventListener("click", toggleInfo);
document.getElementById("filtersToggle").addEventListener("click", toggleFilters);
document.getElementById("clear").addEventListener("click", clearFilters);
document.getElementById("filtersForm").addEventListener("change", updateMap);
