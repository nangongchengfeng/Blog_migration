import os
import shutil
import hashlib


def get_md5(file):
    """计算文件的MD5值"""
    if not os.path.isfile(file):
        return None
    with open(file, 'rb') as f:
        md5 = hashlib.md5()
        md5.update(f.read())
        return md5.hexdigest()


def find_duplicate_images(dir_path):
    """查找重复图片"""
    all_images = []
    md5_list = []
    delete_list = []
    # 遍历整个目录，将所有图片的路径保存到一个列表中
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                all_images.append(os.path.join(root, file))
    # 对于每个图片，计算它的MD5值，并将MD5值和路径保存到两个列表中
    for image in all_images:
        md5 = get_md5(image)
        if md5 is not None:
            md5_list.append(md5)
        else:
            delete_list.append(image)
    # 判断MD5值列表中是否有重复的值，如果有，则说明该图片是重复图片，将其路径保存到一个删除列表中
    for i in range(len(md5_list)):
        for j in range(i + 1, len(md5_list)):
            if md5_list[i] == md5_list[j]:
                delete_list.append(all_images[j])
    # 遍历删除列表，将其中的图片移动到目标目录中
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for image in delete_list:
        try:
            shutil.move(image, os.path.join(target_dir, os.path.basename(image)))
            print('已移动重复文件：', image)
        except Exception as e:
            print('移动失败：%s，错误：%s' % (image, str(e)))
    print('重复图片搜索完成，共找到%d个重复文件！' % len(delete_list))


# 示例
if __name__ == '__main__':
    # 需要移动重复图片的目标目录
    # target_dir设置全局变量
    global target_dir
    target_dir = 'repeat_image'
    dir_path = 'dongman'
    find_duplicate_images(dir_path)
