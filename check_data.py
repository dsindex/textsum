#!/bin/env python

import sys
import os
import glob
import random
import struct

import tensorflow as tf
from tensorflow.core.example import example_pb2

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('data_path', 'data/data', 'Path expression to tf.Example.')

def ExampleGen(recordio_path, num_epochs=None):
  """Generates tf.Examples from path of recordio files.

  Args:
    recordio_path: CNS path to tf.Example recordio
    num_epochs: Number of times to go through the data. None means infinite.

  Yields:
    Deserialized tf.Example.

  If there are multiple files specified, they accessed in a random order.
  """
  epoch = 0
  while True:
    if num_epochs is not None and epoch >= num_epochs:
      break
    filelist = glob.glob(recordio_path)
    assert filelist, 'Empty filelist.'
    random.shuffle(filelist)
    for f in filelist:
      reader = open(f, 'rb')
      while True:
        len_bytes = reader.read(8)
        #skip_byptes = reader.read(4) # skip 4 bytes
        if not len_bytes: break
        str_len = struct.unpack('q', len_bytes)[0]
        example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
        print example_str
        yield example_pb2.Example.FromString(example_str)

    epoch += 1

for ret in ExampleGen(FLAGS.data_path, num_epochs=1) :
  print ret

