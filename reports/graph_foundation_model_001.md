# 学术简报：graph foundation model 方向近期进展

生成时间：2026-06-01 23:41
覆盖来源：arxiv, semantic_scholar
时间窗口：近 730 天

---

## 一、最新论文

### 1. [A Graph Foundation Model for Unified Anomaly Detection](https://www.semanticscholar.org/paper/a82932a62509b68efabd24880f5f349104692e96)
**作者：** Renda Han, Xiaobao Wang, Luzhi Wang, Wenxin Zhang, Guangzhen Yao, Hongxiang Liang
**发表：** 2026-04-12 | **来源：** semantic_scholar | **引用数：** 1
**会议/期刊：** Proceedings of the ACM Web Conference 2026

**核心贡献：** 该研究提出了一种统一的图基础模型，旨在解决不同图结构数据中的异常检测问题。核心方法是通过预训练一个通用的图神经网络，使其能够适应多种异常检测任务，而无需针对每个场景重新训练。主要贡献在于首次尝试构建一个跨领域、跨任务的图异常检测基础模型，显著提升了模型的泛化能力和效率。适用场景包括社交网络欺诈检测、金融交易异常识别、网络安全入侵检测等需要处理复杂图数据的领域。

### 2. [DeXposure-FM: A Time-series, Graph Foundation Model for Credit Exposures and Stability on Decentralized Financial Networks](https://www.semanticscholar.org/paper/064243cfd0db7c01cef36164acbad9fb6809ce5d)
**作者：** Aijie Shu, Wenbin Wu, G. Ibikunle, Fengxiang He
**发表：** 2026-02-03 | **来源：** semantic_scholar | **引用数：** 2
**会议/期刊：** arXiv.org

**核心贡献：** 该研究针对去中心化金融（DeFi）网络中信用暴露与稳定性评估问题，提出了一种名为DeXposure-FM的时序图基础模型。核心方法是将DeFi交易数据建模为动态时序图，并利用图神经网络与时间序列分析技术，学习节点间的信用暴露关系与网络稳定性特征。主要贡献在于首次将基础模型范式引入DeFi信用风险领域，实现了对复杂网络动态风险的端到端预测。该模型适用于DeFi协议的风险监控、借贷平台的信用评估以及去中心化金融系统的稳定性分析等场景。

### 3. [Geometric Structural Knowledge Graph Foundation Model](https://www.semanticscholar.org/paper/75cc38c1d1c64a02dacb56835c4bffb6e7ecb48d)
**作者：** Ling Xin, M. Nayyeri, Zahra Makki Nayeri, Steffen Staab
**发表：** 2025-12-28 | **来源：** semantic_scholar | **引用数：** 0
**会议/期刊：** arXiv.org

**核心贡献：** 该研究提出了一种几何结构知识图谱基础模型，旨在解决传统知识图谱模型在捕捉复杂几何拓扑关系方面的不足。核心方法是通过引入几何结构编码器，将知识图谱中的实体和关系嵌入到非欧几里得空间中，从而更精确地建模层次化与循环结构。主要贡献在于设计了一种统一的基础模型框架，能够同时处理多种几何结构（如双曲、球面空间），并在链接预测、关系推理等任务上显著提升性能。该模型适用于需要处理具有复杂几何拓扑特征的知识图谱场景，例如生物信息网络、社交网络分析及多模态知识推理等。

### 4. [Novae: a graph-based foundation model for spatial transcriptomics data](https://www.semanticscholar.org/paper/96635eda1f59bf68a0b2dca799155c37ea90e441)
**作者：** Quentin Blampey, Hakim Benkirane, N. Bercovici, Kevin Mulder, G. Gessain, Florent Ginhoux
**发表：** 2025-12-01 | **来源：** semantic_scholar | **引用数：** 19
**会议/期刊：** Nature Methods

**核心贡献：** 该研究提出了一种名为Novae的基于图的基础模型，用于处理空间转录组学数据。核心方法是将空间转录组数据建模为图结构，并利用图神经网络进行表征学习，以捕捉基因表达与空间位置之间的复杂关系。主要贡献在于开发了一个统一的预训练框架，能够同时处理多种空间转录组学技术生成的数据，并显著提升下游任务（如细胞类型注释、空间区域识别）的性能。该模型适用于需要整合空间信息和基因表达模式的生物医学研究场景，例如肿瘤微环境分析和组织发育图谱构建。

### 5. [Flock: A Knowledge Graph Foundation Model via Learning on Random Walks](https://www.semanticscholar.org/paper/dd7210edaebda4dc8f4c3ff89aad30d05c244abb)
**作者：** Jinwoo Kim, Xingyue Huang, Krzysztof Olejniczak, Kyung-Min Min, Michael M. Bronstein, Seunghoon Hong
**发表：** 2025-10-01 | **来源：** semantic_scholar | **引用数：** 3
**会议/期刊：** arXiv.org

**核心贡献：** 该研究提出了一种名为Flock的知识图谱基础模型，旨在解决传统知识图谱嵌入方法在泛化性和可扩展性上的局限。其核心方法是通过在知识图谱的随机游走路径上进行学习，从而捕获实体与关系的结构语义，并生成通用的表示。主要贡献在于设计了一种无需任务特定微调即可直接应用于多种知识图谱推理任务的预训练框架。该模型适用于大规模知识图谱的链接预测、关系推理和实体分类等场景，尤其适合需要快速部署且数据稀疏的工业应用。

## 二、最热门论文

### 1. [GFT: Graph Foundation Model with Transferable Tree Vocabulary](https://www.semanticscholar.org/paper/9f6c1c8cd667d886d40bbd2ba9bb0d2e12ec7e5f)
**作者：** Zehong Wang, Zheyuan Zhang, Nitesh V. Chawla, Chuxu Zhang, Yanfang Ye
**发表：** 2024-11-09 | **来源：** semantic_scholar | **引用数：** 75
**会议/期刊：** Neural Information Processing Systems

**核心贡献：** 该研究提出了一种名为GFT的图基础模型，旨在解决图神经网络在跨领域图数据上泛化能力不足的问题。核心方法是通过构建一个可迁移的树状词汇表（Tree Vocabulary），将不同图结构中的子图模式统一编码为共享的语义单元，从而支持模型在多种图任务（如节点分类、图分类）上的迁移学习。主要贡献在于首次将树结构引入图基础模型的词汇设计，显著提升了模型在未见图数据上的零样本和少样本学习性能。该模型适用于需要跨领域、跨任务图分析的场景，例如分子性质预测、社交网络分析和知识图谱推理等。

### 2. [SAMGPT: Text-free Graph Foundation Model for Multi-domain Pre-training and Cross-domain Adaptation](https://www.semanticscholar.org/paper/b0f3a565dd644cdb135d68ec8c1510a08afb4482)
**作者：** Xingtong Yu, Zechuan Gong, Chang Zhou, Yuan Fang, Hui Zhang
**发表：** 2025-02-08 | **来源：** semantic_scholar | **引用数：** 51
**会议/期刊：** The Web Conference

**核心贡献：** 该研究提出了一种名为SAMGPT的文本无关图基础模型，旨在解决多领域图预训练与跨领域自适应问题。其核心方法是通过设计统一的图结构编码器，在不依赖文本信息的情况下学习跨领域的通用图表示。主要贡献在于首次实现了完全脱离文本的图基础模型，并验证了其在多个图数据集上的跨领域迁移能力。该模型适用于缺乏文本标注的图数据场景，如社交网络、分子结构或知识图谱的跨领域分析任务。

### 3. [AnyGraph: Graph Foundation Model in the Wild](https://www.semanticscholar.org/paper/5aa4dc0f24343745175411ca47c8207b41618707)
**作者：** Lianghao Xia, Chao Huang
**发表：** 2024-08-20 | **来源：** semantic_scholar | **引用数：** 51
**会议/期刊：** arXiv.org

**核心贡献：** 该研究提出了一种名为AnyGraph的图基础模型，旨在解决现有图神经网络在面对来自不同领域、具有不同特征和结构的图数据时泛化能力不足的问题。其核心方法是通过构建一个统一的图模型架构，并采用基于元学习的训练策略，使模型能够快速适应未见过的图结构。主要贡献在于首次提出了一个能够处理跨领域、跨任务图数据的通用框架，并在多个基准数据集上验证了其优越的迁移学习性能。该模型适用于需要快速部署图分析能力的场景，例如在缺乏标注数据的电商推荐、社交网络分析或生物分子结构预测等实际应用中。

### 4. [RiemannGFM: Learning a Graph Foundation Model from Riemannian Geometry](https://www.semanticscholar.org/paper/becec5e4a94ec41932753a2bc347e50a01149a14)
**作者：** Li Sun, Zhenhao Huang, Suyang Zhou, Qiqi Wan, Hao Peng, Philip S. Yu
**发表：** 2025-02-05 | **来源：** semantic_scholar | **引用数：** 36
**会议/期刊：** The Web Conference

**核心贡献：** 该研究提出了一种名为RiemannGFM的图基础模型，旨在解决现有图神经网络在非欧几里得结构数据上泛化能力不足的问题。核心方法是将黎曼几何引入图学习框架，通过构建曲率感知的图编码器来捕捉不同几何空间中的复杂拓扑结构。主要贡献在于首次将黎曼几何与图基础模型结合，显著提升了模型在异质图、分子图等非欧数据上的表征能力。该模型适用于需要处理复杂几何结构的场景，如药物分子性质预测、社交网络分析及交通流建模等。

### 5. [A Prompt-Based Knowledge Graph Foundation Model for Universal In-Context Reasoning](https://www.semanticscholar.org/paper/c07151eb48e3923193ac7c50001c5bc240025b5f)
**作者：** Yuanning Cui, Zequn Sun, Wei Hu
**发表：** 2024-10-16 | **来源：** semantic_scholar | **引用数：** 36
**会议/期刊：** Neural Information Processing Systems

**核心贡献：** 该研究提出了一种基于提示的知识图谱基础模型，旨在解决知识图谱推理中缺乏统一框架的问题。核心方法是通过设计可学习的提示模板，将不同推理任务（如链接预测、关系推理）统一转化为上下文学习范式，并利用大规模预训练实现跨任务泛化。主要贡献在于首次将基础模型与提示学习结合用于知识图谱，显著提升了少样本和零样本场景下的推理性能。该模型适用于需要灵活处理多种知识图谱推理任务的场景，例如智能问答、推荐系统和常识推理等。

## 三、最相关论文

### 1. [Graph foundation model](https://www.semanticscholar.org/paper/ce1e38e116b4d950132b1a1033168d84ffb259e4)
**作者：** Chuan Shi, Junze Chen, Jiawei Liu, Cheng Yang
**发表：** 2024-07-05 | **来源：** semantic_scholar | **引用数：** 13
**会议/期刊：** Frontiers of Computer Science
**相关度：** 1.000
**核心贡献：** 该研究探讨了图基础模型（Graph Foundation Model）的构建问题，旨在通过大规模预训练实现图数据的通用表示学习。核心方法包括设计统一的图神经网络架构，结合自监督学习与多任务训练范式，以捕捉节点、边及子图的通用特征。主要贡献在于提出了一个可迁移的图基础模型框架，显著提升了跨领域图任务（如分子性质预测、社交网络分析）的泛化能力。该模型适用于需要图结构理解但标注数据稀缺的场景，例如药物发现、推荐系统及知识图谱推理。

### 2. [Relation-Aware Graph Foundation Model](https://www.semanticscholar.org/paper/e4177554097f2af69ce43b0676628e23ede35d15)
**作者：** Jianxiang Yu, Jiapeng Zhu, Hao Qian, Ziqi Liu, Zhiqiang Zhang, Xiang Li
**发表：** 2025-05-17 | **来源：** semantic_scholar | **引用数：** 1
**会议/期刊：** arXiv.org
**相关度：** 0.969
**核心贡献：** 该研究提出了一种关系感知的图基础模型，旨在解决现有图神经网络在处理复杂关系结构时泛化能力不足的问题。核心方法是通过设计一种新型的图编码器，显式建模节点间的多种关系类型，并利用预训练策略增强模型对关系模式的捕获能力。主要贡献在于提出了一种统一的关系感知框架，能够有效提升图结构数据的表示学习效果，并在多个基准数据集上取得了优于现有方法的性能。该模型适用于社交网络分析、知识图谱推理、生物分子结构预测等需要精细关系建模的场景。

### 3. [Geometric Structural Knowledge Graph Foundation Model](https://www.semanticscholar.org/paper/75cc38c1d1c64a02dacb56835c4bffb6e7ecb48d)
**作者：** Ling Xin, M. Nayyeri, Zahra Makki Nayeri, Steffen Staab
**发表：** 2025-12-28 | **来源：** semantic_scholar | **引用数：** 0
**会议/期刊：** arXiv.org
**相关度：** 0.916
**核心贡献：** 该研究提出了一种几何结构知识图谱基础模型，旨在解决传统知识图谱模型在捕捉复杂几何关系（如对称性、层次结构）方面的不足。核心方法是通过引入几何变换（如旋转、反射）和流形学习，将实体和关系嵌入到非欧几里得空间中，从而更自然地建模结构化知识。主要贡献在于设计了一种统一框架，能够同时处理多种几何结构（如双曲、球面空间），并在链接预测、关系推理等任务上显著提升性能。该模型适用于需要精确表达几何约束的领域，如分子结构预测、3D场景理解或空间关系推理。

### 4. [AnyGraph: Graph Foundation Model in the Wild](https://www.semanticscholar.org/paper/5aa4dc0f24343745175411ca47c8207b41618707)
**作者：** Lianghao Xia, Chao Huang
**发表：** 2024-08-20 | **来源：** semantic_scholar | **引用数：** 51
**会议/期刊：** arXiv.org
**相关度：** 0.893
**核心贡献：** 该研究提出了一种名为AnyGraph的图基础模型，旨在解决现有图神经网络在跨领域、跨结构图数据上泛化能力不足的问题。其核心方法包括构建统一的图表示框架，并采用自监督预训练策略，使模型能够适应不同规模和类型的图结构。主要贡献在于首次实现了对多种图数据（如社交网络、分子图、知识图谱）的通用建模，并验证了其在零样本和少样本场景下的有效性。该模型适用于需要快速适配新图结构或缺乏标注数据的实际应用，例如推荐系统、药物发现和异常检测等。

### 5. [GraphPFN: A Prior-Data Fitted Graph Foundation Model](https://www.semanticscholar.org/paper/0461a4cd6d5fd75305fe67d65a67e244f4e8ec0a)
**作者：** Dmitry Eremeev, Oleg Platonov, Gleb Bazhenov, Artem Babenko, Liudmila Prokhorenkova
**发表：** 2025-09-25 | **来源：** semantic_scholar | **引用数：** 7
**会议/期刊：** arXiv.org
**相关度：** 0.893
**核心贡献：** 该研究提出了一种名为GraphPFN的图基础模型，旨在解决图数据中缺乏统一预训练范式的问题。核心方法是通过先验数据拟合（Prior-Data Fitting）技术，利用合成图数据训练一个通用的Transformer架构，使其能够直接适应多种下游图任务。主要贡献在于无需针对特定任务进行微调，即可在节点分类、图分类和链接预测等任务上取得与专用模型相当的性能。该模型适用于数据稀缺或需要快速部署图分析能力的场景，例如小样本学习或跨领域图任务迁移。

## 四、近期研究进展综述

基于近期论文简报，图基础模型（Graph Foundation Model, GFM）方向呈现以下主要趋势、代表工作、技术路线及潜在研究空白：

**主要趋势**：GFM正从通用图表示学习向跨领域、跨任务、多模态及几何结构感知方向演进。核心目标是构建统一的预训练框架，以提升模型在未见图数据上的泛化能力和零样本/少样本学习性能。

**代表工作与技术路线**：
1.  **统一架构与预训练**：如`AnyGraph`、`Graph foundation model`等，采用统一的图神经网络（GNN）或Transformer架构，结合自监督学习（如掩码建模、对比学习）进行大规模预训练。
2.  **几何与结构感知**：`RiemannGFM`引入黎曼几何，`Geometric Structural Knowledge Graph Foundation Model`利用双曲/球面空间，以捕捉非欧几里得拓扑结构。
3.  **任务与领域适配**：`A Prompt-Based Knowledge Graph Foundation Model`通过提示学习统一推理任务；`SAMGPT`实现文本无关的跨领域迁移；`GFT`构建可迁移的树状词汇表。
4.  **特定领域应用**：`DeXposure-FM`针对DeFi时序图，`Novae`处理空间转录组学，`A Graph Foundation Model for Unified Anomaly Detection`聚焦异常检测。

**潜在研究空白**：
1.  **动态与演化图**：多数模型侧重静态图，对时序动态图（如DeFi网络、社交网络演化）的通用建模能力不足。
2.  **可解释性与因果推理**：当前GFM多为黑盒，缺乏对图结构决策的因果解释机制。
3.  **多模态融合**：图与文本、图像等模态的深度融合（如知识图谱与多模态数据）尚待探索。
4.  **大规模工业部署**：模型在超大规模图上的训练效率、推理延迟及资源消耗优化仍是挑战。
