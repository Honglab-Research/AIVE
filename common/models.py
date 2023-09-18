from django.db import models

#공통코드
class CommCode(models.Model):
    cl_code = models.CharField(max_length=5)
    cl_code_nm = models.TextField()
    code = models.CharField(max_length=3)
    code_nm = models.TextField()
    code_dc = models.TextField(null=True)
    use_yn = models.CharField(max_length=1, default='Y')
    regist_id = models.TextField()
    regist_dt = models.DateTimeField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cl_code','code'],
                name='COMM_CODE Unique',
            ),
        ]
    
    def __str__(self):
        return self.code_nm
    
#바이러스 시퀀스 정보
class VirusSeqInfo(models.Model):
    virus_cd = models.CharField(max_length=3)
    uniprot_rec = models.TextField()
    domain_nm = models.TextField()
    domain_dc = models.TextField()
    virus_mut_nm = models.TextField(default='')
    seq_rgin_st_lc = models.IntegerField()
    seq_rgin_end_lc = models.IntegerField()
    genomic_st_lc = models.IntegerField(null=True)
    genomic_end_lc = models.IntegerField(null=True)
    aa_seq = models.TextField()
    rna_seq = models.TextField(null=True)
    regist_id = models.TextField()
    regist_dt = models.DateTimeField()
    del_yn = models.CharField(max_length=1, default='N')
    del_dt = models.DateTimeField(null=True)
    
    class Meta:
        def __str__(self):
            return self.linge_nm
    