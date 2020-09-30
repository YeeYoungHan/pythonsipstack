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

class SdpAttribute():

  def __init__( self ):
    self.strName = ''
    self.strValue = ''
  
  def Parse( self, strText ):
    self.Clear()

    iPos = 0
    iTextLen = len(strText)
    if( iTextLen == 0 ):
      return -1

    while( iPos < iTextLen ):
      if( strText[iPos] == ':' ):
        self.strName = strText[:iPos]
        self.strValue = strText[iPos+1:iTextLen]
        break
      iPos += 1
    
    if( len(self.strName) == 0 ):
      self.strName = strText
    
    return iTextLen
  
  def __str__( self ):
    if( self.Empty() ):
      return ''
    
    if( len(self.strValue) == 0 ):
      return self.strName

    return self.strName + ":" + self.strValue

  def Clear( self ):
    self.strType = ''
    self.strBandWidth = ''

  def Empty( self ):
    if( len(self.strName) == 0 ):
      return True
    
    return False
