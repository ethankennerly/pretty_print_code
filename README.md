pretty\_print\_code
=================

Indent after each non-whitespace-line-ending "{".
Dedent after each non-whitespace-line-beginning "}".
Also normalizes whitespace to Unix line-ending 
and strips trailing whitespace.

Usage:
    python pretty_print_code.py [filename...]

Beware:  files are reformatted in-place.
Characters to replace are at the top of the program.
Running this program also unit tests a sample.

Not supported
-------------

One line if/else statements such as:

    if (true)
        a = 1;

