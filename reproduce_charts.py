# -*- coding: utf-8 -*-
"""
第二章 30个可视化图表 Python 复现
数据来源：
  /mnt/agents/upload/第二章 图表(前15).xlsx  -> 图表 1-15
  /mnt/agents/upload/第二章 图表(后15).xlsx  -> 图表 16-30
输出：30 张 PNG 图片
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (Rectangle, FancyBboxPatch, Wedge, Circle,
                                FancyArrowPatch, Arc)
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.dates as mdates
from datetime import datetime
from scipy.interpolate import make_interp_spline
import matplotlib.patheffects as pe

OUT = '/mnt/agents/output/第二章_图表复现'
os.makedirs(OUT, exist_ok=True)

# AntV 默认配色
PALETTE = ['#5B8FF9', '#5AD8A6', '#5D7092', '#F6BD16', '#E8684A',
           '#6DC8EC', '#9270CA', '#FF9D4D', '#269A99', '#FF99C3']
GRAY = '#BFBFBF'
DARK = '#333333'

plt.rcParams['figure.dpi'] = 150


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('saved:', name)


def strip_axes(ax):
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


# ---------------------------------------------------------------- 1 渐变柱形图
def chart01():
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    sales = [2354, 1902, 3524, 2698, 2896, 2563]
    fig, ax = plt.subplots(figsize=(8, 5))
    cmap = LinearSegmentedColormap.from_list('g', ['#DCEAFF', '#2E7CE6'])
    for i, (r, v) in enumerate(zip(regions, sales)):
        p = Rectangle((i - 0.32, 0), 0.64, v, fill=False)
        ax.add_patch(p)
        im = ax.imshow(np.linspace(0, 1, 256).reshape(-1, 1), cmap=cmap,
                       extent=[i - 0.32, i + 0.32, 0, v], aspect='auto', zorder=2)
        im.set_clip_path(p)
        ax.text(i, v + 60, str(v), ha='center', va='bottom', fontsize=11, color=DARK)
    ax.set_xlim(-0.7, len(regions) - 0.3)
    ax.set_ylim(0, max(sales) * 1.15)
    ax.set_xticks(range(len(regions)), regions, fontsize=11)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title('各区域销售量（渐变柱形图）', fontsize=14, pad=14)
    save(fig, '01_渐变柱形图.png')


# ---------------------------------------------------------- 2 带均值柱形图
def chart02():
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    sales = np.array([2354, 1902, 3524, 2698, 2896, 2563])
    mean = sales.mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(regions, sales, width=0.55, color=PALETTE[0], zorder=2)
    ax.axhline(mean, color='#E8684A', ls='--', lw=1.8, zorder=3)
    ax.text(-0.45, mean + 45, f'平均值：{mean:,.0f}',
            color='#E8684A', fontsize=11, ha='left')
    for b, v in zip(bars, sales):
        ax.text(b.get_x() + b.get_width() / 2, v + 40, str(v),
                ha='center', fontsize=11, color=DARK)
    ax.set_ylim(0, max(sales) * 1.18)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title('各区域销售量与平均值（带均值柱形图）', fontsize=14, pad=14)
    save(fig, '02_带均值柱形图.png')


# ------------------------------------------------------ 3 渐变圆角柱形图
def chart03():
    goods = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
    sales = [653, 523, 648, 856, 714, 785]
    fig, ax = plt.subplots(figsize=(8, 5))
    cmap = LinearSegmentedColormap.from_list('g', ['#D8F6E9', '#13A87E'])
    for i, (g, v) in enumerate(zip(goods, sales)):
        p = FancyBboxPatch((i - 0.32, 0), 0.64, v,
                           boxstyle='round,pad=0,rounding_size=45',
                           fill=False, ec='none', mutation_aspect=0.02)
        ax.add_patch(p)
        im = ax.imshow(np.linspace(0, 1, 256).reshape(-1, 1), cmap=cmap,
                       extent=[i - 0.32, i + 0.32, 0, v], aspect='auto', zorder=2)
        im.set_clip_path(p)
        ax.text(i, v + 18, str(v), ha='center', fontsize=11, color=DARK)
    ax.set_xlim(-0.7, len(goods) - 0.3)
    ax.set_ylim(0, max(sales) * 1.15)
    ax.set_xticks(range(len(goods)), goods, fontsize=11)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title('各商品销量（渐变圆角柱形图）', fontsize=14, pad=14)
    save(fig, '03_渐变圆角柱形图.png')


# ---------------------------------------------------------- 4 标注柱形图
def chart04():
    goods = ['口红', '面膜', '隔离', '防晒', '精华', '面霜', '眼影', '气垫']
    sales = [9221, 5102, 6571, 5760, 6321, 8612, 2645, 5321]
    colors = [PALETTE[0] if v >= 6000 else '#A6C6F5' for v in sales]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(goods, sales, width=0.55, color=colors, zorder=2)
    for b, v in zip(bars, sales):
        ax.text(b.get_x() + b.get_width() / 2, v + 120, f'{v:,}',
                ha='center', fontsize=10.5, color=DARK)
    ax.set_ylim(0, max(sales) * 1.15)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title('各商品销量（标注柱形图）', fontsize=14, pad=14)
    save(fig, '04_标注柱形图.png')


# ---------------------------------------------------------- 5 层叠柱形图
def chart05():
    quarters = ['2021Q1', 'Q2', 'Q3', 'Q4', '2022Q1', 'Q2']
    sales = [3121, 4086, 4321, 4601, 4936, 4231]
    profit = [1020, 1421, 1502, 1623, 1781, 1432]
    sales = np.array(sales)
    profit = np.array(profit)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(quarters, sales, width=0.55, color=PALETTE[0], label='销售额', zorder=2)
    ax.bar(quarters, profit, width=0.55, bottom=sales, color=PALETTE[3],
           label='利润额', zorder=2)
    for i, (s, p) in enumerate(zip(sales, profit)):
        ax.text(i, s / 2, str(s), ha='center', va='center', fontsize=10, color='white')
        ax.text(i, s + p / 2, str(p), ha='center', va='center', fontsize=10, color=DARK)
        ax.text(i, s + p + 90, f'{s + p:,}', ha='center', fontsize=10, color=DARK)
    ax.set_ylim(0, (sales + profit).max() * 1.15)
    ax.set_yticks([])
    for s_ in ['top', 'right', 'left']:
        ax.spines[s_].set_visible(False)
    ax.tick_params(length=0)
    ax.legend(frameon=False, loc='upper right', fontsize=10)
    ax.set_title('季度销售额与利润额（层叠柱形图）', fontsize=14, pad=14)
    save(fig, '05_层叠柱形图.png')


# ---------------------------------------------------------- 6 蝴蝶图（数值）
def chart06():
    regions = ['华东', '西北', '东北', '华北', '华南']
    y2022 = [1215, 1321, 1426, 1531, 2238]
    y2021 = [1003, 1265, 1531, 1436, 2066]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    y = np.arange(len(regions))[::-1]
    ax.barh(y, [-v for v in y2022], height=0.55, color=PALETTE[0], label='2022年销量', zorder=2)
    ax.barh(y, y2021, height=0.55, color=PALETTE[4], label='2021年销量', zorder=2)
    for yi, v in zip(y, y2022):
        ax.text(-v - 40, yi, str(v), ha='right', va='center', fontsize=10.5, color=DARK)
    for yi, v in zip(y, y2021):
        ax.text(v + 40, yi, str(v), ha='left', va='center', fontsize=10.5, color=DARK)
    ax.axvline(0, color=DARK, lw=1)
    for yi, r in zip(y, regions):
        ax.text(0, yi, r, ha='center', va='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none'), zorder=3)
    xmax = max(max(y2021), max(y2022)) * 1.25
    ax.set_xlim(-xmax, xmax)
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(frameon=False, loc='lower left', bbox_to_anchor=(0.0, -0.14),
              ncol=2, fontsize=10)
    ax.set_title('各区域2021/2022年销量对比（蝴蝶图）', fontsize=14, pad=14)
    save(fig, '06_蝴蝶图_数值.png')


# ---------------------------------------------------------- 7 蝴蝶图（百分比）
def chart07():
    regions = ['华东', '西北', '东北', '华北', '华南']
    p2022 = [0.36, 0.31, 0.18, 0.13, 0.09]
    p2021 = [0.42, 0.26, 0.19, 0.12, 0.05]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    y = np.arange(len(regions))[::-1]
    ax.barh(y, [-v for v in p2022], height=0.55, color=PALETTE[0], label='2022年', zorder=2)
    ax.barh(y, p2021, height=0.55, color=PALETTE[1], label='2021年', zorder=2)
    for yi, v in zip(y, p2022):
        ax.text(-v - 0.012, yi, f'{v:.0%}', ha='right', va='center', fontsize=10.5, color=DARK)
    for yi, v in zip(y, p2021):
        ax.text(v + 0.012, yi, f'{v:.0%}', ha='left', va='center', fontsize=10.5, color=DARK)
    ax.axvline(0, color=DARK, lw=1)
    for yi, r in zip(y, regions):
        ax.text(0, yi, r, ha='center', va='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none'), zorder=3)
    ax.set_xlim(-0.55, 0.55)
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(frameon=False, loc='lower right', fontsize=10)
    ax.set_title('各区域2021/2022年占比对比（蝴蝶图）', fontsize=14, pad=14)
    save(fig, '07_蝴蝶图_百分比.png')


# ---------------------------------------------------------- 8 数值百分比
def chart08():
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    sales = [4321, 1946, 1536, 1872, 1369, 2109]
    yoy = [-0.136, -0.208, -0.093, -0.159, -0.179, -0.058]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    bars = ax.bar(regions, sales, width=0.55, color=PALETTE[0], zorder=2)
    for b, v, r in zip(bars, sales, yoy):
        ax.text(b.get_x() + b.get_width() / 2, v + 60, f'{v:,}',
                ha='center', fontsize=11, color=DARK)
        ax.text(b.get_x() + b.get_width() / 2, v / 2, f'{r:.1%}',
                ha='center', va='center', fontsize=11, color='white',
                bbox=dict(boxstyle='round,pad=0.3', fc='#E8684A', ec='none'))
    ax.set_ylim(0, max(sales) * 1.15)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title('各区域销量及同比（数值百分比图）', fontsize=14, pad=14)
    save(fig, '08_数值百分比.png')


CHARTS_1 = [chart01, chart02, chart03, chart04, chart05, chart06, chart07, chart08]

if __name__ == '__main__':
    for c in CHARTS_1:
        c()


# ---------------------------------------------------------- 9 对比柱形图
def chart09():
    goods = ['口红', '面膜', '隔离', '防晒', '精华']
    s2021 = np.array([3568, 4135, 4436, 4106, 4936])
    s2022 = np.array([2569, 3241, 2965, 3209, 3541])
    diff = s2021 - s2022
    x = np.arange(len(goods))
    w = 0.36
    fig, ax = plt.subplots(figsize=(8.5, 5))
    b1 = ax.bar(x - w / 2, s2021, w, color='#A6C6F5', label='2021销量', zorder=2)
    b2 = ax.bar(x + w / 2, s2022, w, color=PALETTE[0], label='2022销量', zorder=2)
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 60,
                f'{b.get_height():,.0f}', ha='center', fontsize=9.5, color=DARK)
    for xi, d, h in zip(x, diff, np.maximum(s2021, s2022)):
        ax.annotate(f'差值\n{d:,}', xy=(xi, h + 420), ha='center', fontsize=10,
                    color='#E8684A',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#E8684A'))
    ax.set_xticks(x, goods, fontsize=11)
    ax.set_ylim(0, max(s2021) * 1.34)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.legend(frameon=False, loc='upper left', fontsize=10)
    ax.set_title('各商品2021/2022销量对比（对比柱形图）', fontsize=14, pad=14)
    save(fig, '09_对比柱形图.png')


# ---------------------------------------------------------- 10 甘特图
def chart10():
    tasks = ['制定计划', '方案设计', '资源调配', '第一阶段', '第二阶段', '第三阶段', '项目总结']
    starts = [datetime(2022, 3, 1), datetime(2022, 3, 13), datetime(2022, 3, 22),
              datetime(2022, 4, 2), datetime(2022, 4, 16), datetime(2022, 5, 11),
              datetime(2022, 5, 26)]
    days = [11, 8, 10, 13, 24, 14, 7]
    prog = [0.51, 0.32, 0.21, 0.85, 0.36, 0.68, 0.68]
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, (t, s, d, p) in enumerate(zip(tasks, starts, days, prog)):
        y = len(tasks) - 1 - i
        s_num = mdates.date2num(s)
        ax.barh(y, d, left=s_num, height=0.5, color='#DCE6F5', zorder=2)
        ax.barh(y, d * p, left=s_num, height=0.5, color=PALETTE[0], zorder=3)
        ax.text(s_num + d + 0.8, y, f'{p:.0%}', va='center', fontsize=10,
                color=PALETTE[0])
        ax.text(s_num - 1.0, y, t, va='center', ha='right', fontsize=11, color=DARK)
    ax.set_yticks([])
    ax.set_xlim(mdates.date2num(datetime(2022, 2, 20)), mdates.date2num(datetime(2022, 6, 12)))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.grid(axis='x', color='#E8E8E8', lw=0.8, zorder=0)
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    for lbl in ax.get_xticklabels():
        lbl.set_fontsize(9)
    ax.set_title('项目进度（甘特图）', fontsize=14, pad=14)
    save(fig, '10_甘特图.png')


# ---------------------------------------------------------- 11 平滑折线图
def chart11():
    months = ['5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月', '2月', '3月']
    sales = [146, 198, 296, 412, 506, 615, 789, 1021, 3782, 3215, 2936]
    x = np.arange(len(months))
    x_smooth = np.linspace(x.min(), x.max(), 300)
    spl = make_interp_spline(x, sales, k=3)
    y_smooth = spl(x_smooth)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x_smooth, y_smooth, color=PALETTE[0], lw=2.5, zorder=3)
    ax.fill_between(x_smooth, y_smooth, 0, color=PALETTE[0], alpha=0.12, zorder=1)
    ax.scatter(x, sales, s=45, color=PALETTE[0], zorder=4, edgecolor='white', lw=1.2)
    for xi, v in zip(x, sales):
        ax.text(xi, v + 110, str(v), ha='center', fontsize=9.5, color=DARK)
    ax.set_xticks(x, months, fontsize=10.5)
    ax.set_ylim(0, max(sales) * 1.2)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title('月度销量（平滑折线图）', fontsize=14, pad=14)
    save(fig, '11_平滑折线图.png')


# ---------------------------------------------------------- 12 菱形走势图
def chart12():
    months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月']
    rates = [0.536, 0.498, 0.527, 0.708, 0.609, 0.496, 0.586, 0.704]
    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(x, rates, color=PALETTE[0], lw=2, zorder=3)
    ax.fill_between(x, rates, 0.4, color=PALETTE[0], alpha=0.10, zorder=1)
    ax.scatter(x, rates, s=180, marker='D', color=PALETTE[0],
               edgecolor='white', lw=1.5, zorder=4)
    for xi, v in zip(x, rates):
        off = 0.028 if v < 0.65 else -0.038
        va = 'bottom' if v < 0.65 else 'top'
        ax.text(xi, v + off, f'{v:.1%}', ha='center', va=va, fontsize=10, color=DARK)
    ax.set_xticks(x, months, fontsize=10.5)
    ax.set_ylim(0.4, 0.8)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title('月度完成率（菱形走势图）', fontsize=14, pad=14)
    save(fig, '12_菱形走势图.png')


# ---------------------------------------------------------- 13 对比折线图
def chart13():
    months = ['1月', '2月', '3月', '4月', '5月', '6月']
    y2021 = [1686, 1345, 1934, 1658, 1865, 1936]
    y2022 = [1385, 1846, 1654, 1936, 2564, 2236]
    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.plot(x, y2021, color=GRAY, lw=2, marker='o', ms=6, label='2021年', zorder=3)
    ax.plot(x, y2022, color=PALETTE[4], lw=2.5, marker='o', ms=6, label='2022年', zorder=3)
    for xi, v in zip(x[:-1], y2021[:-1]):
        ax.text(xi, v - 130, str(v), ha='center', fontsize=9.5, color='#7F7F7F')
    for xi, v in zip(x[:-1], y2022[:-1]):
        ax.text(xi, v + 60, str(v), ha='center', fontsize=9.5, color=PALETTE[4])
    ax.text(len(months) - 0.82, y2021[-1] - 25, '2021年', fontsize=10.5,
            color='#7F7F7F', va='center')
    ax.text(len(months) - 0.82, y2022[-1] + 55, '2022年', fontsize=10.5,
            color=PALETTE[4], va='center')
    ax.set_xlim(-0.2, len(months) + 0.15)
    ax.set_xticks(x, months, fontsize=11)
    ax.set_ylim(min(y2021) * 0.7, max(y2022) * 1.15)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title('月度数据对比（对比折线图）', fontsize=14, pad=14)
    save(fig, '13_对比折线图.png')


# ---------------------------------------------------------- 14 单值圆环图
def chart14():
    rate = 0.85
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.pie([rate, 1 - rate], startangle=90, counterclock=False,
           colors=[PALETTE[0], '#EDF2FA'],
           wedgeprops=dict(width=0.32, edgecolor='white', lw=2))
    ax.text(0, 0.06, f'{rate:.0%}', ha='center', va='center',
            fontsize=34, color=PALETTE[0], weight='bold')
    ax.text(0, -0.20, '完成率', ha='center', va='center', fontsize=13, color='#7F7F7F')
    ax.set_title('完成率（单值圆环图）', fontsize=14, pad=14)
    save(fig, '14_单值圆环图.png')


# ---------------------------------------------------------- 15 水球图
def liquid_ball(ax, rate, wave=True, color='#2E7CE6'):
    r = 1.0
    circle = Circle((0, 0), r, fill=False, lw=0)
    ax.add_patch(circle)
    level = -r + 2 * r * rate
    x = np.linspace(-r, r, 400)
    if wave:
        y_surface = level + 0.045 * np.sin(2 * np.pi * (x + 0.18) / 0.55)
    else:
        y_surface = np.full_like(x, level)
    y_surface = np.clip(y_surface, -r, r)
    verts = np.concatenate([
        np.column_stack([x, y_surface]),
        [[r, -r], [-r, -r]]
    ])
    poly = plt.Polygon(verts, closed=True, color=color, alpha=0.85, zorder=2)
    ax.add_patch(poly)
    poly.set_clip_path(circle)
    ax.add_patch(Circle((0, 0), r, fill=False, ec=color, lw=3, zorder=4))
    ax.text(0, -0.10, f'{rate:.0%}', ha='center', va='center',
            fontsize=30, color=color, weight='bold', zorder=5,
            path_effects=[pe.withStroke(linewidth=4, foreground='white')])
    ax.text(0, -0.42, '完成率', ha='center', va='center', fontsize=12,
            color='#7F7F7F', zorder=5,
            path_effects=[pe.withStroke(linewidth=3, foreground='white')])


def chart15():
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    liquid_ball(ax, 0.65, wave=False, color='#13A87E')
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect('equal')
    strip_axes(ax)
    ax.set_title('完成率（水球图）', fontsize=14, pad=12)
    save(fig, '15_水球图.png')


CHARTS_2 = [chart09, chart10, chart11, chart12, chart13, chart14, chart15]


# ---------------------------------------------------------- 16 波浪水球图
def chart16():
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    liquid_ball(ax, 0.65, wave=True, color='#2E7CE6')
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect('equal')
    strip_axes(ax)
    ax.set_title('完成率（波浪水球图）', fontsize=14, pad=12)
    save(fig, '16_波浪水球图.png')


# ---------------------------------------------------------- 17 玉玦图
def chart17():
    labels = ['>=50', '[40,50)', '[30,40)', '[20,30)']
    values = [0.125, 0.2083333, 0.2916667, 0.375]
    colors = ['#F6BD16', '#5AD8A6', '#5B8FF9', '#9270CA']
    r0, scale, rmax = 1.0, 2.2, 1.0 + 2.2 * 0.375
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    total = sum(values)
    ang = 0.0
    for lab, v, c in zip(labels, values, colors):
        width = v / total * 2 * np.pi
        ax.barh(r0, width, height=scale * v, left=ang, color=c, zorder=3)
        ax.barh(r0 + scale * v, width, height=scale * (max(values) - v),
                left=ang, color='#EDF0F5', zorder=2)
        mid = ang + width / 2
        ax.text(mid, r0 + scale * max(values) + 0.35, f'{lab}\n{v:.1%}',
                ha='center', va='center', fontsize=10.5, color=DARK)
        ang += width
    ax.set_ylim(0, rmax + 1.0)
    ax.set_thetagrids([])
    ax.set_rgrids([])
    ax.grid(False)
    ax.spines['polar'].set_visible(False)
    ax.set_title('年龄分布（玉玦图）', fontsize=14, pad=22)
    save(fig, '17_玉玦图.png')


# ---------------------------------------------------------- 18 跑道图
def chart18():
    depts = ['人力部', '行政部', '财务部', '工程部', '采购部', '销售部']
    nums = [130, 226, 238, 293, 326, 451]
    total = max(n + p for n, p in zip(nums, [702, 606, 594, 539, 506, 381]))
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(depts))[::-1]
    h = 0.52
    for yi, d, n in zip(y, depts, nums):
        ax.add_patch(FancyBboxPatch((0, yi - h / 2), total, h,
                                    boxstyle='round,pad=0,rounding_size=0.26',
                                    fc='#EDF0F5', ec='none', zorder=1))
        ax.add_patch(FancyBboxPatch((0, yi - h / 2), n, h,
                                    boxstyle='round,pad=0,rounding_size=0.26',
                                    fc=PALETTE[0], ec='none', zorder=2))
        ax.text(n + 12, yi, str(n), va='center', fontsize=11, color=PALETTE[0])
        ax.text(-12, yi, d, va='center', ha='right', fontsize=11, color=DARK)
    ax.set_xlim(-90, total * 1.08)
    ax.set_ylim(-0.7, len(depts) - 0.3)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title('各部门人数（跑道图）', fontsize=14, pad=14)
    save(fig, '18_跑道图.png')


# ---------------------------------------------------------- 19 南丁格尔圆饼图
def nightingale(ax, labels, values, colors, donut=False, r_base=1.0, r_scale=4.0):
    total = sum(values)
    ang = 90.0
    r_inner = 0.55 if donut else 0.0
    for lab, v, c in zip(labels, values, colors):
        width = v / total * 360
        r = r_base + r_scale * v
        ax.add_patch(Wedge((0, 0), r, ang - width, ang, width=r - r_inner,
                           facecolor=c, edgecolor='white', lw=1.5))
        mid = np.deg2rad(ang - width / 2)
        lr = (r + r_inner) / 2 if donut else r * 0.62
        ax.text(lr * np.cos(mid), lr * np.sin(mid), f'{lab}\n{v:.1%}',
                ha='center', va='center', fontsize=9.5,
                color='white' if not donut else DARK)
        ang -= width


def chart19():
    labels = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
    values = [0.292, 0.227, 0.175, 0.136, 0.103, 0.067]
    colors = ['#2E7CE6', '#13A87E', '#F6BD16', '#9270CA', '#FF9D4D', '#5D7092']
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    nightingale(ax, labels, values, colors, donut=False)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.6)
    ax.set_aspect('equal')
    strip_axes(ax)
    ax.set_title('各部门人数占比（南丁格尔圆饼图）', fontsize=14, pad=12)
    save(fig, '19_南丁格尔圆饼图.png')


# ---------------------------------------------------------- 20 南丁格尔圆环图
def chart20():
    labels = ['[20,30)', '[30,40)', '[40,50)', '>=50']
    values = [0.375, 0.2916667, 0.2083333, 0.125]
    colors = ['#2E7CE6', '#13A87E', '#F6BD16', '#9270CA']
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    nightingale(ax, labels, values, colors, donut=True)
    ax.text(0, 0, '年龄\n分布', ha='center', va='center', fontsize=14, color='#7F7F7F')
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.6)
    ax.set_aspect('equal')
    strip_axes(ax)
    ax.set_title('年龄占比（南丁格尔圆环图）', fontsize=14, pad=12)
    save(fig, '20_南丁格尔圆环图.png')


# ------------------------------------------------------ 20(PPT) 南丁格尔玫瑰图
def chart21():
    labels = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
    values = [0.292, 0.227, 0.175, 0.136, 0.103, 0.05]
    colors = ['#2E7CE6', '#13A87E', '#F6BD16', '#9270CA', '#FF9D4D', '#5D7092']
    fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True))
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    total = sum(values)
    ang = 0.0
    for lab, v, c in zip(labels, values, colors):
        width = v / total * 2 * np.pi
        ax.bar(ang + width / 2, v, width=width * 0.92, bottom=0.12,
               color=c, edgecolor='white', lw=1.2, zorder=3)
        ax.text(ang + width / 2, v + 0.045, f'{lab}\n{v:.1%}', ha='center',
                va='bottom', fontsize=9.5, color=DARK)
        ang += width
    ax.set_ylim(0, max(values) * 1.35)
    ax.set_thetagrids([])
    ax.set_rgrids([])
    ax.grid(False)
    ax.spines['polar'].set_visible(False)
    ax.set_title('各部门人数占比（南丁格尔玫瑰图）', fontsize=14, pad=26)
    save(fig, '21_南丁格尔玫瑰图_PPT版.png')


# ---------------------------------------------------------- 22 仪表盘图
def chart22():
    vmin, vmax, value = 50, 150, 76
    fig, ax = plt.subplots(figsize=(8, 5.5))
    def angle(v):
        return 225 - (v - vmin) / (vmax - vmin) * 270
    # 外圈弧带（分段配色：低-中-高）
    bands = [(50, 75, '#13A87E'), (75, 100, '#F6BD16'), (100, 150, '#E8684A')]
    for b0, b1, c in bands:
        ax.add_patch(Wedge((0, 0), 1.0, angle(b1), angle(b0), width=0.16,
                           facecolor=c, alpha=0.85))
    ax.add_patch(Wedge((0, 0), 0.80, -45, 225, width=0.02, facecolor='#D9D9D9'))
    # 刻度
    for v in range(vmin, vmax + 1, 10):
        a = np.deg2rad(angle(v))
        x0, y0 = 0.62 * np.cos(a), 0.62 * np.sin(a)
        x1, y1 = 0.72 * np.cos(a), 0.72 * np.sin(a)
        ax.plot([x0, x1], [y0, y1], color=DARK, lw=1.4)
        ax.text(0.50 * np.cos(a), 0.50 * np.sin(a), str(v), ha='center',
                va='center', fontsize=9.5, color=DARK)
    # 指针
    a = np.deg2rad(angle(value))
    ax.add_patch(FancyArrowPatch((0, 0), (0.58 * np.cos(a), 0.58 * np.sin(a)),
                                 arrowstyle='-|>', mutation_scale=18,
                                 color=DARK, lw=2.5, zorder=5))
    ax.add_patch(Circle((0, 0), 0.045, color=DARK, zorder=6))
    ax.text(0, -0.33, f'{value}', ha='center', fontsize=26, color=PALETTE[0],
            weight='bold')
    ax.text(0, -0.52, '指针数值', ha='center', fontsize=11, color='#7F7F7F')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.75, 1.15)
    ax.set_aspect('equal')
    strip_axes(ax)
    ax.set_title('完成度（仪表盘图）', fontsize=14, pad=10)
    save(fig, '22_仪表盘图.png')


# ---------------------------------------------------------- 23 柱形折线图
def chart23():
    years = ['2017', '2018', '2019', '2020', '2021', '2022']
    sales = [1603, 2106, 2406, 3265, 3721, 3921]
    yoy = [0.27, 0.3138, 0.1425, 0.3570, 0.1397, 0.0537]
    x = np.arange(len(years))
    fig, ax = plt.subplots(figsize=(8.5, 5))
    bars = ax.bar(x, sales, width=0.5, color=PALETTE[0], label='销售量', zorder=2)
    for b, v in zip(bars, sales):
        ax.text(b.get_x() + b.get_width() / 2, v + 60, str(v),
                ha='center', fontsize=10, color=DARK)
    ax.set_ylim(0, max(sales) * 1.2)
    ax.set_yticks([])
    ax.set_xticks(x, years, fontsize=11)
    ax.set_xlim(-0.6, len(years) - 0.4)
    ax2 = ax.twinx()
    ax2.plot(x, yoy, color=PALETTE[4], lw=2.5, marker='o', ms=6,
             label='同比', zorder=3)
    for xi, v in zip(x, yoy):
        ax2.text(xi, v + 0.012, f'{v:.1%}', ha='center', fontsize=9.5,
                 color=PALETTE[4])
    ax2.set_ylim(0, max(yoy) * 1.45)
    ax2.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
        ax2.spines[s].set_visible(False)
    ax.tick_params(length=0)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc='upper left', fontsize=10)
    ax.set_title('年度销售量及同比（柱形折线图）', fontsize=14, pad=14)
    save(fig, '23_柱形折线图.png')


CHARTS_3 = [chart16, chart17, chart18, chart19, chart20, chart21, chart22, chart23]


# ---------------------------------------------------------- 24 目标柱形图
def chart24():
    goods = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
    actual = np.array([653, 523, 648, 856, 714, 785])
    target = np.array([700, 500, 600, 900, 600, 600])
    ratio = actual / target
    x = np.arange(len(goods))
    w = 0.5
    fig, ax = plt.subplots(figsize=(8.5, 5))
    # 目标：描边框（空心柱）
    for xi, t in zip(x, target):
        ax.add_patch(FancyBboxPatch((xi - w / 2, 0), w, t,
                                    boxstyle='round,pad=0,rounding_size=0.02',
                                    fill=False, ec='#E8684A', lw=1.8, zorder=3))
    bars = ax.bar(x, actual, width=w, color=PALETTE[0], zorder=2, label='实际销量')
    for xi, a, t, r in zip(x, actual, target, ratio):
        ax.text(xi - 0.14, a + 22, f'{a}', ha='center', fontsize=10,
                color=PALETTE[0])
        ax.text(xi + 0.14, t + 22, f'{t}', ha='center', fontsize=10,
                color='#E8684A')
        ax.annotate(f'达成率 {r:.0%}', xy=(xi, 0), xytext=(0, -42),
                    textcoords='offset points', ha='center', fontsize=9,
                    color='white',
                    bbox=dict(boxstyle='round,pad=0.3',
                              fc=PALETTE[1] if r >= 1 else '#F6BD16', ec='none'))
    ax.set_xticks(x, goods, fontsize=11)
    ax.tick_params(length=0)
    ax.set_ylim(0, max(target.max(), actual.max()) * 1.22)
    ax.set_yticks([])
    ax.set_xlim(-0.6, len(goods) - 0.4)
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.legend(handles=[bars,
                       Rectangle((0, 0), 1, 1, fill=False, ec='#E8684A', lw=1.8)],
              labels=['实际销量', '目标销量'], frameon=False, loc='upper right',
              fontsize=10)
    ax.set_title('各商品实际销量 vs 目标销量（目标柱形图）', fontsize=14, pad=14)
    save(fig, '24_目标柱形图.png')


# ---------------------------------------------------------- 25 子弹图
def chart25():
    goods = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
    actual = [653, 523, 648, 856, 714, 785]
    target = [700, 500, 600, 900, 600, 600]
    bands = [(600, 200, 200)] * len(goods)  # 及格600/良好200/优秀200（层叠）
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(goods))[::-1]
    h = 0.5
    band_colors = ['#D6E4F5', '#A9C8F0', '#7FAEEB']
    for yi, (a, t, (pass_, good, excel)) in enumerate(
            zip(actual, target, bands)):
        edges = [0, excel, excel + good, excel + good + pass_]
        for j in range(3):
            ax.barh(y[yi], edges[j + 1] - edges[j], left=edges[j],
                    height=h * 1.7, color=band_colors[j], zorder=1)
        ax.barh(y[yi], a, height=h, color='#2E5E8C', zorder=3)
        ax.plot([t, t], [y[yi] - h * 0.9, y[yi] + h * 0.9], color='#E8684A',
                lw=2.2, zorder=4)
        ax.text(edges[-1] + 25, y[yi], f'{a}', va='center', fontsize=10.5,
                color=DARK)
        ax.text(-25, y[yi], goods[yi], va='center', ha='right', fontsize=11,
                color=DARK)
    ax.set_xlim(-110, 1100)
    ax.set_ylim(-0.7, len(goods) - 0.3)
    ax.set_xticks([0, 200, 400, 600, 800, 1000])
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.legend(handles=[Rectangle((0, 0), 1, 1, fc=band_colors[2]),
                       Rectangle((0, 0), 1, 1, fc='#2E5E8C'),
                       plt.Line2D([0], [0], color='#E8684A', lw=2.2)],
              labels=['评价区间（优秀/良好/及格）', '实际', '目标'],
              frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.06),
              fontsize=9.5, ncol=3)
    ax.set_title('各商品实际 vs 目标（子弹图）', fontsize=14, pad=14)
    save(fig, '25_子弹图.png')


# ---------------------------------------------------------- 26 柱形圆
def chart26():
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    sales = [2354, 1902, 3524, 2698, 2896, 2563]
    yoy = [0.12, 0.25, 0.16, 0.21, 0.18, 0.25]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    bars = ax.bar(regions, sales, width=0.5, color=PALETTE[0], zorder=2)
    for b, v, r in zip(bars, sales, yoy):
        cx = b.get_x() + b.get_width() / 2
        ax.scatter(cx, v, s=1050, marker='o', facecolor='white',
                   edgecolor=PALETTE[4], linewidth=2.2, zorder=4)
        ax.annotate(f'{r:.0%}', xy=(cx, v), ha='center', va='center',
                    fontsize=10, color=PALETTE[4], zorder=5)
        ax.text(cx, v - 150, str(v), ha='center', va='top', fontsize=10,
                color='white', zorder=5)
    ax.set_ylim(0, max(sales) * 1.22)
    ax.set_yticks([])
    ax.set_xticks(range(len(regions)), regions, fontsize=11)
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title('各区域销量及同比（柱形圆）', fontsize=14, pad=20)
    save(fig, '26_柱形圆.png')


# ---------------------------------------------------------- 27 簇状柱形折线图
def chart27():
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    s2022 = [2354, 1902, 3524, 2698, 2896, 2563]
    s2021 = [2021, 1563, 3213, 2531, 2631, 2361]
    yoy = [0.16, 0.22, 0.10, 0.07, 0.10, 0.09]
    x = np.arange(len(regions))
    w = 0.34
    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.bar(x - w / 2, s2022, w, color=PALETTE[0], label='2022销量', zorder=2)
    ax.bar(x + w / 2, s2021, w, color='#A6C6F5', label='2021销量', zorder=2)
    for xi, v in zip(x, s2022):
        ax.text(xi - w / 2, v + 55, str(v), ha='center', fontsize=9, color=DARK)
    for xi, v in zip(x, s2021):
        ax.text(xi + w / 2, v + 55, str(v), ha='center', fontsize=9, color=DARK)
    ax.set_ylim(0, max(s2022) * 1.2)
    ax.set_yticks([])
    ax.set_xticks(x, regions, fontsize=11)
    ax2 = ax.twinx()
    ax2.plot(x, yoy, color=PALETTE[4], lw=2.2, marker='o', ms=6, label='同比去年')
    for xi, v in zip(x, yoy):
        ax2.text(xi, v + 0.012, f'{v:.0%}', ha='center', fontsize=9,
                 color=PALETTE[4])
    ax2.set_ylim(0, max(yoy) * 2.6)
    ax2.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
        ax2.spines[s].set_visible(False)
    ax.tick_params(length=0)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc='upper right', fontsize=9.5,
              ncol=3)
    ax.set_title('各区域2021/2022销量及同比（簇状柱形折线图）', fontsize=14, pad=14)
    save(fig, '27_簇状柱形折线图.png')


# ---------------------------------------------------------- 28 复合柱形图
def chart28():
    months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月',
              '10月', '11月', '12月']
    monthly = [2354, 1902, 3524, 2698, 2896, 2563, 3156, 2896, 3621,
               2635, 2963, 2789]
    quarterly = [7780] * 3 + [8157] * 3 + [9673] * 3 + [8387] * 3
    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x, quarterly, width=0.88, color='#A6C6F5', label='季度销量', zorder=2)
    ax.bar(x, monthly, width=0.4, color=PALETTE[0], label='月度销量', zorder=3)
    for xi, v in zip(x, monthly):
        ax.text(xi, v + 80, str(v), ha='center', fontsize=8.5, color=DARK)
    for qi in [1, 4, 7, 10]:
        ax.text(qi, quarterly[qi] + 60, f'季度合计：{quarterly[qi]}',
                ha='center', fontsize=9.5, color='#2E7CE6')
    ax.set_xticks(x, months, fontsize=10)
    ax.set_ylim(0, max(quarterly) * 1.18)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.legend(frameon=False, loc='upper right', fontsize=10)
    ax.set_title('月度销量与季度销量（复合柱形图）', fontsize=14, pad=14)
    save(fig, '28_复合柱形图.png')


# ---------------------------------------------------------- 29 滑珠图
def bead_chart(path, regions, series_list, series_names, series_colors,
               xmax=1.0, fname=''):
    n = len(regions)
    fig, ax = plt.subplots(figsize=(9, 0.9 * n + 1.6))
    y = np.arange(n)[::-1] * 2
    h = 0.5
    for yi, r in zip(y, regions):
        ax.add_patch(FancyBboxPatch((0, yi - h / 2), xmax, h,
                                    boxstyle='round,pad=0,rounding_size=0.25',
                                    fc='#EDF0F5', ec='none', zorder=1))
        ax.text(-0.025, yi, r, ha='right', va='center', fontsize=12, color=DARK)
    for values, name, color, dy in zip(series_list, series_names,
                                       series_colors, [-0.28, 0.28]):
        for yi, v in zip(y, values):
            if len(series_list) == 1:
                ax.add_patch(FancyBboxPatch((0, yi - h / 2), v, h,
                                            boxstyle='round,pad=0,rounding_size=0.25',
                                            fc=color, ec='none', alpha=0.35,
                                            zorder=2))
                yc = yi
            else:
                yc = yi + dy
            ax.scatter(v, yc, s=230, color=color, zorder=4,
                       edgecolor='white', lw=1.6)
            ax.text(v, yc, f'{v:.0%}', ha='center', va='center', fontsize=8.5,
                    color='white', zorder=5)
    ax.set_xlim(-0.13, xmax * 1.13)
    ax.set_ylim(-1, y[0] + (1.4 if len(series_list) > 1 else 1.0))
    ax.set_yticks([])
    ax.set_xticks(np.linspace(0, xmax, 6),
                  [f'{t:.0%}' for t in np.linspace(0, xmax, 6)], fontsize=10)
    ax.tick_params(length=0)
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    if len(series_list) > 1:
        ax.legend(handles=[plt.Line2D([0], [0], marker='o', ls='', ms=10,
                                      color=c) for c in series_colors],
                  labels=series_names, frameon=False, loc='lower right',
                  fontsize=10, ncol=len(series_list))
    ax.set_title(path, fontsize=14, pad=12)
    save(fig, fname)


def chart29():
    regions = ['华东', '西北', '东北', '华北', '华南']
    rates = [0.35, 0.51, 0.62, 0.74, 0.86]
    bead_chart('各区域完成率（滑珠图）', regions, [rates], ['完成率'],
               [PALETTE[0]], fname='29_滑珠图.png')


# ---------------------------------------------------------- 30 对比滑珠图
def chart30():
    regions = ['华东', '西北', '东北', '华北', '华南']
    r2022 = [0.35, 0.51, 0.62, 0.74, 0.86]
    r2021 = [0.45, 0.39, 0.53, 0.69, 0.92]
    bead_chart('各区域2021/2022完成率（对比滑珠图）', regions,
               [r2022, r2021], ['2022完成率', '2021完成率'],
               [PALETTE[0], PALETTE[3]], fname='30_对比滑珠图.png')


CHARTS_4 = [chart24, chart25, chart26, chart27, chart28, chart29, chart30]

ALL_CHARTS = CHARTS_1 + CHARTS_2 + CHARTS_3 + CHARTS_4

if __name__ == '__main__':
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    for i, c in enumerate(ALL_CHARTS, start=1):
        if only and i not in only:
            continue
        c()
    print(f'\n完成：{len(ALL_CHARTS)} 个图表 -> {OUT}')
