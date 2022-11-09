# Dataset Release for CoSpot (SoCC'22)


## Introduction

This dataset and accompanying code are supplemental to our paper:
> Syed M. Iqbal, Haley Li, Shane Bergsma, Ivan Beschastnikh, Alan J. Hu. "[**CoSpot: A Cooperative VM Allocation Framework for Increased Revenue from Spot Instances**](https://dl.acm.org/doi/10.1145/3542929.3563499)", in Proceedings of the 13th ACM Symposium on Cloud Computing (SoCC 2022), November 2022.

We used these datasets to evaluate our VM/spot allocation framework, but release them as we hope they are useful for
others. (However, we make no warranties about this data for any purpose, as noted in our [license](#license).)
You should refer to the paper for additional details.

The workloads in this dataset are derived from the [VM/spot request dataset](https://github.com/Azure/AzurePublicDataset/blob/master/AzureTracesForPacking2020.md) published by Microsoft Azure and Microsoft Research as part of the [Protean paper published at OSDI 2020][protean-paper-url].  We are extremely grateful to them.

The difficulty in their dataset that we address here is that the original dataset does not have concrete resource
requirements, i.e., it doesn't specify how many cores, RAM, SSD, etc., that each VM type requires.  Instead, it contains
only data on the _fractional usage_ of each resource type for some, specific VM/server combinations. This makes it difficult
to reuse the dataset as a workload for _different_ algorithms on _different_ datacenters.

The VM/spot requests in our workloads have consistent concrete resource requirements associated with them. This consistent resource requirement information was derived by casting the fractional resource consumption information from the original dataset as an
integer linear program (ILP).  The directly generated ILP was infeasible (i.e., had no possible solution) because some data in the original dataset were inconsistent.  With a bit of ILP hacking, we were able to identify and eliminate inconsistencies and
generate concrete resource values that are consistent with the published workload.  (Note that we do **not** claim that
these are the actual numbers behind the original dataset, as our ILP will happily generate a solution in which all
the numbers are scaled by arbitrary constants.  E.g., Is RAM specified in gigabytes, or megabytes, or perhaps even in individual bytes?
However, the concrete resource amounts would work the exact same way in a scheduler as the real amounts would have, because
they are all scaled by the same amount.)
The ILP we used can be found in [reconstruct_cores_ram.py](ilp/reconstruct_cores_ram.py), and
the solution to the ILP that we used to construct our workloads in the paper can be found in [server_vm_cores_ram.json](ilp/server_vm_cores_ram.json).

The actual workloads that we used in our experiments are in the [workloads](workloads) directory.
The file [relevant-vm.zip](workloads/relevant-vm.zip) is the entire trace with the derived resource amounts added in.
The two subdirectories show specific trace that we used in our experiments, which were randomly sampled from the full trace.

## Using the Data

### License
The data is made available and licensed under a [CC-BY Attribution License](https://github.com/DCResourceManage/cospot-socc2022/blob/master/LICENSE). By downloading it or using them, you agree to the terms of this license.

### Attribution
If you use our dataset (contained in the [workloads](workloads/) directory), please cite the accompanying paper:

> Syed M. Iqbal, Haley Li, Shane Bergsma, Ivan Beschastnikh, Alan J. Hu. "[**CoSpot: A Cooperative VM Allocation Framework for Increased Revenue from Spot Instances**](https://dl.acm.org/doi/10.1145/3542929.3563499)", in Proceedings of the 13th ACM Symposium on Cloud Computing (SoCC 2022), November 2022.

Also, given that our dataset is derived from the Protean dataset, you should cite the Protean paper, too, if you use our dataset:

> Ori Hadary, Luke Marshall, Ishai Menache, Abhisek Pan, David Dion, Esaias Greeff, Star Dorminey, Shailesh Joshi, Yang Chen, Mark Russinovich and Thomas Moscibroda. "[**Protean: VM Allocation Service at Scale**](https://www.microsoft.com/en-us/research/publication/protean-vm-allocation-service-at-scale/)", in Proceedings of the 14th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2020). USENIX Association, November 2020.

**NOTE:** [vmType.csv](ilp/vmType.csv) is identical to the `vmType` SQLite table from the Protean workload. You **must** cite the Protean paper if you use this CSV file in your own work. This file was included to illustrate the format our ILP script expects in case you would like to perform your own consistent concrete resource requirement reconstruction.

Lastly, if you have any questions, comments, or concerns, or if you would like to share tools for working with the traces, please contact Syed M. Iqbal at syedmubashiriqbal@gmail.com


## Schema and Description

The schema is identical to the original Protean schema. A description of that schema can be found [here](https://github.com/Azure/AzurePublicDataset/blob/master/AzureTracesForPacking2020.md#schema-and-description)

The VM/spot requests in our traces contain additional `core`/`ram` fields that capture concrete requirements for their corresponding VM flavors based on the optimal solution returned for our ILP.

[cospot-paper-url]: https://dl.acm.org/doi/10.1145/3542929.3563499
[protean-paper-url]: https://github.com/Azure/AzurePublicDataset/blob/master/AzureTracesForPacking2020.md#schema-and-description
