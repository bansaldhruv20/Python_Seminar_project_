from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import platform
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget

app = Tk()
app.title("SIMPLY SUPPORTED BEAMS")
style = ttk.Style(app)


def selection():
    global selected
    selected = str(load_type.get())
    print(selected)


# Load Type
load_type = StringVar()
load_type.set("point_load")

selected = "point_load"

# Radio button for load type
load_type_label = Label(app, text="Load Type", font=('normal', 10), padx=5, pady=5)
load_type_label.grid(row=0, column=0, sticky=W)

point_load_button = Radiobutton(app, text="Point Load", variable=load_type, value="point_load", command=selection)
point_load_button.grid(row=0, column=1, sticky=W)

udl_button = Radiobutton(app, text="UDL Load", variable=load_type, value="udl_load", command=selection)
udl_button.grid(row=0, column=2, sticky=W)

uvl_button = Radiobutton(app, text="UVL Load", variable=load_type, value="uvl_load", command=selection)
uvl_button.grid(row=0, column=3, sticky=W)

print(point_load_button)

# INPUT DATA
point_load_text = DoubleVar()
point_load_text.set(0)
point_load_label = Label(app, text="point load", font=('normal', 10), padx=5, pady=5)
point_load_label.grid(row=1, column=0)
point_load_entry = Entry(app, textvariable=point_load_text, width=30)
point_load_entry.grid(row=1, column=1)
point_load_unit = Label(app, text="N", font=('normal', 10), padx=5, pady=5)
point_load_unit.grid(row=1, column=2)

# INPUT LENGTH OF BEAM
length_Beam_text = DoubleVar()
length_Beam_text.set(0)
length_Beam_label = Label(app, text="Length of Beam", font=('normal', 10), padx=5, pady=5)
length_Beam_label.grid(row=2, column=0)
length_Beam_entry = Entry(app, textvariable=length_Beam_text, width=30)
length_Beam_entry.grid(row=2, column=1)
length_Beam_unit = Label(app, text="m", font=('normal', 10), padx=5, pady=5)
length_Beam_unit.grid(row=2, column=2)

# INPUT DISTANCE FROM LEFT END
a_text = DoubleVar()
a_text.set(0)
a_label = Label(app, text="Distance from left end ", font=('normal', 10), padx=5, pady=5)
a_label.grid(row=3, column=0)
a_entry = Entry(app, textvariable=a_text, width=30)
a_entry.grid(row=3, column=1)
a_unit = Label(app, text="m", font=('normal', 10), padx=5, pady=5)
a_unit.grid(row=3, column=2)

udl_load_text = DoubleVar()
udl_load_text.set(0)
udl_load_label = Label(app, text="UDL Load", font=('normal', 10), padx=5, pady=5)
udl_load_label.grid(row=4, column=0)
udl_load_entry = Entry(app, textvariable=udl_load_text, width=30)
udl_load_entry.grid(row=4, column=1)
udl_load_unit = Label(app, text="N/m", font=('normal', 10), padx=5, pady=5)
udl_load_unit.grid(row=4, column=2)

udl_start_text = DoubleVar()
udl_start_text.set(0)
udl_start_label = Label(app, text="UDL Start", font=('normal', 10), padx=5, pady=5)
udl_start_label.grid(row=5, column=0)
udl_start_entry = Entry(app, textvariable=udl_start_text, width=30)
udl_start_entry.grid(row=5, column=1)
udl_start_unit = Label(app, text="m", font=('normal', 10), padx=5, pady=5)
udl_start_unit.grid(row=5, column=2)

udl_end_text = DoubleVar()
udl_end_text.set(0)
udl_end_label = Label(app, text="UDL End", font=('normal', 10), padx=5, pady=5)
udl_end_label.grid(row=6, column=0)
udl_end_entry = Entry(app, textvariable=udl_end_text, width=30)
udl_end_entry.grid(row=6, column=1)
udl_end_unit = Label(app, text="m", font=('normal', 10), padx=5, pady=5)
udl_end_unit.grid(row=6, column=2)

uvl_start_text = DoubleVar()
uvl_start_text.set(0)
uvl_start_label = Label(app, text="UVL Start", font=('normal', 10), padx=5, pady=5)
uvl_start_label.grid(row=7, column=0)
uvl_start_entry = Entry(app, textvariable=uvl_start_text, width=30)
uvl_start_entry.grid(row=7, column=1)
uvl_start_unit = Label(app, text="m", font=('normal', 10), padx=5, pady=5)
uvl_start_unit.grid(row=7, column=2)

uvl_end_text = DoubleVar()
uvl_end_text.set(0)
uvl_end_label = Label(app, text="UVL End", font=('normal', 10), padx=5, pady=5)
uvl_end_label.grid(row=8, column=0)
uvl_end_entry = Entry(app, textvariable=uvl_end_text, width=30)
uvl_end_entry.grid(row=8, column=1)
uvl_end_unit = Label(app, text="m", font=('normal', 10), padx=5, pady=5)
uvl_end_unit.grid(row=8, column=2)

uvl_load_text = DoubleVar()
uvl_load_text.set(0)
uvl_load_label = Label(app, text="UVL Load", font=('normal', 10), padx=5, pady=5)
uvl_load_label.grid(row=9, column=0)
uvl_load_entry = Entry(app, textvariable=uvl_load_text, width=30)
uvl_load_entry.grid(row=9, column=1)
uvl_load_unit = Label(app, text="N/m", font=('normal', 10), padx=5, pady=5)
uvl_load_unit.grid(row=9, column=2)


def save_var_latex(key, value):
    dict_var = {}

    file_path = os.path.join(os.getcwd(), "mydata.dat")

    try:
        with open(file_path, newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                dict_var[row[0]] = row[1]
    except FileNotFoundError:
        pass

    dict_var[key] = value

    with open(file_path, "w") as f:
        for key in dict_var.keys():
            f.write(f"{key},{dict_var[key]}\n")


def pdfconverter():
    # TeX source filename
    tex_filename = 'SimplySupportedBeam.tex'
    filename, ext = os.path.splitext(tex_filename)
    # the corresponding PDF filename
    pdf_filename = filename + '.pdf'

    # compile TeX file
    subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename])

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        raise RuntimeError('PDF output not found')

    # open PDF with platform-specific command
    if platform.system().lower() == 'darwin':
        subprocess.run(['open', pdf_filename])
    elif platform.system().lower() == 'windows':
        os.startfile(pdf_filename)
    elif platform.system().lower() == 'linux':
        subprocess.run(['xdg-open', pdf_filename])
    else:
        raise RuntimeError('Unknown operating system "{}"'.format(platform.system()))


X = [0]
SF = [0]
M = [0]
R1 = 0
R2 = 0


def getvals():
    if selected == "point_load":
        b = length_Beam_text.get() - a_text.get()
        print(b)
        R1 = (point_load_text.get() * b) / length_Beam_text.get()
        R2 = point_load_text.get() - R1
        l = np.linspace(0, length_Beam_text.get(), 100)
        for x in l:
            if x <= a_text.get():
                m = R1 * x
                sf = R1
            elif x > a_text.get():
                m = R1 * x - point_load_text.get() * (x - a_text.get())
                sf = -R2
            M.append(m)
            X.append(x)
            SF.append(sf)
        # Append the end point with all zero to close the hatch
        X.append(x)
        SF.append(0)
        M.append(0)
        print(M)
        print(SF)
        print(X)

        # Create figure and axes
        fig, ax = plt.subplots()

        # Set the x-axis limits
        ax.set_xlim(0, length_Beam_text.get())

        # Set the y-axis limits
        ax.set_ylim(-1, 1)

        # Disable axis labels
        ax.axis('off')

        # Draw the beam
        beam_height = 0.1
        ax.plot([0, length_Beam_text.get()], [0, 0], color='black', linewidth=2)  # Beam line
        ax.plot([0, 0], [-beam_height, beam_height], color='black', linewidth=5)  # Support 1
        ax.plot([length_Beam_text.get(), length_Beam_text.get()], [-beam_height, beam_height], color='black',
                linewidth=5)  # Support 2

        # Draw arrowheads at supports
        ax.arrow(0, -beam_height * 2, 0, beam_height * 2, head_width=0.1, head_length=0.1, fc='black', ec='black')
        ax.arrow(length_Beam_text.get(), -beam_height * 2, 0, beam_height * 2, head_width=0.1, head_length=0.1,
                 fc='black', ec='black')
        ax.arrow(a_text.get(), 0, 0, point_load_text.get(), head_width=0.2, head_length=0.1, fc='red', ec='red', )

        ssbeam_file = "SSbeam.png"
        plt.savefig(ssbeam_file)
        # Show the plot
        plt.show()

        # shear force plot
        plt.plot(X, SF)
        plt.fill(X, SF, fill=True, color='blue')
        plt.title('SFD')
        # adding vertical line in data co-ordinates
        plt.axvline(0, c='black', ls='-')
        # adding horizontal line in data co-ordinates
        plt.axhline(0, c='black', ls='-')
        plt.xlabel("X values in m")
        plt.ylabel("shear force values in N")
        sfd_file = "SFD.png"
        plt.savefig(sfd_file)
        plt.show()

        # bending moment diagram
        plt.plot(X, M)
        plt.fill(X, M, fill=False, hatch='\\')
        plt.title('BMD')
        plt.axvline(0, c='black', ls='-')
        plt.axhline(0, c='black', ls='-')
        plt.xlabel("X values in m")
        plt.ylabel("bending moment  values in N-m")
        bmd_file = "BMD.png"
        plt.savefig(bmd_file)
        plt.show()



    elif selected == "udl_load":
        l = np.linspace(0, length_Beam_text.get(), 100)
        W = udl_load_text.get()
        for x in l:
            if (udl_end_text.get() - udl_start_text.get()) == length_Beam_text.get():
                R1 = udl_load_text.get() * length_Beam_text.get() / 2
                R2 = udl_load_text.get() * length_Beam_text.get() / 2
                m = R1 * x - (udl_load_text.get() * x * x) / 2
                sf = R1 - udl_load_text.get() * x
                M.append(m)
                X.append(x)
                SF.append(sf)

            elif (udl_end_text.get() - udl_start_text.get() != length_Beam_text.get()):
                a = udl_start_text.get()
                b = udl_end_text.get() - udl_start_text.get()
                c = length_Beam_text.get() - (a + b)
                R1 = (W * b * (2 * c + b)) / (2 * length_Beam_text.get())
                R2 = (W * b * (2 * a + b)) / (2 * length_Beam_text.get())
                for x in l:
                    if x < a:
                        sf = R1
                        m = R1 * x
                    elif x > a and x <= (a + b):
                        sf = R1 - W * (x - a)
                        m = R1 * x - (W * (x - a) * (x - a)) / 2
                    elif x > c:
                        sf = R2
                        m = R2 * (length_Beam_text.get() - x)
                M.append(m)
                X.append(x)
                SF.append(sf)
        # Append the end point with all zero to close the hatch
        X.append(x)
        SF.append(0)
        M.append(0)
        print(M)
        print(SF)
        print(X)
        # shear force plot
        plt.plot(X, SF)
        plt.fill(X, SF, fill=True, color='blue')
        plt.title('SFD')
        # adding vertical line in data co-ordinates
        plt.axvline(0, c='black', ls='-')
        # adding horizontal line in data co-ordinates
        plt.axhline(0, c='black', ls='-')
        plt.xlabel("X values in m")
        plt.ylabel("shear force values in N")
        sfd_file = "SFD.png"
        plt.savefig(sfd_file)
        plt.show()

        # bending moment diagram
        plt.plot(X, M)
        plt.fill(X, M, fill=False, hatch='\\')
        plt.title('BMD')
        plt.axvline(0, c='black', ls='-')
        plt.axhline(0, c='black', ls='-')
        plt.xlabel("X values in m")
        plt.ylabel("bending moment  values in N-m")
        bmd_file = "BMD.png"
        plt.savefig(bmd_file)
        plt.show()


    elif selected == 'uvl_load':
        l = np.linspace(0, length_Beam_text.get(), 100)
        P2 = uvl_load_text.get()
        for x in l:
            R1 = uvl_load_text.get() * length_Beam_text.get() / 6
            R2 = uvl_load_text.get() * length_Beam_text.get() / 3
            w = P2 * x / length_Beam_text.get()
            m = R1 * x - (uvl_load_text.get() * x * x * x) / (6 * length_Beam_text.get())
            sf = R1 - w * x / 2
            M.append(m)
            X.append(x)
            SF.append(sf)
        # Append the end point with all zero to close the hatch
        X.append(x)
        SF.append(0)
        M.append(0)

        plt.plot(X, SF)
        plt.fill(X, SF, fill=True, color='cyan')
        plt.title('SFD')
        # adding vertical line in data co-ordinates
        plt.axvline(0, c='black', ls='-')
        # adding horizontal line in data co-ordinates
        plt.axhline(0, c='black', ls='-')
        plt.xlabel("X values in m")
        plt.ylabel("shear force values in N")
        sfd_file = "SFD.png"
        plt.savefig(sfd_file)
        plt.show()

        # bending moment diagram
        plt.plot(X, M)
        plt.fill(X, M, fill=True, color='pink')
        plt.title('BMD')
        plt.axvline(0, c='black', ls='-')
        plt.axhline(0, c='black', ls='-')
        plt.xlabel("X values in m")
        plt.ylabel("bending moment  values in N-m")
        bmd_file = "BMD.png"
        plt.savefig(bmd_file)
        plt.show()

        def getoutput():
            point_load_label.destroy()
            point_load_entry.destroy()
            point_load_unit.destroy()
            length_Beam_label.destroy()
            length_Beam_entry.destroy()
            length_Beam_unit.destroy()
            a_label.destroy()
            a_entry.destroy()
            a_unit.destroy()
            udl_load_label.destroy()
            udl_load_entry.destroy()
            udl_load_unit.destroy()
            udl_start_label.destroy()
            udl_start_entry.destroy()
            udl_start_unit.destroy()
            udl_end_label.destroy()
            udl_end_entry.destroy()
            udl_end_unit.destroy()
            uvl_load_label.destroy()
            uvl_load_entry.destroy()
            uvl_load_unit.destroy()
            button1.destroy()

            tab_control = ttk.Notebook(app, style="lefttab.TNotebook")

            tab6 = ttk.Frame(tab_control)

            # Add tabs to Notebook
            tab_control.add(tab6, text=f'{" Export ":^20s}')

            # tab_control.pack(expand=1, fill='both')
            tab_control.grid(row=0, column=0, padx=5, pady=5)
            wrapper6 = LabelFrame(tab6, text="Generate Pdf")
            wrapper6.pack(fill="both", expand="YES", padx=20, pady=10)

            def save_var_latex(key, value):
                dict_var = {}

                file_path = os.path.join(os.getcwd(), "mydata.dat")

                try:
                    with open(file_path, newline="") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            dict_var[row[0]] = row[1]
                except FileNotFoundError:
                    pass

                dict_var[key] = value

                with open(file_path, "w") as f:
                    for key in dict_var.keys():
                        f.write(f"{key},{dict_var[key]}\n")

            button3.destroy()
            save_var_latex("point_load", str(point_load_text.get()))
            save_var_latex("length_beam", str(length_Beam_text.get()))
            save_var_latex("a_distance", str(a_text.get()))
            save_var_latex("R1", float(f'{R1:.2f}'))
            save_var_latex("R2", float(f'{R2:.2f}'))
            save_var_latex("b", float(f'{b:.2f}'))
            save_var_latex("X", float(f'{X[0]:.2f}'))
            save_var_latex("M", float(f'{M[0]:.2f}'))
            save_var_latex("SF", float(f'{SF[0]:.2f}'))

            def pdfconverter():
                with open('SimplySupportedBeam.tex', 'w') as file:
                    file.write('\\documentclass[12pt,a4paper]{article}\n')
                    file.write('\\usepackage{marginnote} \n')
                    file.write('\\usepackage{wallpaper}\n')
                    file.write('\\usepackage{lastpage}\n')
                    file.write(
                        '\\usepackage[left=1.3cm,right=4.6cm,top=1.8cm,bottom=4.0cm,marginparwidth=3.4cm]{geometry}\n ')
                    file.write('\\usepackage{amsmath}\n')
                    file.write('\\usepackage{amssymb}\n')
                    file.write('\\usepackage{xcolor}\n')
                    file.write('\\usepackage{datatool}\n')
                    file.write('\\usepackage{filecontents}\n')
                    file.write('\\DTLsetseparator{,}\n')
                    file.write('\\DTLloaddb[nosheader, keys={thekey,thevalue}]{mydata}{mydata.dat}\n')
                    file.write('\\newcommand{\\var}[1]{\DTLfetch{mydata}{thekey}{#1}{thevalue}}\n')
                    file.write('\\usepackage{fancyhdr}\n')
                    file.write('\\setlength{\headheight}{80pt} \n')
                    file.write('\\pagestyle{fancy}\\fancyhf{}\n ')
                    file.write('\\renewcommand{\headrulewidth}{0pt} \n')
                    file.write('\\setlength{\parindent}{0cm}\n')
                    file.write('\\newcommand{\\tab}{\hspace*{2em}}\n ')
                    file.write('\\newcommand\BackgroundStructure{ \n')
                    file.write('\\setlength{\\unitlength}{1mm}\n')
                    file.write(' \\setlength\\fboxsep{0mm} \n')
                    file.write('\\setlength\\fboxrule{0.5mm}\n')
                    file.write('\put(10, 10){\\fcolorbox{black}{blue!10}{\\framebox(155,247){}}}\n')
                    file.write('\put(165, 10){\\fcolorbox{black}{blue!10}{\\framebox(37,247){}}}\n')
                    file.write('\put(10, 262){\\fcolorbox{black}{white!10}{\\framebox(192, 25){}}}\n')
                    file.write('\put(137, 263){\includegraphics[height=23mm,keepaspectratio]{logo}}\n')
                    file.write('}\n')
                    file.write('\\fancyhead[L]{\\begin{tabular}{l r | l r}\n')
                    file.write(
                        '\\textbf{Project} & BEAM ANALYSIS & \\textbf{Page} & \\thepage/\pageref{LastPage} \\\ \n')
                    file.write(
                        '\\textbf{Designer} & Harsha Agarwal & \\textbf{Reviewer} & PROF. M. N. Shariff \\\ \n')
                    file.write('\\textbf{Updated} & 06/06/2023 & \\textbf{Reviewed} & 06/06/2023  \\\ \n')
                    file.write('\end{tabular}}\n')
                    file.write('\\begin{document}\n')
                    file.write('Beam figure:\n\n')
                    file.write("\\begin{figure}\n")
                    file.write("\\centering\n")
                    file.write("\\includegraphics[width=0.3\\textwidth]{SSbeam.png}\n")
                    file.write("\\caption{BEAM}\n")
                    file.write("\\end{figure}\n")
                    file.write('\AddToShipoutPicture{\BackgroundStructure} \n')
                    file.write('\section{SFD and BMD of Simply Supported  Beam} \n')
                    file.write('\subsection{Beam  Design} \n\n\n')
                    file.write('\\tab Point\;Load\; on\; the\; beam ($P$)\; =\; \\var{point_load}N \\\[8pt]\n')
                    file.write('\\tab Length\; of\; the\; beam ($L$)\; =\; \\var{length_beam}m \\\[8pt]\n')
                    file.write(
                        '\\tab distance\; of\; the\; left\; support ($a$)\; =\; \\var{a_distance}m \\\[8pt]\n')
                    file.write('\subsection{Procedure:} \n\n\n')
                    file.write(
                        '\\tab distance\; of\; the\; right\; support ($b$)\; =\; \\var{length_beam}m \\\[8pt]\n-\\var{a_distance}m \\\[8pt]\n')
                    file.write('\\tab distance\; of\; the\; right\; support ($b$)\; =\; \\var{b}m \\\[8pt]\n')
                    file.write('Step 1:\n\n')
                    file.write(
                        '- Find reaction force Ra,Rb by applying equilibrium equations and conserving moment about a point ')
                    file.write('\\begin{equation*}\n')
                    file.write('sum F_x &= 0 \\')
                    file.write('sum F_y &= 0 \\')
                    file.write('sum M &= 0 \n\n')
                    file.write('R1 = \\frac{ (point_load \\times b)/{L}}\n\n')
                    file.write('R2 = \\ {point_load}-{R1} \n\n')
                    file.write('\end{equation*}\n')
                    file.write('left\; reaction(Ra) = \\var{R1}\n\n')
                    file.write(' right\; reaction(Rb) = \\var{R2}\n\n')
                    file.write('Step 2:\n\n')
                    file.write('- taking different section at a distance x to calculate shear forces\n\n')
                    file.write(r'l &= \text{np.linspace}(0, \text{{length\_Beam\_text.get()}}, 100)' + '\n\n')
                    file.write(r'X &= [0]' + '\n\n')
                    file.write(r'SF &= [0]' + '\n\n')
                    file.write(r'M &= [0]' + '\n\n')
                    file.write(r'\text{for } x \text{ in } l:' + '\n\n')
                    file.write(r'\quad \text{if } x \leq {a}:' + '\n\n')
                    file.write(r'\quad \quad m &= R1 \cdot x' + '\n\n')
                    file.write(r'\quad \quad sf &= R1' + '\n\n')
                    file.write(r'\quad \text{elif } x > {a}:' + '\n\n')
                    file.write(r'\quad \quad m &= R1 \cdot x - {p}*{(x-{a})}' + '\n\n')
                    file.write(r'\quad \quad sf &= {-R2}' + '\n\n')

                    file.write("\\begin{figure}\n")
                    file.write("\\centering\n")
                    file.write("\\includegraphics{SFD.png}\n")
                    file.write("\\caption{SFD}\n")
                    file.write("\\includegraphics{BMD.png}\n")
                    file.write("\\caption{BMD}\n")
                    file.write("\\end{figure}\n")

                    file.write('\end{document}\n')

                    # TeX source filename
                    tex_filename = 'SimplySupportedBeam.tex'
                    filename, ext = os.path.splitext(tex_filename)
                    # the corresponding PDF filename
                    pdf_filename = filename + '.pdf'

                    # compile TeX file
                    subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename])

                    # check if PDF is successfully generated
                    if not os.path.exists(pdf_filename):
                        raise RuntimeError('PDF output not found')

                    # open PDF with platform-specific command
                    if platform.system().lower() == 'darwin':
                        subprocess.run(['open', pdf_filename])
                    elif platform.system().lower() == 'windows':
                        os.startfile(pdf_filename)
                    elif platform.system().lower() == 'linux':
                        subprocess.run(['xdg-open', pdf_filename])
                    else:
                        raise RuntimeError('Unknown operating system "{}"'.format(platform.system()))

            button_gen_pdf = Button(wrapper6, text="Generate Pdf", width=12, bg='#03A9F4', fg='#fff',
                                    command=pdfconverter)
            button_gen_pdf.pack()

        button3 = Button(app, text="Next", width=12, bg='#03A9F4', fg='#fff', command=getoutput)
        # button3.pack()
        button3.grid(row=23, column=0, padx=10, pady=10)


button1 = Button(app, text="Run", width=12, bg='#03A9F4', fg='#fff', command=getvals)
# button1.pack()
button1.grid(row=17, column=0, padx=10, pady=10)

app.mainloop()
