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

from .SipUri import SipUri
from .SipFrom import SipFrom
from .SipCSeq import SipCSeq
from .SipCallId import SipCallId
from .SipContentType import SipContentType
from .SipTransport import SipTransport
from .SipHeader import SipHeader
from .SipVia import ParseSipVia
from .SipFrom import ParseSipFrom
from .SipCredential import ParseSipCredential
from .SipChallenge import ParseSipChallenge
from .SipStatusCode import GetReasonPhrase

class SipMessage():

  def __init__( self ):
    self.strSipMethod = ''
    self.clsReqUri = SipUri.SipUri()
    self.strSipVersion = ''
    self.iStatusCode = -1
    self.strReasonPhrase = ''
    self.clsFrom = SipFrom.SipFrom()
    self.clsTo = SipFrom.SipFrom()
    self.clsViaList = []
    self.clsContactList = []
    self.clsRecordRouteList = []
    self.clsRouteList = []
    self.clsAuthorizationList = []
    self.clsWwwAuthenticateList = []
    self.clsProxyAuthorizationList = []
    self.clsProxyAuthenticateList = []
    self.clsHeaderList = []
    self.clsCSeq = SipCSeq.SipCSeq()
    self.clsCallId = SipCallId.SipCallId()
    self.clsContentType = SipContentType.SipContentType()
    self.iContentLength = 0
    self.iExpires = -1
    self.iMaxForwards = -1
    self.strUserAgent = ''
    self.strBody = ''
    self.strPacket = ''
    self.eTransport = SipTransport.E_SIP_UDP
    self.strClientIp = ''
    self.iClientPort = 0


  def Parse( self, strText ):

    iTextLen = len(strText)

    if( iTextLen <= 4 ):
      return -1
    
    if( strText[0:4] == "SIP/" ):
      iCurPos = ParseStatusLine( strText )
    else:
      iCurPos = ParseRequestLine( strText )
    
    if( iCurPos == -1 ):
      return -1
    
    clsHeader = SipHeader.SipHeader()

    while( iCurPos < iTextLen ):
      iPos = clsHeader.Parse( strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

      if( clsHeader.strName == "Via" or clsHeader.strName == "v" ):
        ParseSipVia( self.clsViaList, clsHeader.strValue )
      elif( clsHeader.strName == "Max-Forwards" ):
        self.iMaxForwards = int(clsHeader.strValue)
      elif( clsHeader.strName == "From" or clsHeader.strName == "f" ):
        self.clsFrom.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "To" or clsHeader.strName == "t" ):
        self.clsTo.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "CSeq" ):
        self.clsCSeq.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "Call-ID" or clsHeader.strName == "i" ):
        self.clsCallId.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "Contact" or clsHeader.strName == "m" ):
        ParseSipFrom( self.clsContactList, clsHeader.strValue )
      elif( clsHeader.strName == "Record-Route" ):
        ParseSipFrom( self.clsRecordRouteList, clsHeader.strValue )
      elif( clsHeader.strName == "Route" ):
        ParseSipFrom( self.clsRouteList, clsHeader.strValue )
      elif( clsHeader.strName == "Authorization" ):
        ParseSipCredential( self.clsAuthorizationList, clsHeader.strValue )
      elif( clsHeader.strName == "WWW-Authenticate" ):
        ParseSipChallenge( self.clsWwwAuthenticateList, clsHeader.strValue )
      elif( clsHeader.strName == "Proxy-Authorization" ):
        ParseSipCredential( self.clsProxyAuthorizationList, clsHeader.strValue )
      elif( clsHeader.strName == "Proxy-Authenticate" ):
        ParseSipChallenge( self.clsProxyAuthenticateList, clsHeader.strValue )
      elif( clsHeader.strName == "Content-Type" or clsHeader.strName == "c" ):
        self.clsContentType.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "Content-Length" or clsHeader.strName == "l" ):
        self.iContentLength = int(clsHeader.strValue)
      elif( clsHeader.strName == "Expires" ):
        self.iExpires = int(clsHeader.strValue)
      elif( clsHeader.strName == "User-Agent" ):
        self.strUserAgent = clsHeader.strValue
      else:
        self.clsHeaderList.append( clsHeader )
    
    if( self.iContentLength > 0 ):
      if( self.iContentLength > ( iTextLen - iCurPos ) ):
        return -1
      
      self.strBody = strText[iCurPos:iCurPos+self.iContentLength]
      return iCurPos + self.iContentLength
    
    return iCurPos

  def __str__( self ):

    if( len(self.strSipVersion) == 0 ):
      self.strSipVersion = "SIP/2.0"
    
    if( self.iStatusCode > 0 ):
      if( len(self.strReasonPhrase) == 0 ):
        self.strReasonPhrase = GetReasonPhrase( self.iStatusCode )
      
      strText = self.strSipVersion + " " + str(self.iStatusCode) + " " + self.strReasonPhrase + "\r\n"
    else:
      strText = self.strSipMethod + " " + self.clsReqUri + " " + self.strSipVersion + "\r\n"

    strText += ListToString( self.clsViaList, "Via" )
    strText += ListToString( self.clsRecordRouteList, "Record-Route" )
    strText += ListToString( self.clsRouteList, "Route" )
        
    if( self.iMaxForwards >= 0 ):
      strText += "Max-Forwards: " + str(self.iMaxForwards) + "\r\n"
    
    strText += "From: " + self.clsFrom + "\r\n"
    strText += "To: " + self.clsTo + "\r\n"
    strText += "Call-ID: " + self.clsCallId + "\r\n"
    strText += "CSeq: " + self.clsCSeq + "\r\n"

    strText += ListToString( self.clsContactList, "Contact" )
    strText += ListToString( self.clsAuthorizationList, "Authorization" )
    strText += ListToString( self.clsWwwAuthenticateList, "WWW-Authenticate" )
    strText += ListToString( self.clsProxyAuthorizationList, "Proxy-Authorization" )
    strText += ListToString( self.clsProxyAuthenticateList, "Proxy-Authenticate" )

    strText += "Content-Type: " + self.clsContentType + "\r\n"
    strText += "Content-Length: " + str(self.iContentLength) + "\r\n"

    if( self.iExpires >= 0 ):
      strText += "Expires: " + str(self.iExpires) + "\r\n"

    if( len(self.strUserAgent) > 0 ):
      strText += "User-Agent: " + self.strUserAgent + "\r\n"
    
    iCount = len(self.clsHeaderList)
    for i in range( 0, iCount ):
      strText += self.clsHeaderList[i].strName + ": " + self.clsHeaderList[i].strValue + "\r\n"
    
    strText += "\r\n"

    if( self.iContentLength > 0 ):
      strText += self.strBody
    
    return strText
  
  def IsRequest( self ):
    if( len(self.strSipMethod) == 0 ):
      return False
    
    return True
  
  def IsMethod( self, strMethod ):
    if( len(self.strSipMethod) > 0 ):
      if( self.strSipMethod == strMethod ):
        return True
    else:
      if( self.clsCSeq.strMethod == strMethod ):
        return True
    
    return False

  def IsEqualCallId( self, clsMessage ):
    return self.clsCallId == clsMessage.clsCallId

  def ParseStatusLine( self, strText ):
    iTextLen = len(strText)
    iPos = 0
    iType = 0
    iStartPos = -1

    while( iPos < iTextLen ):
      if( iType != 2 ):
        if( strText[iPos] == ' ' ):
          if( iType == 0 ):
            self.strSipVersion = strText[0:iPos]
          elif( iType == 1 ):
            self.iStatusCode = int( strText[iStartPos:iPos] )

          iStartPos = iPos + 1
          iType += 1
      else:
        if( strText[iPos] == '\r' ):
          if( iPos + 1 >= iTextLen or strText[iPos+1] != '\n' ):
            return -1
          
          self.strReasonPhrase = strText[iStartPos:iPos]
          return iPos + 2
    
    return -1


  def ParseRequestLine( self, strText ):
    iTextLen = len(strText)
    iPos = 0
    iType = 0
    iStartPos = -1

    while( iPos < iTextLen ):
      if( iType != 2 ):
        if( strText[iPos] == ' ' ):
          if( iType == 0 ):
            self.strSipMethod = strText[0:iPos]
          elif( iType == 1 ):
            strUri = strText[iStartPos:iPos]
            if( self.clsReqUri.Parse( strUri, 0 ) == -1 ):
              return -1

          iStartPos = iPos + 1
          iType += 1
      else:
        if( strText[iPos] == '\r' ):
          if( iPos + 1 >= iTextLen or strText[iPos+1] != '\n' ):
            return -1
          
          self.strSipVersion = strText[iStartPos:iPos]
          return iPos + 2
    
    return -1
  
  def ListToString( self, clsList, strName ):
    iCount = len(self.clsList)
    strText = ''
    for i in range( 0, iCount ):
      strText += strName + ": " + self.clsList[i] + "\r\n"
    
    return strText

