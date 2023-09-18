from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse

from common.models import VirusSeqInfo, CommCode
from common.froms import UserForm

import requests, json

def signup(request):
    """회원가입 화면으로 이동하고 회원가입 한다.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password) #사용자 인증
            login(request, user) #로그인
            return redirect('/')
    else:
        form = UserForm()
    
    return render(request, 'common/signup.html', {'form':form})

def get_domain_seq_info(request):
    """도메인 정보를 조회한다.

    Args:
        request (_type_): _description_

    Returns:
        json: 
    """

    domain_nm = request.GET.get('domain_nm')
    virus_mut_nm = request.GET.get('virus_mut_nm')

    lineage_aa_info = VirusSeqInfo.objects.filter(domain_nm = domain_nm, virus_mut_nm = virus_mut_nm).values('aa_seq', 'seq_rgin_st_lc', 'seq_rgin_end_lc', 'rna_seq')
    
    wuhan_aa_info = VirusSeqInfo.objects.filter(domain_nm = domain_nm, virus_mut_nm = 'WH').values('aa_seq', 'seq_rgin_st_lc', 'seq_rgin_end_lc', 'rna_seq')
    
    return JsonResponse(
        {
        'lineage_aa_info' : lineage_aa_info[0],
        'wuhan_aa_info' : wuhan_aa_info[0],
        }
    )
            
    
def get_comm_code_list(request):
    """공통코드 목록을 조회한다.

    Args:
        request (_type_): _description_

    Returns:
        json: 공통코드 목록
    """
    cl_code = request.GET.get('cl_code')
    
    code_list = CommCode.objects.filter(cl_code = cl_code, use_yn = 'Y').values('code', 'code_nm', 'code_dc')
    
    return JsonResponse({'code_list' : list(code_list)})


def get_comm_post_request(request):
    dic_param = {}
    url = 'https://www.ncbi.nlm.nih.gov/Structure/mmcifparser/mmcifparser.cgi'
    if request.method == "POST":
        for p_name in request.POST:
            dic_param[p_name] = request.POST.get(p_name)

        res = requests.post(url, data=dic_param, verify=False)        

        return JsonResponse({'result':res.text})

def sitemap(request):
    context = {}
    return render(request, 'common/sitemap.html', context)
