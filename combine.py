# 该文件用于将指定的标注 json 文件进行合并
# 不是单纯合并, 由于每个json文件都是从0开始(有重叠)
# 所以需要改变每个json的id号再进行合并

'''
给出 json 格式:
    
{
    "images": [
        {
            "width": 1280,
            "height": 720,
            "file_name": "ch02_20181031094002_00001.jpg",
            "id": 0
        },
        {
            "width": 1280,
            "height": 720,
            "file_name": "ch02_20181031094002_00002.jpg",
            "id": 1
        },
        {
            "width": 1280,
            "height": 720,
            "file_name": "ch02_20181031094002_00003.jpg",
            "id": 2
        }
    ],
    "annotations": [
        {
            "segmentation": [],
            "bbox": [
                878,
                187,
                84,
                311
            ],
            "category_id": 0,
            "image_id": 0,
            "id": 0,
            "area": 26124
        }
    ],
    "categories": [
        {
            "supercategory": "none",
            "name": "person",
            "id": 0
        },
        {
            "supercategory": "none",
            "name": "face",
            "id": 1
        },
        {
            "supercategory": "none",
            "name": "certificate",
            "id": 2
        },
        {
            "supercategory": "none",
            "name": "Mobile_phone",
            "id": 3
        },
        {
            "supercategory": "none",
            "name": "notebook",
            "id": 4
        },
        {
            "supercategory": "none",
            "name": "chest",
            "id": 5
        }
    ]
}

['images', 'annotations', 'categories'] 三个大字典

'''


import json

class JSON2COCO:
    
    def __init__(self, json_file_list):
        
        self.categories = None # 就是json文件中的 'categories' 那个字典
        self.json_file_list = json_file_list
        
        self.global_img_idx = 0
        self.global_ann_idx = 0
    
    
    def analy_JSON(self, json_dic, json_name):
        
        # 图片数量
        img_num = len(json_dic['images'])
        # 标注数量
        ann_num = len(json_dic['annotations'])
        
        # 由于所有的json的类别都一样, 故而只保留一个
        if self.categories is None: 
            self.categories = json_dic['categories']
        else:
            if self.categories != json_dic['categories']:
                raise ValueError("文件 %s 的 categories 不同"%json_name)
                
        return img_num, ann_num
        
    
    @staticmethod
    def edit_JSON(json_dic, json_name, img_start, ann_start):
        
        if json_dic["images"][0]["id"] != 0:
            raise ValueError("文件 %s 的 起始id不是0"%json_name)
        
        for i, img in enumerate(json_dic["images"]):
            json_dic["images"][i]["id"] += img_start
        
        for i, ann in enumerate(json_dic["annotations"]):
            json_dic["annotations"][i]["image_id"] += img_start
            json_dic["annotations"][i]["id"] += ann_start
            
        return json_dic
    
    @staticmethod
    def combine_JSON(*json_dicts):
        
        all_json = json_dicts[0].copy()
        
        for json_dict in json_dicts[1:]:
            all_json['images'] += json_dict['images']
            all_json['annotations'] += json_dict['annotations']
            
        return all_json
        
    
    def run(self, save_path=None):
        
        all_json_list = []
        for json_file in self.json_file_list:
            
            with open(json_file) as f:
                json_dic = json.load(f)
                            
            json_dic = self.edit_JSON(json_dic, 
                                      json_file, 
                                      self.global_img_idx, 
                                      self.global_ann_idx)
            
            all_json_list.append(json_dic)
            
            img_num, ann_num = self.analy_JSON(json_dic, json_file)            
            self.global_img_idx += img_num
            self.global_ann_idx += ann_num
            
        all_json = self.combine_JSON(*all_json_list)
        
        if save_path is None: return all_json
        
        with open(save_path, 'w') as f:
            json.dump(all_json, f)
        
        return all_json


if __name__ == '__main__':
    
    all_json_path = ["/home/s8/Desktop/~5k/coco1修改后.json",
                     "/home/s8/Desktop/~5k/coco2修改后.json",
                     "/home/s8/Desktop/~5k/coco3_2修改后.json",
                     "/home/s8/Desktop/~5k/coco3修改后.json",
                     "/home/s8/Desktop/~5k/coco4修改后.json",
                     "/home/s8/Desktop/~5k/coco5修改后.json",
                     "/home/s8/Desktop/~5k/coco6修改后.json",
                     "/home/s8/Desktop/~2.4w/photo2.json",
                     "/home/s8/Desktop/~2.4w/photo3_2.json",
                     "/home/s8/Desktop/~2.4w/photo3.json",
                     "/home/s8/Desktop/~2.4w/photo4_2.json",
                     "/home/s8/Desktop/~2.4w/photo4.json",
                     "/home/s8/Desktop/~2.4w/photo6_2.json",
                     "/home/s8/Desktop/~2.4w/photo6.json"]
    go = JSON2COCO(all_json_path)
    all_json = go.run('./all.json')
    
    
    
    
    
    
    
