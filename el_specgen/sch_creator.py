import os
import sys
import shutil
from docx import Document
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docxtpl import InlineImage
from docx.shared import Mm
from PIL import Image


def create_sch(first_page, subsequent_pages, imgs, save_as):
    page = os.getcwd() + first_page
    context = {}
    first = DocxTemplate(page)
    context["image"] = InlineImage(first, imgs[0])
    first.render(context)
    first.save(save_as)

    subpage = os.getcwd() + subsequent_pages
    for i in range(1, len(imgs)):
        subsequent = DocxTemplate(subpage)
        context["image"] = InlineImage(subsequent, imgs[i])
        subsequent.render(context)
        subsequent.save("subsequent.docx")
        template = Document(save_as)
        composer = Composer(template)
        doc_temp = Document("subsequent.docx")
        composer.append(doc_temp)
        composer.save(save_as)


if __name__ == '__main__':
    create_sch("/template/spec_titul.docx",
               "/template/after_titul.docx",
               "resized2_connectors_list.png",
               "sch.docx")
