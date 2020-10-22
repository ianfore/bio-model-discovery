# bio-model-discovery
The aim of this project is to discover the data model of a biological study. The data model reflects the design of the study and is driven by the scientists who create the study. Many systems accommodate this by allowing users to specify the attributes/observations or data elements recorded in the study. It is often not clear which of these attributes are observations and which represent the factors/dimensions of the study.

This work was done as part of the NCI Cancer Data Service and is of more general use to that project in showing how to use the NCBI Entrez APIs to read publically available subject and sample attributes for samples which have genomic data in the CDS.

## BioprojectSampleAttributes.py
Command line utility to retrieve the attributes of the samples for a specified BioProject and summarize the values of those attributes across the project.

The program uses the NCBI Entrez E-utilities

<https://www.ncbi.nlm.nih.gov/books/NBK25497/>

The program should be called using an apikey obtained from your NCBI account settings. See the link for details.


Note that only the first 5000 samples for a project will be retrieved.

### Usage
BioprojectSampleAttributes -k apikey -b bioprojectid

apikey - your personal NCBI API key - see above

If you have an apikey set up it can be checked here <https://www.ncbi.nlm.nih.gov/account/settings/>

bioprojectid - the numeric id of the BioProject to be analyzed e.g. 421626 rather than PRJNA421626.

### Examples
#### Simple three growth-protocol study
The example output for BioProject id 421626 would help a reader identify that the nine samples in the study are organized into three groups according to the "growth protocol" used. There are three replicates in each group. It also identifies that a number of attributes have the same value for all samples. It is likely that these are attributes of the study rather than the sample.

```
Attribute details for BioProject ID: 421626
Accession:PRJNA421626
Title:Mus musculus Transcriptome or Gene expression
No of samples:9
____________________________________
The following attributes vary across samples.
Some may indicate the project design/model.
Some may be sample/subject observations/measurements/data elements.

Attribute:growth_protocol total:9
30¦ÌM ZEA processing 3
Do not add ZEA processing 3
10¦ÌM ZEA processing 3
____________________________________
Attribute:replicate total:9
biological replicate 1 3
biological replicate 2 3
biological replicate 3 3
____________________________________
The following have the same value for all samples.
They are likely to be an attribute of the study rather than the sample
strain:Kunming
age:12 days
dev_stage:not applicable
tissue:Ovarian granulosa cells
sex:female
____________________________________
```
#### Healthy/Diseased, different cell types from same subject
In the case of BioProject 338795 the following report gives a few clues.

```
Attribute details for BioProject ID: 338795
Accession:PRJNA338795
Title:B cell repertoire in myasthenia gravis
No of samples:30
____________________________________
The following attributes vary across samples.
Some may indicate the project design/model.
Some may be sample/subject observations/measurements/data elements.

Attribute:disease_duration_yrs total:30
27 2
<1 6
19 2
2 2
8 6
not applicable 12
____________________________________
Attribute:disease_stage total:30
I 8
IIIa 2
IIIb 4
not applicable 12
IIb 4
____________________________________
Attribute:age total:30
33 6
18 2
31 12
51 8
28 2
____________________________________
Attribute:isolate total:30
MK08 2
HD09 3
MK02 2
MK03 2
MK04 2
MK05 2
HD13 3
HD07 3
AR05 2
AR04 2
HD10 3
AR03 2
AR02 2
____________________________________
Attribute:disease total:30
myasthenia gravis 18
healthy 12
____________________________________
Attribute:sex total:30
male 17
female 13
____________________________________
Attribute:phenotype total:30
MuSK 6
not applicable 22
AchR 2
____________________________________
Attribute:cell_subtype total:30
naive 13
unsorted 4
memory 13
____________________________________
Attribute:thymus_status total:30
No thymoma, No thymectomy 18
not applicable 12
____________________________________
Attribute:treatment total:30
Pred 15 qod 2
None 12
not applicable 12
Pyridostigmine, Pred 20 2
Pyridostigmine, Pred 10, PE 2
____________________________________
The following have the same value for all samples.
They are likely to be an attribute of the study rather than the sample
cell_type:B cell
tissue:Peripheral blood
biomaterial_provider:O'Connor Lab, Yale School of Medicine
____________________________________
```
However it takes some further exploration of the data itself to identify the following structure. see [PRJNA338795.xlsx](https://github.com/ianfore/bio-model-discovery/files/1564065/PRJNA338795.xlsx)

#### dbGaP Study - "Detection of Colorectal Cancer Susceptibility Loci Using Genome-Wide Sequencing"
The dbGaP study id for this project is phs001554. The corresponding Bioproject id is 437032. The following output from BioprojectSampleAttributes.py summarizes the attributes recorded in BioSample for the samples used in this study. Note that only minimal phenotypic data is recorded about each sample. Additional attributes of the samples and subjects are available as controlled access data. For many (most?) dbGaP studies these contolled access attributes are necessary to give proper context to the genomic data held in dbGaP/SRA.

Note: Colloquially this study has been referred to as GECCO. This is actually the name of the consortium that conducted the study [Genetics and Epidemirology of Colorectal Cancer Consortium](https://www.fredhutch.org/en/research/divisions/public-health-sciences-division/research/cancer-prevention/genetics-epidemiology-colorectal-cancer-consortium-gecco.html) . GECCO conducts many studies so phs001554 should probably be referred to by its full title above. "GECCO" has been a convenient shorthand for the study, and will probably continue to be so. Just be aware!

```
____________________________________
Attribute details for BioProject ID: 437032
Accession:PRJNA437032
Title:Detection of Colorectal Cancer Susceptibility Loci Using Genome-Wide Sequencing
No of samples:2892
____________________________________
The following attributes vary across samples.
Some may indicate the project design/model.
Some may be sample/subject observations/measurements/data elements.

Attribute:gap_consent_short_name total:2892
HMB-IRB-NPU 149
HMB-IRB 769
GRU 617
CADM 616
DS-CC-NPU-GSO 741
____________________________________
Attribute:sex total:2892
male 1075
female 1817
____________________________________
Attribute:subject_is_affected total:2892
Yes 1927
No 965
____________________________________
Attribute:gap_consent_code total:2892
1 617
3 149
2 769
5 616
4 741
____________________________________
The following attributes have a unique value for each sample. 
They are therefore likely to some kind of identifier.
submitted_subject_id 2892
biospecimen_repository_sample_id 2892
gap_subject_id 2892
gap_sample_id 2892
submitted_sample_id 2892
____________________________________
The following have the same value for all samples.
They are likely to be an attribute of the study rather than the sample
study_design:Case-Control
molecular_data_type:SNP/CNV Genotypes (NGS)
analyte_type:DNA
study_name:Detection of Colorectal Cancer Susceptibility Loci Using Genome-Wide Sequencing
tissue:Blood
gap_accession:phs001554
biospecimen_repository:NCI_CRC_Susceptibility
is_tumor:No
submitter_handle:NCI_CRC_Susceptibility
____________________________________
The following have only one value in the bioproject
but the attribute is not present for all samples
study_disease:Colorectal Neoplasms 1927
____________________________________
```
