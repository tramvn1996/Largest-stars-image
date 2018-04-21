from pyspark.sql import SparkSession
from pyspark.sql.functions import desc
from pyspark import SparkContext, SparkConf
from pyspark.rdd import RDD

import numpy as np
import argparse
import cv2

import re

conf = SparkConf().setAppName("Stars")
sc = SparkContext(conf=conf)
spark = SparkSession.builder.appName("Starts").getOrCreate()
fnames =sc.textFile("file:///home/tnguyen/BigData/project3/radec.csv")

m = fnames.map(lambda line: line.split(","))
header = m.first()
rows = m.filter(lambda line : line!=header) 
def findstar(names):
    s=[]
    if names is not None:
        st = '/bigdata/data/pan-starrs1/'+names[0]+'.png'
        print(st)
        image = cv2.imread(st,0)
        kernel = np.ones((5,5),np.uint8)
        ero = cv2.erode(image, kernel, iterations = 1)
        circles = cv2.HoughCircles(ero, cv2.HOUGH_GRADIENT, 1, 20,param1=30,param2=10,minRadius=10,maxRadius=100)
        if circles is not None:
            circles = np.round(circles[0,:]).astype("int")
            for (x,y,z) in circles:
                #Since we only care about pixel size of each star, only save the radius=z
                s.append((z,names[1],names[2]))
        else:
            print("circles doesn't exist")
    return s
s = rows.flatMap(findstar)
radius =s.sortBy(lambda x: x[0],ascending=False)
top100=sc.parallelize(radius.take(163))
top100.saveAsTextFile("file:///home/tnguyen/bigresult.csv")

print(top100.collect())
