"""OMD 图表样式配置 — 供 gen_chart.py 使用

标准化的 matplotlib 图表样式，确保所有报告图表风格统一。
"""
import matplotlib
import matplotlib.pyplot as plt

# ===== 中文字体配置 =====
matplotlib.rcParams["font.sans-serif"] = ["SimHei", "STHeiti", "PingFang SC", "Arial"]
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["figure.dpi"] = 150
matplotlib.rcParams["savefig.dpi"] = 150
matplotlib.rcParams["savefig.bbox"] = "tight"

# ===== 配色方案 =====
COLORS = {
    "primary": "#2563EB",     # 主色 — 蓝
    "secondary": "#7C3AED",   # 辅色 — 紫
    "accent": "#EC4899",      # 强调 — 粉
    "success": "#10B981",     # 成功 — 绿
    "warning": "#F59E0B",     # 警告 — 橙
    "danger": "#EF4444",      # 危险 — 红
    "neutral": "#6B7280",     # 中性 — 灰
}

# 柱状图/折线图多色序列
PALETTE = ["#2563EB", "#7C3AED", "#EC4899", "#10B981", "#F59E0B", "#EF4444", "#06B6D4"]

# ===== 图表尺寸 =====
FIG_SIZES = {
    "full": (10, 6),      # 全宽图
    "half": (6, 4),       # 半宽图
    "square": (6, 6),     # 正方形
    "wide": (12, 5),      # 宽图（对比）
    "tall": (6, 8),       # 高图
}

# ===== 通用样式 =====
STYLE = {
    "title_size": 14,
    "label_size": 12,
    "tick_size": 10,
    "legend_size": 10,
    "grid_alpha": 0.3,
    "bar_width": 0.35,
    "line_width": 2,
    "marker_size": 6,
}


def apply_style(ax, title="", xlabel="", ylabel="", grid=True):
    """应用统一样式到坐标轴"""
    if title:
        ax.set_title(title, fontsize=STYLE["title_size"], fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=STYLE["label_size"])
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=STYLE["label_size"])
    ax.tick_params(labelsize=STYLE["tick_size"])
    if grid:
        ax.grid(True, alpha=STYLE["grid_alpha"], linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(fig, path, tight=True):
    """保存图表"""
    if tight:
        fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    print(f"[OMD] Chart saved: {path}")
