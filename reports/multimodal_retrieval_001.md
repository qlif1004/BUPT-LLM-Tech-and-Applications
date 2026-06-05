# 学术简报：multimodal retrieval 方向近期进展

生成时间：2026-06-01 23:57
覆盖来源：arxiv, semantic_scholar
时间窗口：近 7 天

---

## 一、最新论文

### 1. [Beyond Classification: Dynamic Adapter Routing for Continual Multimodal Retrieval](https://arxiv.org/abs/2605.31229v1)
**作者：** Alicja Dobrzeniecka, Filip Szatkowski, Sebastian Cygert, Szymon Lukasik, Bartlomiej Twardowski
**发表：** 2026-05-29 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该论文聚焦于多模态检索任务中的持续学习问题，指出现有研究多沿用类别增量学习（CIL）框架，未能充分捕捉检索场景的动态特性。作者提出了一个面向持续多模态检索（CMR）的评估框架，涵盖多种视觉领域，并系统评估了常见方法，发现标准CIL方法在此场景下效果有限。核心贡献在于提出动态适配器路由（DAR）方法，通过基于原型的路由选择适配器，并结合模型合并技术，显著提升了检索性能。该方法在分布外评估中展现出强泛化能力，适用于需要持续更新视觉-语言模型以应对新领域检索需求的场景，如动态知识库更新或跨域图像搜索。

### 2. [Uncertainty Quantification for Multimodal Retrieval Augmented Generation](https://arxiv.org/abs/2605.29956v1)
**作者：** Simon Binz, Heydar Soudani, Faegheh Hasibi
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究聚焦于多模态检索增强生成（RAG）系统中的不确定性量化问题，旨在提升模型输出可靠性。核心方法提出了一种名为LeMUQ的可学习多模态不确定性量化方法，通过分析输入修改（如移除模态或检索上下文）下的token概率，并利用微调模型编码这些概率信号来捕捉模态与检索间的交互。主要贡献在于首次系统性地建模了多模态RAG管道中检索、视觉理解和生成阶段的不确定性，在多个数据集和模型上平均AUROC指标提升3.8%，并展现出良好的跨检索设置泛化能力。该方法适用于需要高可靠性的多模态问答场景，如医疗影像分析、自动驾驶视觉问答等对错误容忍度极低的应用领域。

### 3. [HiKEY: Hierarchical Multimodal Retrieval for Open-Domain Document Question Answering](https://arxiv.org/abs/2605.29606v1)
**作者：** Joongmin Shin, Gyuho Shim, Jeongbae Park, Jaehyung Seo, Heuiseok Lim
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对开放域文档问答中检索增强生成（RAG）面临的两个关键瓶颈：路由失败（难以定位正确文档）和证据碎片化（分散信息难以整合）。核心方法提出HiKEY框架，通过文档层次解析（DHP）构建逻辑异构图，并采用层次化粗到细策略：先全局路由快速剪枝搜索空间，再细粒度检索结合多模态融合策略捕获最判别性证据。主要贡献在于将文档层次结构作为首要检索信号，并设计混合结构-语义打包策略生成token高效的证据子图。实验表明，该方法在检索召回率上最高提升12.9%，端到端问答性能提升6.8%，适用于大规模工业语料库中需要跨文档、跨模态证据整合的复杂问答场景。

### 4. [VeriTrip: A Verifiable Benchmark for Travel Planning Agents over Unstructured Web Corpora](https://arxiv.org/abs/2605.28683v1)
**作者：** Yuting Xu, Jiayi Tian, Jian Liang, Xin Xiong, Hang Zhang, Mu Xu
**发表：** 2026-05-27 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对现有旅行规划智能体基准测试过度依赖API、忽视开放网络复杂性的问题，提出了一个名为VeriTrip的可验证基准。核心方法包括构建多模态检索库（MRB）和同步可验证知识库（VKB），通过细胞级验证协议精确量化事实可靠性，区分系统性推理错误与参数幻觉。主要贡献在于将评估焦点转向基于证据的推理，并揭示了主流多模态大模型在自主检索时存在的“检索-推理权衡”现象。该基准适用于评估和提升旅行规划智能体在非结构化、多模态网络环境中的鲁棒性与可靠性。

### 5. [Gemini Embedding 2: A Native Multimodal Embedding Model from Gemini](https://arxiv.org/abs/2605.27295v1)
**作者：** Madhuri Shanbhogue, Zhe Li, Shanfeng Zhang, Gustavo Hernández Ábrego, Shih-Cheng Huang, Aashi Jain
**发表：** 2026-05-26 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究提出了一种名为Gemini Embedding 2的原生多模态嵌入模型，旨在将视频、音频、图像和文本等多种模态统一映射到同一表征空间中。核心方法基于Gemini模型的多模态能力，通过大规模对比学习与多任务、多阶段训练，实现对任意组合的交叉模态输入进行有效嵌入。主要贡献在于，该模型在单模态、跨模态及多模态检索等多项基准测试中均达到领先水平（如MSCOCO上R@1达62.9，Vatex上NDCG@10达68.8），且性能超越了许多专用模型。该模型适用于检索增强生成（RAG）、推荐系统和搜索等下游任务，并因其强大的零样本泛化能力，可直接应用于天文、生物科学、艺术等专业领域。

## 二、最热门论文

### 1. [Beyond Classification: Dynamic Adapter Routing for Continual Multimodal Retrieval](https://arxiv.org/abs/2605.31229v1)
**作者：** Alicja Dobrzeniecka, Filip Szatkowski, Sebastian Cygert, Szymon Lukasik, Bartlomiej Twardowski
**发表：** 2026-05-29 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究聚焦于多模态检索场景下的持续学习问题，指出当前工作多沿用类别增量学习（CIL）框架，未能充分捕捉检索任务的动态特性。作者首先构建了一个覆盖多种视觉领域的持续多模态检索（CMR）评估框架，系统对比现有方法后发现标准CIL方法在此场景下效果有限。核心贡献是提出动态适配器路由（DAR）方法，通过基于原型的路由选择适配器，并利用模型合并技术实现高效组合。实验表明DAR在性能上显著超越基线，且在分布外评估中展现出强泛化能力。该工作适用于需要持续更新视觉-语言检索模型以应对新领域或新数据分布的实际应用场景。

### 2. [Uncertainty Quantification for Multimodal Retrieval Augmented Generation](https://arxiv.org/abs/2605.29956v1)
**作者：** Simon Binz, Heydar Soudani, Faegheh Hasibi
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对多模态检索增强生成（RAG）系统中答案可能不准确的问题，提出了一种新的不确定性量化方法。核心方法是通过设计可学习的多模态不确定性量化模型LeMUQ，分析在移除不同模态或检索上下文时token概率的变化，并将这些信号编码为概率令牌进行微调处理。主要贡献在于首次系统性地建模了多模态RAG中检索、视觉理解和生成阶段的不确定性，在多个数据集和模型上平均AUROC指标提升3.8%。该方法适用于需要高可靠性输出的多模态问答场景，如医疗影像分析、自动驾驶决策支持等，尤其适合对检索结果和视觉信息可靠性要求严格的领域。

### 3. [HiKEY: Hierarchical Multimodal Retrieval for Open-Domain Document Question Answering](https://arxiv.org/abs/2605.29606v1)
**作者：** Joongmin Shin, Gyuho Shim, Jeongbae Park, Jaehyung Seo, Heuiseok Lim
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对大规模工业语料库中开放域文档问答（ODQA）面临的两个关键瓶颈：路由失败（难以定位正确文档）和证据碎片化（难以整合分散信息）。核心方法提出HiKEY框架，通过文档层次解析（DHP）构建逻辑异构图，并采用层次化粗到细策略：先利用层次索引全局剪枝搜索空间，再通过多模态融合策略进行细粒度检索。主要贡献在于将文档层次结构作为一级检索信号，并设计了混合结构-语义打包策略生成token高效的证据子图。实验表明，HiKEY在检索召回率上最高提升12.9%，端到端问答性能提升6.8%。该框架适用于需要从包含表格、图表等多模态证据的大型工业文档库中精准检索并整合信息的场景。

### 4. [VeriTrip: A Verifiable Benchmark for Travel Planning Agents over Unstructured Web Corpora](https://arxiv.org/abs/2605.28683v1)
**作者：** Yuting Xu, Jiayi Tian, Jian Liang, Xin Xiong, Hang Zhang, Mu Xu
**发表：** 2026-05-27 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究针对现有旅行规划智能体评测基准过度依赖API调用、忽视开放网络复杂性的问题，提出名为VeriTrip的可验证基准。核心方法包括构建多模态检索库（MRB）和同步可验证知识库（VKB），通过细胞级验证协议量化事实可靠性，区分系统性推理错误与参数幻觉。主要贡献在于将评测焦点转向基于证据的推理，并揭示了多模态大语言模型在自主检索时存在的“检索-推理权衡”现象。该基准适用于评估和提升旅行规划智能体在非结构化、多模态网络环境中的鲁棒性与可靠性。

### 5. [Gemini Embedding 2: A Native Multimodal Embedding Model from Gemini](https://arxiv.org/abs/2605.27295v1)
**作者：** Madhuri Shanbhogue, Zhe Li, Shanfeng Zhang, Gustavo Hernández Ábrego, Shih-Cheng Huang, Aashi Jain
**发表：** 2026-05-26 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv

**核心贡献：** 该研究提出了一种名为Gemini Embedding 2的原生多模态嵌入模型，其核心方法是通过大规模对比学习与多任务多阶段训练，将视频、音频、图像和文本等模态统一映射到同一表示空间。主要贡献在于实现了跨模态与多模态检索任务上的最先进性能，例如在MSCOCO上达到62.9的R@1，在Vatex上达到68.8的NDCG@10，并超越了多个专门化模型。该模型适用于检索增强生成（RAG）、推荐系统和搜索等下游场景，同时因其强大的零样本泛化能力，可直接应用于天文学、生物科学、艺术等专业领域。

## 三、最相关论文

### 1. [Uncertainty Quantification for Multimodal Retrieval Augmented Generation](https://arxiv.org/abs/2605.29956v1)
**作者：** Simon Binz, Heydar Soudani, Faegheh Hasibi
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv
**相关度：** 0.530
**核心贡献：** 该研究聚焦于多模态检索增强生成（RAG）系统中的不确定性量化（UQ）问题，旨在提升模型输出可靠性。核心方法提出LeMUQ，一种可学习的多模态UQ方法，通过分析输入修改（如移除模态或检索上下文）下的token概率，并编码为概率令牌由微调模型处理，以捕捉模态与检索间的交互。主要贡献包括：在多个数据集、检索器和视觉语言模型上平均AUROC提升3.8%，并展现出跨检索设置和数据集的良好泛化能力。适用场景为需要高可靠性的多模态问答系统，如医疗影像分析、视觉知识问答等对错误容忍度低的应用。

### 2. [Can Retrieval Heads See Images? Multimodal Retrieval Heads in Long-Context Vision-Language Models](https://arxiv.org/abs/2605.27243v1)
**作者：** Aaron Branson Cigres Li, Zhaowei Wang, Yu Zhao, Yiming Du, Haobo Li, Xiyu Ren
**发表：** 2026-05-26 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv
**相关度：** 0.518
**核心贡献：** 该研究旨在解决长上下文视觉-语言模型中，模型如何从交错的文本和图像中定位相关证据的问题。核心方法提出了一种多模态检索头检测技术，通过计算问题标记对文本或视觉证据的注意力分数来识别关键注意力头。主要贡献在于发现多模态检索头具有稀疏性（仅占4.4%-10.2%）、内在性和因果重要性，掩码这些头部会导致模型性能大幅下降（如MMLongBench-Doc从48.2%降至5.7%）。该研究适用于需要处理长文档、小时级视频或长期代理轨迹的视觉-语言任务，尤其适合视觉丰富的文档检索场景，如页面检索和布局检索。

### 3. [Beyond Classification: Dynamic Adapter Routing for Continual Multimodal Retrieval](https://arxiv.org/abs/2605.31229v1)
**作者：** Alicja Dobrzeniecka, Filip Szatkowski, Sebastian Cygert, Szymon Lukasik, Bartlomiej Twardowski
**发表：** 2026-05-29 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv
**相关度：** 0.491
**核心贡献：** 该研究聚焦于多模态检索中的持续学习问题，指出现有工作多沿用类增量学习（CIL）框架，未能充分捕捉检索任务的动态特性。核心方法为提出动态适配器路由（DAR），通过基于原型的路由机制选择适配器，并利用模型合并技术组合适配器。主要贡献包括：构建了覆盖多种视觉领域的持续多模态检索（CMR）评估框架，揭示了标准CIL方法在检索场景中的局限性，并验证了DAR在分布外泛化上的优越性。适用场景为需要持续更新视觉-语言模型以应对新领域检索任务的应用，如动态知识库更新、跨域图像搜索等。

### 4. [HiKEY: Hierarchical Multimodal Retrieval for Open-Domain Document Question Answering](https://arxiv.org/abs/2605.29606v1)
**作者：** Joongmin Shin, Gyuho Shim, Jeongbae Park, Jaehyung Seo, Heuiseok Lim
**发表：** 2026-05-28 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv
**相关度：** 0.473
**核心贡献：** 该研究针对开放域文档问答中检索增强生成（RAG）面临的两大瓶颈——文档定位失败与证据碎片化，提出了一种名为HiKEY的分层多模态检索框架。核心方法包括通过文档层次解析（DHP）构建逻辑异构图，并采用从粗到细的分层策略：先利用层次索引快速剪枝搜索空间，再通过多模态融合策略进行细粒度段落排序。主要贡献在于将文档层级结构作为首要检索信号，并设计了混合结构-语义打包策略以生成令牌高效的证据子图。实验表明，HiKEY在检索召回率上最高提升12.9%，端到端问答性能提升6.8%，适用于大规模工业语料库中需要整合表格、图表等多模态证据的复杂文档问答场景。

### 5. [VeriTrip: A Verifiable Benchmark for Travel Planning Agents over Unstructured Web Corpora](https://arxiv.org/abs/2605.28683v1)
**作者：** Yuting Xu, Jiayi Tian, Jian Liang, Xin Xiong, Hang Zhang, Mu Xu
**发表：** 2026-05-27 | **来源：** arxiv | **引用数：** 0
**会议/期刊：** arXiv
**相关度：** 0.378
**核心贡献：** 该研究针对现有旅行规划智能体基准测试过度依赖API、忽略开放网络复杂性的问题，提出了名为VeriTrip的可验证基准。核心方法包括构建多模态检索库（MRB）和同步可验证知识库（VKB），通过细胞级验证协议精确量化事实可靠性，区分系统性推理失败与参数幻觉。主要贡献在于将评估焦点转向基于证据的推理，并揭示了自主检索与指令保持之间的权衡关系。该基准适用于评估和提升旅行规划智能体在非结构化、多模态网络环境中的鲁棒性与可靠性。

## 四、近期研究进展综述

基于近期论文简报，多模态检索方向呈现以下主要趋势与进展：

**主要趋势**：从静态检索向动态、持续、可解释的检索系统演进，强调鲁棒性与可靠性。核心关注点包括：持续学习、不确定性量化、层次化检索、可验证基准以及原生多模态嵌入。

**代表工作与技术路线**：
1.  **持续学习**：针对动态场景，提出动态适配器路由（DAR），通过基于原型的路由选择适配器并结合模型合并，解决类别增量学习在检索中的局限性。
2.  **不确定性量化**：提出可学习多模态不确定性量化方法（LeMUQ），通过分析输入修改下的token概率，系统建模检索、视觉与生成阶段的不确定性，提升RAG可靠性。
3.  **层次化检索**：HiKEY框架通过文档层次解析构建逻辑异构图，采用粗到细策略（全局路由+细粒度多模态融合），有效解决开放域文档问答中的路由失败与证据碎片化。
4.  **可验证基准**：VeriTrip构建多模态检索库与同步可验证知识库，通过细胞级验证协议区分推理错误与幻觉，揭示主流模型在自主检索中的“检索-推理权衡”。
5.  **原生多模态嵌入**：Gemini Embedding 2基于大规模对比学习与多任务训练，将视频、音频、图像、文本统一映射，在多项基准上达到领先水平。
6.  **长上下文机制**：发现多模态检索头具有稀疏性与因果重要性，掩码后性能大幅下降，为长上下文视觉-语言模型中的证据定位提供新视角。

**潜在研究空白**：
- 持续学习与不确定性量化的结合：如何在动态更新中同时保证检索结果的可靠性。
- 层次化检索与原生多模态嵌入的融合：利用统一嵌入空间优化层次化路由与证据整合。
- 可验证基准的跨领域扩展：将VeriTrip的验证协议推广至医疗、法律等高风险领域。
- 长上下文检索头的可解释性应用：如何利用稀疏检索头设计更高效的检索架构。
