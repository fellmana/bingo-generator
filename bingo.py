"""Generate bingocards latex files and/or pdfs"""
import os
import sys
from random import shuffle as shuffle

class Bingo:
    """
    Parameters:
    
    labels: [str]
        List of str that are the contents of the grid.
        If less than number of squares is given the grid
        is populated with filler.
    filler: str
        Text added to labels if less than number of squares
        in grid.
    x,y: int
        Grid dimensions
    cellsize: float
        The size of each individual cell/square.
    vspace: float
        Control the top margin of page.
    title: str
        title text if None is provided no title is created.
    style: str
        Definis style of grid
    fontsize: str
        key to fontsizes dict that contains font definions
        to apply to text. 
    bold: boolean
        Apply bold font
    rounded: boolean
        Apply rounded corners to squares
    centering: boolean
        Apply centering of tikz picture.    
    padding: float
        Apply padding in the cells
    """

    #TODO: implent more styling options 
    fontsizes = {"footnote":"\\footnotesize ",
                "large":"\\large ",
                 "normal":"",
                 "huge":"\\huge "}

    def __init__(self,
                 labels=None,
                 filler="",
                 x=3, y=3,
                 cellsize=4.0,
                 vspace=20,
                 title=None,
                 style="thick",
                 fontsize="large",
                 bold=True,
                 rounded=False,
                 centering=True,
                 padding=0.0):

        self.x = x
        self.y = y
        self.filler = filler
        self.labels = labels
        if self.x * self.y > len(self.labels):
            diff = self.x*self.y - len(self.labels)
            self.labels = self.labels + [filler for _ in range(diff)]
        self.cellsize = cellsize
        self.title = title
        self.style = style
        try:
            self.fontsize=self.fontsizes[fontsize]
        except KeyError as err:
            print(f"Key {err} not in dictionary of fonts, try {self.fontsizes.keys()}"); exit()
        
        self.bold = "font=\\bf, " if bold else ""
        self.rounded = "rounded corners=10 , " if rounded else ""
        self.centering = centering
        self.vspace = vspace
        self.padding = padding

    def generate_latex_document(self,filename="bingo.tex"):
        
        base = ("\\documentclass[10pt]{article}\n"
                "\\usepackage{tikz}\n"
                "\\nofiles\n"
                "\\usepackage{geometry}\n"
                "\geometry{\n"
                "a4paper,\n"
                "total={170mm,257mm},\n"
                "left=20mm,\n"
                f"top={self.vspace}mm,\n"
                "}"
                "\\begin{document}\n")
        
        with open(filename,"w") as f:
            f.write(base)
    
            if self.title != None:
                f.write(f"\\title{{{self.title}}}\n")
                f.write("\\date{}\n")
                f.write("\\author{}\n")
                f.write("\\maketitle\n")
            if self.centering:
                f.write("\\centering\n")
            f.write(f"\\begin{{tikzpicture}}[{self.style}]\n")
            n = 0
            for i in range(self.x):
                for j in range(self.y):
                    f.write(f"\\draw[{self.rounded}] ({{{i*self.cellsize}}},{{{j*self.cellsize}}}) "\
                            f"rectangle ({{{(i+1)*self.cellsize}}},{{{(j+1)*self.cellsize}}});\n")
                    f.write(f"\\node[{self.bold}text width={self.cellsize-self.padding}cm, align=center]"\
                            f"at ({{{(i+0.5)*self.cellsize}}},"\
                            f"{{{(j+0.5)*self.cellsize}}}) {{{self.fontsize + self.labels[n]}}};\n")
                    n += 1
                    
            f.write("\\end{tikzpicture}\n")
            f.write("\\end{document}")


    def generate_pdf(self,filename="bingo.tex"):
        """Call on pdflatex to compile pdf
            NOTE: requires pdflatex 
        """
        #TODO: implement alternative compilation options
        #TODO: use subprocess and handle errors
        os.system(f"pdflatex {filename}")      

    def permutate(self):
        shuffle(self.labels)

    def make_random_bingo(self,n=3,pdf=True,store_tex=True,filename_base="bingo-",store_log=False):
        for i in range(n):
            self.permutate()
            self.generate_latex_document(filename=f"{filename_base}{i}.tex")
            if pdf:
                self.generate_pdf(filename=f"{filename_base}{i}.tex")
                if not store_log:
                    os.remove(f"{filename_base}{i}.log")
            if not store_tex:
                os.remove(f"{filename_base}{i}.tex")


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("i",nargs='?',default=None)
    parser.add_argument("--font",type = str.lower, choices=["footnote","large","normal","huge"],default="large",
                        help="Define fontsize of text")
    parser.add_argument("-x",type=int,default=3,
                        help="Grid size in x")
    parser.add_argument("-y",type=int,default=3,
                        help="Grid size in x")
    parser.add_argument("-cs","--cellsize",type=float,default=3.3,
                        help="Define cellsize")
    parser.add_argument("-vs","--vspace",type=float,default=20,
                        help="Vertical space above grid [mm]")
    parser.add_argument("-t","--title",nargs='+',default=None,
                        help="Title text")
    parser.add_argument("-n",type=int,default=None,
                        help="Make n random bingo cards")
    parser.add_argument("-r","--rounded",action="store_true",default=False,
                        help="Apply rounded corners")
    parser.add_argument("-b","--bold",action="store_true",default=False,
                        help="Apply bold font")
    parser.add_argument("-c","--centering",action="store_false",default=True,
                        help="Turn off centering"),
    parser.add_argument("-s","--style",type=str,default="thick",
                        help="Border stylr")
    parser.add_argument("-f","--filler",type=str,default="",
                        help="Filler text for empty squares")
    parser.add_argument("-fn",type=str,default="bingo.tex",
                        help="filename of .tex file")
    parser.add_argument("--nosave",action="store_true",default=False,
                        help="Dont save .tex files")
    parser.add_argument("--nopdf",action="store_true",default=False,
                        help="Dont create pdffiles")
    parser.add_argument("-p",type=float,default=0,
                        help="Cell text padding")
    args = parser.parse_args()
    
    return args

def make_bingo(args):
    labels = []
    with open(args.i, "r") as inp:
        for line in inp:
            labels.append(line)

    bingo =Bingo(labels=labels,filler=args.filler,x=args.x,y=args.y,
                 cellsize=args.cellsize,title=args.title,
                 style=args.style,fontsize=args.font,bold=args.bold,
                 rounded=args.rounded,centering=args.centering,
                 vspace=args.vspace, padding=args.p)     
    
    store_log = not args.nosave
    store_tex = not args.nosave
    store_pdf = not args.nopdf
    
    if args.n != None:
        bingo.make_random_bingo(args.n,store_log=store_log,store_tex=store_tex,
                                filename_base=args.fn.strip(".tex") + "-",
                                pdf=store_pdf)
    else:
        bingo.generate_latex_document(filename=args.fn)
        if not args.nopdf:
            bingo.generate_pdf()


if __name__ == "__main__":

    def run_in_code(): 
        print("RUNNING EXAMPLE\n -h or --help for commandline usage")
        testlabels = ["fortran", "vim", "emacs","a",
                    "bingo","DFT","LAMMPS","b",
                    "c++","python","asdajdiawd","c",
                    "c++","python","asoiwjdiawd","c"]
        bingo = Bingo(x=4,y=4,labels=testlabels,title="TEST TITLE")
        bingo.make_random_bingo(n=2)


    if len(sys.argv) > 1:
        args = parse_args()
        make_bingo(args)
    else:
        run_in_code()


