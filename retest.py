import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import filter
import scipy.io.wavfile as wavfile
from scipy.fft import fft
from scipy.special import yv
from scipy.signal import tf2sos
from scipy.io import savemat
import serial


# Fonctions pour éviter que l'interface graphique ne devienne floue
def make_dpi_aware():
    import ctypes
    import platform
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)


make_dpi_aware()


# Fonction de dessin
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def maximums(iterable, fs, n=10):
    out = []
    indexs = []
    list = abs(iterable).tolist()
    while len(out) < n:
        imax = list.index(max(list))
        out.append(iterable[imax])
        indexs.append(imax / fs)
        list.pop(imax)
    return indexs, out


ser = serial.Serial(
    port='Com5',  # Change this to the port number of your UART device
    baudrate=9600,  # Change this to your desired baudrate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Création de mise en page
sg.theme('black')
menu_def = [['Application', ['Exit']],
            ['Help', ['About']]]
layout_files = [[sg.Button("Fichier 1"), sg.Button("Fichier 2")],
                [sg.Text('Fichier 1 : Non sélectionné', key='T1')],
                [sg.Text('Fichier 2 : Non sélectionné', key='T2')],
                [sg.Button("Calcule le filtre 1/2")],
                [sg.Text('Fichier non défini', key="mf")]
                ]

layout_graph = [[sg.Text('Filters')], [sg.Button("Add"), sg.Button("Clear")],
                [sg.Slider(default_value=50, range=[0, 5000], orientation='h', key='-SLIDER-')],
                [sg.Canvas(size=[800, 600], key='-CANVAS-')]]

layout_effect = [[sg.Text('Effects')],
                 [sg.Button("Echo", k='Echo')],
                 [sg.Slider(default_value=0, range=(0, 2), resolution=0.1, orientation='h', key='SliderEcho')]]

logging_layout = [[sg.Text("Anything printed will display here!")],
                  [sg.Multiline(size=(60, 15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                                auto_refresh=True)]
                  ]

layout = [[sg.MenubarCustom(menu_def, font='Courier 10', tearoff=False)]]  # , #font : Police et taille.
layout += [[sg.TabGroup([[sg.Tab('Filtres depuis des fichiers', layout_files),
                          sg.Tab('Tracés', layout_graph),
                          sg.Tab('Effets', layout_effect),
                          sg.Tab('Control', logging_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True)
            ]]
layout[-1].append(sg.Sizegrip())

# Créez une fenêtre. finaliser = Doit être vrai.
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True,
                   element_justification='center', font='Monospace 18')

# Créez une figue à incorporer.
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

# Associez la figue à la toile.
fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

# Boucle d'événement
while True:
    event, values = window.read()
    print(event, values)

    if event in (None, "Cancel"):
        break
    elif event == "Fichier 1":
        tempfile1 = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                               filetypes=(("Wav files", "*.wav*"), ("all files", "*.*")))
        window["T1"].update("Fichier 1 :" + tempfile1)

    elif event == "Fichier 2":
        tempfile2 = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                               filetypes=(("Wav files", "*.wav*"), ("all files", "*.*")))
        window["T2"].update("Fichier 2 :" + tempfile2)

    elif event == "Calcule le filtre 1/2":
        try:
            tempfile1
        except NameError:
            window["mf"].update("Fichier 1 non défini")
        else:
            try:
                tempfile2
            except NameError:
                window["mf"].update("Fichier 2 non défini")

            else:
                if (tempfile1.split('.')[-1] != 'wav') and (tempfile2.split('.')[-1] != 'wav'):
                    window["mf"].update("Un des deux n'est pas un fichier .wav")
                else:
                    fs1, input_data1 = wavfile.read(tempfile1, mmap=True)
                    fs2, input_data2 = wavfile.read(tempfile2, mmap=True)
                    input_data1 = input_data1[:5 * fs1, 0] / 2 + input_data1[:5 * fs1, 1] / 2
                    input_data2 = input_data2[:5 * fs2, 0] + input_data2[:5 * fs2, 1] / 2
                    freq_data1 = fft(input_data1)
                    freq_data2 = fft(input_data2)

                    filter_data1_2 = freq_data1 / freq_data2
                    filter_dataX, filter_dataY = maximums(filter_data1_2, fs1, 20)

                    out = yv(20, (filter_dataX, filter_dataY))
                    print(out)
                    out_matrix = tf2sos(abs(out[1]), abs(out[0]))
                    savemat('data.mat', out_matrix)

    elif event == "Add":
        cutoff = values['-SLIDER-']
        filter.plot_filter(ax, ax2, cutoff)
        # Après avoir apporté des modifications, fig_agg.draw()Reflétez le changement avec.
        fig_agg.draw()

    elif event == 'Echo':
        data = b'r'
        data += bytes(str(values['SliderEcho'])[0], encoding='ascii')
        data += bytes(str(values['SliderEcho'])[2], encoding='ascii')
        data += b'e'
        print(data)
        ser.write(data)

    elif event == "Clear":
        ax.cla()
        fig_agg.draw()

# ferme la fenêtre.
window.close()
