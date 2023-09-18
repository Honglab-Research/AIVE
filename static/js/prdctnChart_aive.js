class PrdctnChart {
    constructor(targetId, isEvent, width, height, callbak) {
        this.targetId = targetId;
        this.width = width;
        this.height = height;
        this.amRoot;
        this.amChart;
        this.callbak = callbak;
        this.paeChart;
        this.icn3dObj;
        this.arrAllMutVirusSeq = [];
        this.arrAllMutVirusChain = [];
        this.isEvent = isEvent;
        this.proteinStruc = 'MN';
        this.seq1 = '';
        this.seq2 = '';
        this.seq3 = '';
        this.seq4 = '';
        this.seq5 = '';
        this.seq6 = '';
        this.seq7 = '';
        this.seq8 = '';
    }

    /**
     * 하이차트 좌표를 이용하여 icn3d를 컨트롤할 스크립트를 만든다.
     * @param {*} cmdKnd 명령어
     * @param {*} posX X좌표
     * @param {*} posY Y좌표
     */
    makeIcn3dCmd(cmdKnd, posX, posY){
        let tmpCmd;
        if (cmdKnd == 'select'){

            tmpCmd = `select .${this.arrAllMutVirusChain[posX]}:${this.arrAllMutVirusSeq[posX].replace(/[^0-9]/g, '')}`

            if (posY){
                tmpCmd += ` or .${this.arrAllMutVirusChain[posY]}:${this.arrAllMutVirusSeq[posY].replace(/[^0-9]/g, '')}`
            }
        }

        return tmpCmd;
    }
    /**
     * 리니지 구분에 따라 sub domain chart를 그린다.
     * @param {*} domainNm  도메인
     */
    drawSubDomain(domainNm) {
        const prdctnObj = this;
        let data, categories;

        if (domainNm == 'ORF1ab') {
            data = [{ x: 1, x2: 180, y: 15 }, { x: 181, x2: 818, y: 14 }, { x: 819, x2: 2763, y: 13 }, { x: 2764, x2: 3263, y: 12 }, { x: 3264, x2: 3569, y: 11 }, { x: 3570, x2: 3859, y: 10 }, { x: 3860, x2: 3942, y: 9 }, { x: 3943, x2: 4140, y: 8 }, { x: 4141, x2: 4253, y: 7 }, { x: 4254, x2: 4392, y: 6 }, { x: 4393, x2: 4405, y: 5 }, { x: 4393, x2: 5324, y: 4 }, { x: 5325, x2: 5925, y: 3 }, { x: 5926, x2: 6452, y: 2 }, { x: 6453, x2: 6798, y: 1 }, { x: 6799, x2: 7096, y: 0 },];
            categories = ['NSP16', 'NSP15', 'NSP14', 'NSP13', 'NSP12', 'NSP11', 'NSP10', 'NSP9', 'NSP8', 'NSP7', 'NSP6', 'NSP5', 'NSP4', 'NSP3', 'NSP2', 'NSP1'];
        } else if (domainNm == 'S') {
            data = [{ x: 1, x2: 1273, y: 9 },{ x: 14, x2: 685, y: 8 }, { x: 686, x2: 1273, y: 7 }, { x: 816, x2: 1273, y: 6 }, { x: 319, x2: 541, y: 5 }, { x: 437, x2: 508, y: 4 }, { x: 816, x2: 837, y: 3 }, { x: 835, x2: 855, y: 2 }, { x: 920, x2: 970, y: 1 }, { x: 1163, x2: 1202, y: 0 },];

            categories = ['Heptad repeat 2', 'Heptad repeat 1', 'Fusion peptide 2', 'Fusion peptide 1', 'RBM', 'RBD', 'S2\'', 'S2', 'S1', 'S'];
        } else if (domainNm == 'N') {
            data = [{ x: 1, x2: 419, y: 2 }, { x: 1, x2: 97, y: 1 }, { x: 1, x2: 73, y: 0 },];

            categories = ['ORF9c', 'ORF9b', 'N'];
        }

        Highcharts.chart(prdctnObj.targetId, {
            chart: {
                type: 'xrange'
            },
            title: {
                text: ''
            },
            credits: {
                enabled: false
            },
            accessibility: {
                point: {
                    descriptionFormatter: function (point) {
                        var ix = point.index + 1, category = point.yCategory, from = point.x, to = point.x2;
                        return ix + '. ' + category + ', ' + from +
                            ' to ' + to + '.';
                    }
                }
            },
            xAxis: {
                type: 'string'
            },
            yAxis: {
                title: {
                    text: ''
                },
                categories: categories,
                reversed: false
            },
            series: [{
                name: 'domain',
                // pointPadding: 0,
                // groupPadding: 0,
                borderColor: 'gray',
                pointWidth: 20,
                data: data,
                dataLabels: {
                    enabled: false
                },
                events: {
                    click: function (e) {
                        prdctnObj.callbak(e.point.yCategory);
                    }
                }
            }]
        });
    }

    /**
     * pae 배열 데이터를 이용해 heatmap 차트를 그린다.
     * @param {*} arrPaeData pae 배열 데이터
     */
    drawPaeHeatMap(arrPaeData) {
        this.paeChart = Highcharts.chart(this.targetId, {
            chart: {
                type: 'heatmap',
                events: {
                    click: e =>  {
                        if (this.isEvent) this.icn3dObj.icn3d.loadScriptCls.loadScript(this.makeIcn3dCmd('select', this.paeChart.hoverPoint.x, this.paeChart.hoverPoint.y));
                    }
                }
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'Predicted Aligned Error'
            },

            boost: {
                useGPUTranslations: true
            },

            xAxis: {
                type: 'string',
                min: 0,
                max: arrPaeData[0].length,
                title: {
                    text: 'Aligned residue'
                },
                labels: {
                    align: 'left',
                    x: 5,
                    y: 14,
                    format: '{value}',
                },
                showLastLabel: false,
                tickLength: 1,
            },

            yAxis: {
                categories: this.arrAllMutVirusSeq,
                title: {
                    text: 'Aligned residue'
                },
                labels: {
                    format: '{value}'
                },
                minPadding: 0,
                maxPadding: 0,
                startOnTick: false,
                endOnTick: false,

                tickWidth: 1,
                min: 0,
                max: arrPaeData[1].length,
                reversed: false,
            },

            colorAxis: {
                minColor: '#00441B',
                maxColor: '#FCFFFA',
                startOnTick: false,
                endOnTick: false,
                max: 31.75,     //max값 추가
                labels: {
                    format: '{value}'
                },
            },

            series: [{
                boostThreshold: 100,

                //borderWidth: 1,
                //nullColor: '#EFEFEF',
                data: arrPaeData,
                allowPointSelect: true,
                tooltip: {
                    headerFormat: 'PAE<br/>',
                    pointFormat: '{point.x} {point.y}: <b>{point.value}</b>'
                },
                turboThreshold: Number.MAX_VALUE //#3404, remove after 4.0.5 release
            }],
        });
    }

    /**
     * pae 차트에서 사용할 out virus seq를 전처리 한다.
     * @param {*} resultForm 결과화면 form 객체
     */
    initVirusSeq(resultForm) {
        this.seq1 = $(resultForm).find('input[name=output_virus_seq_1]').val();
        this.seq2 = $(resultForm).find('input[name=output_virus_seq_2]').val();
        this.seq3 = $(resultForm).find('input[name=output_virus_seq_3]').val();
        this.seq4 = $(resultForm).find('input[name=output_virus_seq_4]').val();
        this.seq5 = $(resultForm).find('input[name=output_virus_seq_5]').val();
        this.seq6 = $(resultForm).find('input[name=output_virus_seq_6]').val();
        this.seq7 = $(resultForm).find('input[name=output_virus_seq_7]').val();
        this.seq8 = $(resultForm).find('input[name=output_virus_seq_8]').val();
        
        if (this.seq1)
            for (let idx in this.seq1) { this.arrAllMutVirusSeq.push(this.seq1[idx] + (Number(idx) + 1)); this.arrAllMutVirusChain.push('A'); };
        if (this.seq2)
            for (let idx in this.seq2) { this.arrAllMutVirusSeq.push(this.seq2[idx] + (Number(idx) + 1)); this.arrAllMutVirusChain.push('B'); };
        if (this.seq3)
            for (let idx in this.seq3) { this.arrAllMutVirusSeq.push(this.seq3[idx] + (Number(idx) + 1)); this.arrAllMutVirusChain.push('C'); };
        if (this.seq4)
            for (let idx in this.seq4) { this.arrAllMutVirusSeq.push(this.seq4[idx] + (Number(idx) + 1)); this.arrAllMutVirusChain.push('D'); };
        if (this.seq5)
            for (let idx in this.seq5) { this.arrAllMutVirusSeq.push(this.seq5[idx] + (Number(idx) + 1)); this.arrAllMutVirusChain.push('E'); };
        if (this.seq6)
            for (let idx in this.seq6) { this.arrAllMutVirusSeq.push(this.seq6[idx] + (Number(idx) + 1)); this.arrAllMutVirusChain.push('F'); };
        if (this.seq7)
            for (let idx in this.seq7) { this.arrAllMutVirusSeq.push(this.seq7[idx] + (Number(idx) + 1)); this.arrAllMutVirusChain.push('G'); };
        if (this.seq8)
            for (let idx in this.seq8) { this.arrAllMutVirusSeq.push(this.seq8[idx] + (Number(idx) + 1)); this.arrAllMutVirusChain.push('H'); };

        //프로테인 구조를 확인 후 저장한다.
        if (`${this.seq2}${this.seq3}${this.seq4}${this.seq5}${this.seq6}${this.seq7}${this.seq8}` != '') this.proteinStruc = 'MT'
    }

    /**
     * pae 파일을 다운받아 차트를 그린다.
     * @param {*} paePath pae file path
     * @param {*} icn3dObj  icn3d object
     */
    async drawPae(paePath, icn3dObj, targetId, fileType) {
        this.icn3dObj = icn3dObj;
        this.targetId = targetId ? targetId : this.targetId
        async function getPaeData() {
            const response = await fetch(
                decodeURIComponent(`/filedownload?file_name=${paePath}&file_type=${fileType}`)
            );
            return response.json();
        }

        const data = await getPaeData();

        let arrPaeData = [];
        if (data != '') {
            for (var i = 0; i < data[0].predicted_aligned_error.length; i++) {
                for (var j = 0; j < data[0].predicted_aligned_error[i].length; j++) {
                    arrPaeData.push({
                        x: i,
                        y: j,
                        value: data[0].predicted_aligned_error[i][j]
                    });
                }
            }
        }

        this.drawPaeHeatMap(arrPaeData);

        return data;
    }

    /**
     * AIVE pae를 데이터로 차트를 크린다.
     * @param {string} paeData pae데이터
     * @param {object} icn3dObj  icn3d object
     */
     drawPaeLocal(paeData, icn3dObj, targetId) {
        this.icn3dObj = icn3dObj;
        this.targetId = targetId ? targetId : this.targetId
        
        let arrPaeData = [];
        if (paeData != '') {
            //pae 구조 체크 후 최신버전이 아니면 변환

            if (!paeData[0].predicted_aligned_error) paeData = this.transNewPaeFormatt(paeData[0]);

            for (var i = 0; i < paeData[0].predicted_aligned_error.length; i++) {
                for (var j = 0; j < paeData[0].predicted_aligned_error[i].length; j++) {
                    arrPaeData.push({
                        x: i,
                        y: j,
                        value: paeData[0].predicted_aligned_error[i][j]
                    });
                }
            }
        }

        this.drawPaeHeatMap(arrPaeData);
    }

    /**
     * 과거버전의  colab pae를 최신 버전의 pae 포맷으로 변경한다.
     * @param {json} arrPaeData
     */
    transNewPaeFormatt(oldPaeData){
        let newPaeData = {
            max_predicted_aligned_error: oldPaeData.max_predicted_aligned_error,
        }
        let arrPae = [];
        let arrPaeDis = [];
        let oldVal = '';

        oldPaeData.residue1.map((val,idx) => {
            if (oldVal != val){
                if (idx > 0) arrPae.push(arrPaeDis);
                oldVal = val;
                arrPaeDis = [];
                arrPaeDis.push(oldPaeData.distance[idx]);
            } else {
                arrPaeDis.push(oldPaeData.distance[idx]);
            }
        });

        arrPae.push(arrPaeDis);
        newPaeData['predicted_aligned_error'] = arrPae;

        return [newPaeData];
    }

    /**
     * plddt 배열값으로 line 차트를 그린다.
     * @param {*} arrPlddtData plddt 배열 데이터
     * @param {string} targetId plddt 차트를 그릴 targetId
     */
    drawPlddtLine(arrPlddtData, targetId) {
        this.targetId = targetId ? targetId : this.targetId
        const prdctnObj = this;

        Highcharts.chart(`${prdctnObj.targetId}Line`, {
            chart: {
                zoomType: 'x'
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'Predicted LDDT'
            },
            xAxis: {
                type: 'string',
                title: {
                    text: 'Residue'
                }
            },
            yAxis: {
                title: {
                    text: 'pLDDT'
                },
                max:100
            },
            legend: {
                enabled: false
            },

            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },

            series: [{
                type: 'area',
                name: 'pLDDT',
                data: arrPlddtData,
                events: {
                    click: e => {
                        if (this.isEvent) this.icn3dObj.icn3d.loadScriptCls.loadScript(this.makeIcn3dCmd('select', e.point.x));
                    }
                }
            }]
        });
    }

    /**
     * plddt 배열값으로 line 차트를 그린다.
     * @param {*} arrPlddtData plddt 배열 데이터
     * @param {*} arrPlddtCv2Data SARs-CoV-2 plddt 배열 데이터
     * @param {string} targetId plddt 차트를 그릴 targetId
     */
     drawPlddtCv2Line(arrPlddtData, arrPlddtCv2Data, icn3dObj, icn3dObjCv2, targetId) {
        this.targetId = targetId ? targetId : this.targetId
        const prdctnObj = this;
        
        Highcharts.chart(`${prdctnObj.targetId}Line`, {
            chart: {
                zoomType: 'x',
                type: 'area'
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'Predicted LDDT'
            },
            xAxis: {
                type: 'string',
                title: {
                    text: 'Residue'
                }
            },
            yAxis: {
                title: {
                    text: 'pLDDT'
                },
                max : 100
            },
            legend: {
                enabled: false
            },

            plotOptions: {
                area: {
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },

            legend: {
                layout: 'horizontal',
                align: 'center',
                verticalAlign: 'bottom'
            },

            series: [{
                name: 'Mutation',
                data: arrPlddtData,
                events: {
                    click: e => {
                        if (this.isEvent) icn3dObj.icn3d.loadScriptCls.loadScript(this.makeIcn3dCmd('select', e.point.x));
                    }
                }
            },
            {
                name: 'Wuhan-HU-1',
                data: arrPlddtCv2Data,
                events: {
                    click: e => {
                        if (this.isEvent) icn3dObjCv2.icn3d.loadScriptCls.loadScript(this.makeIcn3dCmd('select', e.point.x));
                    }
                }
            }]
        });
    }

    /**
     * plddt 배열값으로 line 차트를 그린다.
     * @param {*} arrPlddtData plddt 배열 데이터
     * @param {string} targetId plddt 차트를 그릴 targetId
     */
    drawPlddtBoxplot(arrPlddtData,  targetId) {
        this.targetId = targetId ? targetId : this.targetId
        const prdctnObj = this;
        let arrData = [];
        let arrBoxplot = [];
        [...arrPlddtData].forEach(data => arrData.push(data[1]));
        
        const cmmMath = new CommonMath(arrData);
        //q1, q3, iqr
        const q1 = cmmMath.q1(arrData);
        const q3 = cmmMath.q3(arrData);
        const iqr = q3 - q1;
        const maximun = q3 + 1.5*iqr;
        const minimun = q1 - 1.5*iqr
        //boxplot 데이터 생성
        arrBoxplot.push(minimun);      //minimum
        arrBoxplot.push(q1);    //q1
        arrBoxplot.push(cmmMath.median(arrData));   //q2, median
        arrBoxplot.push(q3);    //q3
        arrBoxplot.push(maximun);  //maximun
        
        //이상치 데이터 찾기
        let arrOutliers = [];
        arrData.forEach( data => {
            if (data > maximun || data < minimun) arrOutliers.push([0,data]);
        })
        

        Highcharts.chart(`${prdctnObj.targetId}Boxplot`, {
            chart: {
                type: 'boxplot'
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'pLDDT box-plot'
            },

            legend: {
                enabled: false
            },

            xAxis: {
                
            },

            yAxis: {
                title: {
                    text: 'pLDDT'
                },
            },

            series: [{
                name: 'Observations',
                data: [
                    arrBoxplot,
                ],
                tooltip: {
                    headerFormat: '<em>Experiment No {point.key}</em><br/>'
                }
            }, {
                name: 'Outliers',
                color: Highcharts.getOptions().colors[0],
                type: 'scatter',
                data: arrOutliers,
                marker: {
                    fillColor: 'white',
                    lineWidth: 1,
                    lineColor: Highcharts.getOptions().colors[0]
                },
                tooltip: {
                    pointFormat: 'Observation: {point.y}'
                }
            }]
        });
    }

    /**
     * plddt 배열값으로 line 차트를 그린다.
     * @param {*} arrPlddtData plddt 배열 데이터
     * @param {*} arrPlddtCv2Data SARs-CoV-2 plddt 배열 데이터
     * @param {string} targetId plddt 차트를 그릴 targetId
     */
     drawPlddtCv2Boxplot(arrPlddtData, arrPlddtCv2Data, targetId) {
        this.targetId = targetId ? targetId : this.targetId
        const prdctnObj = this;
        let arrData = [], arrDataCv2 = [];
        let arrBoxplot = [], arrBoxplotCv2 = [];
        [...arrPlddtData].forEach(data => arrData.push(data[1]));
        
        const cmmMath = new CommonMath(arrData);
        //q1, q3, iqr
        const q1 = cmmMath.q1(arrData);
        const q3 = cmmMath.q3(arrData);
        const iqr = q3 - q1;
        const maximun = q3 + 1.5*iqr;
        const minimun = q1 - 1.5*iqr
        //boxplot 데이터 생성
        arrBoxplot.push(minimun);      //minimum
        arrBoxplot.push(q1);    //q1
        arrBoxplot.push(cmmMath.median(arrData));   //q2, median
        arrBoxplot.push(q3);    //q3
        arrBoxplot.push(maximun);  //maximun

        
        [...arrPlddtCv2Data].forEach(data => arrDataCv2.push(data[1]));

        const cmmMathCv2 = new CommonMath(arrDataCv2);
        //q1, q3, iqr
        const q1Cv2 = cmmMathCv2.q1(arrDataCv2);
        const q3Cv2 = cmmMathCv2.q3(arrDataCv2);
        const iqrCv2 = q3Cv2 - q1Cv2;
        const maximunCv2 = q3Cv2 + 1.5*iqrCv2;
        const minimunCv2 = q1Cv2 - 1.5*iqrCv2
        //boxplot 데이터 생성
        arrBoxplotCv2.push(minimunCv2);      //minimum
        arrBoxplotCv2.push(q1Cv2);    //q1
        arrBoxplotCv2.push(cmmMathCv2.median(arrDataCv2));   //q2, median
        arrBoxplotCv2.push(q3Cv2);    //q3
        arrBoxplotCv2.push(maximunCv2);  //maximun
        
        //이상치 데이터 찾기
        let arrOutliers = [], arrOutliersCv2 = [];
        arrData.forEach( data => {
            if (data > maximun || data < minimun) arrOutliers.push([0,data]);
        })

        arrDataCv2.forEach( data => {
            if (data > maximunCv2 || data < minimunCv2) arrOutliersCv2.push([1,data]);
        })
        

        Highcharts.chart(`${prdctnObj.targetId}Boxplot1`, {
            chart: {
                type: 'boxplot'
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'box-plot'
            },

            legend: {
                enabled: false
            },

            xAxis: {
                categories : ['Mutation']
            },

            yAxis: {
                title: {
                    text: 'pLDDT'
                },
            },
            
            series: [
                {
                name: 'User type',
                color: Highcharts.getOptions().colors[0],
                data: [
                    arrBoxplot,
                ],
                tooltip: {
                    headerFormat: ''
                }
            },
            {
                name: 'Outliers',
                color: Highcharts.getOptions().colors[0],
                type: 'scatter',
                data: arrOutliers,
                marker: {
                    fillColor: 'white',
                    lineWidth: 1,
                    lineColor: Highcharts.getOptions().colors[0]
                },
                tooltip: {
                    pointFormat: 'Observation: {point.y}'
                }
            }]
        });

        Highcharts.chart(`${prdctnObj.targetId}Boxplot2`, {
            chart: {
                type: 'boxplot'
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'box-plot'
            },

            legend: {
                enabled: false
            },

            xAxis: {
                categories : ['Wuhan-HU-1']
            },

            yAxis: {
                title: {
                    text: 'pLDDT'
                },
            },
            
            series: [
                {
                name: 'User type',
                color: Highcharts.getOptions().colors[1],
                data: [arrBoxplotCv2],
                tooltip: {
                    headerFormat: ''
                }
            },
            {
                name: 'Outliers',
                color: Highcharts.getOptions().colors[1],
                type: 'scatter',
                data: arrOutliersCv2,
                marker: {
                    fillColor: 'white',
                    lineWidth: 1,
                    lineColor: Highcharts.getOptions().colors[0]
                },
                tooltip: {
                    pointFormat: 'Observation: {point.y}'
                }
            }]
        });
    }

    /**
     * plddt csv파일을 다운로드 하여 데이터 파싱 후 plddt line 및 boxplot 차트를 그린다.
     * @param {string} plddtPath plddt 경로
     * @param {object} icn3dObj icn3d 객체
     * @param {string} targetId 차트를 그릴 div id
     */
    async drawPlddt(plddtPath, icn3dObj, targetId, fileType) {
        this.icn3dObj = icn3dObj;
        this.targetId = targetId ? targetId : this.targetId
        
        async function getPlddtData() {
            const response = await fetch(
                decodeURIComponent(`/filedownload?file_name=${plddtPath}&file_type=${fileType}`)
            );
            return response.text();
        }

        const data = await getPlddtData();
        if (data != '') {
            let tmpCols, arrPlddtData = [];
            const tmpRows = data.split('\n');

            tmpRows.forEach((rows, idx) => {
                tmpCols = rows.split(',');
                if (idx > 0) {
                    tmpCols[0] = Number(tmpCols[0]);
                    tmpCols[1] = Number(tmpCols[1]);
                    arrPlddtData.push(tmpCols);
                }

            });

            this.drawPlddtLine(arrPlddtData);
            this.drawPlddtBoxplot(arrPlddtData);
            
            return data;
        } else {
            return '';
        }
    }

    /**
     * plddt csv파일을 다운로드 하여 데이터 파싱 후 plddt line 및 boxplot 차트를 그린다.
     * @param {string} plddtPath1 plddt 경로
     * @param {string} plddtPath1 plddt 경로
     * @param {object} icn3dObj icn3d 객체
     * * @param {object} icn3dObj SARs-CoV-2 icn3d 객체
     * @param {string} targetId 차트를 그릴 div id
     * @param {string} fileType1 plddt 경로
     * @param {string} fileType2 plddt 경로
     */
     async drawPlddtCv2(plddtPath1, plddtPath2, icn3dObj, icn3dObjCv2, targetId, fileType1, fileType2) {
        this.icn3dObj = icn3dObj;
        this.targetId = targetId ? targetId : this.targetId
        async function getPlddtData(plddtPath, fileType) {
            const response = await fetch(
                decodeURIComponent(`/filedownload?file_name=${plddtPath}&file_type=${fileType}`)
            );
            return response.text();
        }

        const data1 = await getPlddtData(plddtPath1, fileType1);
        const data2 = await getPlddtData(plddtPath2, fileType2);

        if (data1 != '' && data2 != '') {
            let tmpCols, arrPlddtData = [], arrPlddtCv2Data = [];
            const tmpRows1 = data1.split('\n');

            tmpRows1.forEach((rows, idx) => {
                tmpCols = rows.split(',');
                if (idx > 0) {
                    tmpCols[0] = Number(tmpCols[0]);
                    tmpCols[1] = Number(tmpCols[1]);
                    arrPlddtData.push(tmpCols);
                }

            });

            const tmpRows2 = data2.split('\n');

            tmpRows2.forEach((rows, idx) => {
                tmpCols = rows.split(',');
                if (idx > 0) {
                    tmpCols[0] = Number(tmpCols[0]);
                    tmpCols[1] = Number(tmpCols[1]);
                    arrPlddtCv2Data.push(tmpCols);
                }

            });

            this.drawPlddtCv2Line(arrPlddtData, arrPlddtCv2Data,icn3dObj, icn3dObjCv2);
            this.drawPlddtCv2Boxplot(arrPlddtData, arrPlddtCv2Data);
            
            return data1;
        } else {
            return '';
        }
    }

    /**
     * AIVE plddt 파일을 이용하여 차트를 그린다.
     * @param {string} plddtData plddt 데이터
     * @param {object} icn3dObj icn3d 객체
     * @param {string} targetId 차트를 그릴 div id
     */
    drawPlddtAiveLocal(plddtData, icn3dObj, targetId) {
        this.icn3dObj = icn3dObj;
        this.targetId = targetId ? targetId : this.targetId
        
        if (plddtData != '') {
            let tmpCols, arrPlddtData = [];
            const tmpRows = plddtData.split('\n');

            tmpRows.forEach((rows, idx) => {
                tmpCols = rows.split(',');
                if (idx > 0) {
                    tmpCols[0] = Number(tmpCols[0]);
                    tmpCols[1] = Number(tmpCols[1]);
                    arrPlddtData.push(tmpCols);
                }

            });

            this.drawPlddtLine(arrPlddtData);
            this.drawPlddtBoxplot(arrPlddtData);
        } else {
            console.log('No Data');
        }
    }

    /**
     * colab pdb 파일에서 plddt 파일을 이용하여 차트를 그린다.
     * @param {string} pdb pdb 파일
     * @param {object} icn3dObj icn3d 객체
     * @param {string} targetId 차트를 그릴 div id
     */
     drawPlddtColabLocal(pdb, icn3dObj, targetId) {
        this.icn3dObj = icn3dObj;
        this.targetId = targetId ? targetId : this.targetId;
        //pdb파일을 plddt array로 파싱한다.

        const tmpPdb = pdb.split('\n');

        let arrPlddtData = [];
        let plddtNo = 0;
        let oldNo = '';
        tmpPdb.map(pdbLine => {
            let aaNo = pdbLine.slice(22,26).trim();
            let plddtVal = pdbLine.slice(61,66).trim();

            if (oldNo != aaNo){
                oldNo = aaNo;
                if (plddtVal) arrPlddtData.push([plddtNo++, Number(plddtVal)])
            }
        });

        this.drawPlddtLine(arrPlddtData);
        this.drawPlddtBoxplot(arrPlddtData);
    }

    drawBaeApess(apess, targetId){
        this.targetId = targetId ? targetId : this.targetId;
        Highcharts.chart(this.targetId, {
            title: {
                text: 'PPX4, PPX5, BLCR, CPES, APESS'
            },
            credits: {
                enabled: false
            },
            yAxis: {
                title: {
                    text: 'Values'
                }
            },
            xAxis: {
                type: 'string'
            },
        
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
        
            plotOptions: {
                series: {
                    label: {
                        connectorAllowed: false
                    },
                    pointStart: 0
                }
            },
        
            series: [{
                name: 'PPX4',
                data: apess.ppx4
            }, {
                name: 'PPX5',
                data: apess.ppx5
            }, {
                name: 'BLCR',
                data: apess.blcr
            }, {
                name: 'CPES',
                data: apess.cpes
            }, {
                name: 'APESS',
                data: apess.apess
            }],
        
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        
        });
    }

    //20230221 Reference bpes mr chart를 보여준다
    drawReferenceBpesMr(apess, targetId){
        this.targetId = targetId ? targetId : this.targetId;

        Highcharts.chart(this.targetId, {
            chart: {
                zoomType: 'xy'
            },
            credits: {
                enabled: false
            },
            title: {
                text: '',
                align: 'center'
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                type: 'string'
            },
            yAxis: [{ // Primary yAxis
                
                title: {
                    text: 'mr',
                    style: {
                        color: '#FF007F'
                    }
                },
                labels: {
                    format: '{value}',
                    style: {
                        color: '#FF007F'
                    }
                },
                opposite: true
                
            }, { // Secondary yAxis
                title: {
                    text: 'bpes',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    format: '{value}',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                }
                
            }],
            
            tooltip: {
                shared: true
            },
            legend: {
                align: 'center',
                verticalAlign: 'top',
                y : 0,
                floating: true,
                backgroundColor:
                    Highcharts.defaultOptions.legend.backgroundColor || // theme
                    'rgba(255,255,255,0.25)'
            },
            series: [{
                name: 'bpes',
                type: 'column',
                yAxis: 1,
                data: apess.bpes_input
                
            }, {
                name: 'mr',
                type: '',
                color: '#FF007F',
                data: apess.mr_input
            }]
        });

    }

    //20230221 Mutation bpes mr chart를 보여준다
    drawMutationBpesMr(apess, targetId){
        this.targetId = targetId ? targetId : this.targetId;

        Highcharts.chart(this.targetId, {
            chart: {
                zoomType: 'xy'
            },
            credits: {
                enabled: false
            },
            title: {
                text: '',
                align: 'center'
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                type: 'string'
            },
            yAxis: [{ // Primary yAxis
                
                title: {
                    text: 'mr',
                    style: {
                        color: '#FF007F'
                    }
                },
                labels: {
                    format: '{value}',
                    style: {
                        color: '#FF007F'
                    }
                },
                opposite: true
                
            }, { // Secondary yAxis
                title: {
                    text: 'bpes',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    format: '{value}',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                }
                
            }],
            tooltip: {
                shared: true
            },
            legend: {
                align: 'left',
                x: 80,
                verticalAlign: 'top',
                y: 20,
                floating: true,
                backgroundColor:
                    Highcharts.defaultOptions.legend.backgroundColor || // theme
                    'rgba(255,255,255,0.25)'
            },
            series: [{
                name: 'bpes Mutation',
                type: 'column',
                yAxis: 1,
                data: apess.bpes_output
                
            }, {
                name: 'mr Mutation',
                type: '',
                color: '#FF007F',
                data: apess.mr_output
            }]
        });

    }
    //drawPsScps 20230221 수정
    /*drawPsScps(apess, targetId){
        this.targetId = targetId ? targetId : this.targetId;
        Highcharts.chart(this.targetId, {
            title: {
                text: ''
            },
        
            yAxis: {
                title: {
                    enabled: false
                },
                labels: {
                    formatter: function () {
                        let tmpTxt = '';
                        if (this.value == 0) tmpTxt = 'W/O'
                        else if (this.value == 1) tmpTxt = 'W'
                        return tmpTxt;
                    }
                }
            },

            xAxis: {
                type: 'string'
            },
        
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
        
            plotOptions: {
                series: {
                    marker: {
                        enabled: false,
                        symbol: 'circle',
                        radius: 2
                    },
                    labels:{
                        enalbed: false
                    }
                }
            },
            
            series: [ {
                label: false,
                type: 'area',
                step: 'left',
                color: '#CAE1BB',
                name: 'PS',
                data: apess.ps,
            },
            {
                label: false,
                type: 'area',
                step: 'left',
                color: '#F7C5BE',
                name: 'SCPS',
                data: apess.scps,
            }],
        
        });
    }*/
    //20230221 기존 drawPsScps 수정
    drawPsScps(apess, targetId){
        this.targetId = targetId ? targetId : this.targetId;
        Highcharts.chart(this.targetId, {
            chart: {
                type: 'column'
            },
            credits: {
                enabled: false
            },
            title: {
                text: ''
            },
            yAxis: [{
                min: 0,
                title: {
                    text: 'ps'
                },
                reversed: true
            }, {
                title: {
                    text: 'scps',
                },
                opposite: true,
                reversed: true
            }],
            legend: {
                shadow: false
            },
            tooltip: {
                shared: true
            },
            plotOptions: {
                column: {
                    grouping: false,
                    shadow: false,
                    borderWidth: 0
                }
            },
            series: [{
                name: 'ps',
                color: 'rgba(0, 234, 255, 0.75)',
                data: apess.ps,
            }, {
                name: 'scps',
                color: 'rgba(254, 154, 46, 0.75)',
                data: apess.scps,
                yAxis: 1
            },]
        });

    }

    drawBpes(apess, targetId){
        this.targetId = targetId ? targetId : this.targetId;
        Highcharts.chart(this.targetId, {
            chart: {
                type: 'area',
            },
            credits: {
                enabled: false
            },
            title: {
                text: ''
            },
        
            yAxis: {
                labels: {
                    format: '{value:.2f}'
                  },
                title: {
                    useHTML : true,
                    text: 'bpes (x10<sup>-6</sup>)'
                }
            },
            xAxis: {
                type: 'string'
            },
        
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
        
            plotOptions: {
                series: {
                    marker: {
                        enabled: false,
                        symbol: 'circle',
                        radius: 2
                    },
                }
            },
        
            series: [{
                label: false,
                name: 'Mutation',
                data: apess.bpes_output,
                color: '#C2BFFC',
                fillOpacity: 1.0
            }, {
                label: false,
                name: 'Reference',
                data: apess.bpes_input,
                color: '#D08EA4',
                fillOpacity: 0.3
            }],
        
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        
        });
    }

    drawMr(apess, targetId){
        this.targetId = targetId ? targetId : this.targetId;
        Highcharts.chart(this.targetId, {
            title: {
                text: ''
            },
            credits: {
                enabled: false
            },
            yAxis: {
                labels: {
                    format: '{value:.2f}'
                  },
                title: {
                    useHTML : true,
                    text: 'mr (x10<sup>-8</sup>)'

                }
            },
            xAxis: {
                type: 'string'
            },
        
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
        
            plotOptions: {
                series: {
                    marker: {
                        enabled: false,
                        symbol: 'circle',
                        radius: 2
                    },
                }
            },
        
            series: [{
                label: false,
                type : 'area',
                name: 'Mutation',
                data: apess.mr_output,
                color: '#704876',
                fillOpacity: 0.9
            }, {
                label: false,
                type : 'area',
                name: 'Reference',
                data: apess.mr_input,
                color: '#EE9CD9',
                fillOpacity: 0.3
            }],
        
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        
        });
    }

    drawBlcrCpes(apess, targetId){
        this.targetId = targetId ? targetId : this.targetId;
        Highcharts.chart(this.targetId, {
            title: {
                text: ''
            },
            credits: {
                enabled: false
            },
            yAxis: {
                title: {
                    text: 'Values'
                }
            },
            xAxis: {
                type: 'string'
            },
        
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
        
            plotOptions: {
                series: {
                    label: {
                        connectorAllowed: false
                    },
                    pointStart: 0
                }
            },
        
            series: [{
                name: 'BLCR',
                data: apess.blcr
            }, {
                name: 'CPES',
                data: apess.cpes
            }],
        
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        
        });
    }

    //APESS 그래프 기존그래프에서 변경 변경된 위치 숫자랑 타겟 이름 명시
    drawApess(apess, targetId){
        this.targetId = targetId ? targetId : this.targetId;
        
        let input_virus_seq_1 = $('#input_virus_seq_1').val();
        let output_virus_seq_1 = $('#output_virus_seq_1').val();
        let trget_seq_rgin_st_lc = $('#trget_seq_rgin_st_lc').val();

        Highcharts.chart(this.targetId, {
            chart: {
                zoomType: 'xy'
            },
            credits: {
                enabled: false
            },
            title: {
                text: '',
                align: 'center'
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                type: 'string'
            },
            yAxis: [{ 
                title: {
                    text: '' ,
                },
                labels: {
                    format: '{value}'
                }
                
            }],
            plotOptions: {
                series: {
                    borderWidth: 0,
                    dataLabels: {
                        enabled: true,
                        //format: '{point.y:.3f}'
                        formatter: function (){
                            if(this.y != 0){
                                return input_virus_seq_1.substring(this.x,this.x+1)+(Number(this.x)+Number(trget_seq_rgin_st_lc))+output_virus_seq_1.substring(this.x,this.x+1)+"</br>"+this.y.toFixed(3);
                            }
                        }
                    }
                }
            },
            tooltip: {
                shared: true
            },
            
            series: [{
                label: false,
                color:'#FF0000',
                type: 'column',
                name: 'Mutation',
                data: apess.apess  
            }]
            
        });

        /*this.targetId = targetId ? targetId : this.targetId;
        Highcharts.chart(this.targetId, {
            title: {
                text: ''
            },
        
            yAxis: {
                labels: {
                    format: '{value:.2f}'
                  },
                title: {
                    useHTML : true,
                    text: 'APESS (x10<sup>-4</sup>)'
                }
            },
            xAxis: {
                type: 'string'
            },
        
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
        
            plotOptions: {
                series: {
                    marker: {
                        enabled: false,
                        symbol: 'circle',
                        radius: 2
                    },
                    label: {
                        connectorAllowed: false
                    },
                    pointStart: 0
                }
            },
        
            series: [{
                label: false,
                color:'#FF0000',
                type: 'area',
                name: 'Mutation',
                data: apess.apess
            },{
                lineWidth: 10,
                opacity: 0.5,
                type: 'area',
                name: 'Reference',
                data: apess.apess_wild
            }],
        
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        
        });*/
    }
    
    drawApessDist(apess, targetId){
        
        this.targetId = targetId ? targetId : this.targetId;

        let apess_sum = apess.apess.reduce((sum, currVal) => {
            return sum + currVal;
        });

        apess_sum = apess_sum/10;

        Highcharts.chart(this.targetId, {
            chart: {
                type:'spline'
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'Amino acid Property Eigen Selection Score'
            },
        
            yAxis: {
                title: {
                    text: 'Values'
                }
            },
            xAxis: {
                type: 'string',

                //plotLines: [{
                    //color: '#FF0000', // Red
                    //width: 2,
                    //value: apess_sum // Position, you'll have to translate this to the values on your x axis
                //}],

                plotBands: [{
                    from: 1.5,
                    to: 8,
                    color: '#FFEFFF',
                    label: {
                        text: 'Risk',
                        style: {
                            color: '#999999',
                            fontSize: '40pt'
                            
                        },
                        y: 180
                    }
                },
                {
                    from: -0.1,
                    to: -1.0,
                    color: '#EFFFFF',
                    label: {
                        text: '',
                        style: {
                            color: '#999999'
                        },
                        y: 180
                    }
                }], 
                
                reversed: false
            },
        
            plotOptions: {
                series: {
                    marker: {
                        enabled: false,
                        symbol: 'circle',
                        radius: 2
                    },
                    label: {
                        connectorAllowed: false
                    },
                    pointStart: 0
                }
            },
        
            series: [{
                label: false,
                name: 'APESS samples',
                data: apess.apess_dist
            },
            {
                type: 'flags',
                shape: 'flag',
                name: 'Highcharts',
                color: '#FF0000',
                fillColor: '#FF0000',
                width: 100,
                style: { // text style
                    color: 'white'
                },
                y:-200,
                data: [
                    { x: apess_sum, text: 'Mutation', title: 'Mutation'},
                ],
                showInLegend: false
            },
            {
                type: 'flags',
                name: 'Highcharts',
                color: '#333333',
                shape: 'circlepin',
                data: [
                    { x: -0.008, text: 'Alpha', title: 'Alpha' },
                    { x: 2.0, text: 'BA1', title: 'BA1' },
                    { x: 4.9, text: 'Delta', title: 'Delta' },
                    { x: 6.4, text: 'BA.5', title: 'BA.5' },
                    { x: 7.1, text: 'BA.4', title: 'BA.4' },
                ],
                showInLegend: false
            },
            {
                type: 'flags',
                name: 'Highcharts',
                color: '#333333',
                shape: 'circlepin',
                y:-100,
                data: [
                    { x: -0.068,  text: 'Beta', title: 'Beta' },
                    { x: 2.0, text: 'BA2', title: 'BA2' },
                ],
                showInLegend: false
            }
        ],
        
        });
    }
    //Polarity features 그래프 추가
    drawPolarityInfo(polarity, targetId){
        this.targetId = targetId ? targetId : this.targetId;

        var polarityTmpX = Object.keys(polarity.dicInputPolar);
        var inputPolarityTmpY = Object.values(polarity.dicInputPolar);
        var outputPolarityTmpY = Object.values(polarity.dicOutputPolar);

        polarityTmpX.pop();
        inputPolarityTmpY.pop();
        outputPolarityTmpY.pop();

        Highcharts.chart(this.targetId, {
            
            title: {
                text: '',
                align: 'center'
            },
            credits: {
                enabled: false
            },
            subtitle: {
                text: '',
                align: 'left'
            },

            yAxis: {
                title: {
                    text: ''
                }
            },

            xAxis: {
                categories: polarityTmpX
            },

            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },


            series: [{
                name: 'Mutation',
                data: inputPolarityTmpY  
            },{
                name: 'Reference',
                data: outputPolarityTmpY  
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        });
    }

}







