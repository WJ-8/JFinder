import os
import random

import sklearn.metrics
from keras.layers import Lambda

from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
import keras_metrics as km
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.callbacks import ModelCheckpoint, Callback
from keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Input, concatenate, \
    BatchNormalization, LeakyReLU, Dropout, Reshape, MultiHeadAttention
from tensorflow.keras.optimizers import Adam
from network.network import MyMultiHeadAttention
from keras import backend as K
import os
import wandb
from wandb.keras import WandbCallback

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

y_train = np.load("data/ready/train_y.npy")
x_train_emb = np.load("data/ready/emb_train.npy")
x_train_ast = np.load("data/ready/ast_train.npy")
x_train_dfg = np.load("data/ready/dfg_train.npy")
x_train_cfg = np.load("data/ready/cfg_train.npy")

# 加载验证集
# val_dataset = pd.read_pickle('data/embedding/val_0')
y_val = np.load("data/ready/val_y.npy")
x_val_emb = np.load("data/ready/emb_val.npy")
x_val_ast = np.load("data/ready/ast_val.npy")
x_val_dfg = np.load("data/ready/dfg_val.npy")
x_val_cfg = np.load("data/ready/cfg_val.npy")

# 加载测试集
# test_dataset = pd.read_pickle('data/embedding/test_0')
y_test = np.load("data/ready/test_y.npy")
x_test_emb = np.load("data/ready/emb_test.npy")
x_test_ast = np.load("data/ready/ast_test.npy")
x_test_dfg = np.load("data/ready/dfg_test.npy")
x_test_cfg = np.load("data/ready/cfg_test.npy")

input_emb = Input(shape=(1, 768))
input_dfg = Input(shape=(200, 200))
input_cfg = Input(shape=(200, 200))
input_ast = Input(shape=(200, 200))
# 定义图注意力层
att_ast = MyMultiHeadAttention(200, 4)(input_ast)  # 输出维度，多头数量
# print(att_ast.shape)
att_dfg = MyMultiHeadAttention(200, 4)(input_dfg)  # 输出维度，多头数量
att_cfg = MyMultiHeadAttention(200, 4)(input_cfg)  # 输出维度，多头数量
att_emb = MyMultiHeadAttention(400, 4)(input_emb)

# 对emb池化(使用零填充到200，200
reshape_emb = Reshape((200, 2))(att_emb)

combine1 = concatenate([input_dfg, input_cfg])
combine2 = concatenate([reshape_emb, input_ast])
combine3 = concatenate([combine2, combine1])

expend = tf.expand_dims(combine3, axis=-1)
conv_1 = Conv2D(filters=32, kernel_size=(5, 5), strides=(3, 3), padding="valid")(expend)
bn_1 = BatchNormalization(axis=-1, trainable=True, momentum=0.9)(conv_1)
active_1 = LeakyReLU(0.01)(bn_1)
conv_2 = Conv2D(filters=16, kernel_size=(3, 3), strides=(2, 2), padding="valid")(active_1)
active_2 = LeakyReLU(0.01)(conv_2)
maxpool_1 = MaxPooling2D(pool_size=(3, 3), strides=(1, 1), padding="valid")(active_2)
drop_1 = Dropout(0.05)(maxpool_1)
conv_3 = Conv2D(filters=8, kernel_size=(3, 3), strides=(2, 2), padding="valid")(drop_1)
active_3 = LeakyReLU(0.01)(conv_3)
maxpool_2 = MaxPooling2D(pool_size=(3, 3), strides=(1, 1), padding="valid")(active_3)
drop_2 = Dropout(0.1)(maxpool_2)
flatten_1 = Flatten()(drop_2)

dense_1 = Dense(1024, activation="relu")(flatten_1)
# z=Lambda(lambda x: tf.nn.l2_normalize(x, 1), name='emmbeding')(dense_1)

z = Dense(1, activation='sigmoid')(dense_1)
# z = Dense(2,use_bias=False)(z)

model = Model(inputs=[input_emb, input_ast, input_dfg, input_cfg], outputs=z)
model.compile(optimizer=Adam(learning_rate=1e-5), loss=["binary_crossentropy"], 
              metrics=["binary_accuracy", km.f1_score(), km.binary_precision(), km.binary_recall()])
checkpoints = ModelCheckpoint(filepath='model/ck/weights.{epoch:04d}.hdf5', monitor="val_loss", verbose=1,
                              save_weights_only=True, period=100)
history = model.fit(
    [x_train_emb, x_train_ast, x_train_dfg, x_train_cfg], y_train,
    validation_data=([x_val_emb, x_val_ast, x_val_dfg, x_val_cfg], y_val),
    # epochs=20, batch_size=16, verbose=2, callbacks=[checkpoints])
    epochs=50, batch_size=16, verbose=2, callbacks=[WandbCallback(save_model=False, save_graph=False)])

score = model.evaluate([x_test_emb, x_test_ast, x_test_dfg, x_test_cfg], y_test, verbose=0, batch_size=32)
model.save('model/JFinder.h5')
print(score)
print(model.metrics_names)
