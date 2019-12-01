from PIL import Image

WORD_LEN = 32


def bin_to_str(binary_string):
    text = ''
    for i in range(len(binary_string) // 8):
        bin_number = binary_string[i * 8:(i + 1) * 8]
        number = int(bin_number, 2)
        text += chr(number)
    return text


def bin_to_int(binary_string):
    return int(binary_string, 2)


def int_to_bin(number):
    return "{0:b}".format(number).zfill(WORD_LEN)


def str_to_bin(text):
    return ''.join(format(ord(char), 'b').zfill(8) for char in text)


def _set_bit(pixel_byte, data_bit):
    if data_bit:
        return pixel_byte | 1
    else:
        return pixel_byte & ~1


def _get_length_with_offset(img, width, height):
    data_length = ""
    for x in range(width):
        for y in range(height):
            if len(data_length) >= WORD_LEN:
                return bin_to_int(data_length[:WORD_LEN]), x, y

            pixel = list(img[x, y])
            for byte in pixel:
                data_length += str(byte & 1)


def embed(data, image):
    width, height = image.size
    img = image.load()
    color_depth = len(img[0, 0])

    padding = ""
    if WORD_LEN % color_depth != 0:
        padding = (color_depth - WORD_LEN % color_depth) * "0"

    data_len_bin = int_to_bin(len(data))

    data = data_len_bin + padding + data

    data = iter(data)
    for x in range(width):
        for y in range(height):
            pixel = list(img[x, y])
            for (i, pixel_byte), bit in zip(enumerate(pixel), data):
                if bit is None:
                    img[x, y] = tuple(pixel)
                    return

                pixel[i] = _set_bit(pixel_byte, int(bit))

            img[x, y] = tuple(pixel)


def extract(image):
    width, height = image.size
    img = image.load()

    data_length, offset_x, offset_y = _get_length_with_offset(img, width, height)

    data = ""
    for x in range(offset_x, width):
        for y in range(offset_y, height):
            pixel = list(img[x, y])
            for byte in pixel:
                if len(data) == data_length:
                    return data

                data += str(byte & 1)


def embed_message(message, image):
    data = str_to_bin(message)
    embed(data, image)
    return image


def extract_message(image):
    return bin_to_str(extract(image))


if __name__ == '__main__':
    input_file = "image.png"
    output_file = "secret.png"
    message = "BSUIR"

    print(f"Message: {message}")
    input_image = Image.open(input_file)
    secret_image = embed_message(message, input_image)
    secret_image.save(output_file)

    output_image = Image.open(output_file)
    print(f"Extracted message: {extract_message(output_image)}")
