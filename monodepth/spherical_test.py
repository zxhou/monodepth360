import tensorflow as tf

from image_utils import *

from spherical import *

def equirectangular_to_cubic_test():
    # Load equirectangular image.
    filename = "equirectangular"
    equirectangular_image = read_image(filename + ".jpg", [1024, 2048])

    # Extract cube faces.
    cubic_images = equirectangular_to_cubic(equirectangular_image, [512, 512])
    session = tf.Session()

    # Save faces to disk.
    for index in range(6):
        cubic_image = cubic_images[index]
        face = face_map[index]
        image_data = session.run(encode_image(cubic_image))
        write_image(image_data, "cubic_{}.jpg".format(face))

def cubic_to_equirectangular_test():
    # Load cube faces.
    filenames = ["cubic_{}.jpg".format(face) for face in face_map]
    cubic_images = [read_image(filename, [512, 512]) for filename in filenames]

    # Convert to equirectangular format.
    equirectangular_image = cubic_to_equirectangular(cubic_images, [1024, 2048])
    session = tf.Session()

    # Save to disk.
    image_data = session.run(encode_image(equirectangular_image))
    write_image(image_data, "equirectangular_test.jpg")

def rotate_test():
    # Load equirectangular image.
    filename = "equirectangular"
    equirectangular_image = read_image(filename + ".jpg", [1024, 2048])

    rx = tf.stack([0.0, 0.0, 0.5])
    ry = tf.stack([- 0.5, 0.5, 0.0])
    rz = tf.stack([0.0, 0.0, 0.5])

    # Rotate image.
    rotated_images = rotate(tf.tile(equirectangular_image, [3, 1, 1, 1]), rx, ry, rz)
    session = tf.Session()

    image_data = session.run(encode_images(rotated_images, 3))
    for index in range(3):
        write_image(image_data[index], "rotate_test_{}.jpg".format(index))

def fast_rotate_test():
    # Load equirectangular image.
    filename = "equirectangular"
    equirectangular_image = read_image(filename + ".jpg", [1024, 2048])
    dx = - 256

    # Rotate image.
    rotated_image = fast_rotate(equirectangular_image[0], dx)
    session = tf.Session()

    image_data = session.run(encode_image(tf.expand_dims(rotated_image, 0)))
    write_image(image_data, "fast_rotate_test.jpg")


if __name__ == "__main__":
    equirectangular_to_cubic_test()
    cubic_to_equirectangular_test()
    rotate_test()
    fast_rotate_test()