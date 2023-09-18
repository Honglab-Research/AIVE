class AiveUtils {
    constructor() {
        //Amino acid 
        this.DIC_AMINO_ACID = {'ALA' : 'A','ARG' : 'R','ASN' : 'N','ASP' : 'D','CYS' : 'C','GLN' : 'Q','GLU' : 'E','GLY' : 'G','HIS' : 'H','ILE' : 'I','LEU' : 'L','LYS' : 'K',	'MET' : 'M',	'PHE' : 'F','PRO' : 'P','SER' : 'S', 'THR' : 'T','TRP' : 'W',	'TYR' : 'Y',	'VAL' : 'V'	};
        this.AA = 'ARNDCQEGHILKMFPSTWYV';
    }

    /**
     * pdb파일에서 output virus seq 관련 정보를 셋팅하고, plddt 차트를 조회한다.
     * @param {string} pdb pdb 결과 파일
     */
     parsingPdb(pdb){
        const tmpPdb = pdb.split('\n');
        let result = {};
        let aaSeqData = '';
        let arrPlddtData = [];
        let arrAaNo = [];
        let dicChainAaSeq = {};
        let oldNo = '', oldChain = '';
        let plddtNo = 0;
        try{
           tmpPdb.map(pdbLine => {
                let atomStr = pdbLine.slice(77,78).trim();
                let chain = pdbLine.slice(21,22).trim();
                let aaNo = pdbLine.slice(22,26).trim();
                let aaSeq =  pdbLine.slice(17,20).trim();
                let plddtVal = pdbLine.slice(61,66).trim();
    
                //atomStr 정보가 있을때 저장한다.
                if (atomStr != ''){
                    if (oldChain == '') {
                        oldChain = chain;
                        dicChainAaSeq[chain] = '';
                    }
    
                    //chain별 데이터를 저장한다.
                    if (oldChain != chain){
                        dicChainAaSeq[chain] = '';
                        aaSeqData = '';
                        oldChain = chain;
                    }
    
                    //aa seq 및 plddt값 파싱
                    if (oldNo != aaNo){
                        oldNo = aaNo;
                        if (plddtVal) arrPlddtData.push([plddtNo++, Number(plddtVal)]);
                        if (aaSeq) dicChainAaSeq[chain] += this.DIC_AMINO_ACID[aaSeq];
                        if (aaNo) arrAaNo.push(aaNo);
                    }
                }
    
            });

            //pdb 파일 검증
            //1. aa 검증
            let isPdb = true;
            let errNo = 0, errMsg = 'Success';
            let tmpAa = '';
            //AA가 전부 정상인지 확인
            for (let tmpC in dicChainAaSeq){
                if (isPdb){
                    for (let tmpStr of dicChainAaSeq[tmpC]){
                        tmpAa += tmpStr;
                        if (this.AA.indexOf(tmpStr) < 0) {
                            isPdb = false;
                            errNo = 100;
                            errMsg = 'Amino acid matching error.';

                            break;
                        }
                    }
                } else break;
            }
            
            //plddt 값이 전부 정상(숫자)인지 확인
            if (isPdb){
                for (let tmpVal of arrPlddtData){
                    if (isNaN(tmpVal[1])){
                        isPdb = false;
                        errNo = 101;
                        errMsg = 'pLDDT parsing error.';
    
                        break;
                    }
                };
                
            }

            //AA와 plddt 수가 같은지 확인
            if (isPdb){
                if (tmpAa.length != arrPlddtData.length){
                    isPdb = false;
                        errNo = 102;
                        errMsg = 'PDB file error';
                }
            }

            result = {
                errorNo : errNo,
                errorMsg : errMsg,
                dicChainAaSeq : dicChainAaSeq,
                arrPlddtData : arrPlddtData,
                arrAaNo : arrAaNo
            };
        } catch(err){
            debugger;
            result = {
                errorNo: -100,
                errorMsg: 'PDB file parsing error',
                dicChainAaSeq : '',
                arrPlddtData : ''
            };
        }

        return result;
    }
}







