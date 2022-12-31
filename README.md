# SpiderPractice

在2022-2023第一学期，爬虫实践作业



## 运行环境

```python
Python 	  3.9.7
scrapy    2.7.1
```



## 运行方式

```python
python main.py *args
```



### 课程及参数要求

|                  课程要求                  |                             网站                             |   参数   |                  结果                  |
| :----------------------------------------: | :----------------------------------------------------------: | :------: | :------------------------------------: |
|            新浪财经机构持股汇总            | [新浪财经](http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml) | xinlang  |  [xinlang.csv](./request/xinlang.csv)  |
|       给定城市（北上广深）的空气质量       |            [空气知音](http://www.air-level.com/)             | airlevel | [airlevel.csv](./request/airlevel.csv) |
| 给定城市（北上广深） 2022 年每天的天数数据 |             [2345天气](https://tianqi.2345.com/)             | weather  | [weather.csv](./request/weather.csv)  |
| 小米商店中“全部百变锁屏＂的高清壁纸 | [小米商店](http://zhuti.xiaomi.com/lockstyle) | milockimg | [milockimg](./request/milockimg) |

### 实例

```python
# 在同一个进程中并行多个爬虫
python main.py xinlang airlevel weather 
```

