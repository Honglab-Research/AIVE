from audioop import lin2lin
from django.conf import settings
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import glob

class ApesUtils():
    """
        APES 관련 계산 및 이미지 출력을 관리하는 클래스
    """
    _aive_dir = settings.AIVE_DIR[settings.AIVE_ENV]
    
    #apes계산을 위한 데이터 파일 경로
    wdir = _aive_dir[3]
    #아웃풋 경로
    outputDir = _aive_dir[4]

    #def get_apess_result(self, region, input_virus_seq, output_virus_seq, input_rna_seq):
    def get_apess_result(self, prdctn_info, input_rna_seq):
    
        """apess 결과를 조회하고 관련 chart를 생성한다.

        Args:
            region (_type_): virus seq 위치
            input_virus_seq (_type_): input virus seq 정보
            output_virus_seq (_type_): output virus seq 정보
            input_rna_seq (_type_): target virus rna seq 정보

        Returns:
            _type_: _description_
        """
        
        
        #region = list(range(377,589))
        #prdctn_info.input_virus_seq_1 = 'QAEGVECDFSPLLSGTPPQVYNFKRLVFTNCNYNLTKLLSLFSVNDFTCSQISPAAIASNCYSSLILDYFSYPLSMKSDLSVSSAGPISQFNYKQSFSNPTCLILATVPHNLTTITKPLKYSYINKCSRLLSDDRTEVPQLVNANQYSPCVSIVPSTVWEDGDYYRKQLSPLEGGGWLVASGSTVAMTEQLQMGFGITVQYGTDTNSVCPKL'
        #prdctn_info.output_virus_seq_1 = 'QAEGVECDFSPLLSGTPPQVYNFKRLVFTNCNYNLTKLLSLFSVNDFTCSQISPAAIASNCYSSLILDYFSYPLSMKSDLSVSSAGPISQFNYKQSFSNPTCLILATVPHNLTTITKPLKYSYINKCSRLLSDGRTEVPQLVNANQYSPCVSTVPSTVWEDGDYYRKQLSPLEGGGWLVASGSTVAMTEQLQMGFGITVQYGTDTNSVCPKL'
        
        #virus_seq polarity 계산
        region = list(range(int(prdctn_info.trget_seq_rgin_st_lc),int(prdctn_info.trget_seq_rgin_end_lc)))
        input_polarity = self.calc_polarity(prdctn_info.input_virus_seq_1)
        tmp_ppx = self.calc_PPX(input_polarity, region)
        blcr = self.calc_BLCR(input_rna_seq, region)
        cpes = self.calc_CPES(prdctn_info.input_virus_seq_1, prdctn_info.output_virus_seq_1, region)
        
        #결과 합치기
        tmp_result = pd.DataFrame([blcr, cpes])
        ppx = pd.DataFrame(tmp_ppx)
        base_apess = pd.concat([tmp_result, ppx])
        base_apess.index = ['BLCR','CPES','PPX4','PPX5']
        base_apess = base_apess.fillna(0.5)
        
        #APESS 계산
        result_apess = []
        for i in range(len(base_apess.columns)):
            result_apess.append(base_apess.iloc[0,i]*base_apess.iloc[1,i]*base_apess.iloc[2,i])
            
        #x,y 차트 그리기
        #self.create_xy_chart(base_apess.loc['PPX4'],'position', 'PPX4', 'Polarity Base Feature Score', region, 'PPX4')
        #self.create_xy_chart(base_apess.loc['PPX5'],'position', 'PPX5', 'Polarity Base Feature Score', region, 'PPX5')
        #self.create_xy_chart(base_apess.loc['BLCR'],'position', 'BLCR', 'Base Level Change Rate', region, 'BLCR')
        #self.create_xy_chart(base_apess.loc['CPES'],'position', 'CPES', 'Chemical Property Eigen Score', region, 'CPES')
        #self.create_xy_chart(result_apess,'position', 'APESS', 'Amino acid Property Eigen Selection Score', region, 'APESS')
        
        #sars-cov-2 sublineage 분포 차트 그리기
        #self.create_sublineage_dist_chart(result_apess, 'apess_dist')
        
        #분포를 그리기 위해 데이터 조회
        f1 = glob.glob(os.path.abspath(self.wdir + 'sublineage_APESS_1800.txt'))[0]
        subtype = pd.read_table(f1)
        dic_apess_dist = {
            '-0.030':0,
            '-0.025':0,
            '-0.020':0,
            '-0.015':0,
            '-0.010':0,
            '-0.005':0,
            '0.000':0,
            '0.005':0,
            '0.010':0,
        }
        
        for curr_apess in subtype.APESS:
            if  curr_apess <= -0.030:
                dic_apess_dist['-0.030'] += 1
            elif  curr_apess <= -0.025:
                dic_apess_dist['-0.025'] += 1
            elif  curr_apess <= -0.020:
                dic_apess_dist['-0.020'] += 1
            elif  curr_apess <= -0.015:
                dic_apess_dist['-0.015'] += 1
            elif  curr_apess <= -0.010:
                dic_apess_dist['-0.010'] += 1
            elif  curr_apess <= -0.005:
                dic_apess_dist['-0.005'] += 1
            elif  curr_apess <= 0.000:
                dic_apess_dist['0.000'] += 1
            elif  curr_apess <= 0.005:
                dic_apess_dist['0.005'] += 1
            else:
                dic_apess_dist['0.010'] += 1
        
        lst_apess = list(dic_apess_dist.items())
        
        lst_apess.sort(key=lambda x:x[0])
        
        return {
            'ppx4': base_apess.loc['PPX4'].tolist(),
            'ppx5': base_apess.loc['PPX5'].tolist(),
            'blcr': base_apess.loc['BLCR'].tolist(),
            'cpes': base_apess.loc['CPES'].tolist(),
            'apess': result_apess,
            'apess_1800': lst_apess,
        }

    def calc_polarity(self, aa_seq):
        npolar=['A','V','L','G','I','M','W','F','P']
        polar=['S','C','N','Q','T','Y']
        acidic=['D','E']
        basic=['K','R','H']
        
        f1=['K','R','H']
        f2=['D','E']
        f3=['S','N','Q','T']
        f4=['C','G','P']
        f5=['A','V','L','I','M','W','F','Y']
        
        polar_aa=[]
        for seq in aa_seq:
            if seq in npolar:
                polar_aa.append(1)
            elif seq in polar:
                polar_aa.append(2)
            elif seq in acidic:
                polar_aa.append(3)
            elif seq in basic: 
                polar_aa.append(4)
            else:
                polar_aa.append(0)
                
    
        five_aa=[]
        for seq in aa_seq:
            if seq in f1:
                five_aa.append(1)
            elif seq in f2:
                five_aa.append(2)
            elif seq in f3:
                five_aa.append(3)
            elif seq in f4:
                five_aa.append(4)
            elif seq in f5:
                five_aa.append(5)
            else:
                five_aa.append(0)
                
        return [polar_aa, five_aa]
    
    def calc_PPX(self, input_polarity, region):
        rbd_pp4 = input_polarity[0]
        rbd_pp4 = [str(i) for i in rbd_pp4]

        ppx1234=[]
        for i in range(len(region)-2):
            val = (rbd_pp4[i]+rbd_pp4[i+1]+rbd_pp4[i+2])
            if val[:2] == '22' :
                ppx1234.append(1)
            else:
                ppx1234.append(0.5)

        rbd_pp5 = input_polarity[1]
        rbd_pp5 = [str(i) for i in rbd_pp5]

        ppx12345=[]
        for i in range(len(region)-2):
            val = (rbd_pp5[i]+rbd_pp5[i+1]+rbd_pp5[i+2])
            if val[:2] == '33' :
                ppx12345.append(1)
            else:
                ppx12345.append(0.5)

        ppx = []
        ppx.append(ppx1234)
        ppx.append(ppx12345)
        
        return ppx
    
    def calc_BLCR(self, input_rna_seq, region):
        col1=[]
        col2=[]
        col3=[]
        for i in range(len(input_rna_seq)-2):
            col1.append(input_rna_seq[i])
            col2.append(input_rna_seq[i+1])
            col3.append(input_rna_seq[i+2])
            
        rnaseq = pd.DataFrame([col1, col2, col3])
        
        file_name1='AA_64_score.txt'
        aa64=pd.read_table(self.wdir+file_name1)
        
        w_seq=rnaseq.iloc[:,region]
        blcr=[]
        for i in w_seq.columns:
            blcr.append(float(aa64[(aa64['seq1']==rnaseq.loc[0,i]) & (aa64['seq2']==rnaseq.loc[1,i]) & (aa64['seq3']==rnaseq.loc[2,i])]['BLCR']))
        
        return (blcr)
    
    def calc_CPES(self, input_virus_seq, output_virus_seq, region):
        file_name2='AA_400_score.txt'
        aa400=pd.read_table(self.wdir + file_name2)
        
        cpes=[]
        
        for i in range(len(region)):
            cpes.append(float(aa400[(aa400['origin']==input_virus_seq[i]) & (aa400['mutation']==output_virus_seq[i])]['sum.n']))
        
        return (cpes)
    
    def create_xy_chart(self, arrData, xlabel, ylabel, title, region, file_name):
        """apess 값을 이용하여 차트를 생성하고 이미지로 저장한다.

        Args:
            arrData (Array): 차트 데이터
            xlabel (str): x축 라벨 명
            ylabel (str): y축 라벨 명
            title (str): 차트 제목
            file_name (str): 저장할 파일명
            region (int): aa 범위
            
        Returns:
            str : 차트 이미지 경로
        """
        
        x=np.arange(region[0], region[len(region)-1]+1)
        
        y=np.array(arrData)
        
        #figure 초기화
        plt.figure()
        
        plt.plot(x,y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        
        #이미지 저장 
        plt.savefig(os.path.abspath(self.outputDir + file_name), dpi=100)
        
        return file_name
    
    def create_sublineage_dist_chart(self, result_apess, file_name):
        """SARS-COV-2 sublineage 분포 차트를 그린다.

        Args:
            result_apess (Dataframe): 최종 apess 결과
            file_name (_type_): 차트 파일명

        Returns:
            _type_: 차트 파일명
        """
        f1 = glob.glob(os.path.abspath(self.wdir + 'sublineage_APESS_1800.txt'))[0]
        subtype = pd.read_table(f1)
        subtype.index = range(0,1800)
        
        sns.set(style="darkgrid")
        sns.kdeplot(subtype.APESS)

        apess_sum=sum(result_apess)
        plt.axvline(x=apess_sum, color='r', linestyle='--', linewidth=3)
        plt.savefig(os.path.abspath(self.outputDir + file_name), dpi=100)
        #plt.show()
        return file_name