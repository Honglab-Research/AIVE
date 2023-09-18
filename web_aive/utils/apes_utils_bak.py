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
    
    #우한 AA 명    
    wuhan_amino_name= ['N', 'S', 'N', 'N', 'L', 'D', 'S', 'K', 'V', 'G', 'G', 'N', 'Y', 'N', 'Y', 'L', 'Y', 'R', 'L', 'F',
                        'R', 'K', 'S', 'N', 'L', 'K', 'P', 'F', 'E', 'R', 'D', 'I', 'S', 'T', 'E', 'I', 'Y', 'Q', 'A', 'G',
                        'S', 'T', 'P', 'C', 'N', 'G', 'V', 'E', 'G', 'F', 'N', 'C', 'Y', 'F', 'P', 'L', 'Q', 'S', 'Y', 'G',
                        'F', 'Q', 'P', 'T', 'N', 'G', 'V', 'G', 'Y', 'Q', 'P', 'Y']

    def get_apess_result(self, nm, sc1, sc2_1, sc2_2, sc3):
        """apes 결과를 조회한다.

        Args:
            nm (int): Number of Mutations
            sc1 (float): Selection score1 -1.0 ~ 1.0
            sc2_1 (float): Selection score2 첫번째 조건 0 ~ 0.02
            sc2_2 (float): Selection score2 두번째 조건 0 ~ 0.02
            sc3_1 (array): Selection score3 첫번째 조건 ??현재 사용 안함 1,2,3,4,5,6

        Returns:
            _type_: _description_
        """
        #기초 데이터를 조회한다.
        init_data = self.get_init_data()
        step23 = init_data[0]
        amino_factor = init_data[1]
        mutation = init_data[2]
        
        #APES를 조회한다.
        muts_apes = self.make_apes_point(nm, mutation, amino_factor)
        
        #리니지 정보를 조회한다.
        lineage = self.get_lineage_top_20()
        
        #사용자가 선택한 mutation의 apes를 조회한다.
        lin_mut_apes = self.selection_mutations(nm, sc1, sc2_1, sc2_2, step23, muts_apes)
        
        #eigen 점수 조회
        #오른쪽 값에 0이면 오류가 발생하여 378로 변경
        aa_eigen_score = self.get_aa_eigen_score(14, lineage, 378, lin_mut_apes, step23, amino_factor)
        
        #pae 파일목록 및 평균값 조회
        predicted_errors = self.get_predicted_aligned_erros()
        
        #eigen 차트 이미지 생성
        left_eigen_chart_path = self.create_eigen_chart(aa_eigen_score[0], 'left_aa_eigen_scroe.png')
        right_eigen_chart_path = self.create_eigen_chart(aa_eigen_score[1], 'right_aa_eigen_scroe.png')
        
        #predicted 차트 이미지 생성
        left_predicted_chart_path = self.create_predicted_aligned_error_char(8, predicted_errors[0], predicted_errors[1], 'left_predicted_error.png')
        right_predicted_chart_path = self.create_predicted_aligned_error_char(0, predicted_errors[0], predicted_errors[1], 'rigth_predicted_error.png')

        dic_result = {
            'left_eigen_chart_path' : left_eigen_chart_path,
            'right_eigen_chart_path' : right_eigen_chart_path,
            'left_predicted_chart_path' : left_predicted_chart_path,
            'right_predicted_chart_path' : right_predicted_chart_path,
        }

        #결과를 어떻게 넘겨야 하는지 확인해야함.        
        return dic_result

    def get_init_data(self):
        """APES에서 사용할 기초데이터를 불러온다.
            step23 :: step2_ste3_72_7.txt 
            amino_factor :: step1_400_7.txt
            mutation :: Amino_acid_mutation_72_10000.txt
        Returns:
            tuple: 0 : step23, 1 : amino_factor, 3 : mutation
        """
        # step23 :: step2_ste3_72_7.txt
        f1 = glob.glob(os.path.abspath(self.wdir + 'step2_ste3_72_7.txt'))[0]

        # amino_factor :: step1_400_7.txt
        f2 = glob.glob(os.path.abspath(self.wdir + 'step1_400_7.txt'))[0]

        # mutation  :: Amino_acid_mutation_72_10000.txt
        f3 = glob.glob(os.path.abspath(self.wdir + 'Amino_acid_mutation_72_10000.txt'))[0]

        #조회한 파일을 데이터로 변환
        step23 = pd.read_table(f1)
        step23.index = range(0,72)
        amino_factor = pd.read_table(f2)
        
        mutation = pd.read_table(f3)
        mutation.columns = self.wuhan_amino_name

        mutation.index = range(0,710000)
        
        return (step23, amino_factor, mutation)

    def make_apes_point(self, nm, mutation, amino_factor):
        """사용자가 선택한 mutation의 수에 따라 mutation의 APES를 계산한다.

        Args:
            nm (int): Number of Mutations
            mutation (DataFrame):  mutation 정보
            amino_factor (DataFrame): amino_factor 정보

        Returns:
            _type_: _description_
        """

        mut_lin = mutation.iloc[0:nm,:]

        muts_apes=[]
        if nm < 1000:
            for i in range(nm):
                n=[]
                for j in range(72):
                    o = self.wuhan_amino_name[j]
                    m= mut_lin.iloc[i,j]
                    n.append(float(amino_factor[(amino_factor['origin']==o) & (amino_factor['mutation']==m)]['sum.n']))
                muts_apes.append(n)
                
            muts_apes = pd.DataFrame(muts_apes)
        else:
            #pandas에서 read_csv로 조회시 첫번째 Unnamed: 0 컬럼 제거 방법
            #1. 첫번째 컬럼을 인덱스로 사용하여 조회
            muts_apes = pd.read_csv('muts_apes.csv', index_col=0)
            
            #2. nnamed: 0 컬럼을 제거
            #muts_apes.drop(['Unnamed: 0'], axis = 1, inplace = True)
        
        return muts_apes
    
    def selection_mutations(self, nm, sc1, sc2_1, sc2_2, step23, muts_apes):
        """사용자가 선택한 조건에 맞는  mutation apes를 선택한다.

        Args:
            nm (int): Number of Mutations
            sc1 (float): Selection score1
            sc2_1 (float): Selection score2_1
            sc2_2 (float): Selection score2_2

        Returns:
            DataFrame: 사용자가 선택한 mutation 별 apes 값
        """

        wh2 = step23[(step23['trans.rate'] > sc2_1) & (step23['trans.rate'] < sc2_2)].index

        ct1= list(step23[(step23['clust.'] == 1)].index)
        ct3= list(step23[(step23['clust.'] == 3)].index)

        ct1 = list(set(ct1)& set(wh2))
        ct3 = list(set(ct3)& set(wh2))

        wh13=[]

        for i in range(nm):
            res_ct1=[]
            res_ct3=[]
            for j in ct1:
                if muts_apes.iloc[i,j] < sc1:
                    res_ct1.append(j)
            for k in ct3:
                if muts_apes.iloc[i,k] < sc1:
                    res_ct3.append(k)
            
            if len(res_ct1)>0 and len(res_ct3)>0:
                wh13.append(i)

        lin_mut_apes=pd.DataFrame(muts_apes.iloc[wh13, :])
        
        return lin_mut_apes

    def get_lineage_top_20(self):
        """lineages.xlsx 파일에서 리니지 정보 20개를 조회한다. 

        Returns:
            dataframe: 리니지 정보 20개
        """
        f4 = glob.glob(os.path.abspath(self.wdir+'lineages.xlsx'))[0]

        lineage = pd.read_excel(f4, sheet_name='Lineages')
        lineage = lineage.iloc[:23,]
        lineage.set_index('Spike Seq', inplace=True)

        return lineage

    def get_aa_eigen_score(self, left_lineage_no,  left_lineage, right_lineage_no, lin_mut_apes, step23, amino_factor):
        """Amino acid Property Eigen Score 정보를 조회한다.

        Args:
            left_lineage_no (int): 왼쪽에 표시될 lineage 번호
            left_lineage (DataFrame): 오른쪽에 표시될 lineage 정보
            right_lineage_no (int) : 오른쪽에 표시될 lineage 번호
            lin_mut_apes (DataFrame) : 오른쪽에 표시될 mutation lineage 정보
            step23 (DataFrame): step23 정보
            amino_factor (DataFrame): amino factor 정보

        Returns:
            Tuple : 0 : Left Aa eigen 점수, 1 : Right Aa Eigen 점수
        """
        
        #left Eigen score
        left_lineage.iloc[left_lineage_no]

        lin_apes=[]
        for i in range(3,23):
            n=[]
            for j in range(72):
                o = self.wuhan_amino_name[j]
                m = left_lineage.iloc[i,j]
                n.append(float(amino_factor[(amino_factor['origin']==o) & (amino_factor['mutation']==m)]['sum.n']))
            lin_apes.append(n)
            
        lin_apes = pd.DataFrame(lin_apes)

        step23_plot = step23.T

        a_plot = pd.concat([lin_apes, step23_plot])
        ii=left_lineage_no-3
        left_plot = a_plot.loc[[ii,'clust.','trans.rate']] # lineage index -3해서 하면됨
        

        #right Eigen score
        lin_mut_apes.iloc[0]

        a_plot = pd.concat([lin_mut_apes, step23_plot])
        right_plot = a_plot.loc[[right_lineage_no,'clust.','trans.rate']]
        
        return (left_plot, right_plot)

    def get_predicted_aligned_erros(self):
        """Colab 디렉토리의 pae 결과파일을 조회하고 각각의 평균을 계산한다.

        Returns:
            Tuple: 0 : pae 파일명, 1 : pae 파일별 평균
        """
        wdir2= self.wdir+"PAE/Colab/"
        paes = os.listdir(wdir2)
        pae = [file for file in paes if file.endswith('.csv')]
        average=[]
        for i in range(len(pae)):
            if i == 0:
                paes = pd.read_csv(wdir2+pae[i])
                average.append(np.mean(sum(paes.values.tolist(),[])))
            else:
                p = pd.read_csv(wdir2+pae[i])
                paes = pd.concat([paes,p])
                average.append(np.mean(sum(p.values.tolist(),[])))
        paes = paes.iloc[:,1:]
        
        return (paes, average)

    def create_eigen_chart(self, eigen_score, file_name):
        """eigen 점수를 이용하여 차트를 생성하고 이미지로 저장한다.

        Args:
            eigen_score (DataFrame): eigen 점수 정보
            file_name (str): 저장할 파일명
            
        Returns:
            str : 차트 이미지 경로
        """
        
        #figure 초기화
        plt.figure()
        
        #이미지 저장 
        sns.pairplot(eigen_score.T)
        
        plt.savefig(os.path.abspath(self.outputDir + file_name), dpi=100)
        
        return file_name

    def create_predicted_aligned_error_char(self, lineage_no, paes, pae_avg_list, file_name):
        """predicted alinged error 차트 이미지를 생성한다.

        Args:
            lineage_no (int): lineage 번호
            paes (_type_): pae 값
            pae_avg_list (_type_): pae 평균 목록
            file_name (_type_): 저장할 파일 명

        Returns:
            str : 차트 이미지 경로
        """
        
        target_avg = pae_avg_list[lineage_no]
        #figure 초기화
        plt.figure()
        
        sns.set(style="darkgrid")
        sns.kdeplot(sum(paes.values.tolist(),[]))
        
        for i in pae_avg_list:
            if i ==  target_avg :
                plt.axvline(x=i, color='r', linestyle='--', linewidth=3)
            else:
                plt.axvline(x=i, color='grey', linestyle='--', linewidth=3)

        plt.savefig(os.path.abspath(self.outputDir + file_name), dpi=100)
        
        return file_name
    
    

"""

계산된 PAE 결과 파일 불러오기 & 평균 구하기

이 부분은 PAE 값을 돌린 결과를 가져와야 해서 최원종에게 이번주 중으로 받아서 첨부할 예정!!

### Output2 :: Control22 :: Mutation 378

Outout2_left.png 로 대체 부탁드립니다.

### Output3 :: Control21
"""



"""### Output3 :: Control21 :: BA4 :: Select Score Distribution plot"""

#Outout2_left.png 로 대체 부탁드립니다.

"""### Output3 :: Control22"""



"""### Output3 :: Control22 :: Mutation 378 :: Select Socre Distribution plot """

#Outout2_left.png 로 대체 부탁드립니다.