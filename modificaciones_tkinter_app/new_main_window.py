#new main_window
from new_SQLServer_functions import * 

# Main window
def start_window():
    #Tk() crea la ventana
    main_window = tk.Tk()
    #geomtry() is el tamano de la venta
    main_window.geometry("400x300")
    #.title() is el titulo de la venta
    main_window.title("Database Management")
    #.Button(window, text, command)
    #window is la venta en donde se cread el Button
    #text is el texto del button
    #command is la funcion que se llama al clickar el button
    add_button = tk.Button(main_window, text="Add Data", command=add_select_table)
    #.pack() se usa siempre que se anade algo a una venta
    #pad y/x is la distancia entre los objetos
    add_button.pack(pady=10)

    visualize_button = tk.Button(main_window, text="Visualize Data", command=visualize_select_table)
    visualize_button.pack(pady=10)

    delete_button = tk.Button(main_window, text="Delete Data", command=delete_select_table)
    delete_button.pack(pady=10)

    modify_button = tk.Button(main_window, text="Modify Data", command=modify_select_table)
    modify_button.pack(pady=10)

    invert_button = tk.Button(main_window, text="Invert data", command=invert_select)
    invert_button.pack(pady=10)
    #mainloop() is lo que mantiene 'alerta' a las acciones del usuario
    main_window.mainloop()

start_window()



    

