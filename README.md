# Bingo Generator

Simple script to generate latex (.tex) files of bingocards and build them to pdfs. 

## Dependencies
- pdflatex for building 


## Usage

usage: bingo.py [-h] [--font {large,normal,huge}] [-x X] [-y Y] [-cs CELLSIZE]
                [-vs VSPACE] [-t TITLE [TITLE ...]] [-n N] [-r] [-b] [-c]
                [-s STYLE] [-f FILLER] [-fn FN] [--nosave] [--nopdf]
                [i]

positional arguments:
  i

options:
  -h, --help            show this help message and exit
  --font {large,normal,huge}
                        Define fontsize of text
  -x X                  Grid size in x
  -y Y                  Grid size in x
  -cs CELLSIZE, --cellsize CELLSIZE
                        Define cellsize
  -vs VSPACE, --vspace VSPACE
                        Vertical space above grid [mm]
  -t TITLE [TITLE ...], --title TITLE [TITLE ...]
                        Title text
  -n N                  Make n random bingo cards
  -r, --rounded         Apply rounded corners
  -b, --bold            Apply bold font
  -c, --centering       Turn off centering
  -s STYLE, --style STYLE
                        Border stylr
  -f FILLER, --filler FILLER
                        Filler text for empty squares
  -fn FN                filename of .tex file
  --nosave              Dont save .tex files
  --nopdf               Dont create pdffiles