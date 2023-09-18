AIVE
===============

Artificial Intelligence analytics toolkit for predicting Virus mutation in protEin (AIVE) is a Web and GPU based analysis tool that can predict protein structures and properties from user-entered viral sequences. AIVE uses AlphaFold2 software (https://github.com/deepmind/alphafold) to evaluate protein structures. AIVE provides independently developed mathematical models (SCPS, PS, MR, BPES, APESS). It provides information on structural differences (SCPS, PS), physical changes (MR), and biochemical changes (BPES) at the amino acid and nucleotide levels. These tools were calculated using various information such as amino acid chemical properties (RH, Hydrophobic, Residue), molecular structure prediction results (PAE, pLDDT), mutation and codon frequencies in viruses, and amino acid polarity features. AIVE serves optimized analysis and prediction for SARS-CoV-2 viral mutations. Analysis and prediction of other virus species will be updated later.

<img src="http://ai-ve.org/static/img/main/img_aive.png" alt="AIVE"/>

#### The information and analysis tools we provide are the following:
##### A. Protein structure prediction from viral sequences using learning models
* Prediction of folding and docking from viral mutations
* Comparison of folding and docking scores

##### B. Polarity changes in protein sequences
* Measurement of repeated polarity changes

##### C. Mathematical models based on amino acid and nucleotide levels (MR & BPES)
* Scoring of rate of change for nucleotide levels
* Scoring of rate of change for amino acid properties (Residue, Hydrophobic, and PH)

##### D. Comprehensive mathematical analysis model(APESS)
* Integrating results for protein structure prediction, polarity change, and nucleotide and amino acid properties levels

#### Sitemap
##### Home: 
Shows summary and introduces AIVE (http://ai-ve.org/)
##### Prediction-local: 
Submit Amino Acid sequence that the user wants to predict. Protein prediction uses AlphaFold2 (http://ai-ve.org/prdctn_regist_server)
##### Prediction-colab: 
Submit Amino Acid sequence that the user wants to predict. Protein prediction uses AlphaFold Colab (http://ai-ve.org/prdctn_regist_colab)
##### Report-list: 
Provides the submitted job list, status, and result report page link (http://ai-ve.org/prdctn_list)
##### Report-result viewer: 
Receives results file (http://ai-ve.org/aive_result_viewer)
##### about: 
Displays the citation, license, and browser compatibility of programs (http://ai-ve.org/aive_about)
##### tutorial: 
Provides tutorial of AIVE (http://ai-ve.org/aive_tutorial)
##### Template program: 
Provide a prominent link to the template program (https://github.com/honglab-AIVE/AIVE_github)
##### Required library
python > 3.9 django==4.0.3 django-apschedluer django-dubug-toolbar pandas seaborn openpyxl scikit-learn requests