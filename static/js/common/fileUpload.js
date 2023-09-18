/**
 * m&h fileupload 
 *
 * Requirement : jquery-1.11.3.min.js
 */
class MnHFileUpload {
    constructor() {
        //파일 등록을 위한 기본 셋팅
        this.settings = {
            limitSize: 100,
            limitTotSize: 500,
            multiYn: false,
            fExt: ['pdb', 'PDB', 'csv', 'CSV', 'JSON', 'json','fasta'],
            uploadSrc: '/m/vcfProc/vcf/upload',
            uploadForm: '#mnhUploadForm',
            dragZoneObj: '.dragZone',
            fileListObj: '#tbodyFile' //파일 목록을 관리할 UL 객체
        };

        //등록한 파일배열
        this.uploadFileMap = {};
    }
    /**
     * 파일 드래그앤 드롭 초기화
     * @param options 파일 업로드에 사용할 셋팅
     * @returns
     */
    inti(options) {
        var mngFileUpload = this;

        //파일 등록을 위한 기본 셋팅
        this.settings = $.extend(this.settings, options);

        var fileDragZone = $(this.settings.dragZoneObj);
        //Drag기능 
        fileDragZone.on('dragenter', function (e) {
            e.stopPropagation();
            e.preventDefault();
            // 드롭다운 영역 css
            fileDragZone.css('background-color', '#E3F2FC');
        });
        fileDragZone.on('dragleave', function (e) {
            e.stopPropagation();
            e.preventDefault();
            // 드롭다운 영역 css
            fileDragZone.css('background-color', '#FFFFFF');
        });
        fileDragZone.on('dragover', function (e) {
            e.stopPropagation();
            e.preventDefault();
            // 드롭다운 영역 css
            fileDragZone.css('background-color', '#E3F2FC');
        });
        fileDragZone.on('drop', function (e) {
            e.preventDefault();

            //멀티 입력이 안될경우
            if (!mngFileUpload.settings.multiYn) {
                if ($(mngFileUpload.settings.fileListObj + '>li').length > 0) {
                    alert('파일은 하나만 등록할 수 있습니다.');
                    return;
                }
            }

            // 드롭다운 영역 css
            fileDragZone.css('background-color', '#FFFFFF');

            //드래그된 파일 처리
            var files = e.originalEvent.dataTransfer.files;
            if (files != null) {
                if (files.length < 1) {
                    alert('폴더는 업로드 할 수 없습니다.');
                    return;
                }

                if (!mngFileUpload.settings.multiYn) {
                    if (files.length > 1) {
                        alert('파일은 하나만 등록할 수 있습니다.');
                        return;
                    }
                }
                //선택된 파일 처리
                mngFileUpload.processFiles(files);
            } else {
                alert('파일 등록 중 오류가 발생하였습니다.');
            }
        });

        fileDragZone.on('click', function (e) {
            e.stopPropagation();
            e.preventDefault();

            $(mngFileUpload.settings.tmpFileObj).change(function (e) {
                mngFileUpload.processFiles($(this)[0].files);
            })
                .trigger("click");
        });
    }
    /**
     * 선택된 파일에 대한 처리
     * @param files 선택된 파일
     * @returns
     */
    processFiles(files) {
        // 다중파일 등록
        if (files != null) {
            var dupFileNm = '';

            //파일명 중복검사
            for (var i = 0; i < files.length; i++) {
                for (var key in this.uploadFileMap) {
                    if (this.uploadFileMap[key].name == files[i].name) {
                        dupFileNm += files[i].name + '\n';
                    }
                }
            }

            if (dupFileNm != '') {
                alert('파일명이 중복되어 첨부할 수 없습니다.\n' + dupFileNm);
                return;
            }

            for (var i = 0; i < files.length; i++) {
                // 파일 이름
                var fNm = files[i].name;

                //확장자 확인을 위한 파일 split
                var fNmSplit = fNm.split('\.');
                // 확장자
                var fExt = fNmSplit[fNmSplit.length - 1];
                // 파일 사이즈(단위 :MB)
                var fSize = files[i].size / 1024 / 1024;
                
                if ($.inArray(fExt, this.settings.fExt) < 0) {
                    alert('등록할 수 없는 파일입니다.');
                    break;
                } else if (fSize > this.settings.limitSize) {
                    alert('파일 등록 가능 용량을 초과하였습니다.\n현재 파일 용량 : ' + fSize + 'MB 허용 용량 : ' + this.settings.limitSize + ' MB 입니다.');
                    break;
                } else {
                    //파일 목록 생성
                    this.addfLst(fNm, fSize, files[i]);
                }
            }
        } else {
            alert('파일등록 중 오류가 발생하였습니다.');
        }
    }

    /**
     * 파일 목록 생성
     * @param fNm 파일명
     * @param fSize 파일크기
     * @param file 파일객체
     * @returns
     */
    addfLst(fNm, fSize, file) {
        var fKey = this.geneFileKey();
        var mngFileUpload = this;
        $(this.settings.fileListObj)
            .append(
                $('<li id="' + fKey + '">')
                    .append($('<span>')
                        .html('<i class="fa fa-file text-info" aria-hidden="true"></i> ' + fNm)
                        .append($('<strong>').text('(' + fSize.toFixed(2) + 'MB)'))
                        .append($('<button><i class="fa fa-times-circle text-danger" aria-hidden="true"><em class="sr-only">삭제</em></i></button>')
                            .on('click', function () {
                                mngFileUpload.deleteFile($(this).parent().parent());
                                return false;
                            })
                        )
                        .append(
                            $('<input type="hidden">').val(fSize.toFixed(2))
                        )
                    )
            );

        //파일객체 저장
        this.uploadFileMap[fKey] = file;

        //callback 함수가 있을때 실행한다.
        if (typeof (this.settings.addFileCallback) == 'function') {
            this.settings.addFileCallback();
        }

    }
    /**
     * 업로드할 파일을 파일 목록에서 삭제한다.
     * @param liObj 파일 list 객체
     * @returns
     */
    deleteFile(listObj) {
        //파일정보 삭제
        delete this.uploadFileMap[$(listObj).attr('id')];

        // 업로드 파일 테이블 목록에서 삭제
        $(listObj).remove();

        //callback 함수가 있을때 실행한다.
        if (typeof (this.settings.deleteFileCallback) == 'function') {
            this.settings.deleteFileCallback($(this.settings.fileListObj + '>tr').size());
        }
    }
    /**
     * 첨부파일 등록
     */
    uploadFile() {
        var uploadDf = $.Deferred();

        var totFSize = 0;

        //파일 체크
        if ($(this.settings.fileListObj + '>li').size() < 1) {
            uploadDf.reject('Please select a file.');

            return uploadDf;
        }

        $(this.settings.fileListObj).find('input').each(function (idx) {
            totFSize += $(this).val();
        });

        // 용량을 500MB를 넘을 경우 업로드 불가
        if (totFSize > this.settings.limitTotSize) {
            // 파일 사이즈 초과 경고창
            uploadDf.reject('The file capacity has been exceeded.\n	Current Upload Capacity : ' + totFSize + 'MB Total uploadable capacity : ' + settings.limitTotSize + ' MB');
            return uploadDf;
        }

        if (confirm("Would you like to register?")) {
            // 등록할 파일 리스트를 formData로 데이터 입력
            var form = $(this.settings.uploadForm);

            var formData = new FormData(form.get(0));

            for (var fKey in this.uploadFileMap) {
                formData.append('files', this.uploadFileMap[fKey]);
            }

            $.ajax({
                url: this.settings.uploadSrc,
                data: formData,
                type: 'POST',
                enctype: 'multipart/form-data',
                processData: false,
                contentType: false,
                dataType: 'json',
                cache: false,
            })
                .done(function (result) {
                    console.log(JSON.stringify(result));
                    uploadDf.resolve(result);
                })
                .fail(function (xhr, status, errorThrown) {
                    uploadDf.reject(errorThrown);
                })
                .always(function () {
                });
            ;
        } else {
            uploadDf.reject();
        }

        return uploadDf;
    }
    
    /**
     * 파일 정보 관리를 위한 Key 생성
     * @returns 파일정보Key
     */
    geneFileKey() {
        var resultKey = Math.floor((Math.random() * 10000) + 1);

        if ($(this.settings.fileListObj + '>li').length > 0) {
            //중복된 Key라면 중복되지 않도록 계속 생성
            var dupKey = true;
            while (dupKey) {
                $(this.settings.fileListObj + '>li').each(function (idx) {
                    if (resultKey == $(this).attr('id'))
                        resultKey = Math.floor((Math.random() * 10000) + 1);
                    else
                        dupKey = false;
                });
            }
        }

        return resultKey;
    }

    /**
     * 현재 업로드 대상 파일을 읽어 원하는 결과로 리턴한다.
     */
    async readUploadFileContent() {
        const promises = [];

        for (let key in this.uploadFileMap){
            let file = this.uploadFileMap[key];
            //pdb, pae json, plddt csv, fasta 파일별 시각화를 한다.
            //if (file.name.split('.')[1] == 'pdb') promises.push(this.fileReadAsDataUrl(file))
            //else promises.push(this.fileReadAsText(file));

            promises.push(this.fileReadAsText(file));
        }

        const result = await Promise.all(promises);
        return result;
    }

    /**
     * 파일을 읽어 원하는 결과로 리턴한다.
     * @param {*} fileObjs 파일 객체
     */
    async readFileElement(...fileElems) {
        const promises = [];

        for (let fileObj of fileElems){
            let file = fileObj.files[0];

            promises.push(this.fileReadAsText(file));
        }

        const result = await Promise.all(promises);
        return result;
    }

    fileReadAsText(file){
        const ext = file.name.split('.')[1];
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve({type: ext, content: reader.result});
            reader.readAsText(file);
        });
    }

    fileReadAsDataUrl(file){
        const ext = file.name.split('.')[1];
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve({type: ext, content: reader.result});
            reader.readAsDataURL(file);
        });
    }
}
 
 
 
 
 


