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

from difflib import unified_diff
from os import path
from sys import argv

comment = '//'
comment_begin = '/*'
comment_continue = '*'
comment_continue_prefix = ' '
comment_end = '*/'
indent = '    '
indent_begins = ['{', '[']
indent_ends = ['}', ']']
line_separator = '\n'
ignore = ';'


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


_test_multiple_comments_on_one_line = """/** this */
package multiple_comments_on_one_line 
{
  /**/ import flash.display.MovieClip /**/
  public class
  {
      /**/ private var level:int /**/
      private function getLevel():int   
      {
            var object:Object = {
            };
            var array:Array = [
            ]
            ;
            object = {a: 1};
            var text:String = "{" + a + "}";
        return level;
      }
  }
}
"""

_test_multiple_comments_on_one_line_expected = """/** this */
package multiple_comments_on_one_line
{
    /**/ import flash.display.MovieClip /**/
    public class
    {
        /**/ private var level:int /**/
        private function getLevel():int
        {
            var object:Object = {};
            var array:Array = [];
            object = {a: 1};
            var text:String = "{" + a + "}";
            return level;
        }
    }
}
"""


_test_indented_variables = """
/** this */
package indented_variables
{
  /**/ import flash.display.MovieClip /**/
  public class
  {
     public var objects:Object = {}

        public var empties:Array = [];

      public var oneline:Object = {a: 1, b: 2}
      /**
      * Comment
      */
      public var items:Object = {1: 10,
      2: 20};
        // Comment
      public var levels:Array = [
        1,
        2];
     public var level:int = 0;
     public var text:String = "{" + level + "}";
  }
}
"""

_test_indented_variables_expected = """
/** this */
package indented_variables
{
    /**/ import flash.display.MovieClip /**/
    public class
    {
        public var objects:Object = {}
        
        public var empties:Array = [];
        
        public var oneline:Object = {a: 1, b: 2}
        /**
         * Comment
         */
        public var items:Object = {1: 10,
            2: 20};
        // Comment
        public var levels:Array = [
            1,
            2];
        public var level:int = 0;
        public var text:String = "{" + level + "}";
    }
}
"""


def format_difference(expected, got):
    if got is None:
        got = ''
    difference_lines = unified_diff(
        expected.splitlines(),
        got.splitlines()
    )
    difference = '\n'.join(difference_lines)
    return difference


def newline_after_braces(text):
    indents = [indent_begins[0], indent_ends[0]]
    for indent in indents:
        trimmed = indent + line_separator
        redundant = indent + line_separator + line_separator
        text = text.replace(indent, trimmed)
        text = text.replace(redundant, trimmed)
    return text


def format_text(text):
    """
    >>> got = format_text(_test_text) 
    >>> print format_difference(_test_text_expected, got)
    <BLANKLINE>

    Multiple comments on one line.
    >>> got = format_text(_test_multiple_comments_on_one_line) 
    >>> print format_difference(_test_multiple_comments_on_one_line_expected, got)
    <BLANKLINE>

    Indented variables.
    >>> got = format_text(_test_indented_variables) 
    >>> print format_difference(_test_indented_variables_expected, got)
    <BLANKLINE>
    """
    text = _merge_empty_lines(text)
    lines = text.splitlines()
    is_comment = False
    indent_count = 0
    formatted_lines = []
    for line in lines:
        active = line.replace(ignore, '').split(comment)[0].strip()
        active = active.split(comment_begin)[0].strip()
        is_dedent = False
        if not is_comment:
            for indent_end in indent_ends:
                if active.startswith(indent_end):
                    indent_count -= 1
                    is_dedent = True
                    break
        indent_count = max(0, indent_count)
        prefix = indent * indent_count
        if is_comment and active.startswith(comment_continue.strip()):
            prefix += ' '
        formatted = prefix + line.strip()
        formatted_lines.append(formatted)
        is_indent = False
        if not is_comment:
            for indent_begin in indent_begins:
                if indent_begin in active:
                    indent_count += active.count(indent_begin)
                    is_indent = True
            if not is_dedent:
                for indent_end in indent_ends:
                    if indent_end in active:
                        indent_count -= active.count(indent_end)
        if comment_begin in line:
            is_comment = True
        comments = line.split(comment_begin)
        for a_comment in comments:
            if comment_end in a_comment:
                is_comment = False
    text = line_separator.join(formatted_lines)
    return text


def _merge_empty_lines(text):
    text = '\n'.join([line.strip() for line in text.splitlines()])
    for begin, end in zip(indent_begins, indent_ends):
        text = text.replace(begin + '\n' + end, begin + end)
    text = text.replace('\n' + ignore, ignore)
    return text


def format(text):
    """
    >>> got = format(_test_multiple_comments_on_one_line) 
    >>> print format_difference(_test_multiple_comments_on_one_line_expected, got)
    <BLANKLINE>
    """
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # text = newline_after_braces(text)
    text = format_text(text)
    # text = newline_after_braces(text)
    text = text.strip()
    return text


def realpath(relative_path):
    script_directory = path.dirname(__file__)
    absolute_path = path.join(script_directory, relative_path)
    return absolute_path


def format_files(paths, is_dry_run = False):
    """
    Overwrite file in-place.  Normalizes line-endings.
    >>> path = realpath('pretty_print_code_test.as')
    >>> expected = open(path).read()
    >>> open(path, 'w').write('    ' + expected + '    ')
    >>> format_files([path])
    >>> got = open(path).read()
    >>> print format_difference(expected, got)
    <BLANKLINE>
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
    if len(argv) < 2:
        print __doc__
    else:
        paths = argv[1:]
        format_files(paths)
    doctest.testmod()
