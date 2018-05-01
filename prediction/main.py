import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications

# dimensions of our images.
img_width, img_height = 150, 150

top_model_weights_path = 'bottleneck_fc_model.h5'
train_data_dir = 'data/training'
validation_data_dir = 'data/validation'
nb_train_samples = 19
nb_validation_samples = 14
epochs = 50
batch_size = 10


def save_bottlebeck_features():
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_train = model.predict_generator(
        generator, nb_train_samples // batch_size)
    #print(bottleneck_features_train)
    np.save(open('bottleneck_features_train.npy', 'wb'),str(bottleneck_features_train))

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_validation = model.predict_generator(
        generator, nb_validation_samples // batch_size)
    #print(bottleneck_features_validation);
    np.save(open('bottleneck_features_validation.npy', 'wb'),str(bottleneck_features_validation))
    print('Saved');


def train_top_model():
    train_data = np.load(open('bottleneck_features_train.npy','rb'))
    train_labels = np.array(['card1','card1','card1','card2','card2','card2','card2','keychain','keychain','keychain','keychain','keychain','keychain','keychain','mug','mug','qc','qc','qc'])
    validation_data = np.load(open('bottleneck_features_validation.npy','rb'))
    validation_labels = np.array(['card1','card1','card2','card2','card2','keychain','keychain','keychain','keychain','keychain','keychain','mug','qc','qc'])

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels))
    model.save_weights(top_model_weights_path)


save_bottlebeck_features()
train_top_model()