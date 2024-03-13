
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts


image_path = '/Users/apple/Downloads/510_final_project/1.png'
df = pd.read_csv('pal_index.csv')



col1, col2 = st.columns([1, 5])  

with col1: 
    st.image(image_path, width=100)  

with col2: 
    st.title('Palworld Pal Stats Calculator')

#定义数值计算函数
def Pal_basic(lv=0, hpsss=0, atksss=0, defsss=0, hpiv=0.15, atkiv=0.15, defiv=0.15):
    
    hp = 500 + lv * (5 + hpsss * 0.5 * (1 + hpiv))
    atk = 100 + lv * atksss * 0.075 * (1 + atkiv)
    defense = 50 + lv * defsss * 0.075 * (1 + defiv)

    return hp, atk, defense

def calculate_stats(pal_name, level):
    # 从数据框中获取指定Pal的种族值
    base_stats = df.loc[df['Name'] == pal_name, ['Atk', 'HP', 'Def']].iloc[0]
    # 定义三维对应的增长率
    growth_rates = {'Atk': 0.075, 'HP': 0.5, 'Def': 0.075}
    # 定义不同属性的基础值
    base_values = {'Atk': 100, 'HP': 500, 'Def': 50}
    stats_at_level = {}
    for stat in base_stats.index:
        growth = growth_rates[stat]
        racial_value = base_stats[stat]
        base_value = base_values[stat]

        stats_at_level[stat] = base_value + ((racial_value * growth) * level)
    return stats_at_level

selected_pal = st.selectbox('Select the 1st Pal', ['Choose a Pal'] + list(df['Name'].unique()))
comparison_pal = st.selectbox('Select the 2nd Pal', ['Choose a Pal'] + list(df['Name'].unique()))

if selected_pal != 'Choose a Pal' or comparison_pal != 'Choose a Pal':
    level = st.slider('Select Level', 1, 50, 25)
    if selected_pal != 'Choose a Pal':
        selected_stats = calculate_stats(selected_pal, level)
       
    if comparison_pal != 'Choose a Pal':
        comparison_stats = calculate_stats(comparison_pal, level)
       

    name1 = selected_pal
    name2 = comparison_pal
    selected_level = level
    levels = range(1, 50)
    if selected_pal != 'Choose a Pal' and comparison_pal != 'Choose a Pal':
  
        atk_values_name1 = [float(df[df["Name"] == name1]["Atk"].values[0] + 6.5 * level) for level in levels]
        atk_values_name2 = [float(df[df["Name"] == name2]["Atk"].values[0] + 6.5 * level) for level in levels]
        hp_values_name1 = [float(df[df["Name"] == name1]["HP"].values[0] + 12.5 * level) for level in levels]
        hp_values_name2 = [float(df[df["Name"] == name2]["HP"].values[0] + 12.5 * level) for level in levels]
        def_values_name1 = [float(df[df["Name"] == name1]["Def"].values[0] + 5 * level) for level in levels]
        def_values_name2 = [float(df[df["Name"] == name2]["Def"].values[0] + 5 * level) for level in levels]


        line_chart = (
            Line()
            .add_xaxis(levels)
            
            .add_yaxis("HP", hp_values_name1, linestyle_opts=opts.LineStyleOpts(type_="dashed", color='g'))
            .add_yaxis("HP", hp_values_name2, linestyle_opts=opts.LineStyleOpts(color='g'))
            .add_yaxis("Atk", atk_values_name1, linestyle_opts=opts.LineStyleOpts(type_="dashed", color='r'))
            .add_yaxis("Atk", atk_values_name2, linestyle_opts=opts.LineStyleOpts(color='r'))
            .add_yaxis("Def", def_values_name1, linestyle_opts=opts.LineStyleOpts(type_="dashed", color='k'))
            .add_yaxis("Def", def_values_name2, linestyle_opts=opts.LineStyleOpts(color='k'))
            .set_global_opts(title_opts=opts.TitleOpts(title=name1+"(直线) vs "+name2+"(虚线)"),
                            xaxis_opts=opts.AxisOpts(name="Level"),
                            yaxis_opts=opts.AxisOpts(name=""),
                            legend_opts=opts.LegendOpts(selected_mode="single", pos_left="right"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                            markline_opts=opts.MarkLineOpts(
                           
                            data=[
                               
                                opts.MarkLineItem(                  
                                    name="自定义线",
                                    x = selected_level,              
                                    )],
                            label_opts=opts.LabelOpts(),
                            linestyle_opts=opts.LineStyleOpts(width = 1,color = 'r',)))
        )

        st_pyecharts(line_chart)
    else :
        if name1 == 'Choose a Pal':
            name1 =name2
        atk_values_name1 = [float(df[df["Name"] == name1]["Atk"].values[0] + 6.5 * level) for level in levels]
        hp_values_name1 = [float(df[df["Name"] == name1]["HP"].values[0] + 12.5 * level) for level in levels]
        def_values_name1 = [float(df[df["Name"] == name1]["Def"].values[0] + 5 * level) for level in levels]


        line_chart = (
            Line()
            .add_xaxis(levels)
            
            .add_yaxis("HP", hp_values_name1, linestyle_opts=opts.LineStyleOpts(type_="dashed", color='g'))
            .add_yaxis("Atk", atk_values_name1, linestyle_opts=opts.LineStyleOpts(type_="dashed", color='r'))
            .add_yaxis("Def", def_values_name1, linestyle_opts=opts.LineStyleOpts(type_="dashed", color='k'))
            .set_global_opts(title_opts=opts.TitleOpts(title=name1),
                            xaxis_opts=opts.AxisOpts(name="Level"),
                            yaxis_opts=opts.AxisOpts(name=""),
                            legend_opts=opts.LegendOpts(selected_mode="single", pos_left="right"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                            markline_opts=opts.MarkLineOpts(
                    
                            data=[
                             
                                opts.MarkLineItem(                  
                                    name="自定义线",
                                    x = selected_level,              
                                    )],
                            label_opts=opts.LabelOpts(),
                            linestyle_opts=opts.LineStyleOpts(width = 1,color = 'r',)))
        )

        st_pyecharts(line_chart)
    fig, ax = plt.subplots()
    if selected_pal != 'Choose a Pal':
        ax.bar(selected_stats.keys(), selected_stats.values(), width=-0.4, align='edge', label=selected_pal)
    if comparison_pal != 'Choose a Pal' and comparison_pal != selected_pal:
        ax.bar(comparison_stats.keys(), comparison_stats.values(), width=0.4, align='edge', label=comparison_pal)

    ax.set_ylabel('Value')
    ax.set_title('Stats Comparison at Level {}'.format(level))
    ax.legend()
    st.pyplot(fig)
else:
    st.write('Please select at least one Pal to display stats and comparison.')