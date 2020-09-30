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

class SdpConnection():

  def __init__( self ):
    self.strNetType = ''
    self.strAddrType = ''
    self.strAddr = ''
    self.iMulticastTtl = -1
    self.iMulticastNum = -1
  
  def Parse( self, strText ):
    self.Clear()

    iPos = 0
    iStartPos = 0
    iTextLen = len(strText)
    iType = 0
    if( iTextLen == 0 ):
      return -1
    
    while( iPos < iTextLen ):
      if( strText[iPos] == ' ' or strText[iPos] == '/' ):
        self.SetData( strText[iStartPos:iPos], iType )
        iType += 1
        iStartPos = iPos + 1

      iPos += 1
    
    if( iStartPos < iTextLen ):
      self.SetData( strText[iStartPos:], iType )
    
    return iTextLen
  
  def __str__( self ):
    if( self.Empty() ):
      return ''
    
    strText = self.strNetType + " " + self.strAddrType + " " + self.strAddr

    if( self.iMulticastTtl >= 0 ):
      strText += "/" + str(self.iMulticastTtl)

      if( self.iMulticastNum >= 0 ):
        strText += "/" + str(self.iMulticastNum)
    
    return strText

  def Clear( self ):
    self.strNetType = ''
    self.strAddrType = ''
    self.strAddr = ''
    self.iMulticastTtl = -1
    self.iMulticastNum = -1
  
  def Empty( self ):
    if( len(self.strNetType) == 0 or len(self.strAddrType) == 0 or len(self.strAddr) == 0 ):
      return True
    
    return False

  def SetData( self, strText, iType ):
    if( iType == 0 ):
      self.strNetType = strText
    elif( iType == 1 ):
      self.strAddrType = strText
    elif( iType == 2 ):
      self.strAddr= strText
    elif( iType == 3 ):
      self.iMulticastTtl= int(strText)
    elif( iType == 4 ):
      self.iMulticastNum= int(strText)
