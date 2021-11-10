import os
import random
import json
import tqdm
import xml.dom.minidom

##############################
# 将数据标注格式转换为coco
##############################
def convert_xml_to_coco(split_file, json_out_path, class_name_file, img_start_id=1):
    '''
    Args:
        split_file:.txt file, each line is an valid relative path or absolute path. endswith ".xml"
        json_out_path: e.g.: /home/Codes/train_annotations.json.
        class_name_file: json file, each line is a class name.
        img_start_id: img_id start point.
    '''
    assert json_out_path.endswith(".json"), "output path must be a .json path!"
    assert split_file.endswith(".txt"), "output path must be a .txt path!"
    assert class_name_file.endswith(".json"), "class_name_file must be a .json path!"

    #load class info
    with open(class_name_file, 'r') as f:
        class_names = json.load(f)

    train_names = open(split_file, 'r').readlines()

    category_infos = list()
    for (cls_name, cls_id) in class_names.items():
        category_infos.append(
            dict(
                {
                    'id':cls_id,
                    'name':cls_name,
                    'supercategory':cls_name
                }
            )
        )
    ##############################################
    # 生成anno，包含img信息和bbox信息
    ##############################################

    image_infos = []
    anno_infos = []

    bbox_id = 0
    for i, one_file in enumerate(tqdm.tqdm(train_names)):

        dom_tree = xml.dom.minidom.parse(one_file.rstrip())
        collection = dom_tree.documentElement
        #get image info and anno infos
        img_name = collection.getElementsByTagName('filename')[0].firstChild.data + ".jpg"
        height = int(collection.getElementsByTagName('height')[0].firstChild.data)
        width = int(collection.getElementsByTagName('width')[0].firstChild.data)

        class_ids = collection.getElementsByTagName('name')
        class_ids = [class_id.firstChild.data for class_id in class_ids]
        xmins = collection.getElementsByTagName('xmin')
        xmins = [xmin.firstChild.data for xmin in xmins]
        xmaxs = collection.getElementsByTagName('xmax')
        xmaxs = [xmax.firstChild.data for xmax in xmaxs]
        ymins = collection.getElementsByTagName('ymin')
        ymins = [ymin.firstChild.data for ymin in ymins]
        ymaxs = collection.getElementsByTagName('ymax')
        ymaxs = [ymax.firstChild.data for ymax in ymaxs]

        box_nums = len(class_ids)
        for j in range(box_nums):
            x1, y1, x2, y2 = int(float(xmins[j])), int(float(ymins[j])), int(float(xmaxs[j])), int(float(ymaxs[j]))

            w, h = x2 - x1, y2 - y1
            area = w * h
            anno_infos.append({
                "id": bbox_id,
                "img_id": img_start_id + i,
                "bbox":[x1, y1, w, h],
                "category_id": int(float(class_ids[j])),
                "area": area,
                "iscrowd": 0,
            })
            bbox_id += 1

        image_info = dict({
            'id': img_start_id + i,
            'file_name': img_name,
            'height': height,
            'width': width
        })

        image_infos.append(image_info)

    full_infos = dict({
        'images':image_infos,
        'annotations': anno_infos,
        'categories':category_infos
    })
    full_infos = json.dumps(full_infos, indent=4, separators=[',',':'], ensure_ascii=False)

    with open(json_out_path, 'w') as f:
        f.write(full_infos)


#############################
# 生成test anno，包含img信息
#############################

# coco_infos = dict()
# image_infos = []
# anno_infos = []

# bbox_id = 0
# for i, one_file_path in enumerate(tqdm.tqdm(test_names)):
#     items = one_file_path.rstrip().split('/')
#     img_name = items[-1]
#     img_id = int(img_name[:-4])
#     image_info = dict({
#         'id':img_id,
#         'file_name':img_name,
#         'height':224,
#         'width':224
#     })
#     image_infos.append(image_info)

# full_infos = dict({
#     'images':image_infos,
#     'annotations': None,
#     'categories':None
# })
# full_infos = json.dumps(full_infos, indent=4, separators=[',',':'], ensure_ascii=False)

# with open('./datasets/ZSOR/test_annos.json', 'w') as f:
#     f.write(full_infos)


