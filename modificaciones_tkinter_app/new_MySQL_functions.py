#New MySQL_functions
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Database connection
def get_connection():
    conn = mysql.connector.connect(
        host="localhost",  # Replace with your MySQL server host
        user="root",       # Replace with your MySQL username
        password="2003pochinoDiego",  # Replace with your MySQL password
        database="manga_store1"  # Replace with your database name
    )
    return conn

# Table column mapping
TABLE_COLUMNS = {
    "MANGA": ["Id_Manga", "Manga_name", "Author_name", "Genre", "Publish_date", "Modified_date"],
    "VOLUME": ["Id_Volume", "Volume_nro", "Release_date", "Price", "Stock", "Id_Manga", "Modified_date"],
    "SALES": ["Id_Sales", "Id_Volume", "Quantity", "Modified_date"],
    "CUSTOMER": [
        "Id_Customer", "Customer_name", "Customer_first_surname", 
        "Customer_second_surname", "NIT", "Email", 
        "Customer_birthday", "Modified_date"
    ],
    "EMPLOYEE": [
        "Id_Employee", "Employee_name", "Employee_first_surname",
        "Employee_second_surname", "Salary", "Hired_date",
        "Email", "Phone_number", "Modified_date"
    ],
    "SALES_DETAILS": [
        "Id_Sales", "Id_Customer", "Id_Employee", 
        "Sales_date", "Total_price", "Modified_date"],
}

def confirm_addition_SALES(fields, field,entries, add_window, table_name):
        conn = get_connection()
        cursor = conn.cursor()

        # Build the query dynamically
        #Joins une cada columa pero las separa por ', ' Une cada item de un tuple en una string
        columns = ", ".join(fields[:-1])
        #Crea un string de "%s" en base al numero de columnas
        placeholders = ", ".join(["%s"] * (len(fields) - 1))
        #Retrae los valores incresados previamente usando get() por cada columna
        values = [entries[field].get() for field in fields[:-1]]
        #Asegura que no se deje espacios vacios
        if not entries[field].get():
            messagebox.showinfo("ERROR", "Cannot leave empty data!")
            add_window.destroy()
            return

        try:
            #Inserta los valores de la variable values
            cursor.execute(f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})", values)
            conn.commit()
            messagebox.showinfo("Success", f"Data added to {table_name} successfully!")
        except mysql.connector.errors.IntegrityError as e:
            #Busca si hay un duplicado de llaves
            # Check for duplicate key error
            # Check for PRIMARY KEY in e 
            if "PRIMARY KEY" in str(e):
                messagebox.showerror("Error", "Duplicate ID detected! Please enter a unique ID.")
            else:
                # Handle other integrity errors
                messagebox.showerror("Error", f"An integrity error occurred: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close() 
            add_window.destroy()

def add_data_to_table_SALES(table_name, select_window):
    #Elimina la ventana en la que se muestran las tablas
    select_window.destroy()
    add_window = tk.Tk()
    add_window.title(f"Add Data to {table_name}")
    #lista de las columnas de table_name
    fields = TABLE_COLUMNS[table_name]
    #Variable que almacena las entras del usuario, para anadir posteiormente
    entries = {}
    #for loop para crear las entry para el input del usuario
    #[:-1] no toma encuenta la ultima columna(modified_date)
    for field in fields[:-1]:
        #Label es una etiqueta/texto
        label = tk.Label(add_window, text=field)
        label.pack(pady=5)
        #.Entry() es donde se inserta los datos
        entry = tk.Entry(add_window)
        entry.pack(pady=5)
        #para cada field/column, se asigna el input que ingreso previamente el usuario
        entries[field] = entry

    add_button_confirm = tk.Button(add_window, text="Confirm Addition", command=lambda t=table_name: confirm_addition_SALES(fields, field, entries, add_window, t))
    add_button_confirm.pack(pady=10)
        
def confirm_addition(fields, entries, field, add_window, table_name):
    conn = get_connection()
    cursor = conn.cursor()

    # Build the query dynamically
    columns = ", ".join(fields[1:-1])
    #-2 para omitir dos column
    placeholders = ", ".join(["%s"] * (len(fields) - 2))
    values = [entries[field].get() for field in fields[1:-1]]
        
    if not entries[field].get():
        messagebox.showinfo("ERROR", "Cannot leave empty data!")
        add_window.destroy()
        return

    try:
        cursor.execute(f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        messagebox.showinfo("Success", f"Data added to {table_name} successfully!")
    except mysql.connector.errors.IntegrityError as e:
        # Check for duplicate key error
        # Check for PRIMARY KEY in e, 
        if "PRIMARY KEY" in str(e):
            messagebox.showerror("Error", "Duplicate ID detected! Please enter a unique ID.")
        else:
            # Handle other integrity errors
            messagebox.showerror("Error", f"An integrity error occurred: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        conn.close() 
        add_window.destroy()

# Add data to the table
def add_data_to_table(table_name, del_window):
    del_window.destroy()
    add_window = tk.Tk()
    add_window.title(f"Add Data to {table_name}")
    
    fields = TABLE_COLUMNS[table_name]
    entries = {}

    # Create entry fields for each column, fields are the columns of table_name
    #[1:] is to take all except the first
    #[:-1] es para no tomar el ultimo valor
    for field in fields[1:-1]:
        label = tk.Label(add_window, text=field)
        label.pack(pady=5)
        entry = tk.Entry(add_window)
        entry.pack(pady=5)
        entries[field] = entry

    add_button = tk.Button(add_window, text="Confirm Addition", command=lambda t=table_name: confirm_addition(fields, entries, field, add_window, t))
    add_button.pack(pady=10)

#Crea las opciones de tablas en donde anadir los datos
def add_select_table():
    select_window = tk.Tk()
    select_window.title("Select Table to Add Data")
    #For loop para la creacion de un boton por tabla
    #Si la funcion a llamar en command tiene argumentos, usar lambda:
    #t=table_name asegura manejar la tabla correcta
    #table_name = Nombre de la tabla
    for table_name in TABLE_COLUMNS.keys():
        if table_name == "SALES":
            button = tk.Button(select_window, text=table_name, command=lambda t=table_name: add_data_to_table_SALES(t, select_window))
            button.pack(pady=5)
        else:
            button = tk.Button(select_window, text=table_name, command=lambda t=table_name: add_data_to_table(t, select_window))
            button.pack(pady=5)

# Visualize data from the table
def visualize_table_data(table_name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        #Seleciona todas la data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
    	#Creacion de ventana
        visualize_window = tk.Tk()
        visualize_window.title(f"Data in {table_name}")
        #Variable que almacena las columna de table_name
        columns_table_name = TABLE_COLUMNS[table_name]
        #Treeview(window, columns, show)
        #window es donde se muestra la tabla, columns es el nombre de las columnas
        #show es para mostrar las columns
        tree = ttk.Treeview(visualize_window, columns=columns_table_name, show="headings")
        #For loop para el display de la data
        for col in columns_table_name:
            #encabezado de las columns, sus nombre
            tree.heading(col, text=col)
            #el ancho de cada columna
            tree.column(col, width=100)
        #For loop para el display de las filas
        for row in rows:
            #limpia los datos antes de ser ingresados
            clean_row = tuple(map(str, row))
            #Inserta las tuplas una por una
            #tk.END indica que las tuplas deben insertarce una despues de otra
            #values es los datos a insertar
            #"" indica que no necesitamos jerarquias
            tree.insert("", tk.END, values=clean_row)
        #fill=tk.BOTH is to occupy all the available space
        #expand=True is to adjust to the size of the window
        tree.pack(fill=tk.BOTH, expand=True)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        #Cerra coneccion
        conn.close()

# Select table for visualizing data
def visualize_select_table():
    #Crear venta
    select_window = tk.Tk()
    select_window.title("Select Table to Visualize Data")
    #Crear botones para cadad tabla
    for table_name in TABLE_COLUMNS.keys():
        button = tk.Button(select_window, text=table_name, command=lambda t=table_name: visualize_table_data(t))
        button.pack(pady=5)

def confirm_deletion_SALES(id_sales_entry, id_volume_entry, table_name, delete_window):
    conn = get_connection()
    cursor = conn.cursor()
    #retraer la informacion usando get()
    id_sales_value = id_sales_entry.get()
    id_volume_value = id_volume_entry.get()

    try:
        cursor.execute(f"DELETE FROM `{table_name}` WHERE Id_Sales = %s AND Id_Volume = %s", (id_sales_value, id_volume_value))
        conn.commit()
        #Cuenta las filas afectadas, si es mayor a 0, entonces el codigo fue un exito
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"Row deleted Successfully!")
        else:
            messagebox.showerror("Error", f"No Id_Sales = {id_sales_value} or Id_Volume = {id_volume_value} found!")
    except Exception as e:
        messagebox.showerror("Error", f"An error ocurred: {e}")
    finally:
        conn.close()
        delete_window.destroy()

# Delete data from the table
def delete_data_SALES(table_name, select_window):
    select_window.destroy()
    #Crear ventana
    delete_window = tk.Tk()
    delete_window.title(f"Delete Data from {table_name}")
    
    #Label/mensage/texto
    label1 = tk.Label(delete_window, text=f"Enter Id_Sales to delete:")
    label1.pack(pady=5)
    #Entry para la entra del id_sales
    id_sales_entry = tk.Entry(delete_window)
    id_sales_entry.pack(pady=5)

    label2 = tk.Label(delete_window, text=f"Enter Id_Volume to delete:")
    label2.pack(pady=5)
    #Entrt para la entrad del id_volume
    id_volume_entry = tk.Entry(delete_window)
    id_volume_entry.pack(pady=5)
    
    delete_button = tk.Button(delete_window, text="Confirm Deletion", command=lambda t=table_name: confirm_deletion_SALES(id_sales_entry, id_volume_entry, t, delete_window))
    delete_button.pack(pady=10)

def confirm_deletion(id_entry, table_name, id_column, delete_window):
    conn = get_connection()
    cursor = conn.cursor()
    #Usamos get() para obtener el valo incresados del id por el usuario previamente
    id_value = id_entry.get()

    try:
        cursor.execute(f"DELETE FROM `{table_name}` WHERE `{id_column}` = %s", (id_value,))
        conn.commit()
        #After deleting, rowcount is the number of rows affected or deleted
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"Row with {id_column} = {id_value} deleted successfully!")
        else:
            messagebox.showinfo("Info", f"No row found with {id_column} = {id_value}.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        conn.close()
        delete_window.destroy()

# Delete data from the table
def delete_data_from_table(table_name, select_window):
    select_window.destroy()
    delete_window = tk.Tk()
    delete_window.title(f"Delete Data from {table_name}")
    #Solo obtiene la primera columna, el Id
    id_column = TABLE_COLUMNS[table_name][0]  # Assuming the first column is the ID
    label = tk.Label(delete_window, text=f"Enter {id_column} to delete:")
    label.pack(pady=5)

    id_entry = tk.Entry(delete_window)
    id_entry.pack(pady=5)

    delete_button = tk.Button(delete_window, text="Confirm Deletion", command=lambda t=table_name: confirm_deletion(id_entry, t, id_column, delete_window))
    delete_button.pack(pady=10)

# Select table for deleting data
def delete_select_table():
    select_window = tk.Tk()
    select_window.title("Select Table to Delete Data")

    for table_name in TABLE_COLUMNS.keys():
        if table_name == "SALES":
            button = tk.Button(select_window, text=table_name, command=lambda t=table_name: delete_data_SALES(t, select_window))
            button.pack(pady=5)
        else:
            button = tk.Button(select_window, text=table_name, command=lambda t=table_name: delete_data_from_table(t, select_window))
            button.pack(pady=5)

def confirm_modification(Id_entry, column_entry, new_data_entry, table_name, modify_data_window):
    #Usar get() para obtener la informacion guardada previamente
    id_value = Id_entry.get()
    column_value = column_entry.get()
    new_data_value = new_data_entry.get()
    #No dejar espacio vacio
    if not id_value or not column_value or not new_data_value:
        messagebox.showerror("Error", "Must fill in all values!")
        return
        
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"UPDATE {table_name} SET {column_value} = %s WHERE Id_{table_name} = %s", (new_data_value, id_value))
        conn.commit()
        #Verificar que el .execute() fue un exito
        if cursor.rowcount == 0:
            messagebox.showerror("Error", f"No rows found with Id_{table_name} = {id_value}")
        else:
            messagebox.showinfo("Success", f"Successfully updated: {new_data_value}")
            
    except Exception as e:
        messagebox.showerror("Error", f"An error ocurred: {e}")

    finally:
        conn.close()
        modify_data_window.destroy()

#MODIFY FUNCTS
def modify_data(table_name, select_window):
    select_window.destroy()
    #Creacion de ventana donde trabajar
    modify_data_window = tk.Tk()
    modify_data_window.title(f"Modify Data from {table_name}")

    label_Id = tk.Label(modify_data_window, text="ID")
    label_Id.pack(pady=5)
    #Entry para el id/fila
    Id_entry = tk.Entry(modify_data_window)
    Id_entry.pack(pady=5)

    label_column = tk.Label(modify_data_window, text="Column")
    label_column.pack(pady=5)
    #Entry para la column
    column_entry = tk.Entry(modify_data_window)
    column_entry.pack(pady=5)

    label_new_data = tk.Label(modify_data_window, text="New Data")
    label_new_data.pack(pady=5)
    #Entry para la nueva data
    new_data_entry = tk.Entry(modify_data_window)
    new_data_entry.pack(pady=5)

    confirm_button = tk.Button(modify_data_window, text="Confirm Modification", command=lambda t=table_name: confirm_modification(Id_entry, column_entry, new_data_entry, t, modify_data_window))
    confirm_button.pack(pady=5)

def confirm_modification_SALES(Id_Sales, Id_Volume, new_data_entry, table_name, modify_data_window):
    #Usar get() para obtener la informacion guardada previamente
    id_sales_value = Id_Sales.get()
    id_volume_value = Id_Volume.get()
    new_data_value = new_data_entry.get()
    #No dejar espacio vacio
    if not id_sales_value or not id_volume_value or not new_data_value:
        messagebox.showerror("Error", "Must fill in all values!")
        return
        
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"UPDATE `{table_name}` SET Quantity = %s WHERE Id_Sales = %s AND Id_Volume = %s", (new_data_value, id_sales_value, id_volume_value))
        conn.commit()
        #Verificar que el .execute() fue un exito
        if cursor.rowcount == 0:
            messagebox.showerror("Error", f"No rows found with Id_Sales = {id_sales_value} OR Id_Volume = {id_volume_value}")
        else:
            messagebox.showinfo("Success", f"Successfully updated: {new_data_value}")
            
    except Exception as e:
        messagebox.showerror("Error", f"An error ocurred: {e}")

    finally:
        conn.close()
        modify_data_window.destroy()

def modify_data_SALES(table_name, select_window):
    select_window.destroy()
    #Creacion de ventana donde trabajar
    modify_data_window = tk.Tk()
    modify_data_window.title(f"Modify Data from {table_name}")

    label_Id_Sales = tk.Label(modify_data_window, text="Id_Sales")
    label_Id_Sales.pack(pady=5)
    #Entry para el id/fila
    Id_Sales_entry = tk.Entry(modify_data_window)
    Id_Sales_entry.pack(pady=5)

    label_Id_Volume = tk.Label(modify_data_window, text="Id_Volume")
    label_Id_Volume.pack(pady=5)
    #Entry para el id/fila
    Id_Volume_entry = tk.Entry(modify_data_window)
    Id_Volume_entry.pack(pady=5)

    label_new_data = tk.Label(modify_data_window, text="New Data")
    label_new_data.pack(pady=5)
    #Entry para la nueva data
    new_data_entry = tk.Entry(modify_data_window)
    new_data_entry.pack(pady=5)

    confirm_button = tk.Button(modify_data_window, text="Confirm Modification", command=lambda t=table_name: confirm_modification_SALES(Id_Sales_entry, Id_Volume_entry, new_data_entry, t, modify_data_window))
    confirm_button.pack(pady=5)


#Creacion de botones para que el usuario escoja la tabla
def modify_select_table():
    select_window = tk.Tk()
    select_window.title("Select Table to Modify Data")
    #check if t=table_name is necessary
    for table_name in TABLE_COLUMNS.keys():
        if table_name == "SALES":
            button = tk.Button(select_window, text=table_name, command=lambda t=table_name: modify_data_SALES(t, select_window))
            button.pack(pady=5)
        else:
            button = tk.Button(select_window, text=table_name, command=lambda t=table_name: modify_data(t, select_window))
            button.pack(pady=5)

def reverse_str(str_list, i):
    if(i < len(str_list) / 2):
        aux = str_list[i]
        str_list[i] = str_list[len(str_list) - i - 1]
        str_list[len(str_list) - i -1] = aux
        return reverse_str(str_list, i + 1)
    else:
        new_str = "".join(str_list)
        return new_str

def invert_data(table_name, window):
    window.destroy()
    invert_window = tk.Tk()
    invert_window.title("Enter data to invert")
    
    id_label = tk.Label(invert_window, text="Enter Id:")
    id_label.pack(pady=5)
    id_entry = tk.Entry(invert_window)
    id_entry.pack(pady=5)

    column_name_label = tk.Label(invert_window, text="Enter column name:")
    column_name_label.pack(pady=5)
    column_name_entry = tk.Entry(invert_window)
    column_name_entry.pack(pady=5)

    def confirm_invertion():
        id_value = id_entry.get()
        column_name_value = column_name_entry.get()

        if not id_value or not column_name_value:
            messagebox.showerror("ERROR", "Must fill in all fields!")

        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT {table_name}.{column_name_value} FROM `{table_name}` WHERE Id_{table_name} = %s", (id_value,))
        data = cursor.fetchone()
        aux = data[0]
        aux = list(aux)
        inverted_data = reverse_str(aux, 0)
        
        try:
            cursor.execute(f"UPDATE `{table_name}` SET {column_name_value}  = %s WHERE Id_{table_name} = %s", (inverted_data, id_value))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Data inverted Successfully!")
            else:
                messagebox.showerror("Error", "No Data inverted!")
        except Exception as e:
            messagebox.showerror("Error", f"Error ocurred: {e}")
        finally:
            conn.close()
            invert_window.destroy()

    confirm_button = tk.Button(invert_window, text="Confirm Invertion", command=confirm_invertion)
    confirm_button.pack(pady=5)

def invert_select():
    select_window = tk.Tk()
    select_window.title("Select Tablee:")
    
    for table_name in TABLE_COLUMNS.keys():
        button = tk.Button(select_window, text=table_name, command=lambda t=table_name: invert_data(t, select_window))
        button.pack(pady=5)