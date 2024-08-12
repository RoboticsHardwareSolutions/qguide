import os
import sys
import shutil
from docx import Document
from docxtpl import DocxTemplate
from sch_preview import find_previews
from sch_preview import cut_preview
from sch_preview import get_cut
from sch_preview import delete_cut
from bom_parser import get_bom_quantity
from bom_parser import get_bom_content_like_context
from table import *
from sch_creator import create_sch


def create_spec(vault, name):
    tables = get_bom_quantity(vault) // 25
    if get_bom_quantity(vault) % 25 != 0:
        tables += 1
    create_lists_with_tables("/template/spec_table.docx", tables, name)
    fill_tables_in_template(name)
    doc = DocxTemplate(name)
    doc.render(get_bom_content_like_context(vault))
    doc.save(name)


def create_schematics(vault, save_as):
    previews = find_previews(vault)
    cut_preview(vault, previews)
    cuts = get_cut()
    print(cuts)
    create_sch("/template/after_titul.docx", "/template/after_titul.docx", cuts, save_as)


# os.remove(os.getcwd() + "/template.docx")
# os.remove(os.getcwd() + "/template1.docx")
# try:
#     os.remove(save_to + "СПЕЦИФИКАЦИЯ.docx")
# except:
#     print("")
# doc.save("СПЕЦИФИКАЦИЯ.docx")
# shutil.move(os.getcwd() + "/СПЕЦИФИКАЦИЯ.docx", save_to)

def merge_schematics_and_spec(vault, spec, schematics, save_as):
    template = Document(schematics)
    composer = Composer(template)
    doc_temp = Document(spec)
    composer.append(doc_temp)
    composer.save(save_as)


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

    create_spec(get_vault(), "spec.docx")
    create_schematics(get_vault(), "schematics.docx")
    merge_schematics_and_spec(get_vault(), "spec.docx", "schematics.docx", "output.docx")
    print("Бесполезные файлы готовы")
