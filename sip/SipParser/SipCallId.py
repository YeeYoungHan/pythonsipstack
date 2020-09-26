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

class SipCallId():

  def __init__( self ):
    self.strName = ''
    self.strHost = ''

  def Parse( self, strText, iStartPos ):
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)

    while( iPos < iTextLen ):
      if( strText[iPos] == '@' ):
        self.strName = strText[iStartPos:iPos]
        self.strHost = strText[iPos+1:]
        break
      iPos += 1

    if( len(self.strName) == 0 ):
      self.strName = strText[iStartPos:]

  def __str__( self ):
    if( len(self.strHost) == 0 ):
      return self.strName
    
    return self.strName + "@" + self.strHost

  def __eq__( self, clsCallId ):
    if( self.strName == clsCallId.strName and self.strHost == clsCallId.strHost ):
      return True
    
    return False

  def Clear( self ):
    self.strName = ''
    self.strHost = ''