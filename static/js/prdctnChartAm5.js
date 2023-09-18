function PrdctnChart(targetId, width, height, callbak){
    this.targetId = targetId;
    this.width = width;
    this.height = height;
    this.amRoot;
    this.amChart;
    this.callbak = callbak;
}

PrdctnChart.prototype.drawSubLineage = function(lineage){
    let prdctnObj = this;
    
    var root = am5.Root.new(prdctnObj.targetId);

    root.setThemes([
        am5themes_Animated.new(root)
    ]);

    var chart = root.container.children.push(am5xy.XYChart.new(root, {
        panX: false,
        panY: false,
        wheelX: false,
        wheelY: false
    }));

    var colors = chart.get("colors");

    let orf1abSubData = [{category:"NSP1",startPos:1,endPos:180,columnSettings:{fill:am5.Color.brighten(colors.getIndex(0),0)}},{category:"NSP2",startPos:181,endPos:818,columnSettings:{fill:am5.Color.brighten(colors.getIndex(1),0)}},{category:"NSP3",startPos:819,endPos:2763,columnSettings:{fill:am5.Color.brighten(colors.getIndex(2),0)}},{category:"NSP4",startPos:2764,endPos:3263,columnSettings:{fill:am5.Color.brighten(colors.getIndex(3),0)}},{category:"NSP5",startPos:3264,endPos:3569,columnSettings:{fill:am5.Color.brighten(colors.getIndex(4),0)}},{category:"NSP6",startPos:3570,endPos:3859,columnSettings:{fill:am5.Color.brighten(colors.getIndex(5),0)}},{category:"NSP7",startPos:3860,endPos:3942,columnSettings:{fill:am5.Color.brighten(colors.getIndex(6),0)}},{category:"NSP8",startPos:3943,endPos:4140,columnSettings:{fill:am5.Color.brighten(colors.getIndex(7),0)}},{category:"NSP9",startPos:4141,endPos:4253,columnSettings:{fill:am5.Color.brighten(colors.getIndex(8),0)}},{category:"NSP10",startPos:4254,endPos:4392,columnSettings:{fill:am5.Color.brighten(colors.getIndex(9),0)}},{category:"NSP11",startPos:4393,endPos:4405,columnSettings:{fill:am5.Color.brighten(colors.getIndex(10),0)}},{category:"NSP12",startPos:4393,endPos:5324,columnSettings:{fill:am5.Color.brighten(colors.getIndex(11),0)}},{category:"NSP13",startPos:5325,endPos:5925,columnSettings:{fill:am5.Color.brighten(colors.getIndex(12),0)}},{category:"NSP14",startPos:5926,endPos:6452,columnSettings:{fill:am5.Color.brighten(colors.getIndex(13),0)}},{category:"NSP15",startPos:6453,endPos:6798,columnSettings:{fill:am5.Color.brighten(colors.getIndex(14),0)}},{category:"NSP16",startPos:6799,endPos:7096,columnSettings:{fill:am5.Color.brighten(colors.getIndex(15),0)}}];
    let sSubdata=[{category:"S1",startPos:14,endPos:685,columnSettings:{fill:am5.Color.brighten(colors.getIndex(0),0)}},{category:"S2",startPos:686,endPos:1273,columnSettings:{fill:am5.Color.brighten(colors.getIndex(1),0)}},{category:"S2'",startPos:816,endPos:1273,columnSettings:{fill:am5.Color.brighten(colors.getIndex(2),0)}},{category:"RBD",startPos:319,endPos:541,columnSettings:{fill:am5.Color.brighten(colors.getIndex(3),0)}},{category:"RBM",startPos:437,endPos:508,columnSettings:{fill:am5.Color.brighten(colors.getIndex(4),0)}},{category:"Fusion peptide 1",startPos:816,endPos:837,columnSettings:{fill:am5.Color.brighten(colors.getIndex(5),0)}},{category:"Fusion peptide 2",startPos:835,endPos:855,columnSettings:{fill:am5.Color.brighten(colors.getIndex(6),0)}},{category:"Heptad repeat 1",startPos:920,endPos:970,columnSettings:{fill:am5.Color.brighten(colors.getIndex(7),0)}},{category:"Heptad repeat 2",startPos:1163,endPos:1202,columnSettings:{fill:am5.Color.brighten(colors.getIndex(8),0)}}];

    let maxPos, data;

    if (lineage == 'ORF1ab')  {
        data = orf1abSubData;
        maxPos = 7096;
    } else{
        data = sSubdata;
        maxPos = 1273;
    } 

    var legend = chart.children.push(am5.Legend.new(root, {
        centerX: am5.p50,
        x: am5.p50
    }))
    
    // Create axes
    var yAxis = chart.yAxes.push(
        am5xy.CategoryAxis.new(root, {
            categoryField: "category",
            renderer: am5xy.AxisRendererY.new(root, { inversed: true }),
            tooltip: am5.Tooltip.new(root, {
                themeTags: ["axis"],
                animationDuration: 200
            })
        })
    );
  
    if (lineage == 'ORF1ab')  {
        yAxis.data.setAll([
            { category: "NSP1" },{ category: "NSP2" },{ category: "NSP3" },{ category: "NSP4" },{ category: "NSP5" },{ category: "NSP6" },{ category: "NSP7" },{ category: "NSP8" },{ category: "NSP9" },{ category: "NSP10" },{ category: "NSP11" },{ category: "NSP12" },{ category: "NSP13" },{ category: "NSP14" },{ category: "NSP15" },{ category: "NSP16" }
        ]);
    } else {
        yAxis.data.setAll([
            { category: "S1" },{ category: "S2" },{ category: "S2'" },{ category: "RBD" },{ category: "RBM" },{ category: "Fusion peptide 1" },{ category: "Fusion peptide 2" },{ category: "Heptad repeat 1" },{ category: "Heptad repeat 2" },
        ]);  
    };
  
    var xAxis = chart.xAxes.push(am5xy.ValueAxis.new(root, {
        min : 1,
        max : maxPos,
        renderer: am5xy.AxisRendererX.new(root, {})
      }));
  
    // Add series
    // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
    var series = chart.series.push(am5xy.ColumnSeries.new(root, {
        xAxis: xAxis,
        yAxis: yAxis,
        openValueXField: "startPos",
        valueXField: "endPos",
        categoryYField: "category",
        sequencedInterpolation: true
    }));

    series.columns.template.setAll({
        templateField: "columnSettings",
        strokeOpacity: 0,
        tooltipText: "{category}: {openValueX} - {valueX}"
    });
   
    series.data.setAll(data);


    series.columns.template.events.on("click", function(ev) {
        prdctnObj.callbak(ev.target.dataItem.dataContext.category);
    });

    // Make stuff animate on load
    // https://www.amcharts.com/docs/v5/concepts/animations/
    series.appear();
    chart.appear(1000, 100);

  
/*
    am5.utils.addEventListener(root.dom, "click", function(ev) {
        debugger;
        var localPoint = chart.plotContainer.toLocal({
          x: ev.clientX,
          y: ev.clientY
        });
        
        var yPosition = yAxis.coordinateToPosition(localPoint.y);
        var yValue = yAxis.positionToValue(yPosition);
        
        var xPosition = xAxis.coordinateToPosition(localPoint.x);
        var xDate = xAxis.positionToDate(xPosition);
        
        console.log("X date", xDate);
        console.log("Y value", yValue);
      });
*/
}