
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

slim = tf.contrib.slim


def andreanet(images, num_classes=2, is_training=False,
          dropout_keep_prob=0.5,
          prediction_fn=slim.softmax, reuse=None, scope='AndreaNet'):
  """Creates a variant of the LeNet model.
  Note that since the output is a set of 'logits', the values fall in the
  interval of (-infinity, infinity). Consequently, to convert the outputs to a
  probability distribution over the characters, one will need to convert them
  using the softmax function:
        logits = lenet.lenet(images, is_training=False)
        probabilities = tf.nn.softmax(logits)
        predictions = tf.argmax(logits, 1)
  Args:
    images: A batch of `Tensors` of size [batch_size, height, width, channels].
    num_classes: the number of classes in the dataset. If 0 or None, the logits
      layer is omitted and the input features to the logits layer are returned
      instead.
    is_training: specifies whether or not we're currently training the model.
      This variable will determine the behaviour of the dropout layer.
    dropout_keep_prob: the percentage of activation values that are retained.
    prediction_fn: a function to get predictions out of logits.
    scope: Optional variable_scope.
  Returns:
     net: a 2D Tensor with the logits (pre-softmax activations) if num_classes
      is a non-zero integer, or the inon-dropped-out nput to the logits layer
      if num_classes is 0 or None.
    end_points: a dictionary from components of the network to the corresponding
      activation.
  """
  end_points = {}
  
  with tf.variable_scope(scope, 'AndreaNet', [images], reuse=reuse):
    net = end_points['conv1'] = slim.conv2d(images, 32, [3, 3], scope='conv1')
    net = end_points['conv2'] = slim.conv2d(net, 32, [3, 3], scope='conv2')
    net = end_points['pool1'] = slim.max_pool2d(net, [4, 4], 4, scope='pool1')
    net = end_points['dropout1'] = slim.dropout(
        net, 0.25, is_training=is_training, scope='dropout1')
    net = end_points['conv3'] = slim.conv2d(net, 64, [3, 3], scope='conv3')
    net = end_points['conv4'] = slim.conv2d(net, 64, [3, 3], scope='conv4')
    net = end_points['pool2'] = slim.max_pool2d(net, [4, 4], 4, scope='pool2')
    net = end_points['dropout2'] = slim.dropout(
        net, 0.25, is_training=is_training, scope='dropout2')
    net = end_points['dense1'] = slim.conv2d(net, 256, [3, 3], scope='dense1')
    net = end_points['dropout3'] = slim.dropout(
        net, dropout_keep_prob, is_training=is_training, scope='dropout3')
    net = end_points['dense2'] = slim.conv2d(net, 1, [1, 1], scope='dense2')
    net = slim.flatten(net)
    end_points['Flatten'] = net

    # net = end_points['fc3'] = slim.fully_connected(net, 512, scope='fc3')
    # if not num_classes:
    #   return net, end_points
    # net = end_points['dropout3'] = slim.dropout(
    #     net, dropout_keep_prob, is_training=is_training, scope='dropout3')
    # logits = end_points['Logits'] = slim.fully_connected(
    #     net, num_classes, activation_fn=None, scope='fc4')

  #end_points['Predictions'] = prediction_fn(logits, scope='Predictions')

  #return logits, end_points
  return end_points
andreanet.default_image_size = 48


def andreanet_arg_scope(weight_decay=0.0):
  """Defines the default lenet argument scope.
  Args:
    weight_decay: The weight decay to use for regularizing the model.
  Returns:
    An `arg_scope` to use for the inception v3 model.
  """
  with slim.arg_scope(
      [slim.conv2d, slim.fully_connected],
      weights_regularizer=slim.l2_regularizer(weight_decay),
      weights_initializer=tf.truncated_normal_initializer(stddev=0.1),
      activation_fn=tf.nn.relu) as sc:
    return sc
