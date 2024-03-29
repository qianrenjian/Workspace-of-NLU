# View of Lexical Analysis

### ETH-DS3Lab at SemEval-2018 Task 7: Effectively Combining Recurrent and Convolutional Neural Networks for Relation Classification and Extraction

- 本文来自苏黎世联邦理工学院 DS3Lab，文章针对实体关系抽取任务进行了非常系统的实验，并在第十二届国际语义评测比赛 SemEval 2018 的语义关系抽取和分类任务上获得冠军。本文思路严谨，值得国内学者们仔细研读。

### Personalizing Dialogue Agents: I have a dog, do you have pets too?

- 本文是 Facebook AI Research 发表于 NIPS 2018 的工作。论文根据一个名为 PERSONA-CHAT 的对话数据集来训练基于 Profile 的聊天机器人，该数据集包含超过 16 万条对话。
- 本文致力于解决以下问题：
- 聊天机器人缺乏一致性格特征
  - 聊天机器人缺乏长期记忆
  - 聊天机器人经常给出模糊的回应，例如 I don't know
- 数据集链接
- https://github.com/facebookresearch/ParlAI/tree/master/parlai/tasks/personachat

### 人民日报语料下载

### NCRF++:An Open-source Neural Sequence Labeling Toolkit
+ NCRF++ 被设计用来快速实现带有CRF层的不同神经序列标注模型
+ 可编辑配置文件灵活建立模型
+ 论文笔记:COLING 2018 最佳论文解读:序列标注经典模型复现

### Neural CRF
- http://nlp.cs.berkeley.edu/pubs/Durrett-Klein_2015_NeuralCRF_paper.pd

### FoolNLTK
- 中文处理工具包
- 特点：
	- 可能不是最快的开源中文分词，但很可能是最准的开源中文分词
	- 基于 BiLSTM 模型训练而成
	- 包含分词，词性标注，实体识别，都有比较高的准确率
	- 用户自定义词典
- 项目链接：https://github.com/rockyzhengwu/FoolNLTK 


### Adversarial training for multi-context joint entity and relation extraction
+ 根特大学
+ EMNLP2018
+ 同时执行实体识别和关系抽取的multi-head selection 联合模型
+ 实验证明该文提出的方法在大多数数据集上, 可以不依赖NLP工具,且不使用人工特征设置的情况下,同步解决多关系问题

- NER
  - 命名实体识别（NER）的主要任务是将诸如Guido van Rossum，Microsoft，London等的命名实体分类为人员，组织，地点，时间，日期等预定类别。许多NER系统已经创建，其中最好系统采用的是神经网络。
  - 在《Neural Architectures for Named Entity Recognition》文章中，提出了两种用于NER模型。这些模型采用有监督的语料学习字符的表示，或者从无标记的语料库中学习无监督的词汇表达[4]。使用英语，荷兰语，德语和西班牙语等不同数据集，如CoNLL-2002和CoNLL-2003进行了大量测试。该小组最终得出结论，如果没有任何特定语言的知识或资源（如地名词典），他们的模型在NER中取得最好的成绩。
- POS
  - 在《Part-of-Speech Tagging with Bidirectional Long Short-Term Memory Recurrent Neural Network》工作中，提出了一个采用RNN进行词性标注的系统[5]。该模型采用《Wall Street Journal data from Penn Treebank III》数据集进行了测试，并获得了97.40％的标记准确性。



https://github.com/FuYanzhe2/Name-Entity-Recognition