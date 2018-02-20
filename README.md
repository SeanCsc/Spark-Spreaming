# Spark-Spreaming

## 项目目标

实现Spark Streaming 应用连接给定TCP Socket,接收字符数据并对数据进行MapReduce计算单词出现的频次。

Spark streaming 处理过程：

![Process](https://github.com/SeanCsc/Spark-Spreaming/blob/master/Other/spark-stream.png)
![pro](https://github.com/SeanCsc/Spark-Spreaming/blob/master/Other/stream%20process.png)

## Spark Streaming编程模型

类似于Spark，先创建Context对象，并对抽象数据对象进行操作。

处理对象：DStream

## 编程语言及库函数
本次项目基于Linux下的pyspark实现。
```python
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
```

## 开发流程：
#### 首先创建SparkConf对象，包括一系列应用信息（应用程序名，主节点URL等）->创建SparkContext(让Spark知道如何连接Spark集群）->创建StreamingContext 对象

```python
# 创建本地的SparkContext对象，包含2个执行线程，APP名字命名为StreamWordCount
sc = SparkContext("local[2]", "StreamWordCount")
# 创建本地的StreamingContext对象，第二个参数为处理的时间片间隔时间，设置为1秒
ssc = StreamingContext(sc, 1)
```
#### 创建DStream
连接一个打开的TCP服务端口获取流数据。
```python
lines = ssc.socketTextStream("localhost", 9999)
# 数据源来自于本机9999端口
```
#### 预处理
-在进行map-reduce前先进行数据分割
```python
words = lines.flatMap(lambda line: line.split(" "))
```

#### Map
将每个单词map到一个元组(word,1)
```python
pairs = words.map(lambda word:(word,1))
```
#### Reduce
根据上一步中的元组，按照单词（key)将value相加。
```python
wordCounts = pairs.reduceByKey(lambda x, y: x + y)
```

#### 存储
```python
# 输出文件夹的前缀，Spark Streaming会自动使用当前时间戳来生成不同的文件夹名称
outputFile = "/tmp/ss"
# 将结果输出
wordCounts.saveAsTextFiles(outputFile)
```
#### 执行文件
-启动Spark Streaming 应用
```Python
# 启动Spark Streaming应用
ssc.start() 
ssc.awaitTermination()
```
-spark-submit

#### 测试
－启动NetCat创建一个数据服务器
```
$ nc -lk 9999
```
在该界面输入字符后，在另一个执行的终端中会进行字符统计，并自动保存文件。
文件结果：
![result](https://github.com/SeanCsc/Spark-Spreaming/blob/master/Other/result.jpg)







