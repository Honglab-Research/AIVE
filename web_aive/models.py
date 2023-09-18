from django.db import models
#예측 정보
class PrdctnInfo(models.Model):
    prdctn_info_seq = models.AutoField(primary_key=True)
    trget_virus = models.TextField(default='ALL')
    domain_nm = models.TextField(default='')
    virus_mut_nm = models.TextField(default='')
    prdctn_sj = models.TextField(null=True)
    prdctn_protein_struct = models.CharField(max_length=2)
    trget_seq_rgin_st_lc = models.IntegerField(null=True)
    trget_seq_rgin_end_lc = models.IntegerField(null=True)
    input_virus_seq_1 = models.TextField()
    input_virus_seq_2 = models.TextField(null=True)
    input_virus_seq_3 = models.TextField(null=True)
    input_virus_seq_4 = models.TextField(null=True)
    input_virus_seq_5 = models.TextField(null=True)
    input_virus_seq_6 = models.TextField(null=True)
    input_virus_seq_7 = models.TextField(null=True)
    input_virus_seq_8 = models.TextField(null=True)
    output_virus_seq_1 = models.TextField()
    output_virus_seq_2 = models.TextField(null=True)
    output_virus_seq_3 = models.TextField(null=True)
    output_virus_seq_4 = models.TextField(null=True)
    output_virus_seq_5 = models.TextField(null=True)
    output_virus_seq_6 = models.TextField(null=True)
    output_virus_seq_7 = models.TextField(null=True)
    output_virus_seq_8 = models.TextField(null=True)
    output_virus_rna_seq_1 = models.TextField(null=True)
    prdctn_knd = models.CharField(max_length=1)
    public_yn = models.CharField(max_length=1, default='N')
    regist_dt = models.DateTimeField()
    regist_id = models.TextField()
    del_yn = models.CharField(max_length=1, default='N')
    del_dt = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.prdctn_info_seq

#작업 정보    
class JobInfo(models.Model):
    prdctn_info = models.ForeignKey(PrdctnInfo, on_delete=models.CASCADE)
    job_seq_knd = models.CharField(max_length=3)
    job_prgss_sttus = models.CharField(max_length=1, default='S')
    job_gpu_no = models.IntegerField(default=-1)
    job_cn = models.TextField(null=True)
    job_st_dt = models.DateTimeField(null=True)
    job_end_dt = models.DateTimeField(null=True)
    regist_dt = models.DateTimeField()
    
    def __str__(self):
        return self.job_prgss_sttus
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['prdctn_info_id','job_seq_knd'],
                name='JOB_INFO Unique IDX 1',
            ),
        ]

#알파폴드2 결과    
class Af2Result(models.Model):
    prdctn_info = models.ForeignKey(PrdctnInfo, on_delete=models.CASCADE)
    aa_seq_knd = models.CharField(max_length=4)
    regist_dt = models.DateTimeField()
    
    def __str__(self):
        return self.aa_seq_knd
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['prdctn_info_id','aa_seq_knd'],
                name='AF2_RESULT Unique IDX 1',
            ),
        ]

#Apes결과
class ApesResult(models.Model):
    prdctn_info = models.ForeignKey(PrdctnInfo, on_delete=models.CASCADE)
    apes_result_seq = models.AutoField(primary_key=True)
    ph = models.FloatField() 
    rsdue = models.FloatField()
    regist_dt = models.DateTimeField()
    
    def __str__(self):
        return self.apes_result_seq
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['prdctn_info_id','apes_result_seq'],
                name='APES_RESULT Unique IDX 1',
            ),
        ]

#극성정보
class PolarResult(models.Model):
    prdctn_info = models.ForeignKey(PrdctnInfo, on_delete=models.CASCADE)
    polar_feature_se = models.CharField(max_length=5)
    struct_se = models.CharField(max_length=5)
    polar_cnt = models.IntegerField()
    regist_dt = models.DateTimeField()

    def __str__(self):
        return self.polar_feature_se
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['prdctn_info_id','polar_feature_se','struct_se'],
                name='POLAR_RESULT Unique IDX 1',
            ),
        ]