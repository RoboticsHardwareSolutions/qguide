import os
import sys
import shutil
from docx import Document
from docxtpl import DocxTemplate
import tomli
from bom_parser import get_bom_quantity
from bom_parser import get_bom_content_like_context
from template import template_merger
from template import template_filler


def get_config():
    with open('config.toml', mode="rb") as f:
        return tomli.load(f)


def gen_spec(vault, save_to):
    tables = get_bom_quantity(vault) // 25
    if get_bom_quantity(vault) % 25 != 0:
        tables += 1
    config = get_config()
    template_merger(config.get("templates"), tables)
    temp_doc = Document('template.docx')
    template_filler(temp_doc)
    doc = DocxTemplate('template1.docx')
    doc.render(get_bom_content_like_context(vault))
    os.remove(os.getcwd() + "/template.docx")
    os.remove(os.getcwd() + "/template1.docx")
    try:
        os.remove(save_to + "СПЕЦИФИКАЦИЯ.docx")
    except:
        print("")
    doc.save("СПЕЦИФИКАЦИЯ.docx")
    shutil.move(os.getcwd() + "/СПЕЦИФИКАЦИЯ.docx", save_to)


def get_vault():
    arg = sys.argv[1]
    vault = (arg, arg + "/")[arg[len(arg) - 1] != "/"]
    return vault


def get_save_to():
    arg = sys.argv[2]
    save_to = (arg, arg + "/")[arg[len(arg) - 1] != "/"]
    return save_to


if __name__ == '__main__':
    print("Electrical specgen запущен")
    print("PS Всем кто любит ЕСКД там где он не нужен, посвящается")
    gen_spec(get_vault(), get_save_to())
    print("Бесполезные файлы готовы")
