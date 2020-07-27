import menu
import console_IO_helper as cio
import file_IO_helper as fio

def main():
    file_name = input("If you want to read a different file, enter it here: ")
    file_name = "graphs" if file_name == "" else file_name
    graphs = fio.read_file(file_name)
    loop = True

    while loop:
        first_choice = menu.do_menu("What would you like to do?",
                                ["View graphs","Edit a graph","Add a graph",
                                 "Fold to get graphs"])

        if first_choice == 1:
            cio.print_graphs(graphs)
        elif first_choice == 2:
            print("Sorry, we don't have that functionality right now.")
        elif first_choice == 3:
            graph = cio.enter_graph()
            cont = input_checker("Would you like to add this graph to the list?",
                                 ["yes","y","no","n"])[0]
            if cont == y:
                graphs.append(graph)
        elif first_choice == 4:
            i = 0
            while i < len(graphs):
                graphs[i].perform_legal_folds(graphs)
                print(i)
                i += 1
            print(graphs)
        loop = True if cio.input_checker("Would you like to exit?")[0]=="n" else False
    graphs[0].update_matrix()
    file_name = input("If you want to write to a different file, enter it here: ")
    file_name = "graphs" if file_name == "" else file_name
    print("Saving...")
    fio.write_file(graphs, file_name)
    print("Saved.")

if __name__ == "__main__":
    main()
