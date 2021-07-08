from importing_modules import *

def compile_task():
    errors_file = open('errors_cpp.txt', 'a', encoding='windows-1251')
    warnings_file = open('warnings_cpp.txt', 'a', encoding='windows-1251')
    infos_file = open('infos_cpp.txt', 'a', encoding='windows-1251')
    lines_found_file = open('lines_found.txt', 'a', encoding='windows-1251')

    errors_list = errors_file.readlines()
    warnings_list = warnings_file.readlines()
    infos_list = infos_file.readlines()
    lines_found_dict = {elem.split()[0]: elem.split()[2] for elem in lines_found_file}

    for index in range(len(errors_list)):
        try:
            error_id = lines_found_dict[errors_list[index].split()[0]]
        except KeyError:
            error_id = "Не найдена"


if __name__ == '__main__':
    compile_task()