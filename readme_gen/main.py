import os
import sys


def delete_if_found(file_list, name):
    try:
        index = file_list.index(name)
    except ValueError:
        index = None
    if index is not None:
        file_list.remove(name)


def get_schematic_previews_list(vault):
    str = vault + "doc/schematic_previews/"
    pictures = os.listdir(str)
    delete_if_found(pictures, '.DS_Store')  # fucking NTFS / APFS
    return pictures


def create_name(vault):
    index = None
    for i in range(2, len(vault)):
        if vault[i * -1] == "/" and i != 0:
            index = len(vault) + (i * -1)
            break
    if index is not None:
        last_index = (len(vault) - 1, len(vault) - 2)[vault[len(vault) - 1] != "/"]
        name = vault[index + 1: last_index]
        name = name.replace("_", " ")
        name = name.replace("-", " ")
        name = name.upper()
        name = "## " + name
        return name
    return None


def cmplt_readme(vault):
    readme = open(vault + 'README.md', 'w')
    name = create_name(vault)
    readme.write(name + "\n")
    pic = get_schematic_previews_list(vault)
    pic_xx_ = []
    pic_x_ = []
    for name in pic:
        if name[0].isnumeric() and name[1].isnumeric():
            pic_xx_.append(name)
        if name[0].isnumeric() and not name[1].isnumeric():
            pic_x_.append(name)
    if len(pic_x_) != 0:
        pic_x_.sort()
        for i in pic_x_:
            readme.write("![pic](doc/schematic_previews/" + i + ")    \n")
    if len(pic_xx_) != 0:
        pic_xx_.sort()
        for i in pic_xx_:
            readme.write("![pic](doc/schematic_previews/" + i + ")    \n")


def get_readme_name(vault):
    dir_list = os.listdir(vault)
    try:
        index = dir_list.index("Readme.md")
    except ValueError:
        index = None
    try:
        index = dir_list.index("README.md")
    except ValueError:
        index = None

    if index is None:
        return None
    else:
        return dir_list[index]


def delete_current_readme(vault):
    if get_readme_name(vault) is not None:
        os.remove(vault + "/" + get_readme_name(vault))


def gen_readme(vault):
    delete_current_readme(vault)
    cmplt_readme(vault)


def get_vault():
    arg = sys.argv[1]
    vault = (arg, arg + "/")[arg[len(arg) - 1] != "/"]
    return vault


if __name__ == '__main__':
    print("Electrical Readme generator")
    gen_readme(get_vault())
    print("Файл Readme готов")
