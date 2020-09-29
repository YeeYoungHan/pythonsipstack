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

from .SipParameter import SipParameter

class SipParameterList():

  def __init__( self ):
    self.clsParamList = []

  def HeaderListParamParse( self, strText, iStartPos ):
    iCurPos = iStartPos
    iTextLen = len(strText)

    while( iCurPos < iTextLen ):
      if( strText[iCurPos] == ' ' or strText[iCurPos] == '\t' or strText[iCurPos] == ';' ):
        iCurPos += 1
        continue
      elif( strText[iCurPos] == ',' ):
        break

      iPos = self.ParamParse( strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos
    
    return iCurPos

  def ParamParse( self, strText, iStartPos ):
    clsParam = SipParameter()
  
    iPos = clsParam.Parse( strText, iStartPos )
    if( iPos == -1 ):
      return -1
    
    self.clsParamList.append( clsParam )

    return iPos

  def InsertParam( self, strName, strValue ):
    clsParam = SipParameter()

    clsParam.strName = strName
    clsParam.strValue = strValue

    self.clsParamList.append( clsParam )

  def SelectParam( self, strName ):

    for clsParam in self.clsParamList:
      if( clsParam.strName.lower() == strName ):
        return clsParam.strValue
    
    return ''

  def UpdateParam( self, strName, strValue ):

    for clsParam in self.clsParamList:
      if( clsParam.strName.lower() == strName ):
        clsParam.strValue = strValue
        return True
    
    return False

  def ClearParam( self ):
    self.clsParamList.clear()

  def __str__( self ):
    strText = ''

    for clsParam in self.clsParamList:
      strText += ';' + str( clsParam )

    return strText
