''' 
Copyright (C) 2020 Yee Young Han <websearch@naver.com> (http://blog.naver.com/websearch)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

class SipCSeq():

  def __init__( self ):
    self.iDigit = -1
    self.strMethod = ''
  
  def Parse( self, strText, iStartPos ):
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)

    while( iPos < iTextLen ):
      if( self.iDigit == -1 ):
        if( strText[iPos] == ' ' ):
          strDigit = strText[iStartPos:iPos]
          self.iDigit = int( strDigit )
      elif( strText[iPos] == ' ' or strText[iPos] == '\t' ):
        iPos += 1
        continue
      else:
        self.strMethod = strText[iPos:]
        break

      iPos += 1

  def __str__( self ):
    return str(self.iDigit) + " " + self.strMethod
  
  def Clear( self ):
    self.iDigit = -1
    self.strMethod = ''
  
  def Empty( self ):
    if( self.iDigit == -1 ):
      return True
    
    return False

  def Set( self, iDigit, strMethod ):
    self.iDigit = iDigit
    self.strMethod = strMethod