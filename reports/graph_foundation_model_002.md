# 学术简报：graph foundation model 方向近期进展

生成时间：2026-06-01 23:54
覆盖来源：arxiv, semantic_scholar
时间窗口：近 1095 天

---

## 一、最新论文

### 1. [GraphARC: A Comprehensive Benchmark for Graph-Based Abstract Reasoning](https://arxiv.org/abs/2605.31031v1)
**作者：** Saku Peltonen, August Bøgh Rønberg, Andreas Plesner, Roger Wattenhofer
**发表：** 2026-05-29 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究提出了一个名为GraphARC的图结构抽象推理基准，旨在解决现有基准局限于网格或文本格式的问题。核心方法是将抽象与推理语料库（ARC）的少样本变换学习范式推广到图数据，要求模型从少量输入-输出对中推断变换规则并应用于新测试图。主要贡献包括：支持大规模生成多样图族和尺寸的实例，系统评估泛化能力；揭示了当前语言模型在图属性问答上表现良好但难以完成完整图变换任务的“理解-执行差距”；以及性能随实例规模增大而下降的扩展障碍。该基准适用于评估和推动图基础模型在节点分类、链接预测和图生成等综合任务上的抽象推理能力。

### 2. [When Do Graph Foundation Models Transfer? A Data-Centric Theory](https://arxiv.org/abs/2605.29828v1)
**作者：** Jiajun Zhu, Ying Chen, Peihao Wang, Yixuan He, Pan Li, Aditya Akella
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 这篇论文研究了图基础模型（GFMs）在不同图领域间迁移时表现不均甚至出现负迁移的问题。核心方法是从数据中心视角出发，利用基于图极限（graphon）的连续极限理论，对固定表征模型在跨域输出上的变化进行显式分解。主要贡献在于将输出偏移分解为图特定的有限样本近似项和反映结构不匹配的、与重标号无关的固有域差异，并建立了位置编码（PE）的稳定性理论。该研究适用于指导图基础模型迁移中的数据筛选与领域适配，帮助识别哪些图对更适合共享模型。

### 3. [Boosting Knowledge Graph Foundation Models via Enhanced Negative Sampling](https://arxiv.org/abs/2605.27023v1)
**作者：** Yinan Liu, Wenjin Xu, Zhiyuan Zha, Xiaochun Yang, Bin Wang
**发表：** 2026-05-26 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究聚焦于知识图谱基础模型（KGFMs）在零样本知识图谱补全任务中因随机负采样导致训练监督信号弱的问题。核心方法提出了一种自适应负采样方法KMAS，通过利用KGFM关系编码器生成的更新关系嵌入来构造困难负三元组，并动态调整困难负样本比例（预热后线性增减）。主要贡献在于无需显著增加时间或内存消耗即可提升多种现有KGFMs的性能，在44个数据集上验证了有效性。适用场景包括跨不同关系词汇表的未知知识图谱补全，以及问答系统、推荐系统等依赖知识图谱的下游任务。

### 4. [Scalable Heterogeneous Graph Foundation Models for Data-Driven Optimal Power Flow in Smart Grids](https://arxiv.org/abs/2605.23194v1)
**作者：** Massimiliano Lupo Pasini, Yijiang Li, Kibaek Kim, Teja Kuruganti
**发表：** 2026-05-22 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对现有学习型最优潮流（OPF）代理模型忽略电网异构结构、拓扑适应性有限及缺乏可扩展图基础模型（GFM）训练基础设施的问题，提出了一种基于HydraGNN的可扩展异构图神经网络（GNN）工作流。核心方法通过保留电网中母线、发电机、负荷、交流线路、变压器等不同节点与边类型，并支持分布式预处理、超参数优化（HPO）及下游微调，在ORNL Frontier超级计算机上利用DeepHyper对300万个异构图实例（涵盖14至13,659个母线的10个PGLib-OPF案例）进行HPO，识别出约160-170万参数的紧凑模型。主要贡献包括：首次在超算规模上实现异构图基础模型的端到端训练，并验证了预训练OPF-GFM在可行性分类和N-1故障回归等下游任务中，通过部分或仅头部微调可提升低数据精度、稳定训练、加速收敛并降低适配成本。该工作适用于需要快速、可靠且适应多种电网拓扑的智能电网实时运行场景，尤其适合在超算环境下进行大规模模型预训练与部署。

### 5. [Deep Neural Sheaf Diffusion](https://arxiv.org/abs/2605.19021v2)
**作者：** Rémi Bourgerie, Šarūnas Girdzijauskas, Viktoria Fodor
**发表：** 2026-05-18 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对深层图神经网络（GNN）中因重复聚合导致的表示坍塌和灵敏度下降问题，提出了一种名为“深度神经层扩散”（DNSD）的方法。核心创新在于用层邻接算子替代层拉普拉斯算子，并结合归一化、奇非线性函数和门控机制，以维持深层网络中的信息信号。主要贡献包括：理论层面揭示了层扩散在深层失效的机制，并对比了层扩散与图注意力机制的区别；实验层面在合成长程数据集上实现了高达30个百分点的准确率提升，并在真实基准上持续优于现有GNN和层扩散基线。该方法适用于需要深层图网络处理长程依赖的任务，如图结构数据的分类与回归，为构建图基础模型提供了有效的深层架构支持。

## 二、最热门论文

### 1. [GraphARC: A Comprehensive Benchmark for Graph-Based Abstract Reasoning](https://arxiv.org/abs/2605.31031v1)
**作者：** Saku Peltonen, August Bøgh Rønberg, Andreas Plesner, Roger Wattenhofer
**发表：** 2026-05-29 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究提出了一个名为GraphARC的基准测试，专门用于评估图结构数据上的抽象推理能力。其核心方法是将抽象与推理语料库（ARC）中的少样本变换学习范式推广到图领域，要求模型从少量输入-输出图对中推断变换规则并应用于新测试图。主要贡献在于，GraphARC能够大规模生成涵盖局部、全局和层次化图变换的多样化任务，从而系统评估模型的泛化能力。实验发现，当前最先进的语言模型在回答图属性问题时表现尚可，但在完整图变换任务上存在明显的“理解-执行差距”，且性能随图规模增大而下降。该基准适用于评估和推动未来图基础模型在节点分类、链接预测和图生成等综合任务上的发展。

### 2. [When Do Graph Foundation Models Transfer? A Data-Centric Theory](https://arxiv.org/abs/2605.29828v1)
**作者：** Jiajun Zhu, Ying Chen, Peihao Wang, Yixuan He, Pan Li, Aditya Akella
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究聚焦于图基础模型（GFMs）在不同图域间迁移时表现不均甚至出现负迁移的问题，从数据中心视角提出核心问题：两个图域的哪些属性决定了固定表征模型输出变化的大小？方法上，作者利用基于图论的连续极限（graphon）对稠密图进行建模，证明对于基于集合和消息传递的两种标记化方式，任何Lipschitz骨干网络的跨域输出偏移可分解为（i）图特定的有限样本近似误差和（ii）反映结构不匹配的、与重标号无关的固有域差异。主要贡献包括：建立位置编码（PE）稳定性理论，揭示基于特征向量与基于子空间的PE在迁移中的不同行为，并通过合成与真实图实验验证了该分解的有效性。该工作适用于指导GFM迁移中的数据筛选与域适配策略设计，尤其适用于需要评估不同图数据集间迁移可行性的场景。

### 3. [Boosting Knowledge Graph Foundation Models via Enhanced Negative Sampling](https://arxiv.org/abs/2605.27023v1)
**作者：** Yinan Liu, Wenjin Xu, Zhiyuan Zha, Xiaochun Yang, Bin Wang
**发表：** 2026-05-26 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对知识图谱基础模型（KGFMs）在零样本补全任务中因随机负采样导致训练监督信号弱的问题，提出了一种自适应负采样方法KMAS。核心方法是通过KGFM的关系编码器生成更新后的关系嵌入，构造高质量硬负三元组，并在训练过程中动态调整硬负三元组的比例（先线性增加后线性减少）。主要贡献在于无需显著增加时间和内存消耗，即可显著提升多种现有KGFMs在44个数据集上的性能。该方法适用于需要跨不同关系词汇表进行零样本知识图谱补全的场景，如问答系统和推荐系统中的缺失链接预测。

### 4. [GFT: Graph Foundation Model with Transferable Tree Vocabulary](https://www.semanticscholar.org/paper/9f6c1c8cd667d886d40bbd2ba9bb0d2e12ec7e5f)
**作者：** Zehong Wang, Zheyuan Zhang, Nitesh V. Chawla, Chuxu Zhang, Yanfang Ye
**发表：** 2024-11-09 | **来源：** semantic_scholar | **引用数：** 75
**会议/期刊：** Neural Information Processing Systems

**核心贡献：** 该研究提出了一种名为GFT（Graph Foundation Model with Transferable Tree Vocabulary）的图基础模型，旨在解决传统图神经网络在跨领域图数据上泛化能力不足的问题。核心方法是通过构建可迁移的树状词汇表（Tree Vocabulary），将不同图结构中的子图模式统一编码为可共享的语义单元，从而支持模型在多种图任务间进行知识迁移。主要贡献在于首次将树结构词汇引入图基础模型，显著提升了模型在节点分类、图分类等任务上的零样本与少样本学习能力。该模型适用于需要跨领域图数据泛化的场景，如分子性质预测、社交网络分析及知识图谱推理等。

### 5. [Scalable Heterogeneous Graph Foundation Models for Data-Driven Optimal Power Flow in Smart Grids](https://arxiv.org/abs/2605.23194v1)
**作者：** Massimiliano Lupo Pasini, Yijiang Li, Kibaek Kim, Teja Kuruganti
**发表：** 2026-05-22 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究旨在解决现有学习型最优潮流（OPF）代理模型忽略电网异构结构、拓扑适应性有限以及缺乏可扩展图基础模型（GFM）训练基础设施的问题。核心方法基于HydraGNN构建了一个可扩展的异构图神经网络（GNN）工作流，保留了电力网络中不同节点和边的类型（如母线、发电机、变压器等），并支持分布式预处理、训练、超参数优化（HPO）及下游微调。主要贡献包括：在ORNL Frontier超级计算机上利用300万个异构图实例进行HPO，识别出约160-170万参数的紧凑模型；通过预训练OPF-GFM的微调，在可行性分类和N-1事故回归任务中提升了低数据精度、稳定了训练并降低了适应成本。该工作适用于大规模智能电网的实时OPF近似、拓扑变化下的快速决策以及数据稀缺场景下的模型迁移。

## 三、最相关论文

### 1. [Graph foundation model](https://www.semanticscholar.org/paper/ce1e38e116b4d950132b1a1033168d84ffb259e4)
**作者：** Chuan Shi, Junze Chen, Jiawei Liu, Cheng Yang
**发表：** 2024-07-05 | **来源：** semantic_scholar | **引用数：** 13
**会议/期刊：** Frontiers of Computer Science
**相关度：** 1.000
**核心贡献：** 该研究探讨了图基础模型（Graph Foundation Model）的构建问题，旨在解决传统图神经网络在跨领域泛化能力上的不足。核心方法是通过大规模预训练与统一图表示学习框架，使模型能够捕捉不同图结构中的通用模式。主要贡献在于提出了一个可迁移的图基础模型架构，显著提升了在节点分类、链接预测等任务上的零样本与少样本学习性能。该模型适用于社交网络分析、生物分子图预测、推荐系统等需要处理多样化图数据的场景。

### 2. [Relation-Aware Graph Foundation Model](https://www.semanticscholar.org/paper/e4177554097f2af69ce43b0676628e23ede35d15)
**作者：** Jianxiang Yu, Jiapeng Zhu, Hao Qian, Ziqi Liu, Zhiqiang Zhang, Xiang Li
**发表：** 2025-05-17 | **来源：** semantic_scholar | **引用数：** 1
**会议/期刊：** arXiv.org
**相关度：** 0.969
**核心贡献：** 该研究提出了一种**关系感知的图基础模型**，旨在解决现有图神经网络在处理复杂关系结构时泛化能力不足的问题。核心方法是通过设计**关系感知的编码机制**，使模型能够显式捕捉节点间不同类型或强度的关系，并基于大规模图数据进行预训练。主要贡献在于提出了一种统一的关系建模框架，显著提升了模型在多种图任务（如节点分类、链接预测）上的迁移学习能力。该模型适用于**社交网络分析、知识图谱推理**等需要精细刻画实体间多样关系的场景。

### 3. [Geometric Structural Knowledge Graph Foundation Model](https://www.semanticscholar.org/paper/75cc38c1d1c64a02dacb56835c4bffb6e7ecb48d)
**作者：** Ling Xin, M. Nayyeri, Zahra Makki Nayeri, Steffen Staab
**发表：** 2025-12-28 | **来源：** semantic_scholar | **引用数：** 0
**会议/期刊：** arXiv.org
**相关度：** 0.916
**核心贡献：** 该研究提出了一种几何结构知识图谱基础模型，旨在解决传统知识图谱模型难以捕捉复杂几何拓扑关系的问题。核心方法是将图神经网络与几何深度学习相结合，通过嵌入空间中的几何变换来建模实体间的结构依赖。主要贡献在于设计了一种统一框架，能够同时处理对称性、层次性和非欧几里得关系，显著提升了知识推理的准确性。该模型适用于生物信息学、分子结构分析以及社交网络等需要精细几何结构建模的场景。

### 4. [AnyGraph: Graph Foundation Model in the Wild](https://www.semanticscholar.org/paper/5aa4dc0f24343745175411ca47c8207b41618707)
**作者：** Lianghao Xia, Chao Huang
**发表：** 2024-08-20 | **来源：** semantic_scholar | **引用数：** 51
**会议/期刊：** arXiv.org
**相关度：** 0.893
**核心贡献：** 该研究提出了一种名为AnyGraph的图基础模型，旨在解决现有图神经网络在跨领域、跨结构图数据上的泛化能力不足问题。其核心方法是通过构建统一的图表示学习框架，结合自监督预训练与多任务适配机制，使模型能够适应不同规模和类型的图结构。主要贡献在于首次实现了对多种图数据（如社交网络、分子图、知识图谱）的通用建模，并显著提升了零样本迁移性能。该模型适用于需要快速部署图分析能力的场景，例如推荐系统、药物发现和异常检测等跨领域图任务。

### 5. [GraphPFN: A Prior-Data Fitted Graph Foundation Model](https://www.semanticscholar.org/paper/0461a4cd6d5fd75305fe67d65a67e244f4e8ec0a)
**作者：** Dmitry Eremeev, Oleg Platonov, Gleb Bazhenov, Artem Babenko, Liudmila Prokhorenkova
**发表：** 2025-09-25 | **来源：** semantic_scholar | **引用数：** 7
**会议/期刊：** arXiv.org
**相关度：** 0.893
**核心贡献：** 该研究提出了一种名为GraphPFN的图基础模型，旨在解决传统图神经网络需要针对不同任务重新训练的问题。核心方法是通过在大量图结构数据上拟合先验分布，使模型能够直接进行少样本或零样本预测。主要贡献在于构建了一个通用的图学习框架，无需微调即可处理节点分类、图分类等下游任务。该模型适用于数据标注成本高或需要快速部署图分析能力的场景，如分子性质预测或社交网络分析。

## 四、近期研究进展综述

基于近期论文简报，图基础模型（GFM）研究呈现以下主要趋势与进展：

**主要趋势**：研究正从单一任务模型向跨领域、可迁移的通用图模型演进，核心挑战包括抽象推理、跨域迁移、深层架构稳定性及异构数据处理。

**代表工作与技术路线**：
1. **抽象推理与基准**：GraphARC将抽象推理范式推广至图数据，揭示语言模型存在“理解-执行差距”，为评估GFM综合推理能力提供基准。
2. **迁移学习理论**：基于图极限理论，将输出偏移分解为有限样本误差与结构域差异，指导数据筛选与领域适配。
3. **知识图谱增强**：KMAS通过自适应负采样（利用关系编码器构造困难负三元组）提升零样本补全性能。
4. **异构与大规模**：基于HydraGNN的异构图工作流，在超算上预训练OPF-GFM，支持下游微调，验证了大规模异构GFM的可行性。
5. **深层架构**：深度神经层扩散（DNSD）通过层邻接算子与门控机制，解决深层GNN表示坍塌问题，提升长程依赖处理能力。
6. **可迁移词汇**：GFT引入树状词汇表统一编码子图模式，实现跨域零样本/少样本迁移；AnyGraph与GraphPFN分别通过统一框架与先验分布拟合实现通用建模。

**潜在研究空白**：
- **理论统一**：缺乏统一的GFM泛化边界理论，现有迁移理论多针对特定模型。
- **动态与时空图**：多数工作聚焦静态图，对动态、时序图的基础模型研究不足。
- **可解释性与鲁棒性**：GFM的决策过程与对抗鲁棒性分析尚属空白。
- **大规模预训练数据**：缺乏高质量、多领域、标准化的图预训练语料库。
- **计算效率**：深层架构与异构模型在资源受限场景下的轻量化部署方案亟待探索。
