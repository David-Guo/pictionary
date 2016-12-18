# -*- coding: utf-8 -*-
# see this https://github.com/BVLC/caffe/issues/462 to hack for gray image
import os
import caffe
import numpy as np
import time


repo_dir = '../'

class classfy():
    def __init__(self):

        # loading the deployment version of your model and not the training version
        # for inof at: https://github.com/BVLC/caffe/issues/712
        model_def_file = repo_dir + 'data/deploy.prototxt'
        pretrained_model_file = repo_dir + 'data/googlenet_iter_80000.caffemodel'
        print os.path.isfile(pretrained_model_file)

        # 加载 proto 类型均值文件
        mean_file = repo_dir + 'data/sketch200.binaryproto'
        proto_data = open(mean_file, "rb").read()
        a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
        mu = np.array(caffe.io.blobproto_to_array(a))[0].mean(1).mean(1)

        self.net = caffe.Classifier(model_def_file, pretrained_model_file, 
                mean=mu, image_dims=(256, 256), raw_scale=255)

        self.namelist = []
        fin = "./label.txt"
        with open(fin) as f:
            data = f.readlines(1)
        for line in data:
            classname, label = line.split()
            self.namelist.append(classname)
        f.close()

    def predict(self, f="file.ps"):
        # f = "file.ps"
        # 读取灰度图像
        image = caffe.io.load_image(f, color=False)
        # scores 表示每个种类的相似度(102个元素)
        starttime = time.time()
        scores = self.net.predict([image], oversample=False).flatten()
        endtime = time.time()
        #print (-scores).argsort()[:5]
        pre_label = (-scores).argsort()[0]
        #print pre_label
        print "use time: %.2f" % (endtime - starttime)
        print self.namelist[pre_label]
        return self.namelist[pre_label]

 
