import menu
import console_IO_helper as cio
import fio_IO_helper as fio

def main():
    loop = True
    while loop:
        first_choice = menu.do_menu("What would you like to do?",
                                    ["Do all of the folds."])
        if first_choice == 1:
