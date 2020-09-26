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

from .SipParameterList import SipParameterList

class SipReason( SipParameterList ):

  def __init__( self ):
    super().__init__()
    self.strProtocol = ''
  
  def Parse( self, strText, iStartPos ):
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)
    bParam = False

    while( iPos < iTextLen ):
      if( strText[iPos] == ';' ):
        self.strProtocol = strText[iStartPos:iPos]
        bParam = True
        break
      if( strText[iPos] == ',' ):
        self.strProtocol = strText[iStartPos:iPos]
        break
      iPos += 1
    
    iCurPos = iPos

    if( len(self.strProtocol) == 0 ):
      self.strProtocol = strText[iStartPos:iCurPos]
    
    if( bParam ):
      iPos = super().HeaderListParamParse( strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

      iCount = len(super().clsParamList)

      for i in range( 0, iCount ):
        if( len(super().clsParamList[i].strValue) > 0 and super().clsParamList[i].strValue[0] == '"' ):
          super().clsParamList[i].strValue.replace( '"', '' )

  def __str__( self ):
    return self.strProtocol + super().__str__()

  def Clear( self ):
    self.strProtocol = ''
    super().ClearParam()