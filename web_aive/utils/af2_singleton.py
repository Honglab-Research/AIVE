import string
import subprocess
from django.utils import timezone
from django.conf import settings
from web_aive.models import JobInfo, PrdctnInfo

class Af2Singleton(object):
    _aive_dir = settings.AIVE_DIR[settings.AIVE_ENV]
    #환경에 따라 명령어를 변경한다.
    if (settings.AIVE_ENV == 'REAL' or settings.AIVE_ENV == 'jenon-MAC'):
        _proc0 = subprocess.Popen(['ls',], shell=True, stdout=subprocess.PIPE)
        _proc1 = subprocess.Popen(['ls',], shell=True, stdout=subprocess.PIPE)
        _proc2 = subprocess.Popen(['ls',], shell=True, stdout=subprocess.PIPE)
    else:
        _proc0 = subprocess.Popen(['dir',], shell=True, stdout=subprocess.PIPE)
        _proc1 = subprocess.Popen(['dir',], shell=True, stdout=subprocess.PIPE)
        _proc2 = subprocess.Popen(['dir',], shell=True, stdout=subprocess.PIPE)
        
    _proc0.wait()
    _proc1.wait()
    _proc2.wait()
    _job_info0 = {
                    'prdctn_info_id' : 0,
                    'job_seq_knd' : 'none'
                 }
    
    _job_info1 = {
                    'prdctn_info_id' : 0,
                    'job_seq_knd' : 'none'
                 }
    
    _job_info2 = {
                    'prdctn_info_id' : 0,
                    'job_seq_knd' : 'none'
                 }
    
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(Af2Singleton, cls).__new__(cls)
        #else:
        #    print('recycle')
        return cls.instance
    
    def get_global_gpu_var(cls, var_kind:str, gpu_no:int):
        """
            var_kind의 종류에 따랄 gpu_no에 맞는 객체를 넘긴다.

        Args:
            var_kind (string): proc : subprocess 객체, job_info: 작업중인 정보
            gpu_no (int): gpu 번호

        Returns:
            object: var_kind에 따라 다름
        """
        if (var_kind == 'proc'):
            return cls._proc0 if gpu_no == 0 else cls._proc1 if gpu_no == 1 else cls._proc2
        elif (var_kind == 'job_info'):
            return cls._job_info0 if gpu_no == 0 else cls._job_info1 if gpu_no == 1 else cls._job_info2 
    
    def set_global_gpu_proc(cls, job_proc:str, gpu_no:int):
        """
            var_kind의 종류에 따랄 gpu_no에 맞는 객체를 넘긴다.

        Args:
            job_proc (subprocess.Popen): subprocess 객체
            gpu_no (int): gpu 번호
        """
        if (gpu_no == 0 ):
            cls._proc0 = job_proc
        elif(gpu_no == 1):
            cls._proc1 = job_proc
        elif(gpu_no == 2):
            cls._proc2 = job_proc
    
    #현재 선택된 GPU 작업이 완료되었는지 확인한다.
    def is_gpu_job_fin(cls, gpu_no):
        """
            gpu의 작업 종료 여부를 확인한다.

        Args:
            gpu_no (int): 확인할 gpu번호

        Returns:
            bool : True : 작업 완료, False : 사용 중
        """
        tmp_result = False
        tmp_proc = cls.get_global_gpu_var('proc', gpu_no)
        
        if (type(tmp_proc) == subprocess.Popen):
            tmp_result = True if tmp_proc.poll() == 0 else False
            
        return tmp_result
    
    #선택한 GPU 작업을 시작한다.
    def start_gpu_job(cls, gpu_no, job_file_name):
        """gpu에 알파폴드2 작업을 할당한다.

        Args:
            gpu_no (int): 할당할 gpu번호
            fasta_full_path (string): 작업할 스크립트 전체 경로
        """
        job_proc = cls.get_global_gpu_var('proc', gpu_no) 
        if (settings.AIVE_ENV == 'REAL' or settings.AIVE_ENV == 'jenon-MAC'):
            job_proc = subprocess.Popen([cls._aive_dir[1] + 'device{}.sh'.format(gpu_no),job_file_name])
        else:
            job_proc = subprocess.Popen([cls._aive_dir[1] + 'device{}.bat'.format(gpu_no),job_file_name])
            
        cls.set_global_gpu_proc(job_proc, gpu_no)
        print(job_proc.poll())
        
    #실제 작업할 fasta파일을 생성한다.
    def create_job_fasta_file(cls, gpu_no, prdctn_info, job_info):
        """예측정보, 작업 정보를 이용하여 실제 gpu에서 작업할 수 있도록 fasta 파일을 만든다.
            virus : prdctn_info.input_virus_seq_1
            mutated : prdctn_info.output_virus_seq_1
            host : prdctn_info.input_virus_seq_2
        Args:
            gpu_no (_type_): 사용될 gpu 번호 
            prdctn_info (_type_): 예측 정보
            job_info (_type_): 작업 정보
        """
        #작업정보에 따른 AA Seq를 조회하고 fasta파일을 만든다.
        fasta_full_path = cls._aive_dir[0] + '{}_{}_{}.fasta'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd, prdctn_info.prdctn_protein_struct)
        with open(fasta_full_path,'w') as f:    
            f.write('>{}_{}\n'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd))
            f.write('{}'.format(prdctn_info.output_virus_seq_1))
            
            if (prdctn_info.output_virus_seq_2 != ''):
                f.write('\n>{}_{}\n'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd))
                f.write('{}'.format(prdctn_info.output_virus_seq_2))
            
            if (prdctn_info.output_virus_seq_3 != ''):
                f.write('\n>{}_{}\n'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd))
                f.write('{}'.format(prdctn_info.output_virus_seq_3))
                
            if (prdctn_info.output_virus_seq_4 != ''):
                f.write('\n>{}_{}\n'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd))
                f.write('{}'.format(prdctn_info.output_virus_seq_4))
                
            if (prdctn_info.output_virus_seq_5 != ''):
                f.write('\n>{}_{}\n'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd))
                f.write('{}'.format(prdctn_info.output_virus_seq_5))
                
            if (prdctn_info.output_virus_seq_6 != ''):
                f.write('\n>{}_{}\n'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd))
                f.write('{}'.format(prdctn_info.output_virus_seq_6))
                
            if (prdctn_info.output_virus_seq_7 != ''):
                f.write('\n>{}_{}\n'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd))
                f.write('{}'.format(prdctn_info.output_virus_seq_7))
                
            if (prdctn_info.output_virus_seq_8 != ''):
                f.write('\n>{}_{}\n'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd))
                f.write('{}'.format(prdctn_info.output_virus_seq_8))
        
        #만들어진 fasta파일으로 작업을 돌린다.
        cls.start_gpu_job(gpu_no, '{}_{}_{}'.format(prdctn_info.prdctn_info_seq, job_info.job_seq_knd, prdctn_info.prdctn_protein_struct))     
    
    #가용 GPU를 확인하고 작업 이력에 정보를 등록한다.
    def start_job(cls):
        """가용 gpu를 확인하고 사용가능하면 등록된 작업큐에서 작업정보를 조회하여 작업을 실행한다.
        """
        for gpu_no in range(0,3):
        
            #GPU가 사용되고 있는지 데이터에서 먼저 확인한다.
            result = JobInfo.objects.filter(job_prgss_sttus = 'S', job_gpu_no = gpu_no).values('job_gpu_no').distinct()

            if (len(result) == 0):
                #실제 해당 프로세스가 작업중인지 한번더 확인한다.
                if (cls.is_gpu_job_fin(gpu_no)):
                    #GPU가 사용 가능하면 현재 등록되어 있는 JOB_INFO에서 처음에 등록된 JOB을 작업한다.
                    now_job_info = JobInfo.objects.filter(job_prgss_sttus = 'S').order_by('prdctn_info_id', 'id')
                    
                    #작업할 내용이 있으면 작업을 돌리도록 한다.
                    if (len(now_job_info) > 0):
                        #작업상태 변경
                        now_job_info[0].job_prgss_sttus = 'P'
                        now_job_info[0].job_gpu_no = gpu_no
                        now_job_info[0].job_st_dt = timezone.now()
                        now_job_info[0].save()
                        
                        #작업정보를 전역 변수에 저장한다.
                        tmp_job_info = cls.get_global_gpu_var('job_info', gpu_no)
                        
                        tmp_job_info['prdctn_info_id'] = now_job_info[0].prdctn_info_id
                        tmp_job_info['job_seq_knd'] = now_job_info[0].job_seq_knd
                        
                        #해당 gpu에 작업을 할당한다.
                        cls.create_job_fasta_file(gpu_no, now_job_info[0].prdctn_info, now_job_info[0])
     
    #1분에 한번씩 작업이 끝났는지 확인 후 끝났다면 종료 처리후 새로운 작업을 실행한다.                
    def prdctn_job_check(cls):
        """작업이 종료되었는지 확인 후 종려되었다면 새로운 작업을 실행한다.
        """
        #종료된 작업이 있는지 검사하고 있다면 종료 처리
        for gpu_no in range(0,3):
            if (cls.is_gpu_job_fin(gpu_no)):
                tmp_job_info = cls.get_global_gpu_var('job_info', gpu_no)
                #작업이 진행된 내용이 있다면 진행중인 작업의 상태를 변경한다.
                if tmp_job_info['prdctn_info_id'] > 0:
                    fin_prdctn_info = PrdctnInfo.objects.filter(prdctn_info_seq = tmp_job_info['prdctn_info_id'])
                    
                    #job_info = JobInfo(prdctn_info = now_prdctn_info, job_seq_knd = tmp_job_info['job_seq_knd'])
                    fin_job_info = JobInfo.objects.get(prdctn_info = fin_prdctn_info[0], job_seq_knd = tmp_job_info['job_seq_knd'])
                    fin_job_info.job_prgss_sttus = 'C'
                    fin_job_info.job_end_dt = timezone.now()
                    fin_job_info.save()
                
                #전역변수 초기화
                tmp_job_info['prdctn_info_id'] = 0
                tmp_job_info['job_seq_knd'] = 'none'
        
        #새로운 작업을 시작한다.                
        cls.start_job()
