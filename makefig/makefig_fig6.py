import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

########## GIVE THE NAME OF THE COMPOSITE FIGURE TO BE GENERATED ##########
composite_figure_name_root = 'benchmark_poolsize'

########## DEFINE PANELS AND THE FIGURE ##########
h_major, h = 4, 1.75
left, top_a, top_b, top_c, bottom = 1.5, 0.5, 0.5, 1, 0.8
shift_y_major = 0.0
panels_dict = {
    "plot_major_weak":        {"width": 8, "height": h_major, "position":    (1, bottom+h*4+h_major+top_b+top_c+shift_y_major)},
    "legend_major_weak":      {"width": 2, "height": h_major, "position":    (9, bottom+h*4+h_major+top_b+top_c+shift_y_major)},

    "plot_phases_weak":        {"width": 8, "height": h_major, "position":   (1, bottom+h*4+top_c+shift_y_major)},
    "legend_phases_weak":      {"width": 2, "height": h_major, "position":   (9, bottom+h*4+top_c+shift_y_major)},

    "conn_source_distr_a2n_10":   {"width": 2.5, "height": h, "position": (left, bottom+h*3)},
    "conn_target_distr_a2n_10":   {"width": 2.5, "height": h, "position": (left+2.5, bottom+h*3)},
    "conn_num_distr_a2n_10":      {"width": 2.5, "height": h, "position": (left+5, bottom+h*3)},
    "conn_per_target_a2n_10":      {"width": 2.5, "height": h, "position": (left+7.5, bottom+h*3)},

    "conn_source_distr_a2n_100":   {"width": 2.5, "height": h, "position": (left, bottom+h*2)},
    "conn_target_distr_a2n_100":   {"width": 2.5, "height": h, "position": (left+2.5, bottom+h*2)},
    "conn_num_distr_a2n_100":      {"width": 2.5, "height": h, "position": (left+5, bottom+h*2)},
    "conn_per_target_a2n_100":      {"width": 2.5, "height": h, "position": (left+7.5, bottom+h*2)},

    "conn_source_distr_a2n_1000":   {"width": 2.5, "height": h, "position": (left, bottom+h)},
    "conn_target_distr_a2n_1000":   {"width": 2.5, "height": h, "position": (left+2.5, bottom+h)},
    "conn_num_distr_a2n_1000":      {"width": 2.5, "height": h, "position": (left+5, bottom+h)},
    "conn_per_target_a2n_1000":      {"width": 2.5, "height": h, "position": (left+7.5, bottom+h)},

    "conn_source_distr_a2n_10000":   {"width": 2.5, "height": h, "position": (left, bottom)},
    "conn_target_distr_a2n_10000":   {"width": 2.5, "height": h, "position": (left+2.5, bottom)},
    "conn_num_distr_a2n_10000":      {"width": 2.5, "height": h, "position": (left+5, bottom)},
    "conn_per_target_a2n_10000":      {"width": 2.5, "height": h, "position": (left+7.5, bottom)},
}
final_panel_shrink = 1.0
figure_size_inch = (12, bottom+4*h+2*h_major+top_a+top_b+top_c)

########## SET PANEL LABELS ##########
label_shift_x = 0.1
label_names = [
    [
        {"A": (label_shift_x, bottom+4*h+2*h_major+top_b+top_c+0.2)},
        {"B": (label_shift_x, bottom+4*h+0.4)},
    ],
]
label_text_1 = [
    [
        {"Weak scaling": (0.8, bottom+h*4+2*h_major+top_b+top_c+0.2)},
        {"Astrocyte-to-neuron connectivity (at scale = 4)": (0.8, bottom+h*4+0.4)},
    ],
]
text_shift_x = 1.6
text_shift_y = 0.9
label_text_2 = [
    [
        {"pool_size\n= 10": (0.5*left, bottom+h*3+text_shift_y)},
        {"pool_size\n= 100": (0.5*left, bottom+h*2+text_shift_y)},
        {"pool_size\n= 1000": (0.5*left, bottom+h+text_shift_y)},
        {"pool_size\n= 10000": (0.5*left, bottom+text_shift_y)},
        {"Number of connected\nastrocytes\nper target neuron": (left+text_shift_x, 0.5*bottom)},
        {"Number of connected\ntarget neurons\nper astrocyte": (left+2.5+text_shift_x, 0.5*bottom)},
        {"Number of connections\nper astrocyte-neuron\npair": (left+5+text_shift_x, 0.5*bottom)},
        {"Number of connections\nper target neuron\n": (left+7.5+text_shift_x, 0.5*bottom)},
    ],
]
label_text_3 = [
    [
        {"Phases of state propagation": (5, bottom+h*4+h_major+top_c+0.2)},
    ],
]

# get figure dimensions in cm
cm_per_inch = 2.54
figure_size_cm = (figure_size_inch[0]*cm_per_inch, figure_size_inch[1]*cm_per_inch)
figure_left_cm = -figure_size_cm[0]/2
figure_bottom_cm = -figure_size_cm[1]/2

def panel_label(s, pos, size=15, bold=True, transform="figure", ha="left", va="center"):
    ax = plt.gca()
    fig = plt.gcf()
    transform_object = fig.dpi_scale_trans if transform == "figure" else ax.transAxes
    if bold:
        plt.text(pos[0],pos[1],r'\bfseries{}%s' % s,transform=transform_object,ha=ha,va=va,size=size)
    else:
        plt.text(pos[0],pos[1],r'%s' % s,transform=transform_object,ha=ha,va=va,size=size)

    return 0

def some_matplotlib_figure(
        fig_size=(8, 4),             ## figure size (width, height) in inches
        dpi=400,                     ## print resolution
        name_root="",
    ):

    plt.rcParams['text.usetex'] = True
    #plt.rcParams['font.size']= font_size
    plt.figure(1,figsize=fig_size,dpi=dpi)
    plt.clf()

    # Do it without subplots
    plt.axis("off")

    def function_a(list_in, size, bold, ha, va):
        for x in list_in:
            for y in x:
                try:
                    panel_label(list(y.keys())[0], list(y.values())[0], size=size, bold=bold, ha=ha, va=va)
                except:
                    pass

    function_a(label_names, size=40, bold=True, ha="left", va="center")
    function_a(label_text_1, size=30, bold=False, ha="left", va="center")
    function_a(label_text_2, size=18, bold=False, ha="center", va="center")
    function_a(label_text_3, size=25, bold=False, ha="center", va="center")

    fname = 'master_figure'
    plt.savefig("%s.pdf" % fname)
    plt.savefig("%s.eps" % fname)

    return fname, fig_size

def create_composite_figure(name_root,master_file_name,panels_dict,draw_grid=False,fig_size=(10,10)):

    file = open('%s.tex' % name_root , 'w')
    file.write(r"\documentclass{article}")
    file.write("\n")
    file.write(r"\usepackage{geometry}")
    file.write("\n")
    file.write(r"\geometry{paperwidth=%.3fin, paperheight=%.3fin, top=0pt, bottom=0pt, right=0pt, left=0pt}" % (fig_size[0],fig_size[1]))
    file.write("\n")
    file.write(r"\usepackage{tikz}")
    file.write("\n")
    file.write(r"\usepackage{graphicx}")
    file.write("\n")
    file.write(r"\pagestyle{empty}")
    file.write("\n")
    file.write(r"\begin{document}")
    file.write("\n")
    file.write(r"\noindent")
    file.write("\n")
    file.write(r"  \begin{tikzpicture}%")
    file.write("\n")
    file.write(r"    \node[inner sep=-1pt] (matplotlib_figure) at (0,0)")
    file.write("\n")
    file.write(r"    {\includegraphics{%s}};" % (master_file_name))
    file.write("\n")
    for key, value in panels_dict.items():
        file_path = key
        if not os.path.isfile(file_path + ".eps"):
            print(f"{file_path + '.eps'} does not exist!")
            continue
        position_cm = (figure_left_cm+value["position"][0]*cm_per_inch,figure_bottom_cm+value["position"][1]*cm_per_inch)
        file.write(r"    \node[inner sep=-1pt,rectangle,anchor=south west] (inkscape_sketch) at (%.4f,%.4f)" % position_cm)
        file.write("\n")
        file.write(r"    {\includegraphics[width=%.2fcm]{%s}};" % (value["width"]*cm_per_inch*final_panel_shrink, file_path))
        file.write("\n")
    file.write(r"  \end{tikzpicture}%")
    file.write("\n")
    file.write(r"\end{document}")
    file.write("\n")

    file.close()

    ## generate eps of composite figure
    os.system('latex %s.tex; dvips -o %s.eps %s.dvi' % (name_root,name_root,name_root))

    return 0

########################################

def run_all():
        ## create a matplotlib master figure and save as pdf (and eps)
        # (this figure defines the layout of the final composite figure)
        master_file_name, fig_size_out = some_matplotlib_figure(
            fig_size=figure_size_inch,
            name_root=composite_figure_name_root,
        )

        ## create the composite figure
        create_composite_figure(
            composite_figure_name_root,
            master_file_name,
            panels_dict,
            fig_size=fig_size_out
        )

        ## clean files
        os.system("rm *.log *.aux  *.dvi")

run_all()
