import sys
import os
from tytycss.tytycss import beautify_cssfile

src_file = sys.argv[1]
dr,fn = os.path.split(src_file)

dst_file = dr+'beau.'+fn

def main():
    beautify_cssfile(src_file,dst_file)
