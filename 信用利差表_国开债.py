# -*- coding:utf-8 -*-
import pymysql
import pandas as pd

#从本地数据库提取数据并转化为dataframe格式
def get_mysql_data(sql_order):
    """
    提取mysql中的数据并返回dataframe格式的数据
    参数仅为sql语句
    :param sql_order:
    :return:
    """
    # 创建数据库连接（方法一）
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='111111', db='test', charset='utf8')
    cursor = conn.cursor()  # 初始化游标（创建游标）
    cursor.execute(sql_order)  # 执行sql语句
    data = cursor.fetchall()  # 获取查询结果
    # colname = cursor.description # 获取字段名
    # columns = []
    # for i in range(len(colname)):
    #     columns.append(colname[i][0])
    result = pd.DataFrame(list(data))
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return result

#期限对应表
term = {'债券期限(年)': ['0.411', '0.4932', '0.5753', '0.7377', '0.7397', '1', '2', '3', '4', '5', '6',
                    '7', '8', '9', '10', '15', '20', '30', '40', '50'],
        '对应列名': ['中债国开债到期收益率:6个月', '中债国开债到期收益率:6个月', '中债国开债到期收益率:6个月', '中债国开债到期收益率:6个月',
                 '中债国开债到期收益率:9个月', '中债国开债到期收益率:1年', '中债国开债到期收益率:2年', '中债国开债到期收益率:3年',
                 '中债国开债到期收益率:4年', '中债国开债到期收益率:5年', '中债国开债到期收益率:6年', '中债国开债到期收益率:7年',
                 '中债国开债到期收益率:8年', '中债国开债到期收益率:9年', '中债国开债到期收益率:10年', '中债国开债到期收益率:15年',
                 '中债国开债到期收益率:20年', '中债国开债到期收益率:30年', '中债国开债到期收益率:40年', '中债国开债到期收益率:50年']}
term = pd.DataFrame(term)

# 从本地数据库提取债券基本信息
sql_order = """SELECT `Wind代码`,`债券期限(年)` FROM 天津城投债基本资料"""
info = get_mysql_data(sql_order)
info.columns = ['Wind代码', '债券期限(年)']
num = info.iloc[:, 0].size
#初始化
spread = pd.DataFrame()
temp = []

for i in range(0, num):
    windcode = info.loc[i, 'Wind代码']
    code = '\'' + windcode + '\''
    info_term = info.loc[i, '债券期限(年)']
    # 从本地数据库提取债券日行情数据
    sql_order = """select * from 天津城投债日行情 where Wind代码=""" + code
    data = get_mysql_data(sql_order)
    if data.size != 0:
        data.columns = ['Wind代码', '交易日期', '成交量(手)', '收盘价(元)', '到期收益率', '久期', '修正久期', '凸性']

        # 从本地数据库提取相应期限的国债到期收益率数据
        row = term[term['债券期限(年)'] == info_term].index.tolist()[0]
        column = term.loc[row, '对应列名']
        sql_order = """select `交易日期`,`""" + column + """` from `国开债收益率`"""
        national_debt = get_mysql_data(sql_order)
        national_debt.columns = ['交易日期', '国开债到期收益率']
        df = pd.merge(data.loc[:, ['Wind代码', '交易日期', '到期收益率']], national_debt, how='left', on='交易日期')

        # 计算信用利差
        df['到期收益率'] = df['到期收益率'].astype('float64')
        df['国开债到期收益率'] = df['国开债到期收益率'].astype('float64')
        df['信用利差'] = df['到期收益率'] - df['国开债到期收益率']
        spread = spread.append(df)

spread.to_csv('H:/1.收益率预测模型/基础数据/测试集天津城投债/信用利差分析_国开债.csv', encoding='utf_8_sig')
