import os
import random
from datasets.scripts.gen_coco import convert_xml_to_coco

#######################
##  生成训练集和验证集
#######################
#1、根据原始的数据集文件夹层级生成train.txt和val.txt,其中包含每个数据标注的路径
#2、根据train.txt和val.txt中标注的路径，读取并生成coco格式的标注
#3、调整文件夹层级，生成coco层级：
# datasets\
    #wildlife\
        #images\
        #annotations\
#4、images文件夹中包含所有的数据，annotations文件夹中包含所有的标注
#以及train.txt、val.txt、train_annotations.json、val_annotations.json、part_train.txt、part_val.txt以及相应json

train_txt_path = "./datasets/train.txt"
val_txt_path = './datasets/val.txt'
train_json_path = './datasets/train_annotations.json'
val_json_path = './datasets/val_annotations.json'
#step1:生成txt
#从每个类里面随机取一定比例作为训练集，剩下的作为验证集
#txt中存储的是*.xml标注
root_path = "/home/lyx/Codes/New Data"
split_ratio = 0.7 #训练集占比
part_ratio = 0.1 # 从完整的训练集中采样的比例
with open(train_txt_path, 'w') as f1:
    with open(val_txt_path, 'w') as f2:
        cls_names = os.listdir(root_path)
        for cls_name in cls_names:#查看每个类的文件夹
            cls_root_path = os.path.join(root_path, cls_name)
            names = os.listdir(cls_root_path)
            names = [name for name in names if name.endswith('.xml')]
            random.shuffle(names)

            names = names[: int(part_ratio * len(names))] # 进行采样

            split = int(split_ratio * len(names))#进行训练验证划分
            train_names = names[:split]
            train_names = [os.path.join(cls_root_path, name) + '\n' for name in train_names]

            val_names = names[split:]
            val_names = [os.path.join(cls_root_path, name) + '\n' for name in val_names]

            f1.writelines(train_names)
            f2.writelines(val_names)

#step2:生成coco格式标注
class_names_path = "./datasets/classes.json"
# train set
convert_xml_to_coco(train_txt_path, train_json_path, class_names_path)
#val set
convert_xml_to_coco(val_txt_path, val_json_path, class_names_path)

####################################
##    统计数据集每个图片目标数量分布
####################################


# obj_num_statics = dict()

# root_path = 'data/train_data'
# file_paths = os.listdir(root_path)
# txt_file_path = [file for file in file_paths  if file.endswith('.txt')]

# for i, one_file in enumerate(tqdm.tqdm(txt_file_path)):
#     with open(os.path.join(root_path, one_file), 'r') as f:
#         lines = f.readlines()  #list str
#         num = len(lines)
#         if num not in obj_num_statics.keys():
#             obj_num_statics.update({num:1})
#         else:
#             obj_num_statics[num] += 1
            
# #对每个数目级的图片进行排序
# obj_num_statics = sorted(obj_num_statics.items(), key=lambda kv: (kv[1], kv[0]))[:: -1]
# #记录类别名
# with open('obj_num_statics.txt' 'w') as f:
#     f.write(obj_num_statics.keys())

    #记录类别个数
# with open('obj_num_statics.json', 'w') as f:
#     # f.writelines([class_name + ' ' + str(count) + '\n' for class_name, count in classes.items()])

#     json.dump(dict(obj_num_statics), f, indent=4, separators=(',',":"), ensure_ascii=False)
