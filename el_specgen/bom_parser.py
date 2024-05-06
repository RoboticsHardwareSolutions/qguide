import os
import csv


def make_rows(reader):
    rows = []
    for row in reader:
        rows.append(row)
    return rows


def find_bom(bom_vault):
    bom_list = os.listdir(bom_vault + "doc/")
    for i in bom_list:
        if i.find("parts list") == 0 and i.find(".csv") != -1:
            return i
    return None


def get_bom_quantity(bom_vault):
    bom = bom_vault + "doc/" + find_bom(bom_vault)
    with open(bom, newline='', encoding='UTF-8', ) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        rows = make_rows(reader)
    csvfile.close()
    return len(rows) - 1


def get_bom_content_like_context(bom_vault):
    bom = bom_vault + "doc/" + find_bom(bom_vault)
    with open(bom, newline='', encoding='UTF-8', ) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        rows = make_rows(reader)
    context = {}
    for i in range(1, get_bom_quantity(bom_vault) + 1):
        context["n" + str(i)] = i
        context["descriptions" + str(i)] = rows[i][0]
        context["manuf" + str(i)] = rows[i][2]
        context["part" + str(i)] = rows[i][1]
        context["quan" + str(i)] = str(int((1, rows[i][3])[rows[i][3].isdigit()]) * int(rows[i][5]))
        context["unity" + str(i)] = rows[i][4]
        csvfile.close()
    return context


def get_bom_vault():
    return "/Users/doc/projects/dm/server-cabinet/"


if __name__ == '__main__':
    print(get_bom_quantity(get_bom_vault()))
    print(get_bom_content_like_context(get_bom_vault()))
