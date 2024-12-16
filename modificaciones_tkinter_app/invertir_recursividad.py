def inv_rec(str_list, i):
    if(i < len(str_list) / 2):
        aux = str_list[i]
        str_list[i] = str_list[len(str_list) - i - 1]
        str_list[len(str_list) - i -1] = aux
        inv_rec(str_list, i + 1)
    else:
        new_str = "".join(str_list)
        return new_str

str1 = "comida"
str_list = list(str1)
new_str = " "
#print(try_str)  
#print(invert(str_list, 1, new_str))
print(inv_rec(str_list, 0))
#inv_rec(new_str, 0)
#inv_rec(new_str, 0)
#print("comida")
#print(inv_rec(new_str, 0))