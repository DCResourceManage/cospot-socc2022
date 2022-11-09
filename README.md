# Dataset Release for CoSpot (SoCC'22)


## Introduction
The workloads in this dataset are based on the [VM/spot request dataset](https://github.com/Azure/AzurePublicDataset/blob/master/AzureTracesForPacking2020.md) published by Microsoft Azure and Microsoft Research as part of the Protean paper published at OSDI 2020.

The VM/spot requests in our workloads have consistent concrete resource requirements associated with them. This consistent resource requirement information was extracted by casting the fractional resource consumption information from the original dataset as an ILP.

The optimal solution to the ILP that we used to construct our workloads can be found in [server_vm_cores_ram.json](ilp/server_vm_cores_ram.json), and the ILP itself can be found in [reconstruct_cores_ram.py](ilp/reconstruct_cores_ram.py).


## Using the Data

### License
The data is made available and licensed under a [CC-BY Attribution License](https://github.com/DCResourceManage/cospot-socc2022/blob/master/LICENSE). By downloading it or using them, you agree to the terms of this license.

### Attribution
If you use our dataset (contained in the [workloads](workloads/) directory), please cite the accompanying paper:

> Syed M. Iqbal, Haley Li, Shane Bergsma, Ivan Beschastnikh, Alan J. Hu. "[**CoSpot: A Cooperative VM Allocation Framework for Increased Revenue from Spot Instances**](https://dl.acm.org/doi/10.1145/3542929.3563499)", in Proceedings of the 13th ACM Symposium on Cloud Computing (SoCC 2022), November 2022.

We would also strongly encourage you to cite the Protean paper if you use our dataset:

> Ori Hadary, Luke Marshall, Ishai Menache, Abhisek Pan, David Dion, Esaias Greeff, Star Dorminey, Shailesh Joshi, Yang Chen, Mark Russinovich and Thomas Moscibroda. "[**Protean: VM Allocation Service at Scale**](https://www.microsoft.com/en-us/research/publication/protean-vm-allocation-service-at-scale/)", in Proceedings of the 14th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2020). USENIX Association, November 2020.

**NOTE:** [vmType.csv](ilp/vmType.csv) is identical to the `vmType` SQLite table from the Protean workload. Please cite the Protean paper if you use this CSV file in your own work. This file was included to illustrate the format our ILP script expects in case you would like to perform your own consistent concrete resource requirement reconstruction.

Lastly, if you have any questions, comments, or concerns, or if you would like to share tools for working with the traces, please contact Syed M. Iqbal at syedmubashiriqbal@gmail.com


## Schema and Description

The schema is identical to the original Protean schema. A description of that schema can be found [here](https://github.com/Azure/AzurePublicDataset/blob/master/AzureTracesForPacking2020.md#schema-and-description)

The VM/spot requests in our traces contain additional `core`/`ram` fields that capture concrete requirements for their corresponding VM flavors based on the optimal solution returned for our ILP.
