# 学术简报：graph foundation model 方向近期进展

生成时间：2026-06-08 22:15
覆盖来源：dblp:WWW
时间窗口：近 1095 天

---

## 一、最新论文

### 1. [Towards Graph Foundation Model: Node Feature Transfer Invariant Modeling on General Graphs.](https://doi.org/10.1145/3774904.3792236)
**作者：** Jitao Zhao, Yi Wang, Yawen Li 0001, Dongxiao He, Di Jin 0001, Zhiyong Feng 0002
**发表：** 2026-01-01 | **来源：** dblp | **引用数：** 0
**会议/期刊：** WWW

**核心贡献：** 该研究旨在解决通用图数据上节点特征分布差异导致的图基础模型泛化能力不足的问题。核心方法提出了一种节点特征迁移不变建模框架，通过设计特征对齐与结构保持机制，使模型在不同图结构间学习到鲁棒的节点表示。主要贡献在于首次将迁移不变性引入图基础模型构建，显著提升了跨图节点分类与链接预测任务的性能。该工作适用于需要统一图模型处理多源异构图数据的场景，如社交网络分析、生物分子图预测等。

### 2. [GraphCLIP: Enhancing Transferability in Graph Foundation Models for Text-Attributed Graphs.](https://doi.org/10.1145/3696410.3714801)
**作者：** Yun Zhu 0007, Haizhou Shi, Xiaotang Wang, Yongchao Liu 0004, Yaoke Wang, Boci Peng
**发表：** 2025-01-01 | **来源：** dblp | **引用数：** 0
**会议/期刊：** WWW

**核心贡献：** 该研究聚焦于文本属性图（TAGs）中图基础模型的迁移能力提升问题。核心方法提出GraphCLIP框架，通过对比学习对齐图结构与文本语义，并设计跨领域知识蒸馏策略增强模型泛化性。主要贡献在于首次系统性地解决了图基础模型在跨领域TAGs任务中的迁移瓶颈，显著提升了零样本和少样本场景下的性能。适用场景包括社交网络分析、知识图谱推理及推荐系统等需要处理文本与图结构混合数据的实际应用。

## 二、最热门论文

### 1. [Towards Graph Foundation Model: Node Feature Transfer Invariant Modeling on General Graphs.](https://doi.org/10.1145/3774904.3792236)
**作者：** Jitao Zhao, Yi Wang, Yawen Li 0001, Dongxiao He, Di Jin 0001, Zhiyong Feng 0002
**发表：** 2026-01-01 | **来源：** dblp | **引用数：** 0
**会议/期刊：** WWW

**核心贡献：** 该研究旨在解决通用图数据上节点特征分布不一致的问题，以推动图基础模型的构建。核心方法提出了一种节点特征迁移不变建模框架，通过设计特征对齐与图结构约束机制，使模型在不同图域间保持稳定的表征能力。主要贡献在于首次在通用图场景下实现了跨图节点特征的迁移不变性，并验证了其有效性。该工作适用于需要图模型具备跨领域泛化能力的场景，如社交网络分析、分子性质预测及推荐系统等。

### 2. [GraphCLIP: Enhancing Transferability in Graph Foundation Models for Text-Attributed Graphs.](https://doi.org/10.1145/3696410.3714801)
**作者：** Yun Zhu 0007, Haizhou Shi, Xiaotang Wang, Yongchao Liu 0004, Yaoke Wang, Boci Peng
**发表：** 2025-01-01 | **来源：** dblp | **引用数：** 0
**会议/期刊：** WWW

**核心贡献：** 该研究聚焦于提升文本属性图（TAGs）中图基础模型的迁移能力。核心方法是通过引入对比学习框架GraphCLIP，将图结构与文本语义进行对齐，从而学习跨领域通用的图表示。主要贡献在于提出了一种无需微调即可直接迁移至多种下游任务的图基础模型，显著提升了零样本和少样本场景下的性能。该模型适用于需要处理文本与图结构混合数据的场景，如社交网络分析、知识图谱推理及推荐系统等。

## 三、最相关论文

### 1. [Towards Graph Foundation Model: Node Feature Transfer Invariant Modeling on General Graphs.](https://doi.org/10.1145/3774904.3792236)
**作者：** Jitao Zhao, Yi Wang, Yawen Li 0001, Dongxiao He, Di Jin 0001, Zhiyong Feng 0002
**发表：** 2026-01-01 | **来源：** dblp | **引用数：** 0
**会议/期刊：** WWW
**相关度：** 0.805
**核心贡献：** 该研究聚焦于构建通用图基础模型时面临的核心挑战——如何在不同图结构间实现节点特征的有效迁移。作者提出了一种节点特征迁移不变性建模方法，通过设计特征对齐与结构适配的联合学习框架，使模型能够捕捉跨图共享的语义模式。主要贡献在于首次从不变性角度系统解决了图数据分布偏移问题，并验证了该方法在节点分类、链接预测等任务上的泛化能力。该工作适用于需要跨领域、跨图结构进行知识迁移的场景，如社交网络分析、生物分子图建模及推荐系统等。

### 2. [GraphCLIP: Enhancing Transferability in Graph Foundation Models for Text-Attributed Graphs.](https://doi.org/10.1145/3696410.3714801)
**作者：** Yun Zhu 0007, Haizhou Shi, Xiaotang Wang, Yongchao Liu 0004, Yaoke Wang, Boci Peng
**发表：** 2025-01-01 | **来源：** dblp | **引用数：** 0
**会议/期刊：** WWW
**相关度：** 0.760
**核心贡献：** 该研究聚焦于文本属性图（Text-Attributed Graphs）中图基础模型的迁移能力提升问题。核心方法是通过对比学习框架GraphCLIP，将图结构与文本语义进行联合对齐，从而增强模型在不同图任务间的泛化性能。主要贡献在于提出了一种无需微调即可迁移的图基础模型，显著提升了跨领域、跨任务的零样本学习效果。该模型适用于需要利用文本信息进行图分析的应用场景，如社交网络分析、知识图谱推理和推荐系统等。

## 四、近期研究进展综述

基于近期论文简报，图基础模型（Graph Foundation Model, GFM）的研究正从单一图结构建模向跨领域、多模态泛化方向演进，主要趋势聚焦于解决数据分布差异与迁移能力瓶颈。

**主要趋势与代表工作**：当前两大核心挑战为**跨图节点特征分布差异**与**文本-图结构语义对齐**。代表工作包括：1）《Towards Graph Foundation Model》提出节点特征迁移不变建模框架，通过特征对齐与结构保持机制，首次将迁移不变性引入GFM，显著提升跨图节点分类与链接预测性能；2）《GraphCLIP》针对文本属性图（TAGs），采用对比学习对齐图结构与文本语义，并设计跨领域知识蒸馏策略，系统性解决跨领域迁移瓶颈，在零样本/少样本场景表现优异。

**技术路线**：主流方法采用**对比学习**（如GraphCLIP）与**特征对齐**（如迁移不变建模）相结合，辅以**结构保持**与**知识蒸馏**，以增强模型对异构数据（多源图、文本-图混合）的鲁棒性。

**潜在研究空白**：当前工作多聚焦于节点级任务，对**图级任务**（如图分类、图生成）的迁移性研究不足；此外，**动态图**与**大规模异构时序图**上的基础模型构建尚属空白，且缺乏统一的评估基准来衡量跨领域泛化能力。未来可探索**多模态融合**与**自监督预训练**在更复杂图结构上的泛化机制。
