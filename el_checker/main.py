import sys, os
from check_list import check_list
from bom import bom_check


def get_vault():
    arg = sys.argv[1]
    return arg if arg.endswith("/") else arg + "/"

if __name__ == '__main__':
    print("Electrical checker запущен")
    print("Описание требований тут :")
    print("https://roboticshardwaresolutions.github.io/qguide/")

    vault = get_vault()
    check_list(vault)
    bom_check(vault + "doc" + os.sep)

    print("Cодержимое репозитория соответствует стандартам")
