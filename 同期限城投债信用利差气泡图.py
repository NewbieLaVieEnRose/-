# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt


#提取数据
info = pd.read_csv('H:/1.城投债评级模型/python/信用利差分析_国开债.csv', engine='python')
info = info.astype({'交易日期': 'str'})
info = info.sort_values(by='所属区县', ascending=True)

# 循环绘制各区县各期限信用利差气泡图
for area in info['所属区县'].unique():
    data0 = info[['交易日期', '信用利差', '成交量(手)', '债券期限(年)']][info['所属区县'] == area]
    data0 = data0.sort_values(by='债券期限(年)', ascending=True)
    for term in data0['债券期限(年)'].unique():
        data = data0[data0['债券期限(年)'] == term]
        data = data.sort_values(by='交易日期', ascending=True)
        # 绘制信用利差气泡图
        plt.rcParams['font.sans-serif'] = ['STZhongsong']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时符号-显示为方块的问题
        # 设置画板
        fig = plt.figure()
        ax = plt.subplot(111)
        # 绘制气泡图，横轴为交易日期，纵轴为信用利差，气泡大小为成交量
        ax.scatter(data.loc[:, '交易日期'], data.loc[:, '信用利差'], data.loc[:, '成交量(手)'] / 100, c='#FF9999', alpha=0.7)
        # # 绘制散点图，横轴为交易日期，纵轴为信用利差
        # ax.scatter(data.loc[:, '交易日期'], data.loc[:, '信用利差'], c='#FF9999')
        # 设置标题
        title = area + ' ' + str(term) + '年期'
        plt.title(title)
        # 设置y轴坐标范围
        # # 方案一：纵轴范围随数据变化
        # ymax = data.loc[:, '信用利差'].max() + 1
        # ymin = data.loc[:, '信用利差'].min() - 1
        # 方案二：纵轴范围固定
        ymax = 10
        ymin = -1
        plt.ylim(ymin=ymin, ymax=ymax)
        # 若交易频繁，数据量大，则x轴坐标间隔显示
        nrow = data.iloc[:, 0].size
        if nrow > 8:
            num = nrow // 5
            for label in ax.get_xticklabels():
                label.set_visible(False)
            for label in ax.get_xticklines():
                label.set_visible(False)
            for label in ax.get_xticklabels()[::num]:
                label.set_visible(True)
            for label in ax.get_xticklines()[::num]:
                label.set_visible(True)
        # 设置坐标轴字体
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        # 网格线
        plt.grid(axis='y', c='gainsboro')
        # 边框颜色
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_color('dimgray')
        ax.spines['left'].set_color('dimgray')
        ax.spines['right'].set_visible(False)

        # 输出图像
        if term<0.5:
            plt.savefig('H:/1.城投债评级模型/python/图像/' + area + ' 0.4110年期信用利差走势(%).png')
        else:
            plt.savefig('H:/1.城投债评级模型/python/图像/' + title + '信用利差走势(%).png')