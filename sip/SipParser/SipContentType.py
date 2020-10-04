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

class SipContentType(SipParameterList):

  def __init__( self ):
    super().__init__()
    self.strType = ''
    self.strSubType = ''
  
  def Parse( self, strText, iStartPos ):
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)
    iSubTypePos = -1
    iParamPos = -1

    while( iPos < iTextLen ):
      if( strText[iPos] == '/' ):
        self.strType = strText[iStartPos:iPos]
        iSubTypePos = iPos + 1
      elif( iSubTypePos != -1 ):
        if( strText[iPos] == ';' or strText[iPos] == ',' ):
          self.strSubType = strText[iSubTypePos:iPos]
          iParamPos = iPos + 1
          break
      elif( strText[iPos] == ',' ):
        break
      
      iPos += 1
    
    if( len(self.strType) == 0 ):
      self.strType = strText[iStartPos:]
    elif( iSubTypePos != -1 and len(self.strSubType) == 0 ):
      self.strSubType = strText[iSubTypePos:]
    
    if( iParamPos != -1 ):
      super().HeaderListParamParse( strText, iParamPos )


  def __str__( self ):
    return self.strType + "/" + self.strSubType + super().__str__()

  def __eq__( self, clsContentType ):
    if( self.strType == clsContentType.strType and self.strSubType == clsContentType.strSubType ):
      return True
    
    return False
  
  def IsEqual( self, strType, strSubType ):
    if( self.strType == strType and self.strSubType == strSubType ):
      return True
    
    return False

  def Clear( self ):
    self.strType = ''
    self.strSubType = ''
    super().ClearParam()

  def Empty( self ):
    if( len(self.strType) == 0 or len(self.strSubType) == 0 ):
      return True

    return False
  
  def Set( self, strType, strSubType ):
    self.strType = strType
    self.strSubType = strSubType
