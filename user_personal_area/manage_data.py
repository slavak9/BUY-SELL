import string
import random
import cv2
import os
import datetime
import numpy
from django.conf import settings
import subprocess


def get_size_by_width(img,w):
    return cv2.resize(img, (w, img.shape[0] - round((img.shape[1] - w)/(img.shape[1]/img.shape[0]))))


def get_size_by_height(img,h):
    return cv2.resize(img, (img.shape[1] - round((img.shape[0] - h) / (img.shape[0] / img.shape[1])),h))


def set_ratio_16_9_h(img,h):
    ratio = 1.77777778
    side = (h - round(img.shape[0]*ratio))//2
    if side >= 0:
        return img[:,side:h-side]
    else:
        side = round((img.shape[0] - h/ratio)//2)
        print(side)
        return img[side:img.shape[0] - side, :]


def set_ratio_16_9_v(img,v):
    print('v')
    ratio = 1.77777778
    side = (v - round(img.shape[1]*ratio))//2
    if side >= 0:
        return img[side:v-side, :]
    else:
        return img


def get_img_size(image,width):
    if image.shape[0] > image.shape[1]:
       return get_size_by_height(image, width)
    elif image.shape[0] < image.shape[1]:
        return get_size_by_width(image, width)


def get_hd_size(image,size):
    return get_img_size(image, size)


def get_sd_size(image,size):
    new_image = get_img_size(image, size)
    if new_image.shape[0] > new_image.shape[1]:
        return set_ratio_16_9_v(new_image, size)
    elif image.shape[0] < image.shape[1]:
        return set_ratio_16_9_h(new_image, size)


def add_sides_to_v_img(image):
    ratio = 1.77777778
    r = round(((image.shape[0] * ratio) - image.shape[1])/2)
    if r >= 0:
        missing_height = numpy.full((image.shape[0], r, 3), (24, 24, 24), dtype='uint8')
        return numpy.hstack([missing_height, image, missing_height])
    else:
        r = round(((image.shape[1]/ratio)-image.shape[0])//2)
        missing_height = numpy.full((r,image.shape[1], 3), (24, 24, 24), dtype='uint8')
        return numpy.vstack([missing_height, image, missing_height])


def get_img_initial(img, hd_size=None, sd_size=None):
    try:
        if hd_size and (img.shape[1] > hd_size or img.shape[0] > hd_size):
            return get_hd_size(img, hd_size)
        elif hd_size and (img.shape[1] < hd_size and img.shape[0] < hd_size) and ((16/9) != (img.shape[1] / img.shape[0])):
            return add_sides_to_v_img(img)
        elif sd_size and (img.shape[1] > sd_size or img.shape[0] > sd_size):
            img = get_sd_size(img, sd_size)
            if img.shape[0] > img.shape[1]:
                img = add_sides_to_v_img(img)
                if img.shape[0] > sd_size or img.shape[1] >sd_size:
                    img = get_img_size(img,sd_size)
            return img
        elif sd_size and (img.shape[1] <= sd_size and img.shape[0] <= sd_size) and ((16/9) != (img.shape[1] / img.shape[0])):
            img = add_sides_to_v_img(img)
            if img.shape[0] > sd_size or img.shape[1] > sd_size:
                return get_img_size(img,sd_size)
            else:
                return add_sides_to_v_img(img)
        else:
            return img
    except Exception:
        return False


def get_date():
    return str(datetime.datetime.date(datetime.datetime.now())).split('-')


def get_data_path():
    date = get_date()
    return os.path.join(date[0], date[1], date[2], '')


def get_hd_path():
    return os.path.join('product_img', 'hd', get_data_path())


def get_category_path():
    return os.path.join('categories', 'sd')


def get_category_item_path():
    return os.path.join('item_category_img', 'sd')


def get_sd_path():
    return os.path.join('product_img', 'sd', get_data_path())


def get_video_path():
    return os.path.join('product_video', get_data_path())


def make_dirs_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def get_full_path(path):
        return os.path.join(settings.MEDIA_ROOT,path)


def save_img(image,file):
    cv2.imwrite(file,image)


def new_file_name(s):
    sting = random.choices(string.ascii_letters, k=3)
    return s[:s.rfind('.')]+(''.join(sting))+s[s.rfind('.'):]


def get_file_name(path,name):
    if not os.path.isfile(os.path.join(path,name)):
        return name
    else:
        return get_file_name(path,new_file_name(name))



def get_path_file(img,path,name):
    full_path = get_full_path(path)
    make_dirs_path(full_path)
    file_name = get_file_name(full_path, name)
    try:
        save_img(img, os.path.join(full_path,file_name))
    except Exception:
        return False
    return {'path':path,'file_name':file_name}


def convert_img(img_file):
    value = numpy.fromstring(img_file.read(), numpy.uint8)
    return cv2.imdecode(value, cv2.IMREAD_COLOR)


def set_img_initial(img_file, hd_size=None, sd_size=None):
    img = convert_img(img_file)
    hd = get_img_initial(img,hd_size=hd_size)
    HD_SD_path = {'HD':'','SD':''}
    if type(hd) == bool:
        return False
    HD_SD_path['HD'] = get_path_file(hd,get_hd_path(),img_file.name)
    if sd_size:
        sd = get_img_initial(img, sd_size=sd_size)
        HD_SD_path['SD'] = get_path_file(sd, get_sd_path(),img_file.name)
    return HD_SD_path


def set_des_img(img_file, hd_size=None):
    img = convert_img(img_file)
    hd = get_img_initial(img, hd_size=hd_size)
    if type(hd) == bool:
        return False
    if hd.shape[0] > hd.shape[1]:
        hd = add_sides_to_v_img(hd)
    return get_path_file(hd,get_hd_path(),img_file.name)


def get_video_by_width(w, h, s):
    return (s, h - round((w - s) / (w / h)))

def get_video_by_height(w, h, s):
    return (s - round((h - s) / (h / w)), s)


def get_size_video(path):
    video = cv2.VideoCapture(path)
    size = 960
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if width <= size and height <= size:
        size = [width, height]
    else:
        if width > height:
            size = get_video_by_width(width, height, size)
        elif height > width:
            size = get_video_by_height(width, height, size)
    size = [i - 1 if i % 2 else i for i in size]
    fps = round(video.get(cv2.CAP_PROP_FPS)) if round(video.get(cv2.CAP_PROP_FPS)) < 30 else 30
    size.append(fps)
    return size


def transform_video(file,file_destination):
    path = file.temporary_file_path()
    size = get_size_video(path)
    time_start = '00:00'
    duration_of_time = '120'
    fps = f'{size[2]}'
    crf = '28'
    width = size[0]
    height = size[1]
    process = subprocess.run(
        [f'ffmpeg', '-i', path,
         '-ss', time_start, '-t', duration_of_time,
         '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
         '-r', fps, '-crf', crf, '-c:a', 'aac',
         '-b:a', '128k', '-filter:v', f'scale={width}:{height}',
         file_destination], shell=True)
    file.close()
    if process.returncode:
        print('FFMPEG ERROR: in user_personal_area\manage_data.py could not make process')
        return process.returncode



def get_video_file_path(path,name):
    full_path = get_full_path(path)
    make_dirs_path(full_path)
    file_name = get_file_name(full_path, name)
    return {'full_path':full_path,'path':path,'file_name':file_name}


def video_load_initial(file):
    path = get_video_file_path(get_video_path(),file.name)
    path['file_name'] = path['file_name'][0:path['file_name'].rfind('.')]+'.mp4'
    response = transform_video(file,os.path.join(path['full_path'],path['file_name']))
    return response if response else path


def set_category_img(img_file, boolean,sd_size=None):
    img = convert_img(img_file)
    sd = get_img_initial(img, sd_size=sd_size)
    if type(sd) == bool:
        return False
    if sd.shape[0] > sd.shape[1]:
        sd = add_sides_to_v_img(sd)
    if boolean:
        return get_path_file(sd,get_category_path(),img_file.name)
    else:
        return get_path_file(sd, get_category_item_path(), img_file.name)



# def transform_video():
#     size = get_size_video()
#     file_source = 'J:\python_django\progect_2\Buy-sell.by\Video.mp4'
#     file_destination = 'J:\python_django\progect_2\Buy-sell.by/new.mp4'
#     time_start = '00:00'
#     duration_of_time = '120'
#     fps = f'{size[2]}'
#     crf = '28'
#     width = size[0]
#     height = size[1]
#     subprocess.run(
#         [f'ffmpeg', '-i', file_source,
#          '-ss', time_start, '-t', duration_of_time,
#          '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
#          '-r', fps, '-crf', crf, '-c:a', 'aac',
#          '-b:a', '128k', '-filter:v', f'scale={width}:{height}',
#          file_destination], shell=True)



    # from io import BytesIO
    #
    # Create a new BytesIO object
    # binary_buffer = BytesIO()

    # Hexadecimal representation of "Hello"
    # binary_buffer.write(data)

    # Get the contents of the buffer as bytes
    # result_bytes = binary_buffer.getvalue()

    # Print the result

    # from PIL import Image
    # import requests
    # endpoint = "http://127.0.0.1/getimage"
    # files = {'file': data}
    # headers = {"content-type": "image/jpg"}
    # response = requests.post(url="",files=files, headers=headers)
    # return response
    # img = Image.open(requests.get(url, stream=True).raw)

    # with open(f'J:/python_django/progect_2/Buy-sell.by/buy_sell/media/product_img/{img_file.name}','wb') as f:
    #     f.write(data)

    # return FileResponse(data,as_attachment=True,filename='new_file',headers=headers)


    # files = {'file': data}
    # headers = {"content-type": "image/jpg"}
    # response = requests.post(files=files, headers=headers)
    # img = Image.open(img_sd)
    # response = HttpResponse(content_type='image/png')
    # response['Content-Disposition'] = 'attachment; filename="output.png"'
    # img.save(response, "PNG")



    # print(data)
    # FileResponse
    # get_hd_size(image, size)
    # f = get_sd_size(img,896)
    # f = add_sides_to_v_img(f)
    # g =cv2.imwrite('new_audi.jpg',f)

