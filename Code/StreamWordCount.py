from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext("local[2]","SreamWordCount")

ssc = StreamingContext(sc,1)

lines = ssc.socketTextStream("localhost",9999)

words = lines.flatMap(lambda line:line.split(" "))

pairs = words.map(lambda word:(word,1))
wordCounts = pairs.reduceByKey(lambda x,y:x+y)

outputFile = "/tmp/ss"
wordCounts.saveAsTextFiles(outputFile)

ssc.start()
ssc.awaitTermination()

