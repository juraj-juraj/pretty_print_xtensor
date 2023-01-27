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
    if(c_name in ['float', 'double', 'long double']):
        return float
    elif(c_name.startswith('std::complex')):
        return complex
    else:
        return int
    
def fetch_array(begin_it: gdb.Value, end_it:gdb.Value) -> np.array:
    n_size = end_it - begin_it
    d_type = c_to_py_type(str(begin_it.dereference().type)) #get datatype of one value as is in C++
    
    return np.fromiter(map(lambda index: int((begin_it+index).dereference()), range(n_size)), dtype=d_type)

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

    def children(self):
        shape = fetch_array(self.m_value['m_shape']['m_begin'], self.m_value['m_shape']['m_end'])
        data = fetch_array(self.m_value['m_storage']['p_begin'], self.m_value['m_storage']['p_end'])
        data = data.reshape(shape)
        yield('shape', str(shape))
        yield('data', str(data))

    # def to_string(self):
    #     shape = fetch_array(self.m_value['m_shape']['m_begin'], self.m_value['m_shape']['m_end'])
    #     data = fetch_array(self.m_value['m_storage']['p_begin'], self.m_value['m_storage']['p_end'])
    #     data = data.reshape(shape)
    #     return f"shape is {shape}, data: {data}"    

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
