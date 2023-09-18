class PolarityUtils {
    constructor(targetId, inputVirusSeq, outputVirusSeq, callbak) {
        this.targetId = targetId;
        
        this.callbak = callbak;
        this.inputVirusSeq = inputVirusSeq;
        this.outputVirusSeq = outputVirusSeq;
        this.diffVirusSeq = '';
        this.inputPolarSeq = '';
        this.inputFiveSeq = '';
        this.outputPolarSeq = '';
        this.outputFiveSeq = '';
        //N-N-X, P-P-X외 추가
        this.dicInputPolar = {'N-N-X' : 0,'N-P-X' : 0,'N-A-X' : 0,'N-B-X' : 0,'P-N-X' : 0,'P-P-X' : 0,'P-A-X' : 0,'P-B-X' : 0,'A-N-X' : 0,'A-P-X' : 0,'A-A-X' : 0,'A-B-X' : 0,'B-N-X' : 0,'B-P-X' : 0,'B-B-X' : 0,'B-A-X' : 0,'ETC' : 0,};
        this.dicOutputPolar = {'N-N-X' : 0,'N-P-X' : 0,'N-A-X' : 0,'N-B-X' : 0,'P-N-X' : 0,'P-P-X' : 0,'P-A-X' : 0,'P-B-X' : 0,'A-N-X' : 0,'A-P-X' : 0,'A-A-X' : 0,'A-B-X' : 0,'B-N-X' : 0,'B-P-X' : 0,'B-B-X' : 0,'B-A-X' : 0,'ETC' : 0,};
        //Polarity feature	Polarity feature_S	Amino acid
        this.DIC_POLAR_FEATURE = {'A' : 'N','V' : 'N','L' : 'N','G' : 'N','I' : 'N','M' : 'N','W' : 'N','F' : 'N','P' : 'N','S' : 'P','C' : 'P','N' : 'P','Q' : 'P','T' : 'P','Y' : 'P','D' : 'A','E' : 'A','K' : 'B','R' : 'B','H' : 'B',};
        //Five amino acid properties 
        this.DIC_FIVE_AA = {'K' : 'E','R' : 'E','H' : 'E','D' : 'O','E' : 'O','S' : 'P','N' : 'P','Q' : 'P','T' : 'P','C' : 'S','G' : 'S','P' : 'S','A' : 'H','V' : 'H','L' : 'H','I' : 'H','M' : 'H','W' : 'H','F' : 'H', 'Y' : 'H',};
    }

    /**
     * polarity 를 계산한다.
     * @returns promise 결과
     */
    async drawVirusInfo(){
        const promises = [];

        promises.push(this.calcPolarFiveSeq());
        promises.push(this.calcPolarity());
        promises.push(this.calcDiffSeq());

        const result = await Promise.all(promises);
        return result;
    }

    /**
     * aa seq 정보를 그린다.
     * @param {string} targetId aa seq를 표시할 div id
     */
    makeVirusSeqInfo(){
        const arrSeq = Array.from(this.inputVirusSeq);
        arrSeq.forEach((seq, idx) => {
            $(`#${this.targetId}Input`)
            .append(
                $('<span class="row">')
                .append($('<span class="mut">').text(`${this.diffVirusSeq[idx] == '1' ? '↓': ''}`))
                .append($('<span class="txt color ">').html(seq == undefined ? '&nbsp;' : seq).addClass(`diffSeq${this.diffVirusSeq[idx]}`))
                .append($('<span class="txt color ">').html(this.inputPolarSeq[idx] == undefined ? '&nbsp;' : this.inputPolarSeq[idx]).addClass(`polar${this.inputPolarSeq[idx]}${this.diffVirusSeq[idx]}`))
                .append($('<span class="txt color ">').html(this.inputFiveSeq[idx] == undefined ? '&nbsp;' : this.inputFiveSeq[idx]).addClass(`five${this.inputFiveSeq[idx]}${this.diffVirusSeq[idx]}`))
            );

            $(`#${this.targetId}Output`)
            .append(
                $('<span class="row">')
                .append($('<span class="mut">').text(`${this.diffVirusSeq[idx] == '1' ? '↓': ''}`))
                .append($('<span class="txt color ">').html(this.outputVirusSeq[idx] == undefined ? '&nbsp;' : this.outputVirusSeq[idx]).addClass(`diffSeq${this.diffVirusSeq[idx]}`))
                .append($('<span class="txt color ">').html(this.outputPolarSeq[idx] == undefined ? '&nbsp;' : this.outputPolarSeq[idx]).addClass(`polar${this.outputPolarSeq[idx]}${this.diffVirusSeq[idx]}`))
                .append($('<span class="txt color ">').html(this.outputFiveSeq[idx] == undefined ? '&nbsp;' : this.outputFiveSeq[idx]).addClass(`five${this.outputFiveSeq[idx]}${this.diffVirusSeq[idx]}`))
            );
        })
    }

    /**
     * aa seq 정보를 그린다.
     * @param {string} targetId aa seq를 표시할 div id
     */
     makePolarityInfo(){
        for (let key in this.dicInputPolar){
            if(key == "P-P-X" || key == "N-N-X"  || key == "ETC" ){
            $(`#${this.targetId}Tbl > tbody`)
            .append(
                $('<tr>')
                .append($('<td>').text(key))
                .append($('<td>').text(this.dicInputPolar[key]))
                .append($('<td>').text(this.dicOutputPolar[key]))
                );
            }
        }
    }

    /**
     * input, output virus seq를 이용하여  polarity 및 five properties 정보를 만든다.
     */
    calcPolarFiveSeq(){
        return new Promise((resolve, reject) => {
            //input, output virus seq를 이용하여 polar, five seq를 만든다.
            const arrInputSeq = Array.from(this.inputVirusSeq);
            const arrOutputSeq = Array.from(this.outputVirusSeq);

            //input virus seq 변환
            arrInputSeq.map(seq => {
                //pola 기준으로 변환
                this.inputPolarSeq += this.DIC_POLAR_FEATURE[seq];
                //five 기준으로 변환
                this.inputFiveSeq += this.DIC_FIVE_AA[seq];
            });

            //ouput virus seq 변환
            arrOutputSeq.map(seq => {
                //pola 기준으로 변환
                this.outputPolarSeq += this.DIC_POLAR_FEATURE[seq];
                //five 기준으로 변환
                this.outputFiveSeq += this.DIC_FIVE_AA[seq];
            });

            resolve(true)
        });
    }

    /**
     * input, output virus에 대한 polaity를 계산한다.
     * @returns ploaity 계산 결과
     */
    calcPolarity(){
        return new Promise((resolve, reject) => {
            //input polar aa 건수 계산
            for (let i=0; i<this.inputPolarSeq.length -2; i++){
                //기존 3자리조건에서 2자리로 변경, NN,PP에서 추가 ETC는 는 표에 count하기 위해 추가
                if (this.inputPolarSeq.slice(i, i+2) == 'NN') this.dicInputPolar['N-N-X'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'NP') this.dicInputPolar['N-P-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'NA') this.dicInputPolar['N-A-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'NB') this.dicInputPolar['N-B-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'PN') this.dicInputPolar['P-N-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'PP') this.dicInputPolar['P-P-X'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'PA') this.dicInputPolar['P-A-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'PB') this.dicInputPolar['P-B-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'AA') this.dicInputPolar['A-A-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'AB') this.dicInputPolar['A-B-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'AN') this.dicInputPolar['A-N-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'AP') this.dicInputPolar['A-P-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'BN') this.dicInputPolar['B-N-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'BP') this.dicInputPolar['B-P-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'BA') this.dicInputPolar['B-A-X'] += 1, this.dicInputPolar['ETC'] += 1
                else if (this.inputPolarSeq.slice(i, i+2) == 'BB') this.dicInputPolar['B-B-X'] += 1, this.dicInputPolar['ETC'] += 1
                else this.dicInputPolar['ETC'] += 1
            }

            //output polar aa 건수 계산
            for (let i=0; i<this.outputPolarSeq.length -2; i++){
                if (this.outputPolarSeq.slice(i, i+2) == 'NN') this.dicOutputPolar['N-N-X'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'NP') this.dicOutputPolar['N-P-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'NA') this.dicOutputPolar['N-A-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'NB') this.dicOutputPolar['N-B-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'PN') this.dicOutputPolar['P-N-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'PP') this.dicOutputPolar['P-P-X'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'PA') this.dicOutputPolar['P-A-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'PB') this.dicOutputPolar['P-B-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'AA') this.dicOutputPolar['A-A-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'AB') this.dicOutputPolar['A-B-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'AN') this.dicOutputPolar['A-N-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'AP') this.dicOutputPolar['A-P-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'BN') this.dicOutputPolar['B-N-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'BP') this.dicOutputPolar['B-P-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'BA') this.dicOutputPolar['B-A-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else if (this.outputPolarSeq.slice(i, i+2) == 'BB') this.dicOutputPolar['B-B-X'] += 1, this.dicOutputPolar['ETC'] += 1
                else this.dicOutputPolar['ETC'] += 1
            }

            resolve(true)
        });

    }

    /**
     * input virus seq와 output virus seq가 서로 다른 위치를 체크한다.
     */
    calcDiffSeq(){
        return new Promise((resolve, reject) => {
            for (let i=0; i<this.inputVirusSeq.length; i++){
                if (this.inputVirusSeq[i] == this.outputVirusSeq[i]) this.diffVirusSeq +='0'
                else this.diffVirusSeq +='1'
            }
            resolve(true)
        });
    }
}







