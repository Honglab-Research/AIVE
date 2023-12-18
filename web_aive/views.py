from itertools import combinations_with_replacement
from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotAllowed, FileResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from django.db import transaction
from django.db.models import Q
from django.conf import settings

from web_aive.models import Af2Result, JobInfo, PrdctnInfo
from .forms import PrdctnForm
from common.models import CommCode, VirusSeqInfo
from web_aive.utils.af2_result_utils import Af2ResultUtils
from web_aive.utils.apes_utils import ApessUtils
from web_aive.utils.pdockq import PDockQUtils
from datetime import datetime

import math
import json
import os
import zipfile

_aive_dir = settings.AIVE_DIR[settings.AIVE_ENV]

#aive 메인화면을 표시한다.
def aive_main(request):
    return render(request, 'aive/aive_main.html', {})

#virus server prediction 화면 이동
def prdctn_regist_server(request):
    prdctnForm = PrdctnForm()
    
    context = {'title': '제목을 넘기자', 'prdctnForm': prdctnForm, 'devEnv':settings.AIVE_ENV,}
    
    return render(request, 'aive/prdctn_regist_server.html', context)

#virus colab prediction 화면 이동
def prdctn_regist_colab(request):
    prdctnForm = PrdctnForm()
    
    context = {'title': '제목을 넘기자', 'prdctnForm': prdctnForm, 'devEnv':settings.AIVE_ENV,}
    
    return render(request, 'aive/prdctn_regist_colab.html', context)

#virus prediction 정보 등록 및 작업 등록
def prdctn_insert(request):
    if request.method == 'POST':
        prdctnForm = PrdctnForm(request.POST)
        if prdctnForm.is_valid():
            with transaction.atomic():
                #예측정보 저장
                prdctn_info = prdctnForm.save(commit=False)
                
                #입력된 정보가 2개 이상을 경우는 Mutlimor, 아니면 Monomor로 한다.
                if (prdctn_info.input_virus_seq_2 != ''):
                    prdctn_info.prdctn_protein_struct = 'MT'
                else:
                    prdctn_info.prdctn_protein_struct = 'MN'
                
                prdctn_info.regist_dt = timezone.now()
                prdctn_info.regist_id = request.user.username
                prdctn_info.save()
                
                #입력된 전체 AA를 Multimor로 돌린다.(job_seq_knd는 현재 의미가 없어 MUT로 고정)
                job_info2 = JobInfo(prdctn_info = prdctn_info)
                job_info2.job_seq_knd = 'MUT'
                job_info2.regist_dt = timezone.now()
                job_info2.save()
                
                af2_result2 = Af2Result(prdctn_info = prdctn_info)
                af2_result2.aa_seq_knd = 'MUT'
                af2_result2.regist_dt = timezone.now()
                af2_result2.save()
                
                #af2 결과 테이블에 데이터를 저장해야함.            
        context = {'prdctnForm': prdctnForm}
    #return render(request, 'aive/prdctn_regist_server.html', context)     
    return redirect('aive:prdctn_list')
        
#사용자 작업 목록 조회
def prdctn_list(request):
    page = request.GET.get('page',1)
    demo_yn = request.GET.get('demo_yn')
    
    #사용자 예측 목록 조회
    #관리자는 모든 정보 조회
    #사용자는 자신의 장보 조회
    #나머지는 완료되고 공개된 데이터 조회
    
    if request.user.is_superuser:
        prdctn_list = PrdctnInfo.objects.select_related('job_info','').values('prdctn_info_seq','prdctn_sj','prdctn_protein_struct','trget_virus','jobinfo__id','jobinfo__job_prgss_sttus').distinct().order_by('-regist_dt')
    elif request.user.is_authenticated:
        prdctn_list = PrdctnInfo.objects.filter(regist_id = request.user.username).select_related('job_info').values('prdctn_info_seq','prdctn_sj','prdctn_protein_struct','trget_virus','output_virus_seq_1','output_virus_seq_2','output_virus_seq_3','output_virus_seq_4','output_virus_seq_5','output_virus_seq_6','output_virus_seq_7','output_virus_seq_8','jobinfo__id', 'jobinfo__job_prgss_sttus').distinct().order_by('-regist_dt')
    else:
        prdctn_list = PrdctnInfo.objects.filter(public_yn = 'Y').select_related('job_info').values('prdctn_info_seq','prdctn_sj','prdctn_protein_struct','trget_virus','output_virus_seq_1','output_virus_seq_2','output_virus_seq_3','output_virus_seq_4','output_virus_seq_5','output_virus_seq_6','output_virus_seq_7','output_virus_seq_8','jobinfo__id','jobinfo__job_prgss_sttus').distinct().order_by('-regist_dt')
    
    #공통코드 처리를 위한 target virus 조회    
    virus_list = CommCode.objects.filter(cl_code='TV')
    
    
    for row in prdctn_list:
        job_list = JobInfo.objects.select_related('prdctn_info','').filter( Q(id__lte = row['jobinfo__id']) & ~Q(job_prgss_sttus='C') ).values('prdctn_info__prdctn_protein_struct','prdctn_info__output_virus_seq_1','prdctn_info__output_virus_seq_2','prdctn_info__output_virus_seq_3','prdctn_info__output_virus_seq_4','prdctn_info__output_virus_seq_5','prdctn_info__output_virus_seq_6','prdctn_info__output_virus_seq_7','prdctn_info__output_virus_seq_8')
        tmp_hour = 0
        for job_row in job_list:
            if job_row['prdctn_info__prdctn_protein_struct'] == 'MN':
                #Monomor일 경우 72자리를 30분으로 계산
                tmp_hour += math.ceil(len(job_row['prdctn_info__output_virus_seq_1'])/72*0.5)
            else:
                #Multimor일 경우 144자리를 3시간으로 계산
                tmp_virus_seq = job_row['prdctn_info__output_virus_seq_1'] + job_row['prdctn_info__output_virus_seq_2']  + job_row['prdctn_info__output_virus_seq_3'] + job_row['prdctn_info__output_virus_seq_4'] + job_row['prdctn_info__output_virus_seq_5'] + job_row['prdctn_info__output_virus_seq_6'] + job_row['prdctn_info__output_virus_seq_7'] + job_row['prdctn_info__output_virus_seq_8']
                tmp_hour += math.ceil(len(tmp_virus_seq)/144*3)
                
        row['rem_time'] = tmp_hour
            
        
    #한페이지에 10행씩 표시
    paginator = Paginator(prdctn_list, 10)
    page_obj = paginator.get_page(page)
    context = {'prdctn_list': page_obj,
               'virus_list': virus_list,
               }
    #도메인 명이 데모이면 최상단에 데모정보가 보이도록 한다.
    if demo_yn == 'demo':
        context['demo_yn'] = 'Y'
    
    return render(request, 'aive/prdctn_list.html', context)

#사용자 작업 결과
def prdctn_result(request, prdctn_info_seq): 
    #예측정보 조회
    prdctn_info = get_object_or_404(PrdctnInfo, pk = prdctn_info_seq)
    
    #알파폴드2 결과 조회
    af2_result_utils = Af2ResultUtils()
    af2_result_info = af2_result_utils.get_af2_result(prdctn_info)
    
    context = {'prdctn_info':prdctn_info,
               'af2_result_info':af2_result_info,
               'devEnv':settings.AIVE_ENV,
               }
    
    #target virus에 따라 결과 페이지를 다르게 보여준다.
    if prdctn_info.trget_virus == 'CV2':
        result_page = 'aive/prdctn_result_cv2.html'
        #해당하는 도메인의 결과정보를 같이 넘긴다.
        wuhan_result = {
                    'pdb_file' : '{}SARS-CoV-2/{}/selected_prediction.pdb'.format(_aive_dir[5], prdctn_info.domain_nm),
                    'PAE_json_file' : '{}SARS-CoV-2/{}/predicted_aligned_error.json'.format(_aive_dir[5], prdctn_info.domain_nm),
                    'pLDDT_cvs_file' : '{}SARS-CoV-2/{}/pLDDT.csv'.format(_aive_dir[5], prdctn_info.domain_nm),
                }
        context['wuhan_result'] = wuhan_result
    else:
        #비교를 위한 사용자 예측 목록 조회
        prdctn_list = PrdctnInfo.objects.filter(Q(regist_id = request.user.username) | Q(public_yn = 'Y')).select_related('job_info').values('prdctn_info_seq','prdctn_sj','prdctn_protein_struct','trget_virus','output_virus_seq_1','output_virus_seq_2','output_virus_seq_3','output_virus_seq_4','output_virus_seq_5','output_virus_seq_6','output_virus_seq_7','output_virus_seq_8','jobinfo__id', 'jobinfo__job_prgss_sttus').distinct()
        
        #공통코드 처리를 위한 target virus 조회    
        virus_list = CommCode.objects.filter(cl_code='TV')
        context['prdctn_list'] = prdctn_list
        context['virus_list'] = virus_list
        
        result_page = 'aive/prdctn_result.html'
    
    return render(request, result_page, context)

def prdctn_result_compare(request):
    ori_seq = request.GET.get('oriPrdctnInfoSeq')
    compare_seq = request.GET.get('comparePrdctnInfoSeq')
    prdctn_info = get_object_or_404(PrdctnInfo, pk = ori_seq)
    compare_prdctn_info = get_object_or_404(PrdctnInfo, pk = compare_seq)
    
    #알파폴드2 결과 조회
    af2_result_utils = Af2ResultUtils()
    ori_af2_result_info = af2_result_utils.get_af2_result(prdctn_info)
    compare_af2_result_info = af2_result_utils.get_af2_result(compare_prdctn_info)
    
    context = {'prdctn_info':prdctn_info,
               'af2_result_info':ori_af2_result_info,
               'compare_prdctn_info':compare_prdctn_info,
               'compare_af2_result_info':compare_af2_result_info,
               'devEnv':settings.AIVE_ENV,
               }
    
    return render(request, 'aive/prdctn_result_compare.html', context)

def aive_result_viewer(reqeust):
    prdctnForm = PrdctnForm()
    
    context = {'title': '제목을 넘기자', 'prdctnForm': prdctnForm, 'devEnv':settings.AIVE_ENV,}
    return render(reqeust, 'aive/aive_result_viewer.html', context)

def file_download(reqeust):
    file_name = reqeust.GET.get('file_name')
    file_type = reqeust.GET.get('file_type')
    
    if file_type == 'apes':
        #apes 결과 경로
        file_path = _aive_dir[4]  + '{}'.format(file_name)
    elif file_type == 'cv2':
        #apes 결과 경로
        file_path = '{}'.format(file_name)
    else:
        #알파폴드2 결과 경로
        file_path = _aive_dir[2]  + '{}'.format(file_name)
        
    f = open(file_path,'rb')
    
    response = HttpResponse(content_type='application/force-download')
    response = FileResponse(f)
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response

def prdctn_result_download(request):
    prdctn_info_seq = request.POST.get('prdctn_info_seq')
    aa_seq_knd = request.POST.get('aa_seq_knd')
    prdctn_protein_struct = request.POST.get('prdctn_protein_struct')
    
    target_files = []
    
    for param in request.POST:
        if request.POST.get(param) == 'Y':
            if param == 'fasta': target_files.append(f'{_aive_dir[0]}{prdctn_info_seq}_{aa_seq_knd}_{prdctn_protein_struct}.fasta');
            if param == 'ranking': target_files.append('ranking_debug.json');
            
            if param == 'pdb1': target_files.append('ranked_0.pdb')
            if param == 'pdb2': target_files.append('ranked_1.pdb')
            if param == 'pdb3': target_files.append('ranked_2.pdb')
            if param == 'pdb4': target_files.append('ranked_3.pdb')
            if param == 'pdb5': target_files.append('ranked_4.pdb')
            
            if param == 'pae_json1': target_files.append('ranked_0_PAE.json')
            if param == 'pae_json2': target_files.append('ranked_1_PAE.json')
            if param == 'pae_json3': target_files.append('ranked_2_PAE.json')
            if param == 'pae_json4': target_files.append('ranked_3_PAE.json')
            if param == 'pae_json5': target_files.append('ranked_4_PAE.json')
            
            if param == 'pae_cvs1': target_files.append('ranked_0_PAE.csv')
            if param == 'pae_cvs2': target_files.append('ranked_1_PAE.csv')
            if param == 'pae_cvs3': target_files.append('ranked_2_PAE.csv')
            if param == 'pae_cvs4': target_files.append('ranked_3_PAE.csv')
            if param == 'pae_cvs5': target_files.append('ranked_4_PAE.csv')
            
            if param == 'plddt1': target_files.append('ranked_0_pLDDT.csv')
            if param == 'plddt2': target_files.append('ranked_1_pLDDT.csv')
            if param == 'plddt3': target_files.append('ranked_2_pLDDT.csv')
            if param == 'plddt4': target_files.append('ranked_3_pLDDT.csv')
            if param == 'plddt5': target_files.append('ranked_4_pLDDT.csv')
            
            if prdctn_protein_struct == 'MT':
                if param == 'pkl1': target_files.append('result_model_1_multimer_v2_pred_0.pkl')
                if param == 'pkl2': target_files.append('result_model_2_multimer_v2_pred_0.pkl')
                if param == 'pkl3': target_files.append('result_model_3_multimer_v2_pred_0.pkl')
                if param == 'pkl4': target_files.append('result_model_4_multimer_v2_pred_0.pkl')
                if param == 'pkl5': target_files.append('result_model_5_multimer_v2_pred_0.pkl')
            else:
                if param == 'pkl1': target_files.append('result_model_1_ptm_pred_0.pkl')
                if param == 'pkl2': target_files.append('result_model_2_ptm_pred_0.pkl')
                if param == 'pkl3': target_files.append('result_model_3_ptm_pred_0.pkl')
                if param == 'pkl4': target_files.append('result_model_4_ptm_pred_0.pkl')
                if param == 'pkl5': target_files.append('result_model_5_ptm_pred_0.pkl')
    
    now = datetime.now()
    strYmd = now.strftime('%Y%m%d');
    zip_full_path = '{}_aive_result_{}_{}_{}.zip'.format(strYmd, prdctn_info_seq, aa_seq_knd, prdctn_protein_struct)
    
    #압축파일 경로를 제거하기 위해 먼저 디렉토리를 이동한다.
    os.chdir(_aive_dir[2] + '{}_{}_{}/'.format(prdctn_info_seq, aa_seq_knd, prdctn_protein_struct))
    
    #선택된 정보에 맞는 결과 파일을 압축한다.
    with zipfile.ZipFile(zip_full_path, 'w') as af2_result_zip:
        for tmp_file in target_files:
            af2_result_zip.write(tmp_file)
            
        af2_result_zip.close()
    
    f = open(zip_full_path,'rb')
    
    response = HttpResponse(content_type='application/force-download')
    response = FileResponse(f)
    response['Content-Disposition'] = f'attachment; filename={strYmd}_af2_result_{prdctn_info_seq}_{aa_seq_knd}.zip'
    return response

#pdockq 결과를 조회한다.
def get_pdockq(request):
    #apess 결과 조회
    if request.method == 'POST':
        
        pdb_info = request.POST.get('pdb_info')
        
        pDockq = PDockQUtils()
        
        chain_coords, chain_plddt = pDockq.read_pdb(pdb_info)
        t=8 #Distance threshold, set to 8 Å
        pdockq, ppv = pDockq.calc_pdockq(chain_coords, chain_plddt, t)
        
        print('pDockQ =',pdockq)
        pdockq_json = {'pdockq' : pdockq}
    else:
        pdockq_json = {}
        
    return JsonResponse(pdockq_json, safe=False)

#apes 결과를 조회한다.
def get_apess_result(request):
    #apess 결과 조회
    if request.method == 'POST':
        prdctn_info = PrdctnInfo()
        prdctn_info.input_virus_seq_1 = request.POST.get('input_virus_seq_1')
        prdctn_info.trget_virus = request.POST.get('trget_virus')
        prdctn_info.virus_mut_nm = request.POST.get('virus_mut_nm')
        prdctn_info.domain_nm = request.POST.get('domain_nm')
        prdctn_info.output_virus_seq_1 = request.POST.get('output_virus_seq_1')
        prdctn_info.output_virus_rna_seq_1 = request.POST.get('output_virus_rna_seq_1')
        prdctn_info.trget_seq_rgin_st_lc = request.POST.get('trget_seq_rgin_st_lc')
        prdctn_info.trget_seq_rgin_end_lc = request.POST.get('trget_seq_rgin_end_lc')
        
        view_type = request.POST.get('view_type')
        
        #input_rnq_seq를 조회한다.
        input_virus_info = VirusSeqInfo.objects.filter(virus_cd = prdctn_info.trget_virus, virus_mut_nm = 'WH', domain_nm = prdctn_info.domain_nm)
        input_rna_seq = input_virus_info[0].rna_seq
        
        #output_rnq_seq를 조회한다.
        output_virus_info = VirusSeqInfo.objects.filter(virus_cd = prdctn_info.trget_virus, virus_mut_nm = prdctn_info.virus_mut_nm, domain_nm = prdctn_info.domain_nm)
        output_rna_seq = output_virus_info[0].rna_seq
        
        #result_viewer 기능에서 사용 시 사용자 입력값이 없으므로 DB 값을 사용해서 계산하돠록 수정
        if view_type != 'result_viewer':
            #WH 바이러스 일때는 사용자가 입력한 ouput rna seq 변이를 반영하도록 한다.
            if prdctn_info.virus_mut_nm == 'WH':
                arr_output_rna_seq = prdctn_info.output_virus_rna_seq_1.split(',')
                tmp_rna_seq = ''
                for idx, rna_seq in enumerate(arr_output_rna_seq):
                    if rna_seq != '':
                        tmp_rna_seq += rna_seq
                    else:
                        tmp_rna_seq += output_rna_seq[(idx*3): (idx*3) + 3]
                    
                output_rna_seq = tmp_rna_seq

        pae = request.POST.get('pae')
        plddt = request.POST.get('plddt')
        apess_utils = ApessUtils()
        apess_result = apess_utils.get_apess_result(prdctn_info, input_rna_seq, output_rna_seq, pae, plddt)
        
        apess_json = json.dumps(apess_result)
    else:
        apess_json = {}
        
    return JsonResponse(apess_json, safe=False)

#apes 결과를 조회한다.
def apes_view(request):
    if request.method == 'POST':
        #jsonParam = json.loads(request.body)
        # do something
        input_virus_seq_1 = request.POST.get('input_virus_seq_1')
        nm = int(request.POST.get('nm'))
        score_1 = float(request.POST.get('score_1'))
        score_2_1 = float(request.POST.get('score_2_1'))
        score_2_2 = float(request.POST.get('score_2_2'))
        score_3 = request.POST.get('score_3')
        
        apess_utils = ApessUtils()
        resultInfo = apess_utils.get_apess_result(nm,score_1,score_2_1,score_2_2, score_3)
        return JsonResponse(resultInfo)
        
    context = {}
    return render(request, 'aive/apes_view.html', context)

def aive_about(request):
    context = {}
    return render(request, 'aive/aive_about.html', context)

def aive_tutorial(request):
    context = {}
    return render(request, 'aive/aive_tutorial.html', context)
