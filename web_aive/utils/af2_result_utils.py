import json
from web_aive.models import Af2Result, JobInfo, PrdctnInfo
from django.conf import settings

class Af2ResultUtils():
    _aive_dir = settings.AIVE_DIR[settings.AIVE_ENV]
    #알파폴드2 결과 경로
    af2_result_path = _aive_dir[2]
    
    #af2 랭킹별 결과를 조회한다.
    def get_af2_result(self, prdctn_info):
        #결과 조회
        af2_result_list = prdctn_info.af2result_set.all()
        #알파폴드2 전체 결과
        af2_result_info = {}
        
        #각 결과당 사용할 데이터 정제
        for af2_result in af2_result_list:
            #평균 plddt 조회
            #Multimor일 경우만 조회하돠록 한다.
            avg_plddt_info = ['0','0','0','0','0']
            if (prdctn_info.prdctn_protein_struct == 'MT'):
                avg_plddt_info = self.get_avg_plddt(prdctn_info.prdctn_info_seq, af2_result.aa_seq_knd, prdctn_info.prdctn_protein_struct)

            #순위별 결과데이터
            rank_result = []
            
            #랭킹별 정보를 조회한다.
            for rank in range(0,5):
                tmp_result = {
                    'aa_seq_knd' : af2_result.aa_seq_knd,
                    'avg_plddt' : avg_plddt_info[rank],
                    'pdb_file' : '{}_{}_{}/ranked_{}.pdb'.format(prdctn_info.prdctn_info_seq, af2_result.aa_seq_knd, prdctn_info.prdctn_protein_struct, rank),
                    'APESS_file' : '{}_{}_{}/ranked_{}_APESS.png'.format(prdctn_info.prdctn_info_seq, af2_result.aa_seq_knd, prdctn_info.prdctn_protein_struct, rank),
                    'APESS_dist_file' : '{}_{}_{}/ranked_{}_APESS_distribution.png'.format(prdctn_info.prdctn_info_seq, af2_result.aa_seq_knd, prdctn_info.prdctn_protein_struct, rank),
                    'PAE_file' : '{}_{}_{}/ranked_{}_PAE.png'.format(prdctn_info.prdctn_info_seq, af2_result.aa_seq_knd, prdctn_info.prdctn_protein_struct, rank),
                    'PAE_json_file' : '{}_{}_{}/ranked_{}_PAE.json'.format(prdctn_info.prdctn_info_seq, af2_result.aa_seq_knd, prdctn_info.prdctn_protein_struct, rank),
                    'PAE_dist_file' : '{}_{}_{}/ranked_{}_PAE_distribution.png'.format(prdctn_info.prdctn_info_seq, af2_result.aa_seq_knd, prdctn_info.prdctn_protein_struct, rank),
                    'pLDDT_file' : '{}_{}_{}/ranked_{}_pLDDT.png'.format(prdctn_info.prdctn_info_seq, af2_result.aa_seq_knd, prdctn_info.prdctn_protein_struct, rank),
                    'pLDDT_cvs_file' : '{}_{}_{}/ranked_{}_pLDDT.csv'.format(prdctn_info.prdctn_info_seq, af2_result.aa_seq_knd, prdctn_info.prdctn_protein_struct, rank),
                }
                rank_result.append(tmp_result)
                
            af2_result_info[af2_result.aa_seq_knd] = rank_result
        
        return af2_result_info    
            
    
    #랭킹별 평균 plddt 값을 조회한다.
    def get_avg_plddt(self, prdctn_info_seq, aa_seq_knd, prdctn_protein_struct):
        tmp_path = '{}{}_{}_{}/pDockQ.txt'.format(self.af2_result_path,prdctn_info_seq,aa_seq_knd,prdctn_protein_struct)
        f = open(tmp_path,'r')

        list_plddt = f.readlines()
        
        ranking_plddt = [];
        
        for i, plddt_line in enumerate(list_plddt, start=0):
            if (i > 0):
                plddt = plddt_line.split('\t')
                ranking_plddt.append(plddt[1][:-1])
        
        return (ranking_plddt)