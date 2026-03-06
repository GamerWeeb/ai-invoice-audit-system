import layoutparser as lp
import cv2

model = lp.Detectron2LayoutModel(
    "lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config",
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
    label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
)


def detect_layout(image_path):

    image = cv2.imread(image_path)

    layout = model.detect(image)

    tables = [b for b in layout if b.type == "Table"]

    return tables