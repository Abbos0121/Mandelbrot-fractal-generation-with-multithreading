import numpy as np
from PIL import Image
import concurrent.futures

# Параметры изображения
WIDTH, HEIGHT = 800, 800
MAX_ITER = 256

# Границы фрактала на комплексной плоскости
X_MIN, X_MAX = -2.5, 1.5
Y_MIN, Y_MAX = -2.0, 2.0


# Функция для расчета количества итераций для точки
def mandelbrot(c, max_iter=MAX_ITER):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n


# Функция для вычисления части фрактала
def compute_row(y):
    row = np.zeros(WIDTH, dtype=np.uint8)
    for x in range(WIDTH):
        # Преобразование координат
        re = X_MIN + (x / WIDTH) * (X_MAX - X_MIN)
        im = Y_MIN + (y / HEIGHT) * (Y_MAX - Y_MIN)
        c = complex(re, im)
        # Вычисляем фрактал для точки
        color = mandelbrot(c)
        row[x] = color
    return row


# Основная функция для многопоточной генерации изображения
def generate_fractal():
    image = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Параллельно вычисляем строки
        results = executor.map(compute_row, range(HEIGHT))
        for y, row in enumerate(results):
            image[y, :] = row

    return image


# Генерация изображения
image_data = generate_fractal()

# Преобразование данных в изображение и сохранение
img = Image.fromarray(np.uint8(image_data * 255 / MAX_ITER))
img = img.convert("RGB")
img.save("mandelbrot_fractal.png")
img.show()
