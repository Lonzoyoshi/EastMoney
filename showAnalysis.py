import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Bar, Grid, Page, Line, Radar
from pyecharts.globals import ThemeType
from pyecharts.charts import Pie, WordCloud
from pyecharts.globals import CurrentConfig



def show_analysis(ModuleName, PageNum):
    data_df = pd.read_csv('df.csv')
    df = data_df.dropna() # 去除空值
    df1 = df[['名称', '最新价', '最低价', '成交额', '涨跌幅%', '市净率', '换手率%', '昨收', '今开', '最高']]
    df_newPrice = df1.sort_values(by='最新价', ascending=False)
    df_TotalPrice = df1.sort_values(by='成交额', ascending=False)
    df_profit = df1.sort_values(by='市净率', ascending=False)

    # 最新价和最低价饼图
    df2 = df_newPrice.iloc[:15]
    print(df2['名称'].values)
    print(df2['最新价'].values)
    data_name = df2['名称'].values
    data_newPrice = df2['最新价'].values
    data_low = df2['最低价'].values
    inner_data_pair = [list(z) for z in zip(data_name, data_low)]
    outer_data_x = [x[0] for x in inner_data_pair]
    outer_data_y = data_newPrice
    outer_data_pair = [list(z) for z in zip(outer_data_x, outer_data_y)]
    c = (
        Pie(init_opts=opts.InitOpts(width="1440px", height="900px", theme=ThemeType.LIGHT))
        # 设置内圈数据
        .add(series_name="最低价", data_pair=inner_data_pair,
             radius=[0, "30%"], label_opts=opts.LabelOpts(position="inner", formatter="{b}: {c} 元/股",
                                                          font_size=10, font_weight="bold", color="Black"),
             )
        # 设置外圈数据
        .add(series_name="最新价", radius=["40%", "55%"],
             data_pair=outer_data_pair,
             label_opts=opts.LabelOpts(position="outside", formatter="{a|{a}}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}   ",
                                       background_color="#eee", border_color="#aaa",
                                       border_width=1,
                                       border_radius=4,
                                       rich={"a": {"color": "#999", "LineHeight": 22, "align": "center"},
                                             "abg": {"backgroundColor": "#e3e3e3", "width": "100%",
                                                     "align": "right", "height": 22,
                                                     "borderRadius": [4, 4, 0, 0]},
                                             "hr": {"borderColor": "#aaa", "width": "100%",
                                                    "borderWidth": 0.5, "height": 0, },
                                             "b": {"fontSize": 16, "LineHeight": 33},
                                             "per": {"color": "#eee", "backgroundColor": "#334455",
                                                     "padding": [2, 4], "borderRadius": 2,
                                                     },
                                             },
                                       ),
             )
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", ))
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)", )
        )
        .set_global_opts(title_opts=opts.TitleOpts(title='当前页面股票价位前十五饼图',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#181818",
                                                                                           font_size=24,
                                                                                           font_weight="bold"),
                                                   subtitle='元/股'))
    )
    # Pie.render(c, "eastmm_showPrice.html")

    # 成交额柱状图
    print(df_TotalPrice['名称'].values)
    print(df_TotalPrice['成交额'].values)
    df_tp = df_TotalPrice.iloc[:15]
    bar = Bar(init_opts=opts.InitOpts(width="1440px", height="900px", theme=ThemeType.ESSOS))
    bar.add_xaxis(list(df_tp['名称'].values), )
    bar.add_yaxis("成交额", list(df_tp['成交额'].values), color="#FFA07A")
    bar.set_series_opts(label_opts=opts.LabelOpts(position="top", font_size=12, font_weight="bold", color="Black"))
    bar.set_global_opts(title_opts=opts.TitleOpts(title='成交额前十五柱状图', subtitle='单位 元', pos_top="left",
                                                  title_textstyle_opts=opts.TextStyleOpts(color="#181818", font_size=24,
                                                                                          font_weight="bold")),
                        legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", pos_top="48"))
    # 绘制成交量前15的股票的涨跌幅
    line = Line(init_opts=opts.InitOpts(width="1440px", height="900px", theme=ThemeType.ESSOS))
    line.set_global_opts(xaxis_opts=opts.AxisOpts(type_="category", name="股票名称"),
                         yaxis_opts=opts.AxisOpts(type_="value", name="涨跌幅%"),
                         axispointer_opts=opts.AxisPointerOpts(is_show=True, link=[{"xAxisIndex": "all"}]),
                         title_opts=opts.TitleOpts(title='成交额前十五股票涨跌幅', subtitle='单位 %', pos_left="left",
                                                   pos_bottom="500",
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#181818",
                                                                                           font_size=24,
                                                                                           font_weight="bold")),
                         legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", pos_bottom="450"))
    line.add_xaxis(list(df_tp['名称'].values))
    line.add_yaxis("涨跌幅折线图", list(df_tp['涨跌幅%'].values), color="#733202",
                   symbol="triangle", symbol_size=12, is_symbol_show=True, label_opts=opts.LabelOpts(is_show=True))
    grid = (
        Grid(init_opts=opts.InitOpts(width="1440px", height="1080px", theme=ThemeType.ESSOS))
        # 通过设置图形相对位置，来调整是整个并行图是竖直放置，还是水平放置
        .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
        .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
    )

    # 根据市净率分析股票的表现

    df_profit = df_profit.iloc[:15]
    print(df_profit['名称'].values)
    print(df_profit['市净率'].values)

    # 市净率与换手率合成折线图
    line2 = Line(init_opts=opts.InitOpts(width="1280px", height="800px", theme=ThemeType.ESSOS))
    line2.set_global_opts(xaxis_opts=opts.AxisOpts(type_="category", name="股票名称"),
                          yaxis_opts=opts.AxisOpts(type_="value", name="市净率"),
                          title_opts=opts.TitleOpts(title='市净率前十五股票的市净率与换手率折线图', subtitle='单位 %',
                                                    pos_top="left", pos_bottom="400",
                                                    title_textstyle_opts=opts.TextStyleOpts(color="#181818",
                                                                                            font_size=24,
                                                                                            font_weight="bold")),
                          legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", pos_bottom="400"))
    line2.add_xaxis(list(df_profit['名称'].values))
    line2.add_yaxis("市净率折线图", list(df_profit['市净率'].values), color="#7c6c69",
                    symbol="roundRect", is_symbol_show=True, symbol_size=12, label_opts=opts.LabelOpts(is_show=True))
    line2.add_yaxis("换手率折线图", list(df_profit['换手率%'].values), color="#334048",
                    symbol="triangle", is_symbol_show=True, symbol_size=12, label_opts=opts.LabelOpts(is_show=True))

    # 昨收今开雷达图
    n1 = list(df_profit['名称'].values)
    v1 = [list(df_profit['昨收'])]
    v2 = [list(df_profit['今开'])]
    v3 = [list(df_profit['最新价'])]
    v4 = [list(df_profit['最高'])]
    r_schema = [
        opts.RadarIndicatorItem(name=n1[0]),
        opts.RadarIndicatorItem(name=n1[1]),
        opts.RadarIndicatorItem(name=n1[2]),
        opts.RadarIndicatorItem(name=n1[3]),
        opts.RadarIndicatorItem(name=n1[4]),
        opts.RadarIndicatorItem(name=n1[5]),
        opts.RadarIndicatorItem(name=n1[6]),
        opts.RadarIndicatorItem(name=n1[7]),
        opts.RadarIndicatorItem(name=n1[8]),
        opts.RadarIndicatorItem(name=n1[9]),
        opts.RadarIndicatorItem(name=n1[10]),
        opts.RadarIndicatorItem(name=n1[11]),
        opts.RadarIndicatorItem(name=n1[12]),
        opts.RadarIndicatorItem(name=n1[13]),
        opts.RadarIndicatorItem(name=n1[14]),
    ]

    radar = (
        Radar(init_opts=opts.InitOpts(width="1280px", height="800px", theme=ThemeType.LIGHT))
        .add_schema(schema=r_schema,
                    splitarea_opt=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                    )
        .add(
            series_name="昨收",
            data=v1,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
            linestyle_opts=opts.LineStyleOpts(width=1),
            color="#044a80",
        )
        .add(
            series_name="今开",
            data=v2,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
            linestyle_opts=opts.LineStyleOpts(width=1),
            color="#7fbbc3",
        )
        .add(
            series_name="最新价",
            data=v3,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
            linestyle_opts=opts.LineStyleOpts(width=1),
            color="#ce731e",
        )
        .add(
            series_name="最高",
            data=v4,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
            linestyle_opts=opts.LineStyleOpts(width=1),
            color="#46575f",
        )
        .set_colors(['#675bba', '#d14a61', '#f3a43b'])
        .set_series_opts(label_opts=opts.LabelOpts(font_size=11, font_weight="bold", color="#33404d"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title='市净率前十五股票价格雷达图', subtitle='单位 元', pos_top="left",
                                      title_textstyle_opts=opts.TextStyleOpts(color="#181818", font_size=24,
                                                                              font_weight="bold")),
            legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", pos_top="80", padding=5,
                                        item_gap=15, item_height=10))

    )
    df_pf = df1.sort_values(by='涨跌幅%', ascending=False)
    words = df_pf['名称'].values
    values = df_pf['涨跌幅%'].values
    cloud = [(word, value) for word, value in zip(words, values)]
    wordcloud = (
        WordCloud(init_opts=opts.InitOpts(width="1280px", height="800px", theme=ThemeType.ROMA))
        .add("", cloud, word_size_range=[20, 100], rotate_step=30,
             pos_left="center", pos_top="center", width="100%", height="100%", shape="star", )
        .set_global_opts(title_opts=opts.TitleOpts(title='当前页面涨跌幅股票词云图', subtitle='单位 %', pos_top="left",
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#181818",
                                                                                           font_size=24,
                                                                                           font_weight="bold")),
                         legend_opts=opts.LegendOpts(is_show=False))
    )

    # 合并图表
    page = Page()
    page.add(grid, c, line2, radar, wordcloud)
    page.page_title = str(ModuleName + " 第" + str(PageNum) + "页分析结果")
    page.render("eastmm_EastMoney.html")


if __name__ == '__main__':
    data_df = pd.read_csv('df.csv')
    df = data_df.dropna()
    df1 = df[['名称', '最新价', '最低价', '成交额', '涨跌幅%', '市净率', '换手率%', '昨收', '今开', '最高']]
    df_newPrice = df1.sort_values(by='最新价', ascending=False)
    df_TotalPrice = df1.sort_values(by='成交额', ascending=False)
    df_profit = df1.sort_values(by='市净率', ascending=False)

    # 最新价和最低价饼图
    df2 = df_newPrice.iloc[:15]
    print(df2['名称'].values)
    print(df2['最新价'].values)
    data_name = df2['名称'].values
    data_newPrice = df2['最新价'].values
    data_low = df2['最低价'].values
    inner_data_pair = [list(z) for z in zip(data_name, data_low)]
    outer_data_x = [x[0] for x in inner_data_pair]
    outer_data_y = data_newPrice
    outer_data_pair = [list(z) for z in zip(outer_data_x, outer_data_y)]
    c = (
        Pie(init_opts=opts.InitOpts(width="1440px", height="900px", theme=ThemeType.LIGHT))
        # 设置内圈数据
        .add(series_name="最低价", data_pair=inner_data_pair,
             radius=[0, "30%"], label_opts=opts.LabelOpts(position="inner", formatter="{b}: {c} 元/股",
                                                          font_size=10, font_weight="bold", color="Black"),
             )
        # 设置外圈数据
        .add(series_name="最新价", radius=["40%", "55%"],
             data_pair=outer_data_pair,
             label_opts=opts.LabelOpts(position="outside", formatter="{a|{a}}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}   ",
                                       background_color="#eee", border_color="#aaa",
                                       border_width=1,
                                       border_radius=4,
                                       rich={"a": {"color": "#999", "LineHeight": 22, "align": "center"},
                                             "abg": {"backgroundColor": "#e3e3e3", "width": "100%",
                                                     "align": "right", "height": 22,
                                                     "borderRadius": [4, 4, 0, 0]},
                                             "hr": {"borderColor": "#aaa", "width": "100%",
                                                    "borderWidth": 0.5, "height": 0, },
                                             "b": {"fontSize": 16, "LineHeight": 33},
                                             "per": {"color": "#eee", "backgroundColor": "#334455",
                                                     "padding": [2, 4], "borderRadius": 2,
                                                     },
                                             },
                                       ),
             )
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", ))
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)", )
        )
        .set_global_opts(title_opts=opts.TitleOpts(title='当前页面股票价位前十五饼图',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#181818",
                                                                                           font_size=24,
                                                                                           font_weight="bold"),
                                                   subtitle='元/股'))
    )
    # Pie.render(c, "eastmm_showPrice.html")

    # 成交额柱状图
    print(df_TotalPrice['名称'].values)
    print(df_TotalPrice['成交额'].values)
    df_tp = df_TotalPrice.iloc[:15]

    bar = Bar(init_opts=opts.InitOpts(width="1440px", height="900px", theme=ThemeType.ESSOS))
    bar.add_xaxis(list(df_tp['名称'].values), )
    bar.add_yaxis("成交额", list(df_tp['成交额'].values), color="#FFA07A")
    bar.set_series_opts(label_opts=opts.LabelOpts(position="top", font_size=12, font_weight="bold", color="Black"))
    bar.set_global_opts(title_opts=opts.TitleOpts(title='成交额前十五柱状图', subtitle='单位 元', pos_top="left",
                                                  title_textstyle_opts=opts.TextStyleOpts(color="#181818", font_size=24,
                                                                                          font_weight="bold")),
                        legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", pos_top="48"))
    # 绘制成交量前15的股票的涨跌幅
    line = Line(init_opts=opts.InitOpts(width="1440px", height="900px", theme=ThemeType.ESSOS))
    line.set_global_opts(xaxis_opts=opts.AxisOpts(type_="category", name="股票名称"),
                         yaxis_opts=opts.AxisOpts(type_="value", name="涨跌幅%"),
                         axispointer_opts=opts.AxisPointerOpts(is_show=True, link=[{"xAxisIndex": "all"}]),
                         title_opts=opts.TitleOpts(title='成交额前十五股票涨跌幅', subtitle='单位 %', pos_left="left",
                                                   pos_bottom="400",
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#181818",
                                                                                           font_size=24,
                                                                                           font_weight="bold")),
                         legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", pos_bottom="400"))
    line.add_xaxis(list(df_tp['名称'].values))
    line.add_yaxis("涨跌幅折线图", list(df_tp['涨跌幅%'].values), color="#733202",
                   symbol="triangle", symbol_size=12, is_symbol_show=True, label_opts=opts.LabelOpts(is_show=True))
    grid = (
        Grid(init_opts=opts.InitOpts(width="1440px", height="900px", theme=ThemeType.ESSOS))
        # 通过设置图形相对位置，来调整是整个并行图是竖直放置，还是水平放置
        .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
        .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
    )

    # 根据市净率分析股票的表现

    df_profit = df_profit.iloc[:15]
    print(df_profit['名称'].values)
    print(df_profit['市净率'].values)

    # 市净率与换手率合成折线图
    line2 = Line(init_opts=opts.InitOpts(width="1280px", height="800px", theme=ThemeType.ROMA))
    line2.set_global_opts(xaxis_opts=opts.AxisOpts(type_="category", name="股票名称"),
                          yaxis_opts=opts.AxisOpts(type_="value", name="市净率"),
                          title_opts=opts.TitleOpts(title='市净率前十五股票的市净率与换手率折线图', subtitle='单位 %',
                                                    pos_top="left", pos_bottom="400",
                                                    title_textstyle_opts=opts.TextStyleOpts(color="#181818",
                                                                                            font_size=24,
                                                                                            font_weight="bold")),
                          legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", pos_bottom="400"))
    line2.add_xaxis(list(df_profit['名称'].values))
    line2.add_yaxis("市净率折线图", list(df_profit['市净率'].values), color="#7c6c69",
                    symbol="roundRect", is_symbol_show=True, symbol_size=12, label_opts=opts.LabelOpts(is_show=True))
    line2.add_yaxis("换手率折线图", list(df_profit['换手率%'].values), color="#334048",
                    symbol="triangle", is_symbol_show=True, symbol_size=12, label_opts=opts.LabelOpts(is_show=True))

    # 昨收今开雷达图
    n1 = list(df_profit['名称'].values)
    v1 = [list(df_profit['昨收'])]
    v2 = [list(df_profit['今开'])]
    v3 = [list(df_profit['最新价'])]
    v4 = [list(df_profit['最高'])]
    r_schema = [
        opts.RadarIndicatorItem(name=n1[0]),
        opts.RadarIndicatorItem(name=n1[1]),
        opts.RadarIndicatorItem(name=n1[2]),
        opts.RadarIndicatorItem(name=n1[3]),
        opts.RadarIndicatorItem(name=n1[4]),
        opts.RadarIndicatorItem(name=n1[5]),
        opts.RadarIndicatorItem(name=n1[6]),
        opts.RadarIndicatorItem(name=n1[7]),
        opts.RadarIndicatorItem(name=n1[8]),
        opts.RadarIndicatorItem(name=n1[9]),
        opts.RadarIndicatorItem(name=n1[10]),
        opts.RadarIndicatorItem(name=n1[11]),
        opts.RadarIndicatorItem(name=n1[12]),
        opts.RadarIndicatorItem(name=n1[13]),
        opts.RadarIndicatorItem(name=n1[14]),
    ]

    radar = (
        Radar(init_opts=opts.InitOpts(width="1280px", height="800px", theme=ThemeType.LIGHT))
        .add_schema(schema=r_schema,
                    splitarea_opt=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                    )
        .add(
            series_name="昨收",
            data=v1,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
            linestyle_opts=opts.LineStyleOpts(width=1),
            color="#044a80",
        )
        .add(
            series_name="今开",
            data=v2,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
            linestyle_opts=opts.LineStyleOpts(width=1),
            color="#7fbbc3",
        )
        .add(
            series_name="最新价",
            data=v3,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
            linestyle_opts=opts.LineStyleOpts(width=1),
            color="#ce731e",
        )
        .add(
            series_name="最高",
            data=v4,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
            linestyle_opts=opts.LineStyleOpts(width=1),
            color="#46575f",
        )
        .set_colors(['#675bba', '#d14a61', '#f3a43b'])
        .set_series_opts(label_opts=opts.LabelOpts(font_size=11, font_weight="bold", color="#33404d"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title='市净率前十五股票价格雷达图', subtitle='单位 元', pos_top="left",
                                      title_textstyle_opts=opts.TextStyleOpts(color="#181818", font_size=24,font_weight="bold")),
            legend_opts=opts.LegendOpts(pos_left="right", orient="vertical", pos_top="80", padding=5,
                                        item_gap=15, item_height=10))
    )
    df_pf = df1.sort_values(by='涨跌幅%', ascending=False)
    words = df_pf['名称'].values
    values = df_pf['涨跌幅%'].values
    cloud = [(word, value) for word, value in zip(words, values)]
    wordcloud = (
        WordCloud(init_opts=opts.InitOpts(width="1280px", height="800px", theme=ThemeType.ROMA))
        .add("", cloud, word_size_range=[20, 100], rotate_step=30,
             pos_left="center", pos_top="center", width="100%", height="100%", shape="star", )
        .set_global_opts(title_opts=opts.TitleOpts(title='当前页面涨跌幅股票词云图', subtitle='单位 %', pos_top="left",
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#181818",
                                                                                           font_size=24,
                                                                                           font_weight="bold")),
                         legend_opts=opts.LegendOpts(is_show=False))
    )

    # 合并图表
    page = Page()
    page.add(grid, c, line2, radar, wordcloud)
    page.render("eastmm_EastMoney.html")
