
from keras.backend import int_shape
from tensorflow.keras import Sequential, Model
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions

def CnnLSTM(input_shape):


    inputs = Input((input_shape[2],input_shape[0],input_shape[1],1))
    
    cnnlstm1 = ConvLSTM2D(filters=16, kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(inputs)

    batch1 = BatchNormalization() (cnnlstm1)

    cnnlstm2 = ConvLSTM2D(filters=16, kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(batch1)

    batch2 = BatchNormalization() (cnnlstm2)   

    cnnlstm3 = ConvLSTM2D(filters=4, kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(batch2)
    batch3 = BatchNormalization() (cnnlstm3)

    out = ConvLSTM2D(filters=4, kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=False,data_format='channels_last')(batch3)

    output = Conv2D(1, (1, 1), activation='relu',data_format='channels_last')(out) 

    model = Model(input = inputs, output = output)
    return model

def CnnLSTM2(input_shape):

    inputs = Input((input_shape[2],input_shape[0],input_shape[1],1))

    cnnlstm1 = ConvLSTM2D(filters=128, kernel_size=(5, 5), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(inputs)


    batch1 = BatchNormalization() (cnnlstm1)

    cnnlstm2 = ConvLSTM2D(filters=64, kernel_size=(5, 5), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(batch1)

    batch2 = BatchNormalization() (cnnlstm2)   

    cnnlstm3 = ConvLSTM2D(filters=64, kernel_size=(5, 5), activation='relu',
                       padding='same', return_sequences=False,data_format='channels_last')(batch2)

    output = Conv2D(1, (1, 1), activation='relu',data_format='channels_last')(cnnlstm3) 

    model = Model(input = inputs, output = output)
    return model

def CnnLSTM3(input_shape):

    inputs = Input((input_shape[2],input_shape[0],input_shape[1],1))

    cnnlstm1 = ConvLSTM2D(filters=64, kernel_size=(9, 9), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(inputs)


    batch1 = BatchNormalization() (cnnlstm1)

    cnnlstm2 = ConvLSTM2D(filters=32, kernel_size=(5, 5), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(batch1)

    batch2 = BatchNormalization() (cnnlstm2)


    cnnlstm3 = ConvLSTM2D(filters=18, kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(batch2)


    batch3 = BatchNormalization() (cnnlstm3)


    cnnlstm4 = ConvLSTM2D(filters=8, kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(batch3)


    batch4 = BatchNormalization() (cnnlstm4)


    cnnlstm5 = ConvLSTM2D(filters=4, kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=False,data_format='channels_last')(batch4)

    batch5 = BatchNormalization() (cnnlstm5)   

    output = Conv2D(1, (1, 1), activation='sigmoid',data_format='channels_last')(batch5) 

    model = Model(input = inputs, output = output)
    return model


def lstmLayer(inp,filters = [20,20]):

    shape_inp = int_shape(inp)


    lstm_shape = Reshape((shape_inp[-1],shape_inp[1],shape_inp[2],1))(inp)


    lstm_conv = ConvLSTM2D(filters=filters[0], kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(lstm_shape)
    
    

    for i in filters[1:-1]:
        lstm_conv = ConvLSTM2D(filters=i, kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=True,data_format='channels_last')(lstm_conv)
        

    lstm_conv = ConvLSTM2D(filters=filters[-1], kernel_size=(3, 3), activation='relu',
                       padding='same', return_sequences=False,data_format='channels_last')(lstm_conv)
    

    return lstm_conv


def LSTM_Meets_Unet_Upconv(input_shape,
                    n_predictions=1,
                    simpleclassification=None,
                    flatten_output=False,
                    activation_hidden="relu",
                    activation_output="relu"):

    
    inputs = Input(shape=input_shape)


    conv01 = Conv2D(10, kernel_size=(3, 3), padding="same")(inputs)       
    conv01 = Activation(activation_hidden)(conv01)
    conv01 = BatchNormalization() (conv01)
    conv01_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv01)            
    

    conv02 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv01_pool)  
    conv02 = Activation(activation_hidden)(conv02)
    conv02 = BatchNormalization() (conv02)
    conv02_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv02)            
    
    conv03 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv02_pool)  
    conv03 = Activation(activation_hidden)(conv03)
    conv03 = BatchNormalization() (conv03)
    conv03_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv03)            
    

    lstm_conv3 = lstmLayer(conv03,filters = [20,20,20])
    lstm_conv3 = BatchNormalization() (lstm_conv3)
    conv03 = concatenate([conv03, lstm_conv3], axis=3)

    conv04 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv03_pool)  
    conv04 = Activation(activation_hidden)(conv04)
    conv04 = BatchNormalization() (conv04)
    conv04_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv04)            
    

    lstm_conv4 = lstmLayer(conv04,filters = [20,20,20,20])
    lstm_conv4 = BatchNormalization() (lstm_conv4)

    conv04 = concatenate([conv04, lstm_conv4], axis=3)

    ### UPSAMPLING:
    up04 = Conv2DTranspose(20,(3, 3),strides=(2,2),padding="same")(conv04_pool)    
    up04 = BatchNormalization() (up04)
    up04 = concatenate([conv04, up04], axis=3)  
    up04 = Conv2D(20, kernel_size=(3, 3), padding="same")(up04)  
    

    up03 = Conv2DTranspose(20,(3, 3),strides=(2,2),padding="same")(up04)           
    up03 = BatchNormalization() (up03)
    up03 = concatenate([conv03, up03], axis=3)  
    up03 = Conv2D(20, kernel_size=(3, 3), padding="same")(up03)  
    

    up02 = Conv2DTranspose(20,(3, 3),strides=(2,2),padding="same")(up03)           
    up02 = BatchNormalization() (up02)
    up02 = concatenate([conv02, up02], axis=3)  
    up02 = Conv2D(20, kernel_size=(3, 3), padding="same")(up02)  
    

    up01 = Conv2DTranspose(20,(3, 3),strides=(2,2),padding="same")(up02)           
    up01 = BatchNormalization() (up01)
    up01 = concatenate([conv01, up01], axis=3)  
    up01 = Conv2D(20, kernel_size=(3, 3), padding="same")(up01)  
    
    output = Conv2D(n_predictions, (1, 1), activation=activation_output)(up01) 


    model = Model(inputs=inputs, outputs=output)

    return model


def LSTM_Meets_Unet(input_shape,
                    n_predictions=2,
                    simpleclassification=None,
                    flatten_output=False,
                    activation_hidden="relu",
                    activation_output="softmax"):

    
    inputs = Input(shape=input_shape)


    conv01 = Conv2D(10, kernel_size=(3, 3), padding="same")(inputs)       
    conv01 = Activation(activation_hidden)(conv01)
    conv01_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv01)            
    

    conv02 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv01_pool)  
    conv02 = Activation(activation_hidden)(conv02)
    conv02_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv02)            
    
    conv03 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv02_pool)  
    conv03 = Activation(activation_hidden)(conv03)
    conv03_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv03)            
    

    lstm_conv3 = lstmLayer(conv03,filters = [20,20,20])
    conv03 = concatenate([conv03, lstm_conv3], axis=3)

    conv04 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv03_pool)  
    conv04 = Activation(activation_hidden)(conv04)
    conv04_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv04)            
    

    lstm_conv4 = lstmLayer(conv04,filters = [20,20,20,20])
    conv04 = concatenate([conv04, lstm_conv4], axis=3)

    ### UPSAMPLING:
    up04 = UpSampling2D((2, 2))(conv04_pool)    
    up04 = concatenate([conv04, up04], axis=3)  
    up04 = Conv2D(20, kernel_size=(3, 3), padding="same")(up04)  
    

    up03 = UpSampling2D((2, 2))(up04)           
    up03 = concatenate([conv03, up03], axis=3)  
    up03 = Conv2D(20, kernel_size=(3, 3), padding="same")(up03)  
    

    up02 = UpSampling2D((2, 2))(up03)           
    up02 = concatenate([conv02, up02], axis=3)  
    up02 = Conv2D(20, kernel_size=(3, 3), padding="same")(up02)  
    

    up01 = UpSampling2D((2, 2))(up02)           
    up01 = concatenate([conv01, up01], axis=3)  
    up01 = Conv2D(20, kernel_size=(3, 3), padding="same")(up01)  
    
    output = Conv2D(n_predictions, (1, 1), activation=activation_output)(up01) 


    model = Model(inputs=inputs, outputs=output)

    return model

def LSTM_Meets_Unet_Poisson(input_shape,
                    n_predictions=1,
                    simpleclassification=None,
                    flatten_output=False,
                    activation_hidden="relu",
                    activation_output="relu"):

    
    inputs = Input(shape=input_shape)


    conv01 = Conv2D(10, kernel_size=(3, 3), padding="same")(inputs)       
    conv01 = Activation(activation_hidden)(conv01)
    conv01_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv01)            
    

    conv02 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv01_pool)  
    conv02 = Activation(activation_hidden)(conv02)
    conv02_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv02)            
    
    conv03 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv02_pool)  
    conv03 = Activation(activation_hidden)(conv03)
    conv03_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv03)            
    

    lstm_conv3 = lstmLayer(conv03,filters = [20,20,20])
    conv03 = concatenate([conv03, lstm_conv3], axis=3)

    conv04 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv03_pool)  
    conv04 = Activation(activation_hidden)(conv04)
    conv04_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv04)            
    

    lstm_conv4 = lstmLayer(conv04,filters = [20,20,20,20])
    conv04 = concatenate([conv04, lstm_conv4], axis=3)

    ### UPSAMPLING:
    up04 = UpSampling2D((2, 2))(conv04_pool)    
    up04 = concatenate([conv04, up04], axis=3)  
    up04 = Conv2D(20, kernel_size=(3, 3), padding="same")(up04)  
    

    up03 = UpSampling2D((2, 2))(up04)           
    up03 = concatenate([conv03, up03], axis=3)  
    up03 = Conv2D(20, kernel_size=(3, 3), padding="same")(up03)  
    

    up02 = UpSampling2D((2, 2))(up03)           
    up02 = concatenate([conv02, up02], axis=3)  
    up02 = Conv2D(20, kernel_size=(3, 3), padding="same")(up02)  
    

    up01 = UpSampling2D((2, 2))(up02)           
    up01 = concatenate([conv01, up01], axis=3)  
    up01 = Conv2D(20, kernel_size=(3, 3), padding="same")(up01)  
    
    output = Conv2D(1, (1, 1), activation=tf.exp)(up01) 
    
    #output = tfp.layers.DistributionLambda(tfp.distributions.Poisson)(output)
    output = tfp.layers.IndependentPoisson(1)(output)

    model = Model(inputs=inputs, outputs=output)

    return model


def LSTM_Meets_Unet_ZeroInflated(input_shape,
                    n_predictions=1,
                    simpleclassification=None,
                    flatten_output=False,
                    activation_hidden="relu",
                    activation_output="relu"):


    def zeroInflatedPoisson(output):
        rate = tf.math.exp(output[0,:,:,0]) #A 
        s = tf.math.sigmoid(output[0,:,:,1])
        components = [tfd.Deterministic(loc=tf.zeros_like(rate)), #E
         tfd.Poisson(rate=rate) #F 
         ]
        mixture = tfd.Mixture(
              cat=tfd.Categorical(probs=tf.stack([1-s, s],axis=-1)),#D
              components=components)
        return mixture

    def poss(output):
        rate = tf.math.exp(output)
        return tfp.layers.IndependentPoisson(rate)
    
    inputs = Input(shape=input_shape)


    conv01 = Conv2D(10, kernel_size=(3, 3), padding="same")(inputs)       
    conv01 = Activation(activation_hidden)(conv01)
    conv01 = BatchNormalization() (conv01)
    conv01_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv01)            
    

    conv02 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv01_pool)  
    conv02 = Activation(activation_hidden)(conv02)
    conv02 = BatchNormalization() (conv02)
    conv02_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv02)            
    
    conv03 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv02_pool)  
    conv03 = Activation(activation_hidden)(conv03)
    conv03 = BatchNormalization() (conv03)
    conv03_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv03)            
    

    lstm_conv3 = lstmLayer(conv03,filters = [20,20,20])
    lstm_conv3 = BatchNormalization() (lstm_conv3)
    conv03 = concatenate([conv03, lstm_conv3], axis=3)

    conv04 = Conv2D(20, kernel_size=(3, 3), padding="same")(conv03_pool)  
    conv04 = Activation(activation_hidden)(conv04)
    conv04 = BatchNormalization() (conv04)
    conv04_pool = MaxPooling2D((2, 2), strides=(2, 2))(conv04)            
    

    lstm_conv4 = lstmLayer(conv04,filters = [20,20,20,20])
    lstm_conv4 = BatchNormalization() (lstm_conv4)

    conv04 = concatenate([conv04, lstm_conv4], axis=3)

    ### UPSAMPLING:
    up04 = Conv2DTranspose(20,(3, 3),strides=(2,2),padding="same")(conv04_pool)    
    up04 = BatchNormalization() (up04)
    up04 = concatenate([conv04, up04], axis=3)  
    up04 = Conv2D(20, kernel_size=(3, 3), padding="same")(up04)  
    

    up03 = Conv2DTranspose(20,(3, 3),strides=(2,2),padding="same")(up04)           
    up03 = BatchNormalization() (up03)
    up03 = concatenate([conv03, up03], axis=3)  
    up03 = Conv2D(20, kernel_size=(3, 3), padding="same")(up03)  
    

    up02 = Conv2DTranspose(20,(3, 3),strides=(2,2),padding="same")(up03)           
    up02 = BatchNormalization() (up02)
    up02 = concatenate([conv02, up02], axis=3)  
    up02 = Conv2D(20, kernel_size=(3, 3), padding="same")(up02)  
    

    up01 = Conv2DTranspose(20,(3, 3),strides=(2,2),padding="same")(up02)           
    up01 = BatchNormalization() (up01)
    up01 = concatenate([conv01, up01], axis=3)  
    up01 = Conv2D(20, kernel_size=(3, 3), padding="same")(up01)  
    
    output = Conv2D(2, (1, 1), activation=tf.exp)(up01) 
    
    
    output = tfp.layers.DistributionLambda(zeroInflatedPoisson)(output)
    #output = tfp.layers.DistributionLambda(poss)(output)
    #output = tfp.layers.IndependentPoisson()(output)

    model = Model(inputs=inputs, outputs=output)

    return model