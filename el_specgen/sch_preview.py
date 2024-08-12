import os
from PIL import Image

preview_dir = "doc/schematic_previews/"


def find_previews(vault):
    files = os.listdir(vault + preview_dir)
    previews = []
    for i in files:
        if i.find("_") != -1 and i.find(".png") != -1:
            if i.find("nomen") != -1:
                continue
            elif i.find('over') != -1:
                continue
            elif i.find('diagram') != -1:
                continue
            else:
                previews.append(i)
    return previews


def cut_preview(vault, previews):
    for i in previews:
        img = Image.open(vault + preview_dir + i)
        width, height = img.size
        left = 27
        top = 27
        right = width - 7
        bottom = height - 56
        im1 = img.crop((left, top, right, bottom))
        im1.save("resized" + i)


def delete_cut():
    files = os.listdir("./")
    for i in files:
        if i.find("resized") != -1 and i.find(".png") != -1:
            os.remove(i)


def get_cut():
    resized = []
    files = os.listdir("./")
    for i in files:
        if i.find("resized") != -1 and i.find(".png") != -1:
            resized.append(i)
    return resized


if __name__ == "__main__":
    prev = find_previews("/Users/doc/projects/comitas/agv-m-schematics/")
    cut_preview("/Users/doc/projects/comitas/agv-m-schematics/", prev)
    delete_cut()
    print(get_cut(prev))
