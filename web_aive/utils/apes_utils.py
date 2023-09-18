from audioop import lin2lin
from django.conf import settings
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import math
import os
import glob
import json
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

class ApessUtils():
    """
        APES 관련 계산 및 이미지 출력을 관리하는 클래스
    """
    _aive_dir = settings.AIVE_DIR[settings.AIVE_ENV]
    
    #apes계산을 위한 데이터 파일 경로
    wdir = _aive_dir[3]
    #아웃풋 경로
    outputDir = _aive_dir[4]

    #def `get_apess_result`(self, region, input_virus_seq, output_virus_seq, input_rna_seq):
    def get_apess_result(self, prdctn_info, input_rna_seq, output_rna_seq, pae_str, plddt_str):
    
        """apess 결과를 조회하고 관련 chart를 생성한다.

        Args:
            region (_type_): virus seq 위치
            input_virus_seq (_type_): input virus seq 정보
            output_virus_seq (_type_): output virus seq 정보
            input_rna_seq (_type_): target virus rna seq 정보
            output_rna_seq (_type_): output virus rna seq 정보
            pae_str (string): pae 정보(JSON parsing 하여 사용해야함.)
            plddt_str (string): plddt 정보

        Returns:
            _type_: _description_
        """
        
        #22region = list(range(377,589))
        #prdctn_info.input_virus_seq_1 = 'QAEGVECDFSPLLSGTPPQVYNFKRLVFTNCNYNLTKLLSLFSVNDFTCSQISPAAIASNCYSSLILDYFSYPLSMKSDLSVSSAGPISQFNYKQSFSNPTCLILATVPHNLTTITKPLKYSYINKCSRLLSDDRTEVPQLVNANQYSPCVSIVPSTVWEDGDYYRKQLSPLEGGGWLVASGSTVAMTEQLQMGFGITVQYGTDTNSVCPKL'
        #prdctn_info.output_virus_seq_1 = 'QAEGVECDFSPLLSGTPPQVYNFKRLVFTNCNYNLTKLLSLFSVNDFTCSQISPAAIASNCYSSLILDYFSYPLSMKSDLSVSSAGPISQFNYKQSFSNPTCLILATVPHNLTTITKPLKYSYINKCSRLLSDGRTEVPQLVNANQYSPCVSTVPSTVWEDGDYYRKQLSPLEGGGWLVASGSTVAMTEQLQMGFGITVQYGTDTNSVCPKL'
        
        #virus_seq polarity 계산
        pae = json.loads(pae_str)
        #cvs string 또는 array string 인지 확인
        if plddt_str.startswith(',0\n'):
            cvs_plddt_str = StringIO(plddt_str)
            plddt = pd.read_csv(cvs_plddt_str, sep=',', header=None)
            plddt = plddt.iloc[1:]  #불필요한 정보 제거
        else:
            tmp_plddt = json.loads(plddt_str)
            plddt = pd.DataFrame(tmp_plddt)
            
        
        region = list(range(int(prdctn_info.trget_seq_rgin_st_lc),int(prdctn_info.trget_seq_rgin_end_lc)))
        wildtype_polarity = self.calc_polarity(prdctn_info.input_virus_seq_1)
        mutated_polarity = self.calc_polarity(prdctn_info.output_virus_seq_1)
        wildtype_ps = self.calc_ps(wildtype_polarity)
        mutated_ps = self.calc_ps(mutated_polarity)
        
        tmp_ppx = self.calc_dist_ps(wildtype_ps,mutated_ps)
        
        result_aibc = self.calc_AIBC(region, pae, plddt)
        
        #Wild type virus rna seq r
        blcr_1 = self.calc_BLCR(input_rna_seq)
        
        #Mutated type virus rna seq u
        blcr_2 = self.calc_BLCR(output_rna_seq)
        
        #blcr 계산
        tmp_blcr=[]
        for i in range(len(prdctn_info.input_virus_seq_1)):
            tmp_blcr.append(float(abs(blcr_2[i]-blcr_1[i])))
        
        #blcr 계산
        result_blcr=[]
        for i in range(len(prdctn_info.input_virus_seq_1)):
            result_blcr.append(float(abs(blcr_2[i]-blcr_1[i])))
        
        #Wild type Aa seq
        cpes_1 = self.calc_CPES(prdctn_info.input_virus_seq_1)
        #Mutated type Aa seq
        cpes_2 = self.calc_CPES(prdctn_info.output_virus_seq_1)

        #최종 cpess        
        result_cpess=[]
        for i in range(len(prdctn_info.input_virus_seq_1)):
            result_cpess.append(float((cpes_2[i]-cpes_1[i])))

        dt_res = pd.DataFrame([result_blcr,result_cpess])
        ppx= pd.DataFrame(tmp_ppx)
        clustering= pd.DataFrame(result_aibc)
        base_apess = pd.concat([dt_res, ppx.T, clustering.T])
        base_apess.index  = ['BLCR','CPES','PBFS', 'AIBC']
        base_apess = base_apess.fillna(0.1)
        
        #APESS 계산
        result_apess = []
        for i in  range(0,72):
            result_apess.append(base_apess.iloc[0,i]*base_apess.iloc[1,i]*base_apess.iloc[2,i]*base_apess.iloc[3,i])
            
        #x,y 차트 그리기
        #self.create_xy_chart(base_apess.loc['PPX4'],'position', 'PPX4', 'Polarity Base Feature Score', region, 'PPX4')
        #self.create_xy_chart(base_apess.loc['PPX5'],'position', 'PPX5', 'Polarity Base Feature Score', region, 'PPX5')
        #self.create_xy_chart(base_apess.loc['BLCR'],'position', 'BLCR', 'Base Level Change Rate', region, 'BLCR')
        #self.create_xy_chart(base_apess.loc['CPES'],'position', 'CPES', 'Chemical Property Eigen Score', region, 'CPES')
        #self.create_xy_chart(result_apess,'position', 'APESS', 'Amino acid Property Eigen Selection Score', region, 'APESS')
        
        #sars-cov-2 sublineage 분포 차트 그리기
        #self.create_sublineage_dist_chart(result_apess, 'apess_dist')
        
        #분포를 그리기 위해 데이터 조회
        f1 = glob.glob(os.path.abspath(self.wdir + 'APESS_S_subtype_1186_5.txt'))[0]
        subtype = pd.read_table(f1)
        dic_apess_dist = {
            -1.0:0,
            -0.5:0,
            0.0:0,
            0.5:0,
            1.0:0,
            1.5:0,
            2.0:0,
            2.5:0,
            3.0:0,
            3.4:0,
            4.0:0,
            4.5:0,
            5.0:0,
            5.5:0,
            6.0:0,
            6.5:0,
            7.0:0,
            7.5:0,
            8.0:0,
        }
        
        #차트를 그리기 위해 -100백을곱한다.(정승필 박사 요청)
        tmp_apess_dist = subtype.APESS * -100
        for curr_apess in tmp_apess_dist:
            if  curr_apess <= -0.1:
                dic_apess_dist[-1.0] += 1
            elif  curr_apess <= -0.5:
                dic_apess_dist[-0.5] += 1
            elif  curr_apess <= 0.0:
                dic_apess_dist[0.0] += 1
            elif  curr_apess <= 0.05:
                dic_apess_dist[0.5] += 1
            elif  curr_apess <= 1.0:
                dic_apess_dist[1.0] += 1
            elif  curr_apess <= 1.5:
                dic_apess_dist[1.5] += 1
            elif  curr_apess <= 2.0:
                dic_apess_dist[2.0] += 1
            elif  curr_apess <= 2.5:
                dic_apess_dist[2.5] += 1
            elif  curr_apess <= 3.0:
                dic_apess_dist[3.0] += 1
            elif  curr_apess <= 3.5:
                dic_apess_dist[3.5] += 1
            elif  curr_apess <= 4.0:
                dic_apess_dist[4.0] += 1
            elif  curr_apess <= 4.5:
                dic_apess_dist[4.5] += 1
            elif  curr_apess <= 5.0:
                dic_apess_dist[5.0] += 1
            elif  curr_apess <= 5.5:
                dic_apess_dist[5.5] += 1
            elif  curr_apess <= 6.0:
                dic_apess_dist[6.0] += 1
            elif  curr_apess <= 6.5:
                dic_apess_dist[6.5] += 1
            elif  curr_apess <= 7.0:
                dic_apess_dist[7.0] += 1
            elif  curr_apess <= 7.5:
                dic_apess_dist[7.5] += 1
            else:
                dic_apess_dist[8.0] += 1
        
        lst_apess = list(dic_apess_dist.items())
        
        lst_apess.sort(key=lambda x:x[0], reverse=True)

        list_aibc = [];
        for idx, val in enumerate(base_apess.loc['AIBC'].tolist()):
            list_aibc.append({
                    'x':idx,
                    'y':val
                             })

        list_pbfs = [];
        for idx, val in enumerate(base_apess.loc['PBFS'].tolist()):
            list_pbfs.append({
                    'x':idx,
                    'y':val
                             })

        list_mr_input = []
        for idx, val in enumerate(blcr_1):
            list_mr_input.append({
                    'x':idx,
                    'y':val * (10**3)
                             })
        
        
        list_mr_output = []
        for idx, val in enumerate(blcr_2):
            list_mr_output.append({
                    'x':idx,
                    'y':val * (10**3)
                             })
        list_MR = []
        
        for idx, val in enumerate(tmp_blcr):
            list_MR.append({
                    'x':idx,
                    'y':val * (10**3)
                             })
        
        list_bpes_input = []
        for idx, val in enumerate(cpes_1):
            list_bpes_input.append({
                    'x':idx,
                    'y':val * (10**2)
                             })
        
        list_bpes_output = []
        for idx, val in enumerate(cpes_2):
            list_bpes_output.append({
                    'x':idx,
                    'y':val * (10**2)
                             }) 
        list_BPES = []
        for idx, val in enumerate(result_cpess):
            list_BPES.append({
                    'x':idx,
                    'y':val * (10**2)
                             })
                
        list_result_apess = []
        list_wild_apess = []
        for idx, val in enumerate(result_apess):
            list_result_apess.append(val*(10**4))
            list_wild_apess.append(0)

        return {
            'scps': list_aibc,
            'ps': list_pbfs,
            'mr_input': list_mr_input,
            'mr_output': list_mr_output,
            'mr': list_MR,
            'bpes_input': list_bpes_input,
            'bpes_output': list_bpes_output,
            'bpes': list_BPES,
            'apess': list_result_apess,
            'apess_wild': list_wild_apess,
            'apess_dist': lst_apess,
        }

    def calc_polarity(self, aa_seq):
        npolar=['A','V','L','G','I','M','W','F','P']
        polar=['S','C','N','Q','T','Y']
        acidic=['D','E']
        basic=['K','R','H']
        
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
                
        return [polar_aa]

    def calc_ps(self, input_polarity):
        """polarity에 따른 score를 계산한다.

        Args:
            input_polarity (list): polarity 리스트

        Returns:
            list:  polarity에 따른 점수
        """
        list_polarity = input_polarity[0]
        list_polarity = [str(i) for i in list_polarity]
        
        #ppx_score는 0.1로 초기화
        result_ps= [0.1] * len(list_polarity)
        
        for i in range(len(list_polarity)-2):
            val = (list_polarity[i]+list_polarity[i+1])
            if val[:2] == '22' :
                result_ps[i] = 0.5
                result_ps[i+1] = 0.5    
        
        return result_ps
    
    def calc_dist_ps(self,wildtype_ps,mutated_ps):
        """두개의 polarity score의 차이 값을 계산한다.

        Args:
            wildtype_ps (_type_): reference polarity score
            mutated_ps (_type_): usertype polarity score

        Returns:
            _type_: wildtype_ps과 mutated_ps의 차이값을 계산한다.
        """
        result_dist_ps=wildtype_ps
        for i in range(len(wildtype_ps)):
            dppx=(wildtype_ps[i]-mutated_ps[i])
            if float(dppx == 0.4):
                result_dist_ps[i] = 0.9
            elif (dppx == -0.4):
                result_dist_ps[i] = 0.5
                
        return result_dist_ps
    
    def calc_AIBC(self, region, pae, plddt):
        dt_pae = pd.DataFrame(pae[0]['predicted_aligned_error'])
        corr = dt_pae.corr(method='pearson')
        
        pca = PCA(n_components=2)
        printcipalComponents = pca.fit_transform(corr)
        principalDF = pd.DataFrame(data=printcipalComponents, columns= ['principal component1','printcipal component2'])
        
        #k-means cluster 셋팅
        nn=round(math.sqrt(len(principalDF)))
        km = KMeans(
            n_clusters=nn, init='random',
            n_init=10, max_iter=300, 
            tol=1e-04, random_state=0
        )
        
        #pace 클러스터링
        y_km = km.fit_predict(principalDF)
        
        dt_plddt = pd.DataFrame(plddt)
        dt_plddt = dt_plddt.iloc[:,1:]
        
        #plddt 클러스터링
        x_km = km.fit_predict(dt_plddt)

        #정승필 박사 요청으로 한번더 클러스터링 (2023.01.17)        
        xy=[]
        xy = pd.DataFrame(x_km, y_km)
        #pae,plddt 합하여 클러스터링
        xy_km = km.fit_predict(xy)
        
        cluster=pd.DataFrame(xy_km)
        number=pd.DataFrame(region)
        kmeans=pd.concat([number.T, cluster.T])
        
        s_domain_cluster_pos=[452,478]#현재 바이러스는 S도메인의 특정위치가 중요하기 때문에 해당 부분은 하드코딩 되어야함.
        pos2=[]
        for i in range(len(kmeans.columns)):
            if kmeans.iloc[0,i] in s_domain_cluster_pos:
                pos2.append(kmeans.iloc[1,i])
        
        result_aibc=[]
        for i in range(len(kmeans.columns)):
            if kmeans.iloc[1,i] in pos2:
                result_aibc.append(0.9)
            else:
                result_aibc.append(0.1)
        
        return result_aibc
    
    def calc_BLCR(self, input_rna_seq):
        col1=[]
        col2=[]
        col3=[]
        
        for i in range(0, len(input_rna_seq), 3):
            col1.append(input_rna_seq[i])
            col2.append(input_rna_seq[i+1])
            col3.append(input_rna_seq[i+2])
        
        rnaseq = pd.DataFrame([col1, col2, col3])
        
        file_name1='AA_64_score.txt'
        aa64=pd.read_table(self.wdir+file_name1)

        blcr=[]
        for i in rnaseq.columns:
            blcr.append(float(aa64[(aa64['seq1']==rnaseq.loc[0,i]) & (aa64['seq2']==rnaseq.loc[1,i]) & (aa64['seq3']==rnaseq.loc[2,i])]['BLCR']))
        
        return (blcr)
    
    def calc_CPES(self, input_virus_seq):
        file_name2='CPES20.txt'
        aa20=pd.read_table(self.wdir + file_name2)
        
        cpes=[]

        for i in range(len(input_virus_seq)):
            cpes.append(float(aa20[((aa20.index)==input_virus_seq[i])]['r.CPES20']))
        
        
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
        f1 = glob.glob(os.path.abspath(self.wdir + 'APESS_S_subtype_1186_5.txt'))[0]
        subtype = pd.read_table(f1)
        subtype.index = range(0,1800)
        
        sns.set(style="darkgrid")
        sns.kdeplot(subtype.APESS)

        apess_sum=sum(result_apess)
        plt.axvline(x=apess_sum, color='r', linestyle='--', linewidth=3)
        plt.savefig(os.path.abspath(self.outputDir + file_name), dpi=100)
        #plt.show()
        return file_name