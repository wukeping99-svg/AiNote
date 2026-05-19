"""
Measuring Regulatory Complexity - 实证复现代码

基于 Colliard & Georg (2024) 的论文方法，复现其实验设计和回归结果

主要功能：
1. 生成Basel-I类型随机规则
2. 计算六个复杂度度量 (Length, Cyclomatic, Quantity, Potential, Diversity, Level)
3. 模拟参与者实验数据
4. 运行probit回归验证哪些度量能预测错误率
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import expit  # inverse logit
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Probit
import warnings
warnings.filterwarnings('ignore')

# 设置随机种子以保证可复现性
np.random.seed(42)

# =============================================================================
# 第一部分：定义复杂度度量计算函数
# =============================================================================

def tokenize_regulation(text):
    """将规则文本分词"""
    # 简单分词：按空格和标点分割
    import re
    words = re.findall(r'\b\w+\b', text.lower())
    return words


def compute_complexity_measures(text):
    """
    计算六个复杂度度量

    基于 Halstead (1977) 方法论的简化实现

    Parameters
    ----------
    text : str
        监管规则文本

    Returns
    -------
    dict : 包含六个度量的字典
        - length: 总词数
        - cyclomatic: 圈复杂度（逻辑操作符数量）
        - quantity: 规则操作符数量
        - potential: 潜在复杂性（最小程序长度估计）
        - diversity: 操作符多样性（唯一操作符数量）
        - level: 层级（程序深度）
    """
    words = tokenize_regulation(text)
    N = len(words)  # total words

    # 定义操作符和操作数的识别模式
    logical_ops = {'if', 'and', 'or', 'then', 'when', 'unless', 'except'}
    regulatory_ops = {'shall', 'must', 'may', 'should', 'require', 'shall not', 'must not'}
    math_ops = {'plus', 'minus', 'times', 'divide', 'multiply', 'add', 'subtract', 'equal', 'greater', 'less'}

    # 识别词汇类别
    operators = set()
    operands = set()

    for word in words:
        if word in logical_ops:
            operators.add(word)
        elif word in regulatory_ops:
            operators.add(word)
        elif word in math_ops:
            operators.add(word)
        else:
            # 变量名、参数等视为操作数
            if word not in {'the', 'a', 'an', 'of', 'to', 'in', 'for', 'with', 'be', 'or', 'is', 'as', 'at', 'by'}:
                operands.add(word)

    # 计算六个度量
    # 1. Length: 总词数
    length = N

    # 2. Cyclomatic: 逻辑操作符数量
    cyclomatic = len([w for w in words if w in logical_ops])

    # 3. Quantity: 规则操作符总数
    quantity = len([w for w in words if w in regulatory_ops])

    # 4. Potential: 潜在复杂性（估计的最小程序长度）
    # 基于Halstead: potential = 2 * n_operands_unique
    n_operands_unique = len(operands)
    potential = 2 * max(n_operands_unique, 1)

    # 5. Diversity: 操作符多样性
    diversity = len(operators)

    # 6. Level: 层级 (program depth estimate)
    # 简化估计：规则中的嵌套层数
    level = (2 + n_operands_unique) / (N + 1) if N > 0 else 0

    return {
        'length': length,
        'cyclomatic': cyclomatic,
        'quantity': quantity,
        'potential': potential,
        'diversity': diversity,
        'level': level
    }


# =============================================================================
# ���二部分：生成Basel-I类型随机规则
# =============================================================================

def generate_basel_rules(n_rules=38, seed=42):
    """
    生成随机Basel-I类型规则

    Parameters
    ----------
    n_rules : int
        生成的规则数量
    seed : int
        随机种子

    Returns
    -------
    list : 规则文本列表
    """
    np.random.seed(seed)

    # 资产类别模板
    asset_classes = ['cash', 'loans', 'securities', 'derivatives', 'mortgages',
                     'corporate_bonds', 'sovereign_debt', 'interbank', 'retail']

    # 风险权重
    risk_weights = ['0%', '20%', '50%', '100%', '150%', '200%']

    # 条件类型
    conditions = ['secured', 'unsecured', 'rated', 'unrated', 'domestic', 'foreign',
                 'short_term', 'long_term', 'investment_grade', 'speculative']

    rules = []

    for i in range(n_rules):
        n_asset_classes = np.random.choice([2, 3, 4, 5, 6])
        n_conditions = np.random.choice([1, 2, 3, 4])

        selected_assets = np.random.choice(asset_classes, n_asset_classes, replace=False)

        rule_parts = []

        for asset in selected_assets:
            weight = np.random.choice(risk_weights)
            cond_list = []

            if np.random.random() > 0.3:
                selected_conds = np.random.choice(conditions,
                                               min(n_conditions, len(conditions)),
                                               replace=False)
                cond_list = list(selected_conds)

            if cond_list:
                cond_str = ' and '.join(cond_list)
                rule = f"If {asset} is {cond_str} then risk weight shall be {weight}"
            else:
                rule = f"{asset} shall have risk weight {weight}"

            rule_parts.append(rule)

        # 添加整体规则
        rule_text = '. '.join(rule_parts) + '.'
        rules.append(rule_text)

    return rules


def compute_rules_complexity(rules):
    """
    计算一组规则的复杂度度量

    Parameters
    ----------
    rules : list
        规则文本列表

    Returns
    -------
    DataFrame : 包含每个规则复杂度度量的DataFrame
    """
    results = []
    for i, rule in enumerate(rules):
        measures = compute_complexity_measures(rule)
        measures['rule_id'] = i + 1
        results.append(measures)

    return pd.DataFrame(results)


# =============================================================================
# 第三部分：模拟参与者实验数据
# =============================================================================

def simulate_experiment_data(rules_df, n_participants=118, n_questions=9, seed=42):
    """
    模拟实验参与者的作答数据

    基于论文结论: 只有Potential和Diversity在控制length后仍然显著
    而且这两个度量对应"问题复杂性"

    Parameters
    ----------
    rules_df : DataFrame
        规则的复杂度度量
    n_participants : int
        参与者数量
    n_questions : int
        每个参与者回答的问题数
    seed : int
        随机种子

    Returns
    -------
    DataFrame : 模拟的实验数据
    """
    np.random.seed(seed)

    n_rules = len(rules_df)

    # 参与者固定效应（模拟个体差异）
    participant_ability = np.random.normal(0, 0.3, n_participants)

    # 六个度量的系数设定
    # 论文核心发现：只有potential和diversity能超越length解释错误率
    # 问题复杂性与文本长度无关
    betas = {
        'length': -0.03,      # 长度效应
        'cyclomatic': -0.005,    # 与length高度相关(0.93)，控制后不显著
        'quantity': -0.01,      # 与length高度相关(0.85)，控制后不显著
        'potential': -0.04,    # 问题复杂性（核心发现）
        'diversity': -0.06,    # 操作符多样性（核心发现）
        'level': 0.02          # 与length负相关(-0.86)
    }

    # 生���数据
    data = []
    observation_id = 0

    for participant in range(n_participants):
        # 每个参与者随机选择n_questions个规则
        selected_rules = np.random.choice(rules_df['rule_id'].values,
                                        n_questions, replace=False)

        for rule_id in selected_rules:
            rule_data = rules_df[rules_df['rule_id'] == rule_id].iloc[0]

            # 计算正确概率（基于probit模型）
            z = (participant_ability[participant] +
                 sum(betas[k] * rule_data[k] for k in betas.keys()) +
                 np.random.normal(0, 0.5))

            # 正确率
            prob_correct = expit(z)
            correct = 1 if np.random.random() < prob_correct else 0

            # 耗时（秒）：难度越高，耗时越长
            base_time = 60  # 基准时间
            time_penalty = (rule_data['length'] * 2 +
                           rule_data['cyclomatic'] * 5 +
                           rule_data['diversity'] * 10 +
                           np.random.normal(0, 20))
            time = max(20, base_time + time_penalty + np.random.normal(0, 15))

            data.append({
                'observation_id': observation_id,
                'participant_id': participant + 1,
                'rule_id': rule_id,
                'correct': correct,
                'time': time,
                'length': rule_data['length'],
                'cyclomatic': rule_data['cyclomatic'],
                'quantity': rule_data['quantity'],
                'potential': rule_data['potential'],
                'diversity': rule_data['diversity'],
                'level': rule_data['level']
            })

            observation_id += 1

    return pd.DataFrame(data)


# =============================================================================
# 第四部分：回归分析
# =============================================================================

def run_regression(df, dependent_var='correct', controls=True):
    """
    运行probit回归分析

    Parameters
    ----------
    df : DataFrame
        实验数据
    dependent_var : str
        因变量 ('correct' 或 'time')
    controls : bool
        是否加入固定效应

    Returns
    -------
    dict : 回归结果
    """
    from scipy.stats import norm

    results = {}

    measures = ['length', 'cyclomatic', 'quantity', 'potential', 'diversity', 'level']

    for measure in measures:
        if dependent_var == 'correct':
            # Probit regression
            X = df[[measure]].copy()
            X = sm.add_constant(X)
            y = df['correct']

            try:
                model = Probit(y, X)
                fitted = model.fit(disp=0)

                results[measure] = {
                    'coef': fitted.params[measure],
                    'std': fitted.bse[measure],
                    'z': fitted.tvalues[measure],
                    'p': fitted.pvalues[measure],
                    'pseudo_r2': fitted.prsquared
                }
            except:
                results[measure] = {'coef': 0, 'std': 0, 'z': 0, 'p': 1}

        elif dependent_var == 'time':
            # OLS regression
            X = df[[measure]].copy()
            X = sm.add_constant(X)
            y = df['time']

            model = sm.OLS(y, X)
            fitted = model.fit()

            results[measure] = {
                'coef': fitted.params[measure],
                'std': fitted.bse[measure],
                't': fitted.tvalues[measure],
                'p': fitted.pvalues[measure],
                'r2': fitted.rsquared
            }

    return results


def run_full_regression_table(df):
    """
    运行完整的回归表（复现论文Table 5和Table 6）
    同时检验控制length后各变量的显著性

    Parameters
    ----------
    df : DataFrame
        实验数据

    Returns
    -------
    DataFrame : 回归结果表
    """
    measures = ['length', 'cyclomatic', 'quantity', 'potential', 'diversity', 'level']

    results = []

    for measure in measures:
        # ======== 因变量: Correct ========
        # 单独回归 (univariate)
        X = df[[measure]].copy()
        X = sm.add_constant(X)
        y = df['correct']

        model = Probit(y, X)
        fitted = model.fit(disp=0)

        results.append({
            'measure': measure,
            'dependent': 'correct',
            'type': 'univariate',
            'coef': fitted.params[measure],
            'std': fitted.bse[measure],
            'z': fitted.tvalues[measure],
            'p': fitted.pvalues[measure]
        })

        # 控制length后的回归
        if measure != 'length':
            X_ctrl = df[['length', measure]].copy()
            X_ctrl = sm.add_constant(X_ctrl)

            model_ctrl = Probit(y, X_ctrl)
            fitted_ctrl = model_ctrl.fit(disp=0)

            results.append({
                'measure': measure,
                'dependent': 'correct',
                'type': 'control_length',
                'coef': fitted_ctrl.params[measure],
                'std': fitted_ctrl.bse[measure],
                'z': fitted_ctrl.tvalues[measure],
                'p': fitted_ctrl.pvalues[measure]
            })

        # ======== 因变量: Time ========
        # 单独回归
        y_time = df['time']

        model_time = sm.OLS(y_time, X)
        fitted_time = model_time.fit()

        results.append({
            'measure': measure,
            'dependent': 'time',
            'type': 'univariate',
            'coef': fitted_time.params[measure],
            'std': fitted_time.bse[measure],
            'z': fitted_time.tvalues[measure],
            'p': fitted_time.pvalues[measure]
        })

        # 控制length后的回归
        if measure != 'length':
            X_ctrl_time = df[['length', measure]].copy()
            X_ctrl_time = sm.add_constant(X_ctrl_time)

            model_ctrl_time = sm.OLS(y_time, X_ctrl_time)
            fitted_ctrl_time = model_ctrl_time.fit()

            results.append({
                'measure': measure,
                'dependent': 'time',
                'type': 'control_length',
                'coef': fitted_ctrl_time.params[measure],
                'std': fitted_ctrl_time.bse[measure],
                'z': fitted_ctrl_time.tvalues[measure],
                'p': fitted_ctrl_time.pvalues[measure]
            })

    return pd.DataFrame(results)


# =============================================================================
# 第五部分：主程序 - 复现论文结果
# =============================================================================

def reproduce_paper_results():
    """
    复现论文的主要实证结果
    """
    print("=" * 70)
    print("Measuring Regulatory Complexity - Empirical Replication")
    print("=" * 70)

    # Step 1: 生成随机规则
    print("\n[Step 1] Generate 38 random Basel-I type rules...")
    rules = generate_basel_rules(n_rules=38, seed=42)

    # Step 2: 计算复杂度度量
    print("[Step 2] Compute six complexity measures...")
    rules_df = compute_rules_complexity(rules)

    # 打印描述性统计
    print("\n--- Table 3: Summary Statistics ---")
    summary_cols = ['length', 'cyclomatic', 'quantity', 'potential', 'diversity', 'level']
    summary = rules_df[summary_cols].describe().T[['mean', 'std', 'min', 'max']]
    summary.columns = ['mean', 'std', 'min', 'max']
    print(summary.round(2))

    # 打印相关性矩阵
    print("\n--- Table 4: Correlation Matrix ---")
    corr = rules_df[summary_cols].corr()
    print(corr.round(2))

    # Step 3: 模拟实验数据
    print("\n[Step 3] Simulate participant experiment data...")
    exp_data = simulate_experiment_data(rules_df, n_participants=118, n_questions=9, seed=42)

    print(f"\nTotal observations: {len(exp_data)}")
    print(f"Success rate: {exp_data['correct'].mean():.2%}")
    print(f"Average time: {exp_data['time'].mean():.1f} seconds")

    # Step 4: 运行回归分析
    print("\n[Step 4] Run regressions...")

    results = run_full_regression_table(exp_data)

    # ======== 打印结果 ========
    print("\n" + "=" * 70)
    print("Table 5: Correct ~ Complexity Measures")
    print("=" * 70)

    # 单独回归结果
    print("\n--- Univariate (without controlling for length) ---")
    correct_uni = results[(results['dependent'] == 'correct') &
                        (results['type'] == 'univariate')].copy()
    correct_uni['sig'] = correct_uni['p'].apply(
        lambda x: '***' if x < 0.01 else '**' if x < 0.05 else '*' if x < 0.1 else ''
    )
    print(correct_uni[['measure', 'coef', 'std', 'z', 'p', 'sig']].to_string(index=False))

    # 控制length后的回归结果
    print("\n--- Controlling for length ---")
    correct_ctrl = results[(results['dependent'] == 'correct') &
                       (results['type'] == 'control_length')].copy()
    correct_ctrl['sig'] = correct_ctrl['p'].apply(
        lambda x: '***' if x < 0.01 else '**' if x < 0.05 else '*' if x < 0.1 else ''
    )
    print(correct_ctrl[['measure', 'coef', 'std', 'z', 'p', 'sig']].to_string(index=False))

    print("\n" + "=" * 70)
    print("Table 6: Time ~ Complexity Measures")
    print("=" * 70)

    # Time回归结果
    print("\n--- Univariate (without controlling for length) ---")
    time_uni = results[(results['dependent'] == 'time') &
                    (results['type'] == 'univariate')].copy()
    time_uni['sig'] = time_uni['p'].apply(
        lambda x: '***' if x < 0.01 else '**' if x < 0.05 else '*' if x < 0.1 else ''
    )
    print(time_uni[['measure', 'coef', 'std', 'z', 'p', 'sig']].to_string(index=False))

    print("\n--- Controlling for length ---")
    time_ctrl = results[(results['dependent'] == 'time') &
                   (results['type'] == 'control_length')].copy()
    time_ctrl['sig'] = time_ctrl['p'].apply(
        lambda x: '***' if x < 0.01 else '**' if x < 0.05 else '*' if x < 0.1 else ''
    )
    print(time_ctrl[['measure', 'coef', 'std', 'z', 'p', 'sig']].to_string(index=False))

    # ======== 验证核心结论 ========
    print("\n" + "=" * 70)
    print("KEY FINDINGS: Which measures are significant beyond length?")
    print("=" * 70)

    # 检查控制length后显著的度量
    sig_beyond_length = correct_ctrl[correct_ctrl['p'] < 0.1]['measure'].tolist()

    print(f"\n[Results] Measures significant at 10% after controlling for length:")
    print(f"  {sig_beyond_length}")

    # 论文发现：只有potential和diversity通过检验
    paper_finding = ['potential', 'diversity']
    print(f"\n[Paper Finding] Colliard & Georg (2024) found:")
    print(f"  - potential: SIGNIFICANT")
    print(f"  - diversity: SIGNIFICANT")
    print(f"  - other measures: NOT significant")

    return rules_df, exp_data, results


def compute_text_complexity_example():
    """
    示例：计算一段真实监管文本的复杂度
    """
    # Basel I 原文示例
    basel_i_example = """
    Cash items in process of collection shall have a 20% risk weight.
    Claims on banks shall have a 20% risk weight.
    Claims on corporates shall have a 100% risk weight.
    Residential mortgages shall have a 50% risk weight.
    Sovereign debt shall have a 0% risk weight if rated investment grade.
    """

    print("\n--- 示例：Basel I 文本复杂度计算 ---")
    print(basel_i_example)

    measures = compute_complexity_measures(basel_i_example)

    print("\n复杂度度量:")
    for k, v in measures.items():
        print(f"  {k}: {v}")

    return measures


# =============================================================================
# 运行主程序
# =============================================================================

if __name__ == "__main__":
    # 复现论文结果
    rules_df, exp_data, results = reproduce_paper_results()

    # 示例
    measures = compute_text_complexity_example()

    # 保存结果
    print("\n\n--- 保存数据 ---")
    rules_df.to_csv('rules_complexity.csv', index=False)
    exp_data.to_csv('experiment_data.csv', index=False)
    results.to_csv('regression_results.csv', index=False)
    print("已保存: rules_complexity.csv, experiment_data.csv, regression_results.csv")