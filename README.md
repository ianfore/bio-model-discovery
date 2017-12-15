# bio-model-discovery
The aim of this project is to discover the data model of a biological study. The data model reflects the design of the study and is driven by the scientists who create the study. Many systems accommodate this by allowing users to specify the attributes/observations or data elements recorded in the study. It is often not clear which of these attributes are observations and which represent the factors/dimensions of the study.

## BioprojectSampleAttributes.py
Command line utility to retrieve the attributes of the samples for a specified BioProject and summarize the values of those attributes across the project.

The program uses the NCBI Entrez E-utilities

<https://www.ncbi.nlm.nih.gov/books/NBK25497/>

The program should be called using an apikey obtained from your NCBI account settings. See the link for details.


Note that only the first 5000 samples for a project will be retrieved.

### Usage
BioprojectSampleAttributes -k apikey -b bioprojectid

### Example
The example output for BioProject id 421626 would help a reader identify that the nine samples in the study are organized into three groups according to the "growth protocol" used. There are three replicates in each group. It also identifies that a number of attributes have the same value for all samples. It is likely that these are attributes of the study rather than the sample.

```
____________________________________
Attribute details for BioProject ID: 421626
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
```


