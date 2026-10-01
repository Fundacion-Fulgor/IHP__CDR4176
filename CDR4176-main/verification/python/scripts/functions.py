import matplotlib.pyplot as plt
import numpy as np

def readRaw(rawfile: str, variables: list[str]) -> dict[str,list[float]]:
    """
    readRaw()
    =======
    Lee un archivo raw y devuelve las variables indicadas en un
    diccionario. Las llaves son el nombre de las variables en
    la simulacion, y los valores son listas que contienen el resultado
    de simulacion de su respectiva variable.

    @author: pdominguez. Contactense ante cualquier duda.

    Parameters
    ----------

    rawfile: str
             Archivo donde se almacenan las salidas de simulacion de ngspice. 
             El archivo debe estar configurado en filetype = ascii.
                    
    variables: list[str]
               Lista que contiene las llaves del diccionario de salida.
               Las llaves deben ser iguales a los nombres de las senales en la salida ascii.

    Returns
    -------

    dict[str,list[float]]
            Diccionario donde las llaves son strings iguales al nombre de la senal en simulacion, 
            y el valor es la lista de floats que contiene los valores simulados respectivos a esa 
            variable

    Examples of use
    ---------------

    Se supone que el archivo out_simul.raw es una salida de simulacion de ngspice configurada en 
    filetype = ascii, y tiene las siguientes senales con sus respectivos valores:
    
    >>> Variables:
	>>> 0	time	time
	>>> 1	v(vout)	voltage
	>>> 2	v(vout8i)	voltage
	>>> 3	v(vini)	voltage
    >>> Values:
    >>>  0 	0.000000000000000e+00
    >>> 	1.472053331554910e-08
    >>> 	1.472053337682925e-08
    >>> 	0.000000000000000e+00

    >>>  1	1.000000000000000e-13
    >>> 	1.493710519767057e-08
    >>> 	1.493710531305648e-08
    >>> 	4.800000000000000e-03

    >>>  2	2.000000000000000e-13
    >>> 	1.533147593858479e-08
    >>> 	1.533147614939112e-08
    >>> 	9.600000000000001e-03

    ...y demas puntos

    Se podria hacer:

    >>> variables = ['time','v(vout)','v(vout8i)','v(vini)']   
    >>> resultados = readRaw('out_simul.raw',variables)

    y luego:

    >>> time = resultados['time']
    >>> vout = resultados['v(vout)']

    y siguiendo con las otras senales.
    """
    out_dict = {}
    aux_dict = {}
    head = None

    with open(rawfile, 'r') as f:
        for line in f:
            linea = line.strip()
            #Flag para identificar la cabecera con las variables
            if(linea == 'Variables:'):
                head = True
            elif(linea == 'Values:'):
                head = False
            
            #Procesamiento de la cabecera y los datos
            if(head == True and linea != 'Variables:'):
                lin_split = linea.split()
                if lin_split[1] in variables:
                    aux_dict[int(lin_split[0])] = lin_split[1]
                    out_dict[lin_split[1]] = []

            elif(head == False and linea != 'Values:'):
                if(len(linea.split()) > 1):  #Nuevo instante de simulacion
                    offset = 0
                if offset in aux_dict:
                    if (offset != 0):
                        label = aux_dict[offset]
                        out_dict[label].append(float(linea))
                    else:
                        label = aux_dict[offset]
                        out_dict[label].append(float(linea.split()[1]))
                offset = offset + 1
    
    return out_dict



def meas_period(sig_out: list[float],
                sig_time: list[float],
                threshold: float
                ) -> list[float]:
    
    """
    meas_period()
    ============
    Funcion para medir el periodo de una señal (presumiblemente cuadrada) de clock.

    @author: pdominguez - Contactense sin problemas en caso de tener dudas. La funcion esta 
    implementada con algunas cantidades "hardcodeadas". Son libres de copiar esta funcion en
    su codigo y modificar estas cantidades para ajustarlas a su simulacion.

    Parameters
    ---------

    sig_out: list[float]
               senal de salida de simulacion.

    sig_time: list[float]
                senal de tiempo de simulacion.
    """

    meas_period = []
    pos_pw = []
    neg_pw = []
    first_posedge = 0
    time_meas = []
    data_ring = {}

    pos_level = False
    posedge1 = None
    negedge1 = None
    for i in range(len(sig_time)):
        if(sig_out[i] >= threshold and not pos_level):
            # Captura el flanco
            posedge2 = sig_time[i]
            time_meas.append(sig_time[i])
            if (posedge1 is None):
                first_posedge = posedge2
            else: 
                meas_period.append(posedge2 - posedge1)
                neg_pw.append(posedge2 - negedge1)
            pos_level = True
            posedge1 = posedge2
        
        if(sig_out[i] <= threshold and pos_level):
            # Identifica el flanco negativo
            pos_level = False
            negedge1 = sig_time[i]
            pos_pw.append(negedge1 - posedge1)

    data_ring["first_posedge"] = first_posedge
    data_ring["meas_period"] = meas_period
    data_ring["pos_pw"] = pos_pw
    data_ring["neg_pw"] = neg_pw
    data_ring["time_meas"] = time_meas
    
    return data_ring



def graph_QUADRv3(quadr_out: list[float],
                  quadr_time: list[float],
                  quadr: int,
                  stable_period: float,
                  quadr_label: list[str],
                  subplot: plt.Axes) -> None:
    """
    graph_QUADRv3()
    ==============
    Function for plotting all phases of a single quadrant overlaid, in the
    context of a 4-quadrant PI.

    This second version of the function iterates through all quadrants in the
    counterclockwise direction because the phase sweep has already been modified
    to be linear with increasing control.

    @author: pdominguez - Feel free to contact me if you have any questions.
    The function is implemented with some "hardcoded" values. You are free to
    copy this function into your code and modify these values to suit your simulation.

    Parameters
    ---------
    
    quadr_out: list[float]
               simulation output signal.

    quadr_time: list[float]
                simulation time signal,

    quadr: integer
           quadrant number to which the signal belongs,

    quadr_label: list[str]
                 phase limits that define the quadrant.

    subplot: plt.Axes
             subplot (matplotlib Axes object) where the signal is plotted.
    """
    for i in np.arange(0,8):
        len_time_seg1 = np.abs(quadr_time - (i+1)*stable_period*4 - (quadr)*stable_period*32).argmin()
        len_time_seg0 = np.abs(quadr_time - (i)*stable_period*4 - (quadr)*stable_period*32).argmin()
        subplot.plot(quadr_time[len_time_seg0:len_time_seg1]-i*stable_period*4 - (quadr-1)*stable_period*32,
                 quadr_out[len_time_seg0:len_time_seg1],
                 label = f'{i}{quadr_label[0]}+{8-i}{quadr_label[1]}')
        
        subplot.grid(True)
        subplot.legend()



def phase_measv2(quadr_out: list[float],
                     quadr_8i: list[float],
                     quadr_time: list[float],
                     stable_period: float,
                     threshold: float,
                     offset: float,
                     quadr: int
                     ) -> list[float]:

    ph_out = []


    for i in np.arange(0,8):
        start_samp = np.abs(quadr_time - (i)*stable_period*4 - (quadr)*stable_period*32 - stable_period*1).argmin()
        time8I_samp = start_samp
        if (quadr_8i[time8I_samp] >= threshold):
            while (quadr_8i[time8I_samp] >= threshold):
                time8I_samp = time8I_samp+1
    
        while(quadr_8i[time8I_samp] < threshold):
            time8I_samp = time8I_samp+1
        time8I = quadr_time[time8I_samp]

        time_ph_samp = time8I_samp
        if (quadr_out[time_ph_samp] >= threshold):
            while (quadr_out[time_ph_samp] >= threshold):
                time_ph_samp = time_ph_samp+1
        
        while (quadr_out[time_ph_samp] < threshold):
            time_ph_samp = time_ph_samp+1
            
        time_ph = quadr_time[time_ph_samp]
        diff_ph = (time_ph - time8I)*360/stable_period - offset
        if diff_ph >= 360: 
            diff_ph -= 360
        elif diff_ph < -0.03:
            diff_ph += 360
            
        if offset == 0:
            ph_out.append(diff_ph)
        else:
            ph_out.append(np.round(diff_ph, decimals=5))  
    
    return ph_out



def calc_INL(ideal: list[float], real: list[float]) -> list[float]:
    
    INL = [0]*len(ideal)
    step = 360/len(ideal)
    for i in range(0,len(ideal)):
        INL[i] = (real[i] - ideal[i])/step
    
    return INL



def calc_DNL(real: list[float]) -> list[float]:
    
    DNL = [0]*(len(real)-1)
    step = 360/len(real)
    for i in range(0,len(real)-1):
        DNL[i] = (real[i+1] - real[i] - step)/step
    
    return DNL



def calc_SKEW(sig_out: list[float],
              sig_time: list[float],
              stable_period: float,
              threshold: float
              ) -> list[float]:
    

    skew = []
    start_samp = np.abs(sig_time - stable_period*2 -stable_period*32).argmin()
    if (sig_out[start_samp] >= threshold):
        while (sig_out[start_samp] >= threshold):
            start_samp = start_samp+1
    
    while(sig_out[start_samp] < threshold):
        start_samp = start_samp+1
    time_posedge = sig_time[start_samp]

    for i in np.arange(1,32):
        new_start_samp = np.abs(sig_time - time_posedge- stable_period*4).argmin()
        while (sig_out[new_start_samp] < threshold):
            new_start_samp = new_start_samp+1
            
        nx_ph_time_posedge = sig_time[new_start_samp]
        diff_time_posedge = np.round((nx_ph_time_posedge - time_posedge - stable_period*4)*1e12, decimals=4)   # en ps
        
        skew.append(diff_time_posedge)   

        time_posedge = nx_ph_time_posedge

    return skew


def PW_measv3(quadr_out: list[float],
            quadr_time: list[float],
            stable_period: float,
            threshold: float,
            quadr: int
            ) -> list[float]:

    PW_out = []

    for i in np.arange(0,8):
        samp_pw_start = np.abs(quadr_time - (i)*stable_period*4 - (quadr)*stable_period*32 - stable_period*2).argmin()
        
        if (quadr_out[samp_pw_start] >= threshold):
            while (quadr_out[samp_pw_start] >= threshold):
                samp_pw_start = samp_pw_start+1

        while(quadr_out[samp_pw_start] < threshold):
            samp_pw_start = samp_pw_start+1
        
        samp_pw_end = samp_pw_start
        while (quadr_out[samp_pw_end] >= threshold):
            samp_pw_end = samp_pw_end+1
            
        time_pw_start = quadr_time[samp_pw_start]
        time_pw_end = quadr_time[samp_pw_end]
        diff_time = round((time_pw_end - time_pw_start)*1e12, ndigits=3)

        PW_out.append(diff_time)
            
    
    return PW_out


def phase_tran_meas(quadr_out: list[float],
                        quadr_8i: list[float],
                        quadr_time: list[float],
                        threshold: float,
                        offset: float,
                        stable_period: float
                        ) -> list[float]:

    ph_out = []
    cycles = np.round((np.max(quadr_time)-min(quadr_time))/stable_period)

    for i in np.arange(0,cycles-1):
        start_samp = np.abs(quadr_time - i*stable_period - stable_period*32).argmin()
        time8I_samp = start_samp
        if (quadr_8i[time8I_samp] >= threshold):
            while (quadr_8i[time8I_samp] >= threshold):
                time8I_samp = time8I_samp+1

        while(quadr_8i[time8I_samp] < threshold):
            time8I_samp = time8I_samp+1
        time8I = quadr_time[time8I_samp]

        time_ph_samp = time8I_samp
        if (quadr_out[time_ph_samp] > threshold):
            while (quadr_out[time_ph_samp] >= threshold):
                time_ph_samp = time_ph_samp+1
        
        while (quadr_out[time_ph_samp] < threshold):
            time_ph_samp = time_ph_samp+1
        time_ph = quadr_time[time_ph_samp]

        diff_ph = np.round((time_ph - time8I)*360/stable_period - (offset),decimals=7)
        if diff_ph >= 355: 
            diff_ph -= 360
        elif diff_ph < -0.1:
            diff_ph += 360
        
        ph_out.append(diff_ph)
    
    return ph_out



