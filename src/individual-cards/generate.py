#!/usr/local/bin/python3

import os
import subprocess

def xelatex(basename):
    subprocess.check_output(["xelatex", '\def\BLEEDAREA{}\input{' + basename + '.tex}'])
    os.remove(basename + ".aux")
    os.remove(basename + ".log")

def pdftopng(basename):
    subprocess.check_output(["convert", "-density", "300", "-geometry", "732x1101", basename + ".pdf", basename + ".png"])

sources = ["../black.txt", "../white.txt"]
templates = ["black", "white"]

output_directory = "../../PNGs-to-print/individual-cards"

subprocess.run(["rm", "-rf", output_directory])
os.mkdir(output_directory)

j = 0

for i in range(len(sources)):
    print("Generating " + templates[i] + "_back.png")
    xelatex(templates[i] + "_back")
    pdftopng(templates[i] + "_back")
    os.remove(templates[i] + "_back.pdf")
    with open(templates[i] + "_front.tex") as front_template:
        front_tex_template = front_template.readlines()
    front_tex_template = "\n".join(front_tex_template)
    with open(sources[i]) as source:
        for line in source:
            line = line.rstrip()
            j += 1
            print("Generating {:s} card #{:d}: {:s}".format(templates[i], j, line))
            filename = "FRONT{:03d}".format(j)
            front_tex = front_tex_template.replace("CARDTEXTHERE", line)
            with open(filename + ".tex", 'w') as front:
                print(front_tex, file=front)
            xelatex(filename)
            os.remove(filename + ".tex")
            pdftopng(filename)
            os.remove(filename + ".pdf")
            subprocess.run(["mv", filename + ".png", output_directory])
            filename = "BACK{:03d}".format(j)
            subprocess.run(["cp", templates[i] + "_back.png", output_directory + "/" + filename + ".png"])
        os.remove(templates[i] + "_back.png")
