# 学术简报：multimodal retrieval 方向近期进展

生成时间：2026-06-02 00:05
覆盖来源：arxiv, semantic_scholar
时间窗口：近 730 天

---

## 一、最新论文

### 1. [Beyond Classification: Dynamic Adapter Routing for Continual Multimodal Retrieval](https://arxiv.org/abs/2605.31229v1)
**作者：** Alicja Dobrzeniecka, Filip Szatkowski, Sebastian Cygert, Szymon Lukasik, Bartlomiej Twardowski
**发表：** 2026-05-29 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究聚焦于多模态检索场景下的持续学习问题，指出现有工作多沿用类别增量学习（CIL）框架，未能充分捕捉检索任务的动态特性。作者首先构建了一个覆盖多种视觉领域的持续多模态检索（CMR）评估框架，系统对比了常见方法的性能，发现标准CIL方法在此场景下提升有限。核心贡献在于提出动态适配器路由（DAR）方法，通过原型路由选择适配器并结合模型合并技术，在持续检索任务中取得显著性能提升。该方法在分布外评估中展现出强泛化能力，适用于需要不断更新视觉-语言模型以应对新领域检索需求的场景，如动态知识库更新或跨域图像搜索。

### 2. [Uncertainty Quantification for Multimodal Retrieval Augmented Generation](https://arxiv.org/abs/2605.29956v1)
**作者：** Simon Binz, Heydar Soudani, Faegheh Hasibi
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对多模态检索增强生成（RAG）系统中答案可能不准确的问题，提出了一种新的不确定性量化方法。核心方法是通过引入可学习的多模态不确定性量化模型LeMUQ，利用输入修改（如移除模态或检索上下文）下的token概率信号，并编码为概率token进行微调处理。主要贡献在于首次系统性地建模了多模态RAG管道中检索、视觉理解和生成阶段的不确定性，在多个数据集和模型上平均AUROC指标提升3.8%。该方法适用于需要高可靠性答案的多模态问答场景，如医疗影像分析、视觉知识问答等，尤其适合对检索和视觉信息依赖较强的应用。

### 3. [HiKEY: Hierarchical Multimodal Retrieval for Open-Domain Document Question Answering](https://arxiv.org/abs/2605.29606v1)
**作者：** Joongmin Shin, Gyuho Shim, Jeongbae Park, Jaehyung Seo, Heuiseok Lim
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对开放域文档问答中检索增强生成面临的两个瓶颈：文档定位失败和证据碎片化。核心方法提出HiKEY框架，通过文档层次解析构建逻辑异构图，并采用层次化粗到细策略，先全局路由快速剪枝搜索空间，再细粒度检索融合多模态证据。主要贡献在于将文档层级结构作为首要检索信号，并通过混合结构-语义打包策略生成令牌高效的证据子图。实验表明，该方法在检索召回率上提升12.9%，端到端问答性能提升6.8%。适用场景包括大规模工业语料库的开放域问答，尤其需要整合表格、图表等多模态证据的复杂文档检索任务。

### 4. [VeriTrip: A Verifiable Benchmark for Travel Planning Agents over Unstructured Web Corpora](https://arxiv.org/abs/2605.28683v1)
**作者：** Yuting Xu, Jiayi Tian, Jian Liang, Xin Xiong, Hang Zhang, Mu Xu
**发表：** 2026-05-27 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对现有旅行规划基准仅关注API调用、忽略开放网络复杂性的问题，提出了一个名为VeriTrip的可验证基准。核心方法包括构建多模态检索库（MRB）和同步可验证知识库（VKB），通过细胞级验证协议量化事实可靠性，区分系统性推理错误与参数幻觉。主要贡献在于将评估焦点转向基于证据的推理，并揭示了自主检索与指令保留之间的权衡关系。该基准适用于需要处理非结构化多模态网络信息、要求高鲁棒性和可靠性的自主旅行规划代理系统。

### 5. [Gemini Embedding 2: A Native Multimodal Embedding Model from Gemini](https://arxiv.org/abs/2605.27295v1)
**作者：** Madhuri Shanbhogue, Zhe Li, Shanfeng Zhang, Gustavo Hernández Ábrego, Shih-Cheng Huang, Aashi Jain
**发表：** 2026-05-26 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究提出了一种名为Gemini Embedding 2的原生多模态嵌入模型，其核心方法是通过大规模对比学习在多任务、多阶段训练框架下，将视频、音频、图像和文本等模态统一映射到同一表征空间。主要贡献在于该模型在单模态、跨模态及多模态检索基准上均达到领先水平，例如在MSCOCO图像检索中R@1达62.9，在Vatex视频检索中NDCG@10达68.8，并超越了多个领域的专用模型。该模型适用于检索增强生成（RAG）、推荐系统和搜索等下游任务，尤其适合需要处理多种模态混合输入的场景。此外，其强大的零样本泛化能力使其在天文学、生物科学、美术和烹饪等专业领域也能直接作为可靠的表征工具使用。

## 二、最热门论文

### 1. [Beyond Classification: Dynamic Adapter Routing for Continual Multimodal Retrieval](https://arxiv.org/abs/2605.31229v1)
**作者：** Alicja Dobrzeniecka, Filip Szatkowski, Sebastian Cygert, Szymon Lukasik, Bartlomiej Twardowski
**发表：** 2026-05-29 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究聚焦于多模态检索中的持续学习问题，指出现有方法多沿用类别增量学习（CIL）框架，未能充分捕捉检索任务的动态特性。作者首先构建了一个覆盖多种视觉领域的持续多模态检索（CMR）评估框架，并系统验证了标准CIL方法在此场景下效果有限。核心贡献是提出动态适配器路由（DAR）方法，通过基于原型的路由选择适配器，并利用模型合并技术组合多个适配器。实验表明，DAR在持续检索任务中显著优于现有基线，且在分布外场景下展现出强泛化能力。该工作适用于需要持续更新视觉-语言检索模型以应对新领域或新数据分布的实际应用场景。

### 2. [Uncertainty Quantification for Multimodal Retrieval Augmented Generation](https://arxiv.org/abs/2605.29956v1)
**作者：** Simon Binz, Heydar Soudani, Faegheh Hasibi
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对多模态检索增强生成（RAG）系统中答案可能不准确的问题，提出了一种新的不确定性量化（UQ）方法。核心方法是通过引入可学习的多模态UQ模型（LeMUQ），分析输入修改（如移除模态或检索上下文）下的token概率，并将其编码为概率令牌，利用微调模型捕捉模态与检索之间的交互。主要贡献在于首次系统性地建模了多模态RAG管道中检索、视觉理解和生成阶段的不确定性，并在多个数据集、检索器和视觉语言模型上平均提升了AUROC指标3.8%。该方法适用于需要高可靠性输出的多模态问答场景，如医疗影像分析、视觉知识问答等，尤其适合对检索和视觉理解不确定性敏感的复杂任务。

### 3. [HiKEY: Hierarchical Multimodal Retrieval for Open-Domain Document Question Answering](https://arxiv.org/abs/2605.29606v1)
**作者：** Joongmin Shin, Gyuho Shim, Jeongbae Park, Jaehyung Seo, Heuiseok Lim
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对开放域文档问答中检索增强生成面临的两个关键瓶颈：路由失败（难以定位正确文档）和证据碎片化（分散信息难以整合）。核心方法提出HiKEY框架，通过文档层次解析构建逻辑异构图，并采用层次化粗到细策略：先全局路由快速剪枝搜索空间，再细粒度检索利用多模态融合捕获关键证据。主要贡献包括：将文档层级结构作为首要检索信号，设计混合结构-语义打包策略生成token高效的证据子图，在ODQA基准测试中检索召回率提升12.9%，端到端问答性能提升6.8%。该框架适用于大规模工业语料库中需要跨文档、跨模态（如表格、图表）证据整合的复杂问答场景。

### 4. [VeriTrip: A Verifiable Benchmark for Travel Planning Agents over Unstructured Web Corpora](https://arxiv.org/abs/2605.28683v1)
**作者：** Yuting Xu, Jiayi Tian, Jian Liang, Xin Xiong, Hang Zhang, Mu Xu
**发表：** 2026-05-27 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对现有旅行规划基准仅依赖API调用、无法应对开放网络复杂性的问题，提出了名为VeriTrip的可验证基准。核心方法包括构建多模态检索库（MRB）和同步可验证知识库（VKB），通过细胞级验证协议量化事实可靠性，区分系统性推理错误与参数幻觉。主要贡献在于将评估焦点转向基于证据的推理，并揭示了自主检索与指令保持之间的权衡关系。该基准适用于需要处理非结构化多模态网络数据、追求高鲁棒性的旅行规划智能体评估场景。

### 5. [Gemini Embedding 2: A Native Multimodal Embedding Model from Gemini](https://arxiv.org/abs/2605.27295v1)
**作者：** Madhuri Shanbhogue, Zhe Li, Shanfeng Zhang, Gustavo Hernández Ábrego, Shih-Cheng Huang, Aashi Jain
**发表：** 2026-05-26 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究提出了Gemini Embedding 2，一种原生多模态嵌入模型，能够将视频、音频、图像和文本等模态统一映射到同一表示空间。核心方法基于Gemini的多模态能力，通过大规模对比学习与多任务多阶段训练，实现任意模态组合的输入嵌入。主要贡献在于在单模态、跨模态及多模态检索基准上达到最优性能（如MSCOCO的R@1达62.9，Vatex的NDCG@10达68.8），并超越专用模型。该模型适用于检索增强生成（RAG）、推荐系统和搜索等下游任务，其强大的零样本能力使其在天文学、生物科学、艺术等专业领域也能直接作为可靠表示工具。

## 三、最相关论文

### 1. [MM-Embed: Universal Multimodal Retrieval with Multimodal LLMs](https://www.semanticscholar.org/paper/12e3ed574a3433184a267d59e5a08dff6162e5e0)
**作者：** Sheng-Chieh Lin, Chankyu Lee, M. Shoeybi, Jimmy Lin, Bryan Catanzaro, Wei Ping
**发表：** 2024-11-04 | **来源：** semantic_scholar | **引用数：** 131
**会议/期刊：** International Conference on Learning Representations
**相关度：** 0.886
**核心贡献：** 该研究提出了一种名为MM-Embed的通用多模态检索模型，旨在解决现有检索模型在处理文本、图像等多模态数据时缺乏统一框架的问题。核心方法基于多模态大语言模型（MLLMs），通过设计统一的嵌入表示学习机制，使模型能够同时理解并检索跨模态内容。主要贡献在于首次实现了无需任务特定微调的通用多模态检索，显著提升了检索精度与泛化能力。该模型适用于需要跨模态信息匹配的场景，如图文搜索、多模态问答及内容推荐系统。

### 2. [RzenEmbed: Towards Comprehensive Multimodal Retrieval](https://www.semanticscholar.org/paper/19547b20e800026fb73b3c52abecec5cc980b590)
**作者：** Weijian Jian, Yajun Zhang, Dawei Liang, Chunyu Xie, Yixiao He, D. Leng
**发表：** 2025-10-31 | **来源：** semantic_scholar | **引用数：** 13
**会议/期刊：** arXiv.org
**相关度：** 0.882
**核心贡献：** 该研究针对现有多模态检索模型在跨模态对齐和细粒度语义理解上的不足，提出了名为RzenEmbed的综合性多模态检索框架。核心方法是通过联合优化视觉与文本编码器的对比学习目标，并引入跨模态注意力机制以增强特征融合。主要贡献在于设计了一种新的多模态嵌入空间，显著提升了图文匹配、跨模态检索等任务的准确率。该模型适用于电商搜索、社交媒体内容分析等需要高效处理图文混合数据的实际场景。

### 3. [GME: Improving Universal Multimodal Retrieval by Multimodal LLMs](https://www.semanticscholar.org/paper/49e65c03a4f24deaf195b3765e83833412e91edb)
**作者：** Xin Zhang, Yanzhao Zhang, Wen Xie, Mingxin Li, Ziqi Dai, Dingkun Long
**发表：** 2024-12-22 | **来源：** semantic_scholar | **引用数：** 140
**会议/期刊：** arXiv.org
**相关度：** 0.867
**核心贡献：** 该研究旨在解决通用多模态检索中不同模态（如文本、图像）之间语义对齐困难的问题。核心方法是通过多模态大语言模型（MLLMs）构建统一的嵌入表示，提出名为GME的模型，利用MLLMs的跨模态理解能力生成更鲁棒的多模态特征。主要贡献在于显著提升了跨模态检索的准确率，并在多个基准数据集上达到领先性能。该工作适用于需要同时处理文本和图像信息的搜索系统，例如电商产品检索、社交媒体内容匹配等场景。

### 4. [HM-RAG: Hierarchical Multi-Agent Multimodal Retrieval Augmented Generation](https://www.semanticscholar.org/paper/49fb7d86884ff42d1b6fbf6c2eb704399f8a4f65)
**作者：** Pei Liu, Xin Liu, Ruoyu Yao, Junming Liu, Siyuan Meng, Ding Wang
**发表：** 2025-04-13 | **来源：** semantic_scholar | **引用数：** 50
**会议/期刊：** ACM Multimedia
**相关度：** 0.828
**核心贡献：** 该研究提出了一种名为HM-RAG的分层多智能体多模态检索增强生成框架，旨在解决传统RAG系统在处理多模态信息时检索效率低、上下文整合能力弱的问题。核心方法是通过构建分层多智能体架构，将不同模态的检索任务分配给专门的智能体，并利用协同机制实现跨模态信息的动态融合与生成。主要贡献在于显著提升了多模态问答的准确性和响应速度，同时降低了检索噪声对生成结果的影响。该框架适用于需要同时处理文本、图像、表格等多模态数据的复杂问答场景，如医疗诊断辅助、智能客服和学术文献分析等。

### 5. [Unifying Multimodal Retrieval via Document Screenshot Embedding](https://www.semanticscholar.org/paper/28f021fb7de72455788eb3455d0e9ab679cb67e6)
**作者：** Xueguang Ma, Sheng-Chieh Lin, Minghan Li, Wenhu Chen, Jimmy Lin
**发表：** 2024-06-17 | **来源：** semantic_scholar | **引用数：** 115
**会议/期刊：** Conference on Empirical Methods in Natural Language Processing
**相关度：** 0.828
**核心贡献：** 该研究提出了一种统一的多模态检索方法，通过将文档截图作为嵌入表示，来解决传统文本检索难以处理图像、表格等非文本内容的问题。核心方法是将文档页面渲染为截图，并利用视觉语言模型直接对截图进行编码，从而同时捕获文本与视觉信息。主要贡献在于设计了一种端到端的截图嵌入框架，显著提升了跨模态检索的准确性和效率。该方法适用于包含复杂版面、图表或手写内容的文档检索场景，如学术论文、技术手册或历史档案的智能搜索。

## 四、近期研究进展综述

基于近期论文简报，多模态检索领域呈现三大主要趋势：**持续学习与动态适配**、**不确定性量化与可靠性增强**、以及**统一嵌入与层次化检索**。

**主要趋势与代表工作**：首先，持续学习成为热点，如《Beyond Classification》提出动态适配器路由（DAR），通过原型路由和模型合并解决多模态检索中的灾难性遗忘，在分布外场景表现优异。其次，可靠性问题受到关注，《Uncertainty Quantification》提出LeMUQ模型，首次系统建模检索、视觉理解和生成阶段的不确定性，AUROC提升3.8%。此外，统一多模态嵌入模型涌现，如Gemini Embedding 2和MM-Embed，通过对比学习或MLLM实现跨模态统一表征，在MSCOCO等基准上领先。

**技术路线**：主流方法包括：1）基于MLLM的嵌入学习（如GME、MM-Embed），利用大模型跨模态理解能力；2）层次化检索架构（如HiKEY、HM-RAG），通过文档结构解析或多智能体协同提升效率；3）截图嵌入（如Document Screenshot Embedding），直接编码视觉布局信息。

**潜在研究空白**：当前工作多聚焦于静态或单一场景，缺乏对**动态多模态流数据**（如实时视频+语音）的持续检索研究；同时，**跨模态不确定性校准**在开放域、高噪声环境下的鲁棒性仍待探索；此外，**轻量化部署**（如移动端多模态检索）与**隐私保护**（如联邦学习下的多模态检索）也是未充分挖掘的方向。
