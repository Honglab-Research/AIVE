import os

class AiveUtils:
    WLD = 'WLD'
    MUT = 'MUT'
    WHST = 'WHST'
    MHST = "MHST"
    
    #Polarity feature	Polarity feature_S	Amino acid
    DIC_POLAR_FEATURE = {
        'A' : 'N',
        'V' : 'N',
        'L' : 'N',
        'G' : 'N',
        'I' : 'N',
        'M' : 'N',
        'W' : 'N',
        'F' : 'N',
        'P' : 'N',
        'S' : 'P',
        'C' : 'P',
        'N' : 'P',
        'Q' : 'P',
        'T' : 'P',
        'Y' : 'P',
        'D' : 'A',
        'E' : 'A',
        'K' : 'B',
        'R' : 'B',
        'H' : 'B',
    }

    #Five amino acid properties 
    DIC_FIVE_AA = {'K' : 'E','R' : 'E','H' : 'E','D' : 'O','E' : 'O','S' : 'P','N' : 'P','Q' : 'P','T' : 'P','C' : 'S','G' : 'S','P' : 'S','A' : 'H','V' : 'H','L' : 'H','I' : 'H','M' : 'H','W' : 'H','F' : 'H', 'Y' : 'H',};
    # DIC_FIVE_AA = {
    #     'K' : '1',
    #     'R' : '1',
    #     'H' : '1',
    #     'D' : '2',
    #     'E' : '2',
    #     'S' : '3',
    #     'N' : '3',
    #     'Q' : '3',
    #     'T' : '3',
    #     'C' : '4',
    #     'G' : '4',
    #     'P' : '4',
    #     'A' : '5',
    #     'V' : '5',
    #     'L' : '5',
    #     'I' : '5',
    #     'M' : '5',
    #     'W' : '5',
    #     'F' : '5', 
    #     'Y' : '5',
    # }
    
    #파일을 생성한다.
    def file_create(self, path, file_name):
        """
            입력된 경로에 파일이름으로 파일을 생한다.

        Args:
            path (str): 파일이 생성될 경로
            file_name (str): 생성할 파일명
        """
        #디렉토리가 없으면 생성하도록 한다.
        if not os.path.isdir(path):
            os.makedirs(path)
    
    #polarity feature 분류를 조회한다.
    def get_protein_polarity_feature(self, feature_type, input_aa_seq):
        """
            feature 구분에 따라 입력된 AA Seq의 극성구조별 건수를 조회한다.

        Args:
            feature_type (str): polar_feature, five_aa
            input_aa_seq (str): 조회할 AA Seq

        Returns:
            _type_: _description_
        """
        dic_result = {
            'P-P-X' : 0,
            'N-N-X' : 0,
            'ETC' : 0,
        }
        
        list_polar_aa_seq = list(input_aa_seq)
        
        if (feature_type == 'polar_feature'):
            #AA를 기준에 맞게 변환한다.
            for i in range(0, len(input_aa_seq)-1):
                list_polar_aa_seq[i] = self.DIC_POLAR_FEATURE[input_aa_seq[i]]
                #polararity seq가  A, B인 경우는 X로 사용한다.
                list_polar_aa_seq[i] = 'X' if list_polar_aa_seq[i] == 'A' or list_polar_aa_seq[i] == 'B' else list_polar_aa_seq[i]
                    
        else:
            #AA를 기준에 맞게 변환한다.
            for i in range(0, len(input_aa_seq)-1):
                list_polar_aa_seq[i] = self.DIC_FIVE_AA[input_aa_seq[i]]
                #polararity seq가  P나 N이 아닌 경우는 X로 사용한다.
                list_polar_aa_seq[i] = 'X' if list_polar_aa_seq[i] != 'P' or list_polar_aa_seq[i] != 'N' else list_polar_aa_seq[i]
                
        polar_aa_seq = ''.join(list_polar_aa_seq)
        
        #변환된 정보를 이용하여 polararity feature정보를 조회한다.
        for i in range(0, len(polar_aa_seq)- 1):
            #뒤에서 3번째 자리까지만 확인한다.
            if i < len(polar_aa_seq) - 2:
                tmp_aa_polar = polar_aa_seq[i:i+3]
                if 'PPX' == tmp_aa_polar:
                    dic_result['P-P-X'] += 1
                elif 'NNX' == tmp_aa_polar:
                    dic_result['N-N-X'] += 1
                else:
                    dic_result['ETC'] += 1
                
        return dic_result
