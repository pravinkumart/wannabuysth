# coding=utf-8
import os.path, shutil
from PIL import Image, ImageEnhance
import StringIO

quality = 100
resample = 1


def get_size(filename):
    try:
        im = Image.open(filename)
        return im.size
    except:
        return None


def thumbnail(filename, size=(100, 100), thumbnail_filename=None, orientation=None, sharpness=True, quality=100):
    try:
        im = Image.open(filename)
        im = im.convert('RGB')

        if not thumbnail_filename:
            thumbnail_filename = get_default_thumbnail_filename(filename, size)

        if size[0] == 1024:
            if size[0] > im.size[0] - 1 and size[1] > im.size[1] - 1:
                shutil.copyfile(filename, thumbnail_filename)
                return im.size

        if im.size != size:
            path, ext = os.path.splitext(filename)
            if ext.lower() == '.gif':
                im.thumbnail(size)
            else:
                im.thumbnail(size, resample)

        if sharpness:
            if size[0] < 500:
                enhancer = ImageEnhance.Sharpness(im)
                im = enhancer.enhance(2.0)

        if orientation:
            if orientation == 'Rotated 90 CW':
                im = im.rotate(-90)
            elif orientation == 'Rotated 90 CCW':
                im = im.rotate(90)

        # get the thumbnail data in memory.

        im.save(file(thumbnail_filename, 'wb'), "JPEG", quality=quality)

        return im.size
    except:
        return None

def get_default_thumbnail_filename(filename, size):
    return filename
    # path, ext = os.path.splitext(filename)
    # return path + '_'+ str(size[0]) + ext

def rotate(filename, angle):
    im = Image.open(filename)
    im = im.rotate(angle, resample)

    im.save(file(filename, 'wb'), "JPEG", quality=quality)

    return filename


def crop(filename, crop_filename=None, size=(80, 80), sharpness=True):
    im = Image.open(filename)
    im = im.convert('RGB')
    if not crop_filename:
        crop_filename = get_default_thumbnail_filename(filename, size)

    x0, y0 = im.size
    if x0 > y0: y = size[1]; x = y * x0 / y0
    else: x = size[0]; y = y0 * x / x0
    thumb_size = x, y
    im = im.resize(thumb_size, resample)

    if x > y: box = ((x - size[0]) / 2, 0, (x + size[0]) / 2, y)
    else: box = (0, (y - size[1]) / 2, x, (y + size[1]) / 2)
    im = im.crop(box)

    if sharpness:
        if size[0] < 500:
            enhancer = ImageEnhance.Sharpness(im)
            im = enhancer.enhance(2.0)

    im.save(file(crop_filename, 'wb'), 'JPEG', quality=quality)
    return im.size



def thumbnail_img(infile, file_name, size=(1000, 1000), sharpness=True, quality=100):
    '''
    @note: 压缩图片
    @param infile:文件对象StringIO
    @param file_name:文件名字
    @return: 返回文件对象StringIO
    '''

    tmp_img = StringIO.StringIO()
    im = Image.open(infile)
    im = im.convert('RGB')

    if im.size != size:
        path, ext = os.path.splitext(file_name)
        if ext.lower() == '.gif':
            if infile.len < 1000000:  # gif图小于1M 不处理
                infile.seek(0)
                return infile
            im.thumbnail(size)
        else:
            im.thumbnail(size, resample)

    if sharpness:
        if size[0] < 500:
            enhancer = ImageEnhance.Sharpness(im)
            im = enhancer.enhance(2.0)

    im.save(tmp_img, "JPEG", quality=quality)
    tmp_img.seek(0)

    return tmp_img


if __name__ == '__main__':
    file_name = 'd009b3de9c82d158d6ebe27a800a19d8bd3e428b.jpg'
    im = Image.open(file_name)
    im = im.convert('RGB')
    left = 0
    top = 0
    right = 1600
    bottom = 80
    box = (int(left), int(top), int(right), int(bottom))
    region = im.crop(box)
    f = open('1.jpg', 'wb')
#     f.write(f)
    region.seek(0)
    region.save('1.jpg')
#     f.write(region.seek())
#     f.close()

