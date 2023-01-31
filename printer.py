import gdb
import numpy as np

class printerInterface:
    """Interface for pretty printer implementation
    
    Defines prototype for children and to_string methods.
    """
    def __init__(self, value:gdb.Value):
        """Saving value to member called mValue"""
        self.m_value = value
     
    def children(self) -> tuple:
        """Implement iterator hich gives out data."""
        pass
    
    def to_string(self) -> str:
        """Implement method to cast whole object to string, printable to the output.
        This method is sort of complementary to children method"""
        pass
    
def c_to_py_type(c_name: str):
    if(c_name in [gdb.TYPE_CODE_FLT, gdb.TYPE_CODE_FLT]):
        return float
    elif(c_name in [gdb.TYPE_CODE_COMPLEX]):
        return complex
    elif(c_name in [gdb.TYPE_CODE_INT]):
        return int
    
def fetch_array(begin_it: gdb.Value, end_it:gdb.Value) -> np.array:
    n_size = end_it - begin_it
    d_type = c_to_py_type(begin_it.dereference().type.code) #get datatype of one value as is in C++
    
    return np.fromiter(map(lambda index: d_type((begin_it+index).dereference()), range(n_size)), dtype=d_type)

def shape_from_object(in_val : gdb.Value) -> np.array:
    in_val = str(in_val).strip('{}').replace(' ', '').split(',')
    return np.array([int(i) for i in in_val]) 

class prettyXarray (printerInterface):
    """Xtensor pretty printer.

       prikazy:
         arr = gdb.lookup_symbol("meno") # vrati tuple, (gdb.symbol, bool)
         arr = arr[0]
         print(arr.type)
         arr_value = arr.value(gdb.selected_frame())
         print(arr_value['m_shape']['m_data']) -> gdb.Value
         print((arr_value['m_storage']['p_begin'] + 0x2).dereference())
         gdb.Value(...).cast(gdb.lookup_type("char").pointer())
    """

    def __init__(self, value: gdb.Value):
        super().__init__(value)
        self.shape = fetch_array(self.m_value['m_shape']['m_begin'], self.m_value['m_shape']['m_end'])

    def children(self):
        if(self.shape.size == 0):
            return
        order = "F" if str(self.m_value['m_layout']) == "xt::layout_type::column_major" else "C" # F like fortran style, for collumn major
        indices = np.nditer(np.zeros(tuple(self.shape)), flags=['multi_index'], order=order)
        it = self.m_value['m_storage']['p_begin']
        while(it != self.m_value['m_storage']['p_end']):
            yield(f"{indices.multi_index}", it.dereference())
            it += 1
            indices.iternext()

    def to_string(self):
        return f"xarray with shape {self.shape}"   

    def display_hint(self):
        return 'string'

class prettyXtensor (printerInterface):
    """Xtensor pretty
        Prints data, if available, and shape.     
    """
    def __init__(self, value):
        super().__init__(value)    
    
    def children(self):
        shape = shape_from_object(self.m_value['m_shape']['_M_elems'])
        data = fetch_array(self.m_value['m_storage']['p_begin'], self.m_value['m_storage']['p_end'])
        data = data.reshape(shape)
        yield('shape', str(shape))
        yield('data', str(data))


def xtensor_resolve(val):
    match str(val.type):
        case 'xt::xarray':
            return prettyXarray(val)
        case 'xt::xtensor':
            return prettyXtensor(val)
        case _:
            return
        
gdb.pretty_printers.append(xtensor_resolve)
