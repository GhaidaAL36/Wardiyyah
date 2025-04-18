import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


img_size = 224
batch_size = 32
epochs = 35  

# Augmentation 
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.05,
    height_shift_range=0.05,
    zoom_range=0.1,
    brightness_range=[0.9, 1.1],
    horizontal_flip=True,
    validation_split=0.2
)


train_data = datagen.flow_from_directory(
    "flowers_dataset",
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    "flowers_dataset",
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode="categorical",
    subset="validation"
)


class_labels = {v: k for k, v in train_data.class_indices.items()}
with open("flower_class_labels.txt", "w", encoding="utf-8") as f:
    for i in range(len(class_labels)):
        f.write(f"{class_labels[i]}\n")


base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3))
base_model.trainable = False  


x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
predictions = Dense(len(train_data.class_indices), activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer=Adam(learning_rate=1e-4), loss='categorical_crossentropy', metrics=['accuracy'])


callbacks = [
    EarlyStopping(patience=3, restore_best_weights=True),
    ModelCheckpoint("flower_model.h5", save_best_only=True)
]


history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=epochs,
    callbacks=callbacks
)


base_model.trainable = True
for layer in base_model.layers[:-50]:
    layer.trainable = False

model.compile(optimizer=Adam(learning_rate=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])


fine_tune_epochs = 5
total_epochs = epochs + fine_tune_epochs

history_finetune = model.fit(
    train_data,
    validation_data=val_data,
    epochs=total_epochs,
    initial_epoch=history.epoch[-1] + 1,
    callbacks=callbacks
)


acc = history.history['accuracy'] + history_finetune.history['accuracy']
val_acc = history.history['val_accuracy'] + history_finetune.history['val_accuracy']

plt.figure(figsize=(8, 5))
plt.plot(acc, label='دقة التدريب')
plt.plot(val_acc, label='دقة التحقق')
plt.title('دقة النموذج مع Fine-Tuning')
plt.xlabel('Epoch')
plt.ylabel('الدقة')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("training_accuracy_plot.png")
plt.show()
