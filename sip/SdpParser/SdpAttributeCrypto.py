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

class SdpAttributeCrypto():

  def __init__( self ):
    self.strTag = ''
    self.strCryptoSuite = ''
    self.strKey = ''
    self.strText = ''
  
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
        if( iType == 0 ):
          self.strTag = strText[iStartPos:iPos]
        elif( iType == 1 ):
          self.strCryptoSuite = strText[iStartPos:iPos]
        
        iStartPos = iPos + 1
        iType += 1
      elif( iType == 2 ):
        if( strText[iPos] == ':' ):
          iStartPos = iPos + 1
        elif( strText[iPos] == '|' ):
          self.strKey = strText[iStartPos:iPos]
          iStartPos = iPos + 1
          self.strText = strText[iStartPos:]
      
      iPos += 1
    
    if( iType == 2 and len(self.strKey) == 0 ):
      self.strKey = strText[iStartPos:]
    
    return iTextLen


  def __str__( self ):
    if( self.Empty() ):
      return ''
    
    strText = self.strTag + " " + self.strCryptoSuite + " inline:" + self.strKey
    if( len(self.strText) > 0 ):
      strText += "|" + self.strText
    
    return strText
  
  def Clear( self ):
    self.strTag = ''
    self.strCryptoSuite = ''
    self.strKey = ''
    self.strText = ''

  def Empty( self ):
    if( len(self.strTag) == 0 or len(self.strCryptoSuite) == 0 or len(self.strKey) == 0 ):
      return True
    
    return False