from cProfile import label
from dataclasses import field, fields
from email.policy import default
from random import choices
from django import forms
from .models import PrdctnInfo
from common.models import CommCode

class PrdctnForm(forms.ModelForm):
    #대상 바이러스
    virus_list = CommCode.objects.filter(cl_code='TV')
    trget_virus = forms.ChoiceField(label='Target virus',
                                   choices=[(commCdoe.code, commCdoe.code_nm) for commCdoe in CommCode.objects.filter(cl_code='TV')])
    
    #변종 바이러스
    #comm_code_list = CommCode.objects.filter(cl_code='PPS')
    #option tag를 직접 생성함 value값은 순처번호(1,2,3....)
    #prdctn_strct_list = forms.ModelChoiceField(queryset=CommCode.objects.filter(cl_code='PPS'))
    #prdctn_protein_struct = forms.ChoiceField(label='Prediction protein structure', 
#                                              choices=[(commCode.code, commCode.code_nm) for commCode in CommCode.objects.filter(cl_code='PPS')])
    
    input_virus_seq_1 = forms.CharField(label='Input virus Sequence')
    output_virus_seq_1 = forms.CharField(label='Output virus Sequence')
    
    class Meta:
        model = PrdctnInfo
        fields = ['prdctn_protein_struct',
                  'input_virus_seq_1','input_virus_seq_2','input_virus_seq_3','input_virus_seq_4','input_virus_seq_5','input_virus_seq_6','input_virus_seq_7','input_virus_seq_8',
                  'output_virus_seq_1','output_virus_seq_2','output_virus_seq_3','output_virus_seq_4','output_virus_seq_5','output_virus_seq_6','output_virus_seq_7','output_virus_seq_8', 
                  'output_virus_rna_seq_1', 'prdctn_sj', 'trget_seq_rgin_st_lc', 'trget_seq_rgin_end_lc', 'trget_virus', 'domain_nm', 'virus_mut_nm','public_yn',
                  ]
        
    def __init__(self, *args, **kwargs):
        super(PrdctnForm, self).__init__(*args, **kwargs)
        
        self.fields['prdctn_protein_struct'].required = False
        self.fields['trget_seq_rgin_st_lc'].required = False
        self.fields['trget_seq_rgin_end_lc'].required = False
        self.fields['input_virus_seq_2'].required = False
        self.fields['input_virus_seq_3'].required = False
        self.fields['input_virus_seq_4'].required = False
        self.fields['input_virus_seq_5'].required = False
        self.fields['input_virus_seq_6'].required = False
        self.fields['input_virus_seq_6'].required = False
        self.fields['input_virus_seq_7'].required = False
        self.fields['input_virus_seq_8'].required = False
        
        self.fields['output_virus_seq_2'].required = False
        self.fields['output_virus_seq_3'].required = False
        self.fields['output_virus_seq_4'].required = False
        self.fields['output_virus_seq_5'].required = False
        self.fields['output_virus_seq_6'].required = False
        self.fields['output_virus_seq_7'].required = False
        self.fields['output_virus_seq_8'].required = False
        self.fields['output_virus_rna_seq_1'].required = False
        self.fields['public_yn'].required = False