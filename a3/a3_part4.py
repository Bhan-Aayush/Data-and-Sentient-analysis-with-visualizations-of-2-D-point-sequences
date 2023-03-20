import csv  
import plotly.graph_objects as go  
  
from a3_ffwi_system import WeatherMetrics, FfwiOutput  
import a3_ffwi_system as ffwi  
  
  
def load_data(filename: str) -> tuple[list[WeatherMetrics], list[FfwiOutput]]:  
    """Return a tuple of two parallel lists based on the data in filename. The first list contains 
    WeatherMetrics. The second list contains the corresponding FfwiOutput. 
 
    The data in filename is in a csv format with 12 columns. The first six columns correspond to 
    the month, day, temperature, relative humidity, wind speed, and precipitation, in that order. 
    The last six columns correspond to the FFMC, DMC, DC, ISI, BUI, and FWI values that would be 
    calculated based on the first six columns and the previous day's values. 
    """  
    # ACCUMULATOR inputs_so_far: The WeatherMetrics parsed from filename so far  
    inputs_so_far = []  
    # ACCUMULATOR outputs_so_far: The FfwiOutputs parsed from filename so far  
    outputs_so_far = []  
  
    with open(filename) as f:  
        reader = csv.reader(f, delimiter=',')  
        next(reader)  # skip the header  
  
        for row in reader:  
            assert len(row) == 12, 'Expected every row to contain 12 elements.'  
            # row is a list of strings  
            # Your task is to extract the relevant data from row and add it  
            # to the accumulator.  
            wm = WeatherMetrics(int(row[0]), int(row[1]), float(row[2]), float(row[3]),  
                                float(row[4]), float(row[5]))  
            fo = FfwiOutput(float(row[6]), float(row[7]), float(row[8]), float(row[9]),  
                            float(row[10]), float(row[11]))  
            list.append(inputs_so_far, wm)  
            list.append(outputs_so_far, fo)  
  
    return inputs_so_far, outputs_so_far  
  
  
def calculate_ffwi_outputs(readings: list[WeatherMetrics]) -> dict[tuple[int, int], FfwiOutput]:  
    """Return a dictionary mapping (month, day) tuples to their corresponding FfwiOutput based on 
    the daily weather measurements found in readings. 
 
    Use the functions in a3_ffwi_system for initial FFMC, DMC, and DC values and to calculate each 
    attribute needed for FfwiOutput. 
 
    Preconditions: 
        - Every reading in readings has a unique (month, day) pair 
    """  
    date_tuple_list = [(x.month, x.day) for x in readings]  
  
    ffmc_list = [ffwi.calculate_ffmc(x, ffwi.INITIAL_FFMC) for x in readings]  
    dmc_list = [ffwi.calculate_dmc(x, ffwi.INITIAL_DMC) for x in readings]  
    dc_list = [ffwi.calculate_dc(x, ffwi.INITIAL_DC) for x in readings]  
    isi_list = [ffwi.calculate_isi(x, y) for x in readings for y in ffmc_list]  
    bui_list = [ffwi.calculate_bui(x, y) for x in dmc_list for y in dc_list]  
    fwi_list = [ffwi.calculate_fwi(x, y) for x in isi_list for y in bui_list]  
  
    ffwioutput_list = []  
    for i in range(0, len(ffmc_list)):  
        list.append(ffwioutput_list, FfwiOutput(ffmc_list[i], dmc_list[i], dc_list[i], isi_list[i],  
                                                bui_list[i], fwi_list[i]))  
  
    return dict(zip(date_tuple_list, ffwioutput_list))  
  
  
def get_xy_data(outputs: dict[tuple[int, int], FfwiOutput], attribute: str) -> \  
        tuple[list[str], list[float]]:  
    """Return a tuple of two parallel lists. The first list contains the keys of outputs as 
    strings in the format 'month, day'. The second list contains the corresponding value of 
    the attribute of FfwiOutput. 
 
    You can access an attribute from a data class using the getattr built-in function. For example, 
        >>> output = FfwiOutput(2.0, 3.0, 4.0, 5.0, 6.0, 7.0) 
        >>> getattr(output, 'ffmc') 
        2.0 
    """  
    output_key_list = [str(x[0]) + ", " + str(x[1]) for x in outputs]  
    attr_list = [getattr(outputs[x], attribute) for x in outputs]  
    return (output_key_list, attr_list)  
  
  
def plot_ffwi_attribute(outputs: dict[tuple[int, int], FfwiOutput], attribute: str) -> None:  
    """Plot an attribute from FfwiOutput as a time series. 
 
    Preconditions: 
        - attribute in {'ffmc', 'dmc', 'dc', 'isi', 'bui', 'fwi'} 
        - outputs != {} 
    """  
    # Convert the outputs into parallel x and y lists  
    x_data, y_data = get_xy_data(outputs, attribute)  
  
    # Create the figure  
    fig = go.Figure()  
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name=attribute))  
  
    # Configure the figure  
    fig.update_layout(title=f'Time Series of {attribute}',  
                      xaxis_title='(Month, Day)',  
                      yaxis_title=f'Calculated {attribute}')  
  
    # Show the figure in the browser  
    fig.show()  
    # Is the above not working for you? Comment it out, and uncomment the following:  
    # fig.write_html('my_figure.html')  
    # You will need to manually open the my_figure.html file created above.  
  
  
if __name__ == '__main__':  
    import python_ta  
    import python_ta.contracts  
    python_ta.contracts.DEBUG_CONTRACTS = False  
    python_ta.contracts.check_all_contracts()  
