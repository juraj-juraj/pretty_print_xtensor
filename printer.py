class pretyXtensor:
    """Xtensor pretty printer
       prikazy:
         arr = gdb.lookup_symbol("meno") # vrati tuple, (gdb.symbol, bool)
         arr = arr[0]
         print(arr.type)
         arr_value = arr.value(gdb.selected_frame())
         print(arr_value['m_shape']['m_data']) -> gdb.Value
         print((arr_value['m_storage']['p_begin'] + 0x2).dereference())   

    """