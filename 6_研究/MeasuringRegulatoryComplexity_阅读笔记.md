---
created: 2026-05-19
tags:
  - type/paper
  - status/done
aliases: []
---

# Measuring Regulatory Complexity 阅读笔记

**论文信息**

| 项目 | 内容 |
|:---|:---|
| 标题 | Measuring Regulatory Complexity |
| 作者 | Jean-Edouard Colliard, Co-Pierre Georg |
| 单位 | HEC Paris, University of Cape Town |
| 日期 | 2024年1月 |

## 主要研究内容

金融危机后，银行资本监管变得极为复杂，引发广泛争论。Basel委员会（2013）承认监管存在"精确性vs简单性"的权衡。但学界对"监管复杂性"缺乏统一概念框架。

本文提出受计算机科学启发的综合框架，将监管视为一种"算法"（一系列指令），区分复杂性不同维度、分类现有度量、开发新度量，并在Basel I和Dodd-Frank Act两个例子上计算验证。

### 三种复杂性维度

1. **问题复杂性**：监管针对多少不同规则，与语言无关
2. **心理复杂性**：文本对人类读者的理解难度
3. **计算复杂性**：实施监管需要多长时间

### 六个度量（基于Halstead方法）

将词汇分为"算子"（ operators，如"if"、"必须"）和"操作数"（operands，变量/参数）：

- Length（长度）
- Cyclomatic（圈复杂度）
- Quantity（数量）
- Potential（潜在复杂性）
- Diversity（多样性）
- Level（层级）

## 研究方法

- **文本分析**：将监管文本转化为n-gram，手动分类为算子/操作数
- **实验验证**：设计实验室实验，让参与者根据Basel-I类型规则计算风险加权资产
- **规范性模型**：构建银行资本监管模型，计算精度vs复杂性的最优权衡
- **开放工具包**：GitHub公开（github.com/cogeorg/RegulatoryComplexity_Public）

## 主要结论

- 只有**两个度量**（Potential和Diversity，对应问题复杂性）通过实验验证，能预测错误率和耗时，超越了文本长度的解释力
- 问题复杂性是独立于文本长度的维度，实验验证了这一直觉
- Dodd-Frank词典在16个标题间高度重叠（88%操作数、96%算子已在其他标题词典中）
- 更多风险桶带来更高福利，但增加复杂性成本，最优风险桶数量存在均衡

## 优点

- 理论突破：首次统一厘清"问题vs心理vs计算"复杂性的本质区别
- 方法论：将Halstead算法复杂性方法创造性地引入法学/金融监管
- 实验设计：可检验任何文本基础度量的有效性
- 开放共享：提供工具包和词典

## 不足

- 实验样本：仅用学生被试，未使用真实的银行从业者、律师或监管者
- 字典覆盖：仅覆盖Dodd-Frank，需扩展到其他监管文本
- 规范性模型较简化，未考虑监管套利等动态因素

## 未来方向

1. 用实际受众（银行家、律师、监管者）重复实验
2. 扩展词典到Basel III、欧盟MiFID等文本
3. 将度量用于实证研究，检验理论预测
4. 探究复杂度与执法效果的关系

## Related

- [Benabou_Tirole_2011_Laws_and_Norms.md](Benabou_Tirole_2011_Laws_and_Norms.md) — Laws and Norms理论：法律与社会规范交互

## Source

- [MeasuringRegulatoryComplexity_preview.pdf](MeasuringRegulatoryComplexity_preview.pdf)
- 转换后markdown：[MeasuringRegulatoryComplexity.md](MeasuringRegulatoryComplexity.md)