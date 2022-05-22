#Simple Sublime plug in that does code alignment based on input from user 
#Copy this to the Users folder of Sublime plugin 
#Then bind this to your system by editing command file. You'll need another plugin: edit-command-pallete for this 
#Then this will appear in your command pallete

import sublime
import sublime_plugin


class ArgumentInputHandler(sublime_plugin.TextInputHandler):
  def placeholder(self):
    return ':'

class AlignCharCommand(sublime_plugin.TextCommand):
  def input(self, args):
    self.key = args                                                 
    return ArgumentInputHandler()                                                 

  def run(self, edit, argument):
    for sel in self.view.sel():
      row, col  = self.view.rowcol(sel.begin())
      buf = self.view.substr(sel)
      buf = self.align(buf, argument, col)
      if buf != '': 
        self.view.replace(edit, sel, buf)
      
  def align(self, buf, patt, offset=0):
    ref_pos = -1
    new_buf = ''
    line_id = 0
    for line in buf.splitlines(True):
      ref_pos = max(line.find(patt), ref_pos)
      if line_id == 0 and ref_pos > 0:
        ref_pos += offset 
      line_id += 1

    #Character not found, return empty buffer
    if ref_pos < 0: 
      return ''

    line_id = 0
    for line in buf.splitlines(True):
      pos = line.find(patt)            
      #Adjust the location on the first line of buffer 
      if line_id == 0 and pos >= 0: 
        col = pos + offset 
      else: 
        col = pos

      if col < ref_pos and col >= 0 :
        spaces   = ' '*(ref_pos - col)
        new_line = line[0:pos] + spaces + line[pos:]
        new_buf += new_line          
      else: 
        new_buf += line 
      line_id += 1

    return new_buf  