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

class SdpTime():

  def __init__( self ):
    self.strStartTime = ''
    self.strStopTime = ''
    self.clsRepeatTimeList = []
  
  def Parse( self, strText ):
    self.Clear()

    iPos = 0
    iStartPos = 0
    iTextLen = len(strText)
    iType = 0
    if( iTextLen == 0 ):
      return -1
    
    while( iPos < iTextLen ):
      if( strText[iPos] == ' ' ):
        self.SetData( strText[iStartPos:iPos], iType )
        iType += 1
        iStartPos = iPos + 1

      iPos += 1
    
    if( iStartPos < iTextLen ):
      self.SetData( strText[iStartPos:], iType )
      iType += 1
    
    if( iType != 2 ):
      return -1

    return iTextLen

  def __str__( self ):
    if( self.Empty() ):
      return ''
    
    strText = self.strStartTime + " " + self.strStopTime + "\r\n"

    for strTime in self.clsRepeatTimeList:
      strText += "r=" + strTime + "\r\n"
    
    return strText
  
  def Clear( self ):
    self.strStartTime = ''
    self.strStopTime = ''
    self.clsRepeatTimeList.clear()
  
  def Empty( self ):
    if( len(self.strStartTime) == 0 or len(self.strStopTime) == 0 ):
      return True
    
    return False
  
  def SetData( self, strText, iType ):
    if( iType == 0 ):
      self.strStartTime = strText
    elif( iType == 1 ):
      self.strStopTime = strText
