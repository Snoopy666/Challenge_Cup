# Challenge_Cup

清华大学挑战杯项目


主要目标为：**法律文书结构化** 结构化法律文书的核心在于 **事件抽取**

## Pipeline

### 问题思路
一个事件由许多的要素（argument）组成，例如简单的婚姻事件就由 结婚人、结婚时间、是否离婚等一系列要素组成。则我们只要知道句子中的每一个词语在所描述的事件中属于哪一个argument，则能够抽取出事件。所以事件抽取简化成 **序列标注**问题

#### 事件的组成
* Event mention: a phrase or sentence within which an event is described, including a trig- ger and arguments.
* Event trigger: the main word that most clearly expresses the occurrence of an event (An ACE event trigger is typically a verb or a noun).
* Event argument: an entity mention, tempo- ral expression or value (e.g. Job-Title) that is involved in an event (viz., participants).
* Argument role: the relationship between an argument to the event in which it participates.


### 问题模型
crf是用于解决序列标注问题的常见模型。

#### 事件抽取流程
* 定义事件，将事件中重要的arguments进行定义
* 数据标注，通过数据标注平台把事件中的arguments在文书中标注出来
* 拓展数据集，以标注的少量数据作为训练集，通过网上开源工具 python-crfsuite 来对我们目前拥有的所有数据（包括已经标注的和未标注的）进行预测，通过一定的标准（标注详细内容见下）来进行初步筛选
* 数据的再次处理（人工）人工对初步筛选的数据进行再次筛选，确保拓展出的数据集的正确性
* 通过更加复杂的模型来进行句子（词序列）的序列标注


##### 第三步中对数据进行初步筛选的标准
* 拥有所有的key argument
* 只拥有一个trigger


## 刑法top10罪名
* 故意伤害
* 抢劫
* 赌博
* 妨碍公务
* 滥伐林木
* 非法持有毒品
* 非法拘禁
* \[掩饰、隐瞒\]\[犯罪所得、犯罪所得收益\]
* 故意毁坏财物
* 抢夺

