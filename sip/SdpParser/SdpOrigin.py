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

class SdpOrigin():

  def __init__( self ):
    self.strUserName = ''
    self.strSessId = ''
    self.strSessVersion = ''
    self.strNetType = ''
    self.strAddrType = ''
    self.strUnicastAddress = ''
  
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
    
    if( iType != 6 ):
      return -1
    
    return iTextLen
  
  def __str__( self ):
    if( self.Empty() ):
      return ''
    
    return self.strUserName + " " + self.strSessId + " " + self.strSessVersion + " " + self.strNetType + " " + self.strAddrType + " " + self.strUnicastAddress
  
  def Clear( self ):
    self.strUserName = ''
    self.strSessId = ''
    self.strSessVersion = ''
    self.strNetType = ''
    self.strAddrType = ''
    self.strUnicastAddress = ''
  
  def Empty( self ):
    if( len(self.strUserName) == 0 or len(self.strSessId) == 0 or len(self.strSessVersion) == 0 or len(self.strNetType) == 0 or len(self.strAddrType) == 0 or len(self.strUnicastAddress) == 0 ):
      return True
    
    return False
  
  def SetData( self, strText, iType ):
    if( iType == 0 ):
      self.strUserName = strText
    elif( iType == 1 ):
      self.strSessId = strText
    elif( iType == 2 ):
      self.strSessVersion = strText
    elif( iType == 3 ):
      self.strNetType = strText
    elif( iType == 4 ):
      self.strAddrType = strText
    elif( iType == 5 ):
      self.strUnicastAddress = strText