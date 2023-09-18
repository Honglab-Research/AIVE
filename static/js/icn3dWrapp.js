const setupViewer = function(idName, idValue, divid, command, alignPdb, searchPdb, width) {
    let options = {};

    // --Modify iCn3D --: add commands, e.g., 'color spectrum'
    command = (command) ? command : '';
    width = (width) ? width : (1160*0.6);

    let resdef = (alignPdb) ? alignPdb.resdef : ((searchPdb) ? searchPdb.resdef : undefined);
    let pdbstr = (alignPdb) ? alignPdb.pdbstr : ((searchPdb) ? searchPdb.pdbstr : undefined);

    let cfg = {
        divid: divid,
        width: width,
        height: 400,
        resize: false,
        notebook: true,
        mobilemenu: true,
        showcommand: false,
        showtitle: false,
        command: command,
        options: options,
        chains: (alignPdb) ? alignPdb.chains : undefined,
        resdef: resdef,
        masterchain: (searchPdb) ? searchPdb.masterchain : undefined,
        matchedchains: (searchPdb) ? searchPdb.matchedchains : undefined
    };
    if(idName !== '') cfg[idName] = idValue;

    // When pass from VAST neighbor page, use NCBI residue number and use asymmetric units to get all chains
    if(searchPdb) {
        cfg.usepdbnum = 0;
        cfg.bu = 0;
    }

    //let icn3dui = new icn3d.iCn3DUI(cfg);
    _icn3dui = new icn3d.iCn3DUI(cfg);
    
    //icn3dui.show3DStructure();

    //communicate with the 3D viewer with chained functions
    
    $.when(_icn3dui.show3DStructure(pdbstr)).then(function() {
        // add functions here
        //icn3dui.updateHlAll();
    });

    //icn3d 객체 저장
    console.log(divid);
    _arrIcn3d[divid] = _icn3dui;
}

const setupViewerLocal = function(targetId, command, pdbData, width) {
    let cfg = getConfig();
    cfg.version = 3;
    // --Modify iCn3D --: add commands, e.g., 'color spectrum'
    command = (command) ? command : '';
    cfg.command = command;
    cfg.resize = false;

    cfg.width = (1160*0.6);
    cfg.height = 400;
    

    cfg.mobilemenu = true;
    cfg.showcommand = false;
    cfg.showtitle = false;
    
    
    cfg.chains = undefined;
    cfg.resdef = undefined;
    cfg.masterchain = undefined;
    cfg.matchedchains = undefined;

    cfg.divid = targetId;

    _icn3dui = new icn3d.iCn3DUI(cfg);

    $.when(_icn3dui.show3DStructure()).then(function() {
        //icn3dui.setOption('color', 'spectrum');
    });

    //icn3d 객체 저장
    _arrIcn3d[targetId] = _icn3dui;

    //로컬 pdb 파일 표시하기
    _arrIcn3d['divPdbMUT1'].icn3d.pdbParserCls.loadPdbData(pdbData, undefined, undefined, false);
    //$(`#divPdbMUT1_accordion0`).hide();
    //$(`#divPdbMUT1_fullscreen`).hide();
}

//rank에 따른 결과 정보를 표시한다.
const showAf2 = (btnObj, ask, no, pdbNm, paeNm, pLddtNm, width) =>{
    $('.mlNum').removeClass('btn_rank_active');
    $(btnObj).addClass('btn_rank_active');

    $(`div[id^=div${ask}]`).hide();
    $(`div[id^=div${ask}${no}]`).show();

    let command = 'load url ' + decodeURIComponent(`/filedownload?file_name=${pdbNm}`) + ';';
    setupViewer(undefined, undefined, `divPdb${ask}${no}`, command, undefined, undefined, width);
    //메뉴 및 버튼을 숨긴다.
    //$(`#divPdb${ask}${no}_accordion0`).hide();
    $(`#divPdb${ask}${no}_fullscreen`).hide();

    //pae 정보 조회 후 heatmap 차트를 그린다.
    _paeChart.drawPae(paeNm, _arrIcn3d[`divPdb${ask}${no}`], `divPae${ask}${no}`);

    //plddt line차트를 그린다.
    _plddtChart.drawPlddt(pLddtNm, _arrIcn3d[`divPdb${ask}${no}`], `divPlddt${ask}${no}`);
}

//rank에 따른 결과 정보를 표시한다.
const showAf2Compare = (frontId, btnObj, ask, no, pdbNm, paeNm, pLddtNm, width) =>{
    $(btnObj).parent().find('button').removeClass('btn_rank_active');
    $(btnObj).addClass('btn_rank_active');

    
    
    $(`div[id^=${frontId}${ask}]`).hide();
    $(`div[id^=${frontId}${ask}${no}]`).show();
    
    let command = 'load url ' + decodeURIComponent(`/filedownload?file_name=${pdbNm}`) + ';';
    setupViewer(undefined, undefined, `${frontId}Pdb${ask}${no}`, command, undefined, undefined, width);
    //메뉴 및 버튼을 숨긴다.
    //$(`#divCPdb${ask}${no}_accordion0`).hide();
    $(`#divPdb${ask}${no}_fullscreen`).hide();
    $(`#divCPdb${ask}${no}_fullscreen`).hide();
    
    if (frontId == 'div') {
        _oriPLddtNm = pLddtNm
        //pae 정보 조회 후 heatmap 차트를 그린다.
        _paeChart.drawPae(paeNm, _arrIcn3d[`${frontId}Pdb${ask}${no}`], `${frontId}Pae${ask}${no}`);
    } else {
        _comparePLddtNm = pLddtNm
        //pae 정보 조회 후 heatmap 차트를 그린다.
        _paeChartC.drawPae(paeNm, _arrIcn3d[`${frontId}Pdb${ask}${no}`], `${frontId}Pae${ask}${no}`);
    }

    //plddt를 그린다.
    if (_comparePLddtNm != undefined)_plddtChart.drawPlddtCv2(_oriPLddtNm, _comparePLddtNm, _arrIcn3d[`divPdb${ask}${no}`], _arrIcn3d[`divCPdb${ask}${no}`],'divPlddt', 'user','user')
}

//sars-cov2결과의 rank에 따른 결과 정보를 표시한다.
const showAf2Cv2 = (btnObj, ask, no, pdbNm, paeNm, pLddtNm, width, pLddtNmCv2) =>{
    $('.mlNum').removeClass('btn_rank_active');
    $(btnObj).addClass('btn_rank_active');

    $(`div[id^=div${ask}]`).hide();
    $(`div[id^=div${ask}${no}]`).show();

    let command = 'load url ' + decodeURIComponent(`/filedownload?file_name=${pdbNm}`) + ';';
    setupViewer(undefined, undefined, `divPdb${ask}${no}`, command, undefined, undefined, width);
    //메뉴 및 버튼을 숨긴다.
    //$(`#divPdb${ask}${no}_accordion0`).hide();
    $(`#divPdb${ask}${no}_fullscreen`).hide();

    //pae 정보 조회 후 heatmap 차트를 그린다.
    _paeChart.drawPae(paeNm, _arrIcn3d[`divPdb${ask}${no}`], `divPae${ask}${no}`);
    
    //plddt를 그린다.
    _plddtChart.drawPlddtCv2(pLddtNm, pLddtNmCv2,_arrIcn3d[`divPdb${ask}${no}`], _arrIcn3d['divPdbCv2'],'divPlddtCv2', 'user','cv2')
}

//sars-cov2파이러스를 그린다.
const showCv2= (pdbNm, paeNm, pLddtNm, width) =>{
    let command = 'load url ' + decodeURIComponent(`/filedownload?file_name=${pdbNm}&file_type=cv2`) + ';';
    setupViewer(undefined, undefined, 'divPdbCv2', command, undefined, undefined, width);
    //메뉴 및 버튼을 숨긴다.
    //$(`#divPdb${ask}${no}_accordion0`).hide();
    $(`#divPdbCv2_fullscreen`).hide();

    //pae 정보 조회 후 heatmap 차트를 그린다.
    cv2PaeChart = new PrdctnChart('divPaeCv2', true);
    cv2PaeChart.initVirusSeq(document.forms.prdctnForm);
    cv2PaeChart.drawPae(paeNm, _arrIcn3d['divPdbCv2'], 'divPaeCv2','cv2');
}

const getConfig = function() {
    // separating the GET parameters from the current URL
    // repalce "color #" with "color " in the url
    var url = document.URL.replace(/\#/g, '');

    var bNopara = false;
    var ampPos = url.indexOf("?");
    if(ampPos === -1) {
    //  alert("Please include '?pdbid=1GPK,2POR,...' in your url");
        bNopara = true;
    }

    var params = url.split("?");
    // transforming the GET parameters into a dictionnary
    var search = params[params.length - 1];

    var cfg = {};

    if(!bNopara) {
        var decodeSearch = decodeURIComponent(search).replace(/\+/g, ' ');

        // command could contains '&', for example when loading statefile 'load mmdb 1kq2 | parameters &atype=1'
        var commandPos = decodeSearch.indexOf('&command=');
        if(commandPos != -1) {
            cfg.command = decodeSearch.substr(commandPos + 9); // ";" separated commands
            decodeSearch = decodeSearch.substr(0, commandPos);

            var paraPos = decodeSearch.indexOf(' | parameters ');

            if(paraPos != -1) { //When loading statefile (e.g., 'load mmdb 1kq2 | parameters &atype=1'), the commands ends with '}}'.
                var tmpPos = cfg.command.indexOf('}}&');
                if(tmpPos != -1) { // more parameters after the command
                  decodeSearch += cfg.command.substr(tmpPos + 2);
                  cfg.command = cfg.command.substr(0, tmpPos + 2);
                }
            }
            else {
                var paraPos = cfg.command.indexOf(' | parameters ');

                if(paraPos != -1) { //"&command=load mmdb 7DDD | parameters &mmdbid=7DDD; select..." the commands ends with '}}'.
                    var tmpPos = cfg.command.indexOf('}}&');
                    if(tmpPos != -1) { // more parameters after the command
                      decodeSearch += cfg.command.substr(tmpPos + 2);
                      cfg.command = cfg.command.substr(0, tmpPos + 2);
                    }
                }
                else {
                    var tmpPos = cfg.command.indexOf('&');
                    if(tmpPos != -1) {
                      decodeSearch += cfg.command.substr(tmpPos);
                      cfg.command = cfg.command.substr(0, tmpPos);
                    }
                }
            }
        }
        else {
            cfg.command = '';
        }

        var hashes = decodeSearch.split('&');
        for (var i = 0; i < hashes.length; i++) {
            var hash = hashes[i].split('=');
            cfg[hash[0].trim()] = (hash[1] !== undefined) ? hash[1].trim() : undefined;
        }

        // for mmdb structures, pass the parameters after the first "&" sign
        cfg.inpara = "&" + url.substr(ampPos + 1);
    }

    // changed some parameter names
    cfg.rid = cfg.RID;

    cfg.urlname = cfg.url;
    if(cfg.urlname && cfg.urlname.indexOf('%3A%2F%2F') === -1) { // decoded URL
        // should encode it
        cfg.urlname = encodeURIComponent(cfg.urlname);
    }
    cfg.urltype = (cfg.type === undefined) ? 'pdb' : cfg.type;

    cfg.version = getValue(cfg.v);

    if(cfg.version !== undefined && window.localStorage && localStorage.getItem('fixedversion')) {
        var fixedUrl = url.replace('full.html', 'full_' + cfg.version + '.html');
        window.open(fixedUrl, '_self');

        localStorage.removeItem('fixedversion');
    }

    // standardize the input values
    for(var i in cfg) {
        if(i == 'bu') {
          cfg[i] = getInt(cfg[i]);
        }
        else {
           cfg[i] = getValue(cfg[i]);
        }
    }

    // backward compatible with showseq
    cfg.showanno = cfg.showanno || cfg.showseq;

    cfg.shownote = 1; //cfg.shownote;
    cfg.options = (cfg.options !== undefined) ? JSON.parse(cfg.options) : undefined;

    // default to show biological unit
    if(cfg.bu === undefined) cfg.bu = 1; //0;
    if(cfg.buidx !== undefined) cfg.bu = cfg.buidx;

    return cfg;
  }

  const getValue = function(input) {
    if(input == 'true' || input == '1') {
      input = true;
    }
    else if(input == 'false' || input == '0') {
      input = false;
    }

    return input;
  }

  const getInt = function(input) {
    if(input == 'true' || input == '1') {
      input = 1;
    }
    else if(input == 'false' || input == '0') {
      input = 0;
    }

    return input;
  }

const showAfLocal = (targetId, pdbData) =>{
    
    let command = 'append pdb file ranked_0.pdb';
    setupViewerLocal(targetId, command, pdbData);
    //메뉴 및 버튼을 숨긴다.
    $(`#${targetId}_accordion0`).hide();
    $(`#${targetId}_fullscreen`).hide();
}

//============ modify default functions =========
// e.g., add the b-factor information in the mouseover
icn3d.Picking.prototype.showPicking = function(atom, x, y) { 
    let ic = this.icn3d, me = ic.icn3dui;
    //me = ic.setIcn3dui(ic.id);
    if(me.cfg.cid !== undefined && ic.pk != 0) {
        ic.pk = 1; // atom
    }
    else {
        // do not change the picking option
    }
    ic.highlightlevel = ic.pk;
    this.showPickingBase(atom, x, y);

    if(ic.pk != 0) {
        if(x !== undefined && y !== undefined) { // mouse over
        if(me.cfg.showmenu != undefined && me.cfg.showmenu == true) {
            y += me.htmlCls.MENU_HEIGHT;
        }
        let text =(ic.pk == 1) ? atom.resn + atom.resi + '@' + atom.name : atom.resn + atom.resi;
        text += ', b: ' + atom.b;
        if(ic.structures !== undefined && Object.keys(ic.structures).length > 1) {
            text = atom.structure + '_' + atom.chain + ' ' + text;
            $("#" + ic.pre + "popup").css("width", "190px");
        }
        else {
            $("#" + ic.pre + "popup").css("width", "130px");
        }
        $("#" + ic.pre + "popup").html(text);
        $("#" + ic.pre + "popup").css("top", y).css("left", x+20).show();
        }
        else {
            // highlight the sequence background
            ic.hlUpdateCls.updateHlAll();
            let transformation = {}
            transformation.factor = ic._zoomFactor;
            transformation.mouseChange = ic.mouseChange;
            //transformation.quaternion = ic.quaternion;
            transformation.quaternion = {}
            transformation.quaternion._x = parseFloat(ic.quaternion._x).toPrecision(5);
            transformation.quaternion._y = parseFloat(ic.quaternion._y).toPrecision(5);
            transformation.quaternion._z = parseFloat(ic.quaternion._z).toPrecision(5);
            transformation.quaternion._w = parseFloat(ic.quaternion._w).toPrecision(5);
            if(ic.bAddCommands) {
                ic.commands.push('pickatom ' + atom.serial + '|||' + ic.transformCls.getTransformationStr(transformation));
                ic.optsHistory.push(me.hashUtilsCls.cloneHash(ic.opts));
                ic.optsHistory[ic.optsHistory.length - 1].hlatomcount = Object.keys(ic.hAtoms).length;
                if(me.utilsCls.isSessionStorageSupported()) ic.setStyleCls.saveCommandsToSession();
                ic.STATENUMBER = ic.commands.length;
            }
            ic.logs.push('pickatom ' + atom.serial + '(chain: ' + atom.structure + '_' + atom.chain + ', residue: ' + atom.resn + ', number: ' + atom.resi + ', atom: ' + atom.name + ')');
            if( $( "#" + ic.pre + "logtext" ).length )  {
            $("#" + ic.pre + "logtext").val("> " + ic.logs.join("\n> ") + "\n> ").scrollTop($("#" + ic.pre + "logtext")[0].scrollHeight);
            }
            // update the interaction flag
            ic.bSphereCalc = false;
            //me.htmlCls.clickMenuCls.setLogCmd('set calculate sphere false', true);
            ic.bHbondCalc = false;
            //me.htmlCls.clickMenuCls.setLogCmd('set calculate hbond false', true);
        }
    }
}
//============ End of: modify default functions =========