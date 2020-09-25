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
from .SipUtility import SipIpv6Print

class SipVia( SipParameterList ):

  def __init__( self ):
    super().__init__()
    self.strProtocolName = ''
    self.strProtocolVersion = ''
    self.strTransport = ''
    self.strHost = ''
    self.iPort = -1
  
  def Parse( self, strText, iStartPos ):
    self.Clear()

    iCurPos = iStartPos
    iPos = self.ParseSentProtocol( strText, iCurPos )
    if( iPos == -1 ):
      return -1
    iCurPos = iPos
    
    iPos = self.ParseSentBy( strText, iCurPos )
    if( iPos == -1 ):
      return -1
    iCurPos = iPos

    iPos = super().HeaderListParamParse( strText, iCurPos )
    if( iPos == -1 ):
      return -1
    iCurPos = iPos

    return iCurPos

  def __str__( self ):
    strVia = self.strProtocolName + "/" + self.strProtocolVersion + "/" + self.strTransport + " "

    strVia += SipIpv6Print( self.strHost )

    if( self.iPort > 0 ):
      strVia += ":" + str( self.iPort )

    strVia += super().__str__()

    return strVia

  def Clear( self ):
    self.strProtocolName = ''
    self.strProtocolVersion = ''
    self.strTransport = ''
    self.strHost = ''
    self.iPort = -1

    super().ClearParam()

  def ParseSentProtocol( self, strText, iStartPos ):
    iPos = iStartPos
    iType = 0
    iTextLen = len(strText)

    while( iPos < iTextLen ):
      if( strText[iPos] == '/' ):
        if( iType == 0 ):
          self.strProtocolName = strText[iStartPos:iPos]
          iPrevPos = iPos + 1
        elif( iType == 1 ):
          self.strProtocolVersion = strText[iPrevPos:iPos]
          iPrevPos = iPos + 1
        else:
          return -1
        iType += 1
      elif( strText[iPos] == ' ' ):
        if( iType == 2 ):
          self.strTransport = strText[iPrevPos:iPos]
          return iPos + 1
        else:
          return -1
      iPos += 1
    
    return -1

  def ParseSentBy( self, strText, iStartPos ):
    iPortPos = -1
    iLen = len(strText)

    if( strText[iStartPos] == '[' ):
      bIpFound = False

      iPos = iStartPos + 1
      while( iPos < iLen ):
        if( bIpFound == False ):
          if( strText[iPos] == ']' ):
            self.strHost = strText[iStartPos+1:iPos]
            bIpFound = True
        elif( strText[iPos] == ':' ):
          iPortPos = iPos + 1
        elif( strText[iPos] == ';' or strText[iPos] == '?' ):
          iEndPos = iPos
          break
        iPos += 1

      if( bIpFound == False ):
        return -1

      if( iPortPos != -1 and iPortPos < iPos ):
        self.iPort = int( strText[iPortPos:iPos] )

      return iPos
      
    else:

      iPos = iStartPos
      while( iPos < iLen ):
        if( strText[iPos] == ':' ):
          self.strHost = strText[iStartPos:iPos]
          iPortPos = iPos + 1
        elif( strText[iPos] == ';' or strText[iPos] == '?' ):
          break
        iPos += 1          

      if( iPortPos == -1 ):
        if( iPos > iStartPos ):
          self.strHost = strText[iStartPos:iPos]
          return iPos
      else:
        if( iPortPos < iPos ):
          self.iPort = int( strText[iPortPos:iPos] )
        return iPos
    
    return -1


