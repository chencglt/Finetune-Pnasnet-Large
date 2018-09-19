import os
import numpy as np
import tensorflow as tf


FLAGS = tf.app.flags.FLAGS

######################
# Common Flags #
######################
tf.app.flags.DEFINE_string('master', '', 'The address of the TensorFlow master to use.')
tf.app.flags.DEFINE_string('train_dir', './train', 'Directory where checkpoints and event logs are written to.')
tf.app.flags.DEFINE_integer('num_clones', 1,
                            'Number of model clones to deploy. Note For '
                            'historical reasons loss from all clones averaged '
                            'out and learning rate decay happen per clone '
                            'epochs')
tf.app.flags.DEFINE_boolean('clone_on_cpu', True, 'Use CPUs to deploy clones.')
tf.app.flags.DEFINE_integer('worker_replicas', 1, 'Number of worker replicas.')
tf.app.flags.DEFINE_integer('num_ps_tasks', 0,
    'The number of parameter servers. If the value is 0, then the parameters '
    'are handled locally by the worker.')
tf.app.flags.DEFINE_integer('num_readers', 4, 'The number of parallel readers that read data from the dataset.')
tf.app.flags.DEFINE_integer('num_preprocessing_threads', 4, 'The number of threads used to create the batches.')
tf.app.flags.DEFINE_integer('log_every_n_steps', 10, 'The frequency with which logs are print.')
tf.app.flags.DEFINE_integer('save_summaries_secs', 600, 'The frequency with which summaries are saved, in seconds.')
tf.app.flags.DEFINE_integer('save_interval_secs', 600, 'The frequency with which the model is saved, in seconds.')
tf.app.flags.DEFINE_integer('task', 0, 'Task id of the replica running the training.')
    
######################
# Optimization Flags #
######################
tf.app.flags.DEFINE_float(
    'weight_decay', 0.00004, 'The weight decay on the model weights.')
tf.app.flags.DEFINE_string(
    'optimizer', 'rmsprop',
    'The name of the optimizer, one of "adadelta", "adagrad", "adam",'
    '"ftrl", "momentum", "sgd" or "rmsprop".')
tf.app.flags.DEFINE_float(
    'adadelta_rho', 0.95,
    'The decay rate for adadelta.')
tf.app.flags.DEFINE_float(
    'adagrad_initial_accumulator_value', 0.1,
    'Starting value for the AdaGrad accumulators.')
tf.app.flags.DEFINE_float(
    'adam_beta1', 0.9,
    'The exponential decay rate for the 1st moment estimates.')
tf.app.flags.DEFINE_float(
    'adam_beta2', 0.999,
    'The exponential decay rate for the 2nd moment estimates.')
tf.app.flags.DEFINE_float('opt_epsilon', 1.0, 'Epsilon term for the optimizer.')
tf.app.flags.DEFINE_float('ftrl_learning_rate_power', -0.5,
                          'The learning rate power.')
tf.app.flags.DEFINE_float(
    'ftrl_initial_accumulator_value', 0.1,
    'Starting value for the FTRL accumulators.')
tf.app.flags.DEFINE_float(
    'ftrl_l1', 0.0, 'The FTRL l1 regularization strength.')
tf.app.flags.DEFINE_float(
    'ftrl_l2', 0.0, 'The FTRL l2 regularization strength.')
tf.app.flags.DEFINE_float(
    'momentum', 0.9,
    'The momentum for the MomentumOptimizer and RMSPropOptimizer.')
tf.app.flags.DEFINE_float('rmsprop_momentum', 0.9, 'Momentum.')
tf.app.flags.DEFINE_float('rmsprop_decay', 0.9, 'Decay term for RMSProp.')

#######################
# Learning Rate Flags #
#######################
tf.app.flags.DEFINE_string(
    'learning_rate_decay_type',
    'exponential',
    'Specifies how the learning rate is decayed. One of "fixed", "exponential",'
    ' or "polynomial"')
tf.app.flags.DEFINE_float('learning_rate', 0.01, 'Initial learning rate.')
tf.app.flags.DEFINE_float(
    'end_learning_rate', 0.0001,
    'The minimal end learning rate used by a polynomial decay learning rate.')
tf.app.flags.DEFINE_float(
    'label_smoothing', 0.0, 'The amount of label smoothing.')
tf.app.flags.DEFINE_float(
    'learning_rate_decay_factor', 0.94, 'Learning rate decay factor.')
tf.app.flags.DEFINE_float(
    'num_epochs_per_decay', 2.0,
    'Number of epochs after which learning rate decays. Note: this flag counts '
    'epochs per clone but aggregates per sync replicas. So 1.0 means that '
    'each clone will go over full epoch individually, but replicas will go '
    'once across all replicas.')
tf.app.flags.DEFINE_bool(
    'sync_replicas', False,
    'Whether or not to synchronize the replicas during training.')
tf.app.flags.DEFINE_integer(
    'replicas_to_aggregate', 1,
    'The Number of gradients to collect before updating params.')
tf.app.flags.DEFINE_float(
    'moving_average_decay', None,
    'The decay to use for the moving average.'
    'If left as None, then moving averages are not used.')

#######################
# Dataset Flags #
#######################
tf.app.flags.DEFINE_string(
    'dataset_name', 'flowers', 'The name of the dataset to load.')
tf.app.flags.DEFINE_string(
    'dataset_split_name_train', 'train', 'The name of the train split.')
tf.app.flags.DEFINE_string(
    'dataset_split_name_eval', 'validation', 'The name of the validation split.')
tf.app.flags.DEFINE_string(
    'dataset_dir', "./dataset/flowers", 'The directory where the dataset files are stored.')
tf.app.flags.DEFINE_integer(
    'labels_offset', 0,
    'An offset for the labels in the dataset. This flag is primarily used to '
    'evaluate the VGG and ResNet architectures which do not use a background '
    'class for the ImageNet dataset.')
tf.app.flags.DEFINE_string(
    'model_name', 'pnasnet_large', 'The name of the architecture to train.')
tf.app.flags.DEFINE_string(
    'preprocessing_name', None, 'The name of the preprocessing to use. If left '
    'as `None`, then the model_name flag is used.')
tf.app.flags.DEFINE_integer(
    'batch_size', 2, 'The number of samples in each batch.')
tf.app.flags.DEFINE_integer(
    'train_image_size', None, 'Train image size')
tf.app.flags.DEFINE_integer('max_number_of_steps', None,
                            'The maximum number of training steps.')


#####################
# Fine-Tuning Flags #
#####################
tf.app.flags.DEFINE_string('pnasnet_large_exclude', 
    'aux_7/aux_logits/FC/biases,aux_7/aux_logits/FC/weights,aux_7/aux_logits/aux_bn0,aux_7/aux_logits/aux_bn1,final_layer/FC/biases,final_layer/FC/weights', "")
tf.app.flags.DEFINE_string('pnasnet_large_scopes', 'aux_7,final_layer,cell10,cell11', "")

tf.app.flags.DEFINE_string(
    'checkpoint_path', './checkpoint/model.ckpt',
    'The path to a checkpoint from which to fine-tune.')
tf.app.flags.DEFINE_string(
    'checkpoint_exclude_scopes', FLAGS.pnasnet_large_exclude,
    'Comma-separated list of scopes of variables to exclude when restoring '
    'from a checkpoint.')
tf.app.flags.DEFINE_string(
    'trainable_scopes', FLAGS.pnasnet_large_scopes,
    'Comma-separated list of scopes to filter the set of variables to train.'
    'By default, None would train all the variables.')
tf.app.flags.DEFINE_boolean(
    'ignore_missing_vars', False,
    'When restoring a checkpoint would ignore missing variables.')

#####################
# Evaluating Flags #
#####################
tf.app.flags.DEFINE_integer('max_num_batches', None, 'Max number of batches to evaluate by default use all.')
tf.app.flags.DEFINE_string('eval_chepoint_path', './train', "path of checkpoints for evalutating")
tf.app.flags.DEFINE_string('eval_dir', './eval', "path of checkpoints for evalutating")
tf.app.flags.DEFINE_integer('eval_image_size', None, 'Eval image size')
