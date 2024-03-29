## [Text CNN](https://arxiv.org/abs/1408.5882)
![](https://ws4.sinaimg.cn/large/006tNbRwly1fwv4l4e186j30qd0cjmxx.jpg)

+ Framework
  + Embedding Layer
    - Tencent Embedding
    - Fune-tuning
    - Dim 200
  + Convolution Layer
    + 卷积窗口的长度是词向量维度，宽度是定义的窗口大小
    + Filter size [4, 3, 2]
    + Filter number 256
  + Max Pooling Layer
    + 卷积之后的结果经过 max-pooling 进行特征选择和降维， 得到输入句子的表示
  + Results
    + 句子的表示 通过Dense后有两种方式得到最终的结果
      + Sigmoid(Multi Label)
      + Softmax(Single Label)
+ Experiment and Optimization
  + Hyper Parameters
    + Epoch
    + Early Stopping
    + Dropout
+ Varients
  + CNN 的变体