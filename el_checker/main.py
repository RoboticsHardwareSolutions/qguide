import sys, os
from check_list import check_list
from bom import bom_check



def get_vault():
    arg = sys.argv[1]
    vault = (arg, arg + "/")[arg[len(arg) - 1] != "/"]
    return vault


if __name__ == '__main__':
    print("Electrical checker запущен")
    print("Описание требований тут :")
    print("https://roboticshardwaresolutions.github.io/qguide/")
    check_list(get_vault())
    bom_check(get_vault() + "doc/")
    print("Cодержимое репозитория соответствует стандартам")
