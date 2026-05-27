import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import gaussian_kde
import warnings
warnings.filterwarnings('ignore')

import os
os.chdir(r'C:\vs_env\PythonProject\ml-coding-practice')

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ================================
# 1. 데이터 로딩
# ================================
print("데이터 로딩 중...")
student_info       = pd.read_csv('studentInfo.csv')
student_vle        = pd.read_csv('studentVle.csv')
student_assessment = pd.read_csv('studentAssessment.csv')
assessments        = pd.read_csv('assessments.csv')
vle                = pd.read_csv('vle.csv')
print("로딩 완료")

# ================================
# 2. 전처리
# ================================
print("\n전처리 시작...")

student_assessment = student_assessment[
    student_assessment['is_banked'] == 0
].copy()

student_vle = student_vle.groupby(
    ['code_module','code_presentation','id_student','id_site','date']
)['sum_click'].sum().reset_index()

upper = student_vle['sum_click'].quantile(0.99)
student_vle['sum_click'] = student_vle['sum_click'].clip(upper=upper)

assessments = assessments[
    assessments['assessment_type'] != 'Exam'
].copy()

student_info['target'] = student_info['final_result'].map({
    'Pass': 1, 'Distinction': 1,
    'Withdrawn': 0, 'Fail': 0
})

student_info = student_info.sort_values(
    'num_of_prev_attempts'
).drop_duplicates(subset='id_student', keep='last').copy()

print(f"전처리 완료 — 학생 수 {len(student_info):,}명")

# ================================
# 3. 피처 엔지니어링
# ================================
print("\n피처 엔지니어링 시작...")

vle_4w = student_vle[student_vle['date'].between(1, 28)].copy()
feat1 = vle_4w.groupby('id_student')['sum_click'] \
              .sum().reset_index()
feat1.columns = ['id_student', 'total_click_4weeks']
print("피처 1 완료")

feat2 = student_assessment.groupby('id_student')['score'] \
                           .mean().reset_index()
feat2.columns = ['id_student', 'avg_score']
print("피처 2 완료")

total_per_module = assessments.groupby(
    ['code_module','code_presentation']
)['id_assessment'].count().reset_index()
total_per_module.columns = [
    'code_module','code_presentation','total_assessments'
]
submitted_per_module = student_assessment.merge(
    assessments[['id_assessment','code_module','code_presentation']],
    on='id_assessment', how='left'
).groupby(
    ['id_student','code_module','code_presentation']
)['id_assessment'].count().reset_index()
submitted_per_module.columns = [
    'id_student','code_module','code_presentation','submitted_count'
]
feat3_full = submitted_per_module.merge(
    total_per_module,
    on=['code_module','code_presentation'], how='left'
)
feat3_full['submission_rate'] = (
    feat3_full['submitted_count'] / feat3_full['total_assessments']
).clip(0, 1)
feat3 = feat3_full.groupby('id_student')['submission_rate'] \
                   .mean().reset_index()
print("피처 3 완료")

vle_type = student_vle.merge(
    vle[['id_site','activity_type']], on='id_site', how='left'
)
feat4 = vle_type.groupby('id_student')['activity_type'] \
                .nunique().reset_index()
feat4.columns = ['id_student', 'content_diversity']
print("피처 4 완료")

active_types = ['quiz', 'forumng', 'oucollaborate']
active_click = vle_type[
    vle_type['activity_type'].isin(active_types)
].groupby('id_student')['sum_click'].sum()
total_click_all = vle_type.groupby('id_student')['sum_click'].sum()
feat5 = (active_click / total_click_all.replace(0, np.nan)) \
        .reset_index()
feat5.columns = ['id_student', 'active_learning_ratio']
print("피처 5 완료")

base = student_info[['id_student','target']].copy()
for feat in [feat1, feat2, feat3, feat4, feat5]:
    base = base.merge(feat, on='id_student', how='left')
base.fillna(0, inplace=True)

print(f"\n최종 테이블: {base.shape}")
print(f"결측치: {base.isnull().sum().sum()}개")

# ================================
# 4. EDA
# ================================
FEATURE_COLS = [
    'total_click_4weeks',
    'avg_score',
    'submission_rate',
    'content_diversity',
    'active_learning_ratio'
]

feature_kor = {
    'total_click_4weeks':    '초반 4주 클릭 수',
    'avg_score':             '퀴즈 평균 점수',
    'submission_rate':       '퀴즈 제출률',
    'content_diversity':     '콘텐츠 다양성 ★신규',
    'active_learning_ratio': '능동 학습 비율 ★신규'
}

# EDA 1. 타겟 분포
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
target_counts = base['target'].value_counts().sort_index()
labels_t = ['위험군\n(Withdrawn+Fail)', '안전군\n(Pass+Distinction)']
colors_t  = ['#e74c3c', '#2ecc71']
pcts      = target_counts.values / target_counts.sum() * 100

axes[0].pie(
    target_counts.values,
    labels=[f'{l}\n{p:.1f}%' for l, p in zip(labels_t, pcts)],
    colors=colors_t, startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 11}
)
axes[0].set_title('타겟 변수 구성', fontsize=13, fontweight='bold')

bars = axes[1].bar(labels_t, target_counts.values,
                   color=colors_t, alpha=0.85, width=0.5)
for bar, val, pct in zip(bars, target_counts.values, pcts):
    axes[1].text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 100,
        f'{val:,}명\n({pct:.1f}%)',
        ha='center', fontsize=12, fontweight='bold'
    )
axes[1].set_ylim(0, max(target_counts.values) * 1.2)
axes[1].set_ylabel('학생 수', fontsize=12)
axes[1].set_title('위험군 vs 안전군 인원', fontsize=13, fontweight='bold')
axes[1].axhline(y=target_counts.sum()/2, color='gray',
                linestyle='--', linewidth=1, label='50% 기준')
axes[1].legend()
plt.suptitle(f'EDA 1 — 타겟 변수 분포  (총 {len(base):,}명)',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()
input("Enter → 다음")

# EDA 2. 피처별 분포
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

for idx, col in enumerate(FEATURE_COLS):
    ax = axes[idx]
    d0 = base[base['target'] == 0][col].dropna()
    d1 = base[base['target'] == 1][col].dropna()

    ax.hist(d0, bins=40, alpha=0.5, color='#e74c3c',
            label=f'위험군 (n={len(d0):,})', density=True)
    ax.hist(d1, bins=40, alpha=0.5, color='#2ecc71',
            label=f'안전군 (n={len(d1):,})', density=True)

    for d, color in [(d0, '#c0392b'), (d1, '#27ae60')]:
        if d.std() > 0:
            kde = gaussian_kde(d)
            x_range = np.linspace(d.min(), d.max(), 200)
            ax.plot(x_range, kde(x_range), color=color, linewidth=2)

    ax.axvline(np.median(d0), color='#c0392b', linestyle='--',
               linewidth=1.5, label=f'위험군 중앙값 {np.median(d0):.2f}')
    ax.axvline(np.median(d1), color='#27ae60', linestyle='--',
               linewidth=1.5, label=f'안전군 중앙값 {np.median(d1):.2f}')

    ax.set_title(feature_kor[col], fontsize=11, fontweight='bold')
    ax.set_xlabel('값')
    ax.set_ylabel('밀도')
    ax.legend(fontsize=8)

axes[-1].axis('off')
plt.suptitle('EDA 2 — 피처별 분포 (위험군 vs 안전군)',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()
input("Enter → 다음")

# EDA 3. 박스플롯 + 통계 검정
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

print("\n" + "="*55)
print("Mann-Whitney U 검정 결과")
print("="*55)

for idx, col in enumerate(FEATURE_COLS):
    ax = axes[idx]
    d0 = base[base['target'] == 0][col].dropna()
    d1 = base[base['target'] == 1][col].dropna()

    stat, p = stats.mannwhitneyu(d0, d1, alternative='two-sided')
    sig = 'p < 0.001 ✅' if p < 0.001 else f'p = {p:.4f}'

    print(f"{col:<25}  위험군 {np.median(d0):.3f}  "
          f"안전군 {np.median(d1):.3f}  {sig}")

    bp = ax.boxplot(
        [d0, d1], labels=['위험군', '안전군'],
        patch_artist=True,
        medianprops={'color': 'black', 'linewidth': 2.5},
        whiskerprops={'linewidth': 1.5},
        capprops={'linewidth': 1.5}
    )
    bp['boxes'][0].set_facecolor('#e74c3c')
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_facecolor('#2ecc71')
    bp['boxes'][1].set_alpha(0.7)

    med0, med1 = np.median(d0), np.median(d1)
    ax.text(1.35, med0, f'{med0:.3f}', va='center',
            fontsize=10, color='#c0392b', fontweight='bold')
    ax.text(2.05, med1, f'{med1:.3f}', va='center',
            fontsize=10, color='#27ae60', fontweight='bold')
    ax.set_title(f'{feature_kor[col]}\n{sig}',
                 fontsize=11, fontweight='bold')
    ax.set_ylabel('값')

axes[-1].axis('off')
plt.suptitle('EDA 3 — 박스플롯 + 통계 검정',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()
input("Enter → 다음")

# EDA 4. 상관관계 히트맵
corr_matrix = base[FEATURE_COLS + ['target']].corr()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.heatmap(
    corr_matrix, annot=True, fmt='.2f',
    cmap='RdYlGn', center=0, vmin=-1, vmax=1,
    linewidths=0.5, annot_kws={'size': 11, 'weight': 'bold'},
    ax=axes[0]
)
axes[0].set_title('피처 + 타겟 전체 상관관계',
                  fontsize=13, fontweight='bold')
axes[0].set_xticklabels(
    axes[0].get_xticklabels(), rotation=30, ha='right'
)

target_corr = corr_matrix['target'].drop('target').sort_values()
colors_corr = ['#e74c3c' if v >= 0.3 else '#95a5a6'
               for v in target_corr]
bars = axes[1].barh(target_corr.index, target_corr.values,
                    color=colors_corr, alpha=0.85)
for bar, val in zip(bars, target_corr.values):
    axes[1].text(
        val + 0.01, bar.get_y() + bar.get_height()/2,
        f'{val:+.3f}', va='center', fontsize=12, fontweight='bold'
    )
axes[1].axvline(x=0.3, color='#e74c3c', linestyle='--',
                linewidth=2, label='유의미 기준 (r=0.3)')
axes[1].axvline(x=0, color='black', linewidth=0.8)
axes[1].set_xlabel('상관계수 (r)', fontsize=12)
axes[1].set_title('피처별 타겟 상관계수',
                  fontsize=13, fontweight='bold')
axes[1].set_xlim(-0.1, 1.0)
axes[1].legend(fontsize=10)

plt.suptitle('EDA 4 — 상관관계 분석', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()
input("Enter → 다음")

# EDA 5. 제출률 구간별 이탈률
base['sub_bin'] = pd.cut(
    base['submission_rate'],
    bins=[0, 0.2, 0.4, 0.6, 0.8, 1.01],
    labels=['0~20%','20~40%','40~60%','60~80%','80~100%'],
    right=False
)

bin_stats = base.groupby('sub_bin', observed=True).agg(
    인원수=('target', 'count'),
    이탈률=('target', lambda x: (x==0).mean()),
    위험군수=('target', lambda x: (x==0).sum())
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

bar_colors = ['#e74c3c' if v > 0.5 else '#3498db'
              for v in bin_stats['이탈률']]
bars = axes[0].bar(bin_stats['sub_bin'].astype(str),
                   bin_stats['이탈률'], color=bar_colors, alpha=0.85)
for bar, val in zip(bars, bin_stats['이탈률']):
    axes[0].text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.01,
        f'{val:.1%}', ha='center', fontsize=12, fontweight='bold'
    )
axes[0].axhline(y=0.5, color='black', linestyle='--',
                linewidth=2, label='50% 기준선')
axes[0].set_xlabel('퀴즈 제출률 구간', fontsize=12)
axes[0].set_ylabel('이탈률', fontsize=12)
axes[0].set_ylim(0, 1.15)
axes[0].set_title('제출률 구간별 이탈률\n(r=0.80, 가장 강력한 예측 변수)',
                  fontsize=12, fontweight='bold')
axes[0].legend()

axes[1].bar(bin_stats['sub_bin'].astype(str),
            bin_stats['인원수'], color='#3498db',
            alpha=0.7, label='전체')
axes[1].bar(bin_stats['sub_bin'].astype(str),
            bin_stats['위험군수'], color='#e74c3c',
            alpha=0.7, label='위험군')
for i, row in bin_stats.iterrows():
    axes[1].text(i, row['인원수'] + 30,
                 f"{row['인원수']:,}", ha='center', fontsize=9)
axes[1].set_xlabel('퀴즈 제출률 구간', fontsize=12)
axes[1].set_ylabel('학생 수', fontsize=12)
axes[1].set_title('구간별 인원 분포', fontsize=12, fontweight='bold')
axes[1].legend()

plt.suptitle('EDA 5 — 퀴즈 제출률 심층 분석',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()
input("Enter → 다음")

# EDA 6. 산점도
sample = base.sample(n=3000, random_state=42)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for label, color, name in [(0,'#e74c3c','위험군'),(1,'#2ecc71','안전군')]:
    s = sample[sample['target'] == label]
    axes[0].scatter(
        s['content_diversity'], s['active_learning_ratio'],
        c=color, label=name, alpha=0.4, s=25
    )
axes[0].set_xlabel('콘텐츠 다양성', fontsize=11)
axes[0].set_ylabel('능동 학습 비율', fontsize=11)
axes[0].set_title('신규 피처 2개 산점도\n(샘플 3,000명)',
                  fontsize=12, fontweight='bold')
axes[0].legend(fontsize=11)

for label, color, name in [(0,'#e74c3c','위험군'),(1,'#2ecc71','안전군')]:
    s = sample[sample['target'] == label]
    axes[1].scatter(
        s['submission_rate'], s['avg_score'],
        c=color, label=name, alpha=0.4, s=25
    )
axes[1].set_xlabel('퀴즈 제출률', fontsize=11)
axes[1].set_ylabel('퀴즈 평균 점수', fontsize=11)
axes[1].set_title('기존 핵심 피처 산점도',
                  fontsize=12, fontweight='bold')
axes[1].legend(fontsize=11)

plt.suptitle('EDA 6 — 피처 간 관계 시각화',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n" + "="*55)
print("EDA 완료")
print("="*55)