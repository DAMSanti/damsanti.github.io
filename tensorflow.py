import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define las rutas a tus imágenes de entrenamiento y prueba
ruta_entrenamiento = '/proyecto/calidad/fotos/train/'
ruta_prueba = '/proyecto/calidad/fotos/test/'

# Utiliza un generador de imágenes para cargar y preprocesar tus datos
datagen = ImageDataGenerator(rescale=1.0/255.0)  # Normaliza los píxeles al rango [0, 1]

generador_entrenamiento = datagen.flow_from_directory(
    ruta_entrenamiento,
    target_size=(32, 32),  # Ajusta el tamaño de acuerdo a tus necesidades
    batch_size=64,
    class_mode='categorical'  # Cambia esto si tienes otro tipo de problema de clasificación
)

generador_prueba = datagen.flow_from_directory(
    ruta_prueba,
    target_size=(32, 32),
    batch_size=64,
    class_mode='categorical'
)

# Define el modelo de la CNN
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(generador_entrenamiento.num_classes, activation='softmax')  # Número de clases dinámico
])

# Compila el modelo
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Resumen del modelo
model.summary()

# Entrenamiento del modelo con los generadores de imágenes
model.fit(generador_entrenamiento, epochs=10, validation_data=generador_prueba)

# Guarda el modelo entrenado
model.save('modelo_entrenado.h5')
