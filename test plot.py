import math

import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

liste_filtre = []

matplotlib.use('TkAgg')

fig, (ax1, ax2) = plt.subplots(1, 2, sharey="row")
size = (800, 480)

sg.theme('black')
menu_def = [['Application', ['Exit']],
            ['Help', ['About']]]
right_click_menu_def = [[], ['Edit Me', 'Versions', 'Exit']]

paramètres_layout = [
    [sg.Checkbox('Allumer/Eteindre', default=False, k='-Etat-')],
    [sg.Button("Ajouter un filtre", k='-Add_filter-')]
]

trace_layout = [
    [sg.Checkbox('Entrée', default=False, size=(10, 1), k='-BTN_IN-'),
     sg.Checkbox('Sortie', default=False, size=(10, 1), k='-BTN_OUT-')],
    [sg.Graph(canvas_size=(800, 450), graph_bottom_left=(0, 0), graph_top_right=(800, 450),
              background_color='white', enable_events=True, key='-tracés-')]
]

filtre_layout = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                 [sg.Listbox(values=sg.theme_list(),
                             size=(20, 12),
                             key='-THEME LISTBOX-',
                             enable_events=True)],
                 [sg.Button("Set Theme")]]

logging_layout = [[sg.Text("Anything printed will display here!")],
                  [sg.Multiline(size=(60, 15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                                auto_refresh=True)]
                  ]

layout = [[sg.MenubarCustom(menu_def, font='Courier 10', tearoff=False)]]  # , #font : Police et taille.
# [sg.Text('Projet2A API', size=(38, 1), justification='center', font=("Helvetica", 16),
#        relief=sg.RELIEF_RIDGE, enable_events=False)]]# relief => cadre(ici)
layout += [[sg.TabGroup([[sg.Tab('Paramètres', paramètres_layout),
                          sg.Tab('Tracés', trace_layout),
                          # sg.Tab('Filtre', filtre_layout),
                          sg.Tab('Control', logging_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),

            ]]
layout[-1].append(sg.Sizegrip())
window = sg.Window('Projet2A API', layout, right_click_menu=right_click_menu_def,
                   right_click_menu_tearoff=False, grab_anywhere=False, resizable=True, margins=(0, 0),
                   use_custom_titlebar=False, finalize=True, keep_on_top=False)
window.set_min_size(window.size)


def make_filter_liste():
    filtres_layout = [
        [sg.Checkbox("Filtre" + str('i'), default=False, k='-Filtre' + str(i) + '-') for i in range(len(liste_filtre))]
    ]
    filtres_layout[-1].append(sg.Sizegrip())
    filtres_window = sg.Window("Liste des filtres", filtres_layout,
                               right_click_menu_tearoff=False, grab_anywhere=False, resizable=False, margins=(0, 0),
                               use_custom_titlebar=False, finalize=True, keep_on_top=False, modal=True)
    return filtres_window


def make_filter_window():
    filter_layout = [
        [sg.Text("Ajout d'un filtre", size=(50, 1), justification='center')],
        [sg.Combo(values=('Passe bas', 'Passe haut', 'Passe Bande', 'Coupe Bande'), default_value='Passe bas',
                  readonly=False, size=(50, 20), k='-COMBO-')],
        [sg.Text('Fréquence basse (Hz)', size=(20, 1)), sg.Text('Fréquence haute (Hz)', size=(20, 1))],
        [sg.Input(size=(20, 1), k='-F1-'), sg.Input(size=(20, 1), k='-F2-')],
        [sg.Button("OK", size=(50, 1), k='-BTN_CLOSE-')]
    ]
    filter_layout[-1].append(sg.Sizegrip())
    filter_window = sg.Window("Ajout d'un filtre", filter_layout,
                              right_click_menu_tearoff=False, grab_anywhere=False, resizable=False, margins=(0, 0),
                              no_titlebar=True, finalize=True, keep_on_top=True, modal=False)
    return filter_window


def main():
    filters_list_window = make_filter_liste()
    canvas = FigureCanvasTkAgg(fig, window['-tracés-'].Widget)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=0, column=0)

    theta = 0  # offset angle for each sine curve

    buffer_in = False
    buffer_out = False

    while True:
        # print(window.size[0], window.size[1])

        event, values = window.read(timeout=100)

        if values['-BTN_IN-']:
            # if values['-BTN_OUT-']:
            #    window.write_event_value('-BTN_OUT-', False)
            if not buffer_in:
                buffer_in = True
                buffer_out = False

            # Generate points for sine curve.
            x = [degree for degree in range(1080)]
            y = [math.sin((degree + theta) / 180 * math.pi) for degree in range(1080)]
            x2 = [degree for degree in range(1080)]
            y2 = [math.cos((degree + theta) / 180 * math.pi) for degree in range(1080)]

            # Reset ax
            ax1.cla()
            ax1.set_title("Input signal")
            ax1.set_xlabel("t")
            ax1.set_ylabel("A(V)")
            ax1.grid()
            ax1.plot(x, y)  # Plot new curve

            ax2.cla()
            ax2.set_title("Input signal spectrum")
            ax2.set_xlabel("f(Hz)")
            ax2.set_xscale('log')
            ax2.grid()
            ax2.plot(x2, y2)
            fig.canvas.draw()

        elif values['-BTN_OUT-']:
            # if values['-BTN_IN-']:
            #   window.write_event_value('-BTN_IN-', False)
            if not buffer_out:
                buffer_out = True
                buffer_in = False

            x = [degree for degree in range(1080)]
            y = [10 * math.sin((degree + theta) / 180 * math.pi) for degree in range(1080)]
            x2 = [degree for degree in range(1080)]
            y2 = [0.5 * math.cos((degree + theta) / 180 * math.pi) for degree in range(1080)]

            # Reset ax
            ax1.cla()
            ax1.set_title("Output signal")
            ax1.set_xlabel("t")
            ax1.set_ylabel("A(V)")
            ax1.grid()
            ax1.plot(x, y)  # Plot new curve

            ax2.cla()
            ax2.set_title("Output signal spectrum")
            ax2.set_xlabel("f(Hz)")
            ax2.set_xscale('log')
            ax2.grid()
            ax2.plot(x2, y2)
            fig.canvas.draw()

        theta = (theta + 10) % 360  # change offset angle for curve shift on Graph

        # keep an animation running so show things are happening

        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ', values[key])
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break

        elif event == '-Add_filter-':
            temp_window = True
            filter_window = make_filter_window()

            while temp_window:
                event_filter, values_filter = filter_window.read(timeout=100)
                if event_filter == '-BTN_CLOSE-':
                    temp_window = False
                    filter_type = values_filter['-COMBO-']
                    f1 = values_filter['-F1-']
                    f2 = values_filter['-F2-']
                    filter_window.close()
            filter_window.close()
            print(filter_type, f1, f2)
            liste_filtre.append((filter_type, f1, f2))


        elif event == 'About':
            print("[LOG] Clicked About!")
            sg.popup('Project 2A ENSEA',
                     'Trombone modifying sound API ',
                     keep_on_top=True)
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Versions':
            sg.popup_scrolled(__file__, sg.get_versions(), keep_on_top=True, non_blocking=True)
    window.close()
    exit(0)


if __name__ == '__main__':
    sg.theme('black')
    main()
