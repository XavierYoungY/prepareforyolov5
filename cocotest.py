from pycocotools.coco import COCO

coco = COCO("./all.json")

print(coco.getCatIds())
# print()

