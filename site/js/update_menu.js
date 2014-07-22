var MENU_JSON_FNAME = './js/source.json';
var MENU_JSON       = null;

var db    = document.getElementById('db');
var probe = document.getElementById('probe');
var clust = document.getElementById('clust');
 
function makeOption(value, text) {
    return('<option value="' + value + '">' + text + '</option>');
};

/* Load in the first menu's items */
d3.json(MENU_JSON_FNAME, function(thing) { 
    MENU_JSON = thing;

    for (var x in MENU_JSON) {
        db.innerHTML += makeOption(x, x);
    };
    db.selectedIndex = -1;
};

/* Functions for dynamically loading the other menus */
function updateProbeList() {
    var select_db = db.selectedOptions[0].value;
    var SUBMENU   = MENU_JSON[[select_db]];

    probe.innerHTML = "";
    for (var x in SUBMENU) {
        probe.innerHTML += makeOption(x,x);
    };
    probe.selectedIndex = -1;
};

function updateClustList() {
    var select_db    = db.selectedOptions[0].value;
    var select_probe = probe.selectedOptions[0].value;
    var SUBMENU      = MENU_JSON[[select_db]][[select_probe]];

    clust.innerHTML = "";
    for (var x in SUBMENU) {
        x = SUBMENU[x]; /* a little jiggering since SUBMENU now an array */
        clust.innerHTML += makeOption('../' + select_db + '/' + x + '.json', x);
    };
    clust.selectedIndex = -1;
};
