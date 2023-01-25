import gdb
import numpy as np


class prettyXarray:
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
        self.value = value

    def children(self):
        shape = prettyXarray.fetch_array(self.value['m_shape']['m_begin'], self.value['m_shape']['m_end'])
        data = prettyXarray.fetch_array(self.value['m_storage']['p_begin'], self.value['m_storage']['p_end'])
        data = data.reshape(shape)
        yield('shape', str(shape))
        yield('data', str(data))

    # def to_string(self):
    #     shape = prettyXtensor.fetch_array(self.value['m_shape']['m_begin'], self.value['m_shape']['m_end'])
    #     data = prettyXtensor.fetch_array(self.value['m_storage']['p_begin'], self.value['m_storage']['p_end'])
    #     data = data.reshape(shape)
    #     return f"shape is {shape}, data: {data}"

    @staticmethod
    def fetch_array(begin_it: gdb.Value, end_it:gdb.Value, mDtype=int) -> np.array:
        n_size = end_it - begin_it
        return np.fromiter(map(lambda index: int((begin_it+index).dereference()), range(n_size)), dtype=mDtype)        


def xtensor_resolve(val):
    if(str(val.type) == 'xt::xarray'):
        return prettyXarray(val)


gdb.pretty_printers.append(xtensor_resolve)
