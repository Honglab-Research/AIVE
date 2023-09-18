"use strict";




var donors			= [];
var genes			= [];
var observations 	= [];
var prjCds 			= [];
$("input[name=prjCds]").each(function(idx) { prjCds.push($(this).val()); });

var paramData = { prjCds : prjCds };
paramData = $.param(paramData, true);
$.ajax({
    type	: "GET",  
    url		: "/ngs/ngsData/sub/correlationChart.json",
    data	: paramData,
    async	: false,
    dataType: "json",
    success	: function(dataList) {
    			donors = dataList.donors;
    			//genes = dataList.genes;
    			observations = dataList.observations;
    } 
});
/*
donors = [
		  {"id": "DO1", "age_diagnosis": 49, "alive": true,  "foobar": true},
		  {"id": "DO2", "age_diagnosis": 62, "alive": false, "foobar": true},
		  {"id": "DO3", "age_diagnosis": 1,  "alive": true,  "foobar": true},
		  {"id": "DO4", "age_diagnosis": 59, "alive": true,  "foobar": true},
		  {"id": "DO5", "age_diagnosis": 12, "alive": true,  "foobar": true},
		  {"id": "DO6", "age_diagnosis": 32, "alive": true,  "foobar": true},
		  {"id": "DO7", "age_diagnosis": 80, "alive": true,  "foobar": true}
];

observations = [
			    {"id": "MU1",  "donorId": "DO1", "geneId": "ENSG00000157764"},
			    {"id": "MU11", "donorId": "DO1", "geneId": "ENSG00000157764"},
			    {"id": "MU2",  "donorId": "DO1", "geneId": "ENSG00000141510"},
			    {"id": "MU3",  "donorId": "DO3", "geneId": "ENSG00000141510"},
			    {"id": "MU3",  "donorId": "DO3", "geneId": "ENSG00000141510"},
			    {"id": "MU4",  "donorId": "DO3", "geneId": "ENSG00000157764"},
			    {"id": "MU5",  "donorId": "DO4", "geneId": "ENSG00000157764"},
			    {"id": "MU6",  "donorId": "DO4", "geneId": "ENSG00000164796"},
			    {"id": "MU7",  "donorId": "DO5", "geneId": "ENSG00000155657"},
			    {"id": "MU8",  "donorId": "DO5", "geneId": "ENSG00000157764"} 
];
observations = [
    {"id": "MU1",  "donorId": "CGAB-01-00001", "geneId": "ENSG00000129474"},
];*/

genes = [
	{"id": "expression_n", "symbol": "RNA-N",  "totalDonors": 500},
	{"id": "expression_t", "symbol": "RNA-T",  "totalDonors": 500},
	{"id": "mutation", "symbol": "DNA",  "totalDonors": 500},
	{"id": "p_expression_n", "symbol": "PROTEIN-N",  "totalDonors": 500},
	{"id": "p_expression_t", "symbol": "PROTEIN-T",  "totalDonors": 500}
];

var donorOpacity = function (d) {
	if( d.type === 'int' ) { 
		return d.value / 100;
	} else {
		return 1;
	}
};

var donorFill = function (d) {
	if( d.type === 'bool' ) {
		if( d.value === true ) {
			return '#abc';
		} else {
			return '#f00';
		}
	} else if( d.type == 'sex') {
		if( d.value === 'Male' ) {
			return '#a2bdfc';
		} else {
			return '#f2bdec';
		} 
	} else {
		return '#6d72c5';
	}
};

var geneOpacity = function (d) {
	return d.value / 40;
};

var sortBool = function(field) {
	return function(a, b) {
		if( a[field] && !b[field] ) {
			return 1;
		} else if( !a[field] && b[field] ) {
			return -1;
		} else {
			return 0;
		}
	};
};

var sortInt = function(field) {
	return function(a, b) {
		return a[field] - b[field];
	};
};

var sortByString = function(field) {
	return function(a,b) {
		if( a[field] < b[field] ) return -1; 
		else if ( a[field] == b[field] ) return 0; 
		else return 1; 
	};
};


var donorTracks = [
  {'name': 'Age at Diagnosis', 'fieldName': 'age_diagnosis', 'group':'Clinical', 'type': 'int', 'sort': sortInt},
  {'name': 'Stage',            'fieldName': 'stage',         'group':'Clinical', 'type': 'int', 'sort': sortByString},
  {'name': 'Smoking',          'fieldName': 'smk',           'group':'Clinical', 'type': 'int', 'sort': sortByString},
  {'name': 'Gender',           'fieldName': 'gender',        'group':'Clinical', 'type': 'sex', 'sort': sortByString}
  /*{'name': 'Alive', 'fieldName': 'alive', 'type': 'bool', 'group':'Clinical','sort': sortBool},
  {'name': 'Foobar', 'fieldName': 'foobar', 'type': 'bool', 'group':'Data', 'sort': sortBool}*/
];

var params = {
		element			: '#grid-div',
		donors			: donors, 
		genes			: genes,
		observations	: observations,
		//height: 450,
		//width: 600,
		height			: 100,
		width			: 600,
		heatMap			: true, 
		trackHeight		: 20,			//ICGC, Clinical, Data Height 
		trackLegendLabel: '<i>?</i>',	//Track.js, TrackGrup.js Use
		donorTracks		: donorTracks,	//MainGrid.js Use
		donorOpacityFunc: donorOpacity,	//MainGrid.js Use
		donorFillFunc	: donorFill,	//MainGrid.js Use
		geneOpacityFunc	: geneOpacity,	//MainGrid.js Use
		isCorrelation	: true
};

var grid = new OncoGrid(params);
grid.render();

function removeCleanDonors() {
	var criteria = function (d) {
		return d.score === 0;
	};

	grid.removeDonors(criteria);
}

function toggleCrosshair() {
	grid.toggleCrosshair();
}

function toggleGridLines() {
	grid.toggleGridLines();
}

function resize() {
	var width = document.getElementById('width-resize').value;
	var height = document.getElementById('height-resize').value;

	grid.resize(width, height);
}