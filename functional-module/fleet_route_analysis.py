import os

import folium
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import rcParams

# 设置中文字体
rcParams['font.family'] = 'Microsoft YaHei'
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 文件路径
input_file = r"F:\八打雁\aft\八打雁202307_zscore_cleaned.xlsx"
output_dir = r"F:\八打雁\pic"

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 读取数据
try:
    df = pd.read_excel(input_file)
    print(f"数据加载成功，总行数：{len(df)}")
except Exception as e:
    print(f"读取文件失败: {e}")
    exit()

# 数据清洗与预处理
try:
    df["PCDateTime"] = pd.to_datetime(df["PCDate"] + " " + df["PCTime"])
    df["Latitude"] = df["Latitude"].str.replace(" N", "").astype(float)  # 将纬度转换为浮点数
    df["Longitude"] = df["Longitude"].str.replace(" E", "").astype(float)  # 将经度转换为浮点数
except Exception as e:
    print(f"数据预处理失败: {e}")
    exit()

# 航线地图可视化

def plot_route_on_map(df, save_path):
    """
    将航线数据绘制到地图上
    """
    # 创建地图对象
    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=12)
    
    points = df[["Latitude", "Longitude"]].values.tolist()
    
    # 设定每100条航线段使用不同的透明度进行绘制
    num_segments = len(points) - 1
    color = "blue"  # 使用单一颜色进行绘制
    opacity_step = 0.7  # 每20条航线段增加透明度
    opacity = 0.2  # 初始透明度
    
    # 绘制航线段
    for i in range(num_segments):
        # 每100段航线改变透明度
        if i % 100 == 0 and opacity < 1.0:
            opacity += opacity_step  # 增加透明度
        
        # 绘制每条航线段，并设置透明度
        folium.PolyLine([points[i], points[i+1]], color=color, weight=2.5, opacity=opacity).add_to(m)
    
    # 添加起点和终点标记
    folium.Marker(points[0], popup="Start Point", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(points[-1], popup="End Point", icon=folium.Icon(color="red")).add_to(m)
    
    # 保存地图
    m.save(save_path)
    print(f"航线地图已保存到: {save_path}")

# 航速折线图
def plot_speed_trend(df, save_path):
    """
    绘制航速折线图
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df["PCDateTime"], df["ShipSpd"], label="航速 (对地) [节]", color="blue", linewidth=2)
    plt.plot(df["PCDateTime"], df["ShipSpdToWater"], label="航速 (对水) [节]", color="orange", linestyle="--", linewidth=2)
    plt.title("航速趋势图", fontsize=16)
    plt.xlabel("时间 [年-月-日 时:分:秒]", fontsize=14)
    plt.ylabel("航速 (节)", fontsize=14)
    plt.legend(fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    print(f"航速折线图已保存到: {save_path}")
    plt.close()

# 船速分布直方图
def plot_speed_distribution(df, save_path):
    """
    绘制船速分布图
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df["ShipSpd"], kde=True, color="blue", bins=30)
    plt.title("航速分布图", fontsize=16)
    plt.xlabel("航速 (节)", fontsize=14)
    plt.ylabel("频次", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    print(f"航速分布图已保存到: {save_path}")
    plt.close()

# 航向统计分析
def plot_wind_direction_distribution(df, save_path):
    """
    绘制航向分布图
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df["WindDir"], kde=False, color="green", bins=36)
    plt.title("航向分布图", fontsize=16)
    plt.xlabel("航向 (度)", fontsize=14)
    plt.ylabel("频次", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    print(f"航向分布图已保存到: {save_path}")
    plt.close()

# 燃油消耗趋势分析
def plot_fuel_consumption_trend(df, save_path):
    """
    绘制燃油消耗趋势图
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df["PCDateTime"], df["MEActFOCons"], label="主机燃油消耗 [吨]", color="red")
    plt.plot(df["PCDateTime"], df["DGActFOCons"], label="发电机燃油消耗 [吨]", color="blue")
    plt.plot(df["PCDateTime"], df["BlrActFOCons"], label="锅炉燃油消耗 [吨]", color="green")
    plt.title("燃油消耗趋势", fontsize=16)
    plt.xlabel("时间 [年-月-日 时:分:秒]", fontsize=14)
    plt.ylabel("燃油消耗 (吨)", fontsize=14)
    plt.legend(fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    print(f"燃油消耗趋势图已保存到: {save_path}")
    plt.close()

# 调用各分析功能并保存结果
try:
    plot_route_on_map(df, os.path.join(output_dir, "航线地图.html"))
    # plot_speed_trend(df, os.path.join(output_dir, "航速折线图.png"))
    # plot_speed_distribution(df, os.path.join(output_dir, "航速分布图.png"))
    # plot_wind_direction_distribution(df, os.path.join(output_dir, "航向分布图.png"))
    # plot_fuel_consumption_trend(df, os.path.join(output_dir, "燃油消耗趋势图.png"))
    # print("所有分析完成，结果已保存。")
except Exception as e:
    print(f"分析过程中出错: {e}")
