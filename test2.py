import os, cv2
import numpy as np
import matplotlib.pyplot as plt

from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split

from keras import backend as K

K.set_image_dim_ordering('th')
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, RMSprop, adam

class MyClass:
    # %%
    def pre_execute():
        PATH = 'F:\\SupervisedChromeTrex\\keras practise'
        # Define data path
        data_path = PATH + '\data\input_data'
        data_dir_list = os.listdir(data_path)
        img_rows = 128
        img_cols = 128
        num_channel = 1
        num_epoch = 8

        # Define the number of classes
        num_classes = 2

        img_data_list = []

        for dataset in data_dir_list:
            img_list = os.listdir(data_path + '\\' + dataset)
            print('Loaded the images of dataset-' + '{}\n'.format(dataset))
            for img in img_list:
                input_img = cv2.imread(data_path + '\\' + dataset + '\\' + img, 0)
                input_img_resize = cv2.resize(input_img, (128, 128))
                cv2.imwrite(PATH + '\\data\\input_data_resized' + '\\' + dataset + '\\' + img, input_img_resize)
                img_data_list.append(input_img_resize)

        img_data = np.array(img_data_list)
        img_data = img_data.astype('float32')
        img_data /= 255
        print(img_data.shape)

        if num_channel == 1:
            if K.image_dim_ordering() == 'th':
                img_data = np.expand_dims(img_data, axis=1)
                print(img_data.shape)
            else:
                img_data = np.expand_dims(img_data, axis=4)
                print(img_data.shape)
        else:
            if K.image_dim_ordering() == 'th':
                img_data = np.rollaxis(img_data, 3, 1)
                print(img_data.shape)

        # %%
        USE_SKLEARN_PREPROCESSING = False

        if USE_SKLEARN_PREPROCESSING:
            # using sklearn for preprocessing
            from sklearn import preprocessing


            def image_to_feature_vector(image, size=(128, 128)):
                # resize the image to a fixed size, then flatten the image into
                # a list of raw pixel intensities
                return cv2.resize(image, size).flatten()


            img_data_list = []
            for dataset in data_dir_list:
                img_list = os.listdir(data_path + '/' + dataset)
                print('Loaded the images of dataset-' + '{}\n'.format(dataset))
                for img in img_list:
                    input_img = cv2.imread(data_path + '/' + dataset + '/' + img)
                    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
                    input_img_flatten = image_to_feature_vector(input_img, (128, 128))
                    img_data_list.append(input_img_flatten)

            img_data = np.array(img_data_list)
            img_data = img_data.astype('float32')
            print(img_data.shape)
            img_data_scaled = preprocessing.scale(img_data)
            print(img_data_scaled.shape)

            print(np.mean(img_data_scaled))
            print(np.std(img_data_scaled))

            print(img_data_scaled.mean(axis=0))
            print(img_data_scaled.std(axis=0))

            if K.image_dim_ordering() == 'th':
                img_data_scaled = img_data_scaled.reshape(img_data.shape[0], num_channel, img_rows, img_cols)
                print(img_data_scaled.shape)

            else:
                img_data_scaled = img_data_scaled.reshape(img_data.shape[0], img_rows, img_cols, num_channel)
                print(img_data_scaled.shape)

            if K.image_dim_ordering() == 'th':
                img_data_scaled = img_data_scaled.reshape(img_data.shape[0], num_channel, img_rows, img_cols)
                print(img_data_scaled.shape)

            else:
                img_data_scaled = img_data_scaled.reshape(img_data.shape[0], img_rows, img_cols, num_channel)
                print(img_data_scaled.shape)

        if USE_SKLEARN_PREPROCESSING:
            img_data = img_data_scaled
        # %%
        # Assigning Labels

        # Define the number of classes
        num_classes = 2

        num_of_samples = img_data.shape[0]
        labels = np.ones((num_of_samples,), dtype='int64')

        labels[0:117] = 0
        labels[117:] = 1

        names = ['cats', 'dogs']

        # convert class labels to on-hot encoding
        Y = np_utils.to_categorical(labels, num_classes)

        # Shuffle the dataset
        x, y = shuffle(img_data, Y, random_state=2)
        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

        # %%
        # Defining the model
        input_shape = img_data[0].shape

        model = Sequential()

        model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(Convolution2D(32, 3, 3))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.5))

        model.add(Convolution2D(64, 3, 3))
        model.add(Activation('relu'))
        # model.add(Convolution2D(64, 3, 3))
        # model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.5))

        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes))
        model.add(Activation('softmax'))

        # sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        # model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=["accuracy"])
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=["accuracy"])

        # Viewing model_configuration

        model.summary()
        model.get_config()
        model.layers[0].get_config()
        model.layers[0].input_shape
        model.layers[0].output_shape
        model.layers[0].get_weights()
        np.shape(model.layers[0].get_weights()[0])
        model.layers[0].trainable

        # %%
        # Training
        hist = model.fit(X_train, y_train, batch_size=16, nb_epoch=num_epoch, verbose=1, validation_data=(X_test, y_test))

        # hist = model.fit(X_train, y_train, batch_size=32, nb_epoch=20,verbose=1, validation_split=0.2)

        # Training with callbacks
        from keras import callbacks

        filename = 'model_train_new.csv'
        csv_log = callbacks.CSVLogger(filename, separator=',', append=False)

        early_stopping = callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=0, verbose=0, mode='min')

        filepath = "Best-weights-my_model-{epoch:03d}-{loss:.4f}-{acc:.4f}.hdf5"

        checkpoint = callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')

        callbacks_list = [csv_log, early_stopping, checkpoint]

        hist = model.fit(X_train, y_train, batch_size=16, nb_epoch=num_epoch, verbose=1, validation_data=(X_test, y_test),
                         callbacks=callbacks_list)

    # %%

    def mypredict(temp_img):
        # Evaluating the model
        score = model.evaluate(X_test, y_test, verbose=0)
        print('Test Loss:', score[0])
        print('Test accuracy:', score[1])

        # Testing a new image
        #test_image = cv2.imread(path, 0)
        test_image = temp_img
        test_image = cv2.resize(test_image, (128, 128))
        test_image = np.array(test_image)
        test_image = test_image.astype('float32')
        test_image /= 255
        print(test_image.shape)

        if num_channel == 1:
            if K.image_dim_ordering() == 'th':
                test_image = np.expand_dims(test_image, axis=0)
                test_image = np.expand_dims(test_image, axis=0)
                print(test_image.shape)
            else:
                test_image = np.expand_dims(test_image, axis=3)
                test_image = np.expand_dims(test_image, axis=0)
                print(test_image.shape)

        else:
            if K.image_dim_ordering() == 'th':
                test_image = np.rollaxis(test_image, 2, 0)
                test_image = np.expand_dims(test_image, axis=0)
                print(test_image.shape)
            else:
                test_image = np.expand_dims(test_image, axis=0)
                print(test_image.shape)

        # Predicting the test image
        #print((model.predict(test_image)))
        return model.predict_classes(test_image)
