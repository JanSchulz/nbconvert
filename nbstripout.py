#!/usr/bin/env python

"""
Clear outputs of IPython notebooks.

By default, it prints the notebooks without outputs into stdout.
When the --inplace option is given, all files will be overwritten.
If no input is given, STDIN is used and output is printed to STDOUT.

"""

import sys

from IPython.nbformat import current as nbformat


def clear_outputs(nb,strip_prompt=False):
    """Clear output of notebook `nb` INPLACE."""
    for ws in nb.worksheets:
        for cell in ws.cells:
            cell.outputs = []
            if strip_prompt and "prompt_number" in cell:
                del cell["prompt_number"]


def stripoutput(inputs, inplace=False, strip_prompt=False):
    """
    Strip output of notebooks.

    Parameters
    ----------
    inputs : list of string
        Path to the notebooks to be processed.
    inplace : bool
        If this is `True`, outputs in the input files will be deleted.
        Default is `False`.

    """
    if not inputs:
        nb = nbformat.read(sys.stdin, 'ipynb')
        clear_outputs(nb, strip_prompt=strip_prompt)
        nbformat.write(nb, sys.stdout, 'ipynb')
        return
    
    for inpath in inputs:
        with file(inpath) as fp:
            nb = nbformat.read(fp, 'ipynb')
        clear_outputs(nb, strip_prompt=strip_prompt)
        if inplace:
            with file(inpath, 'w') as fp:
                nbformat.write(nb, fp, 'ipynb')
        else:
            nbformat.write(nb, sys.stdout, 'ipynb')


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='*', metavar='input',
                        help='Paths to notebook files.')
    parser.add_argument('-i', '--inplace', default=False, action='store_true',
                        help='Overwrite existing notebook when given.')
    parser.add_argument('--strip-prompt', default=False, action='store_true',
                        help='Strip also the prompt numbers')
    args = parser.parse_args()
    stripoutput(**vars(args))


if __name__ == '__main__':
    main()
