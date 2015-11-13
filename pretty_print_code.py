#!/usr/bin/env python 

""" 
Indent after each non-whitespace-line-ending {
dedent after each non-whitespace-line-beginning }
Also normalizes whitespace to Unix line-ending
And strip trailing whitespace.

Usage:
    python pretty_print_code.py [filename...]
    Beware:  files are reformatted in place.

Characters to replace are at the top of the program.
Running this program also unit tests a sample.
""" 


import os
import sys


comment = '//'
comment_begin = '/*'
comment_continue = '*'
comment_continue_prefix = ' '
comment_end = '*/'
indent = '    '
indent_begin = '{'
indent_end = '}'
line_separator = '\n'


_test_text = """
    { 
      var a;
    }


function f() {  // comment
    {
       var b = 0;
    }
  var d = {k: 1}
    /*
     *
    {
  something
     */
    // {
    // }
    /*
    }
     */
}    
}
var after;
/* not supported */  {
var here;
"""


_test_text_expected = """
{
    var a;
}


function f() {  // comment
    {
        var b = 0;
    }
    var d = {k: 1}
    /*
     *
    {
    something
     */
    // {
    // }
    /*
    }
     */
}
}
var after;
/* not supported */  {
var here;
"""


_test_multiple_comments_on_one_line = """
/** this */
multiple_comments_on_one_line 
{
  /**/ import flash.display.MovieClip /**/
  public class
  {
      /**/ private var level:int /**/
      private function getLevel():int   
      {
        return level;
      }
  }
}
"""

_test_multiple_comments_on_one_line_expected = """
/** this */
multiple_comments_on_one_line
{
    /**/ import flash.display.MovieClip /**/
    public class
    {
        /**/ private var level:int /**/
        private function getLevel():int
        {
            return level;
        }
    }
}
"""


def _test_diff(expected, got):
    gots = got.splitlines()
    expecteds = expected.splitlines()
    for expected, got in zip(expecteds, gots):
        if expected != got:
            print "- %r" % expected
            print "+ %r" % got


def format_text(text):
    """
    >>> got = format_text(_test_text) 
    >>> _test_diff(_test_text_expected, got)

    Multiple comments on one line.
    >>> got = format_text(_test_multiple_comments_on_one_line) 
    >>> _test_diff(_test_multiple_comments_on_one_line_expected, got)
    """
    lines = text.splitlines()
    is_comment = False
    indent_count = 0
    formatted_lines = []
    for line in lines:
        active = line.split(comment)[0].strip()
        active = active.split(comment_begin)[0].strip()
        if active.startswith(indent_end) and not is_comment:
            indent_count -= 1
        indent_count = max(0, indent_count)
        prefix = indent * indent_count
        if is_comment and active.startswith(comment_continue.strip()):
            prefix += ' '
        formatted = prefix + line.strip()
        formatted_lines.append(formatted)
        if active.endswith(indent_begin) and not is_comment:
            indent_count += 1
        if comment_begin in line:
            is_comment = True
        comments = line.split(comment_begin)
        for a_comment in comments:
            if comment_end in a_comment:
                is_comment = False
    return line_separator.join(formatted_lines)


def realpath(relative_path):
    script_directory = os.path.dirname(__file__)
    absolute_path = os.path.join(script_directory, relative_path)
    return absolute_path


def format_files(paths, is_dry_run = False):
    """
    Overwrite file in-place.  Normalizes line-endings.
    >>> path = realpath('pretty_print_code_test.as')
    >>> expected = open(path).read()
    >>> format_files([path])
    >>> got = open(path).read()
    >>> if expected != got:
    ...     _test_diff(expected, got)
    """
    for path in paths:
        file = open(path, 'rU')
        text = file.read()
        text = format_text(text)
	if is_dry_run:
        	print text
	else:
		file = open(path, 'wb')
		file.write(text)


if __name__ == "__main__": 
    import doctest
    if len(sys.argv) < 2:
        print __doc__
    else:
        paths = sys.argv[1:]
        format_files(paths)
    doctest.testmod()
