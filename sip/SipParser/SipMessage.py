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

from copy import copy
from .SipUri import SipUri
from .SipFrom import SipFrom, ParseSipFrom
from .SipCSeq import SipCSeq
from .SipCallId import SipCallId
from .SipContentType import SipContentType
from .SipTransport import SipTransport, SipGetTransport, SipGetProtocol
from .SipHeader import SipHeader
from .SipVia import SipVia, ParseSipVia
from .SipCredential import ParseSipCredential
from .SipChallenge import ParseSipChallenge
from .SipStatusCode import SipStatusCode, GetReasonPhrase
from .SipUtility import SipMakeBranch

class SipMessage():

  def __init__( self ):
    self.strSipMethod = ''
    self.clsReqUri = SipUri()
    self.strSipVersion = ''
    self.iStatusCode = -1
    self.strReasonPhrase = ''
    self.clsFrom = SipFrom()
    self.clsTo = SipFrom()
    self.clsViaList = []
    self.clsContactList = []
    self.clsRecordRouteList = []
    self.clsRouteList = []
    self.clsAuthorizationList = []
    self.clsWwwAuthenticateList = []
    self.clsProxyAuthorizationList = []
    self.clsProxyAuthenticateList = []
    self.clsHeaderList = []
    self.clsCSeq = SipCSeq()
    self.clsCallId = SipCallId()
    self.clsContentType = SipContentType()
    self.iContentLength = 0
    self.iExpires = -1
    self.iMaxForwards = -1
    self.strUserAgent = ''
    self.strBody = ''
    self.strPacket = ''
    self.eTransport = SipTransport.UDP
    self.strClientIp = ''
    self.iClientPort = 0


  def Parse( self, strText ):

    iTextLen = len(strText)

    if( iTextLen <= 4 ):
      return -1
    
    if( strText[0:4] == "SIP/" ):
      iCurPos = self.ParseStatusLine( strText )
    else:
      iCurPos = self.ParseRequestLine( strText )
    
    if( iCurPos == -1 ):
      return -1
    
    clsHeader = SipHeader()

    while( iCurPos < iTextLen ):
      iPos = clsHeader.Parse( strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

      if( len(clsHeader.strName) == 0 ):
        break

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
        self.clsHeaderList.append( copy(clsHeader) )
    
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
      strText = self.strSipMethod + " " + str(self.clsReqUri) + " " + self.strSipVersion + "\r\n"

    strText += self.ListToString( self.clsViaList, "Via" )
    strText += self.ListToString( self.clsRecordRouteList, "Record-Route" )
    strText += self.ListToString( self.clsRouteList, "Route" )
        
    if( self.iMaxForwards >= 0 ):
      strText += "Max-Forwards: " + str(self.iMaxForwards) + "\r\n"
    
    strText += "From: " + str(self.clsFrom) + "\r\n"
    strText += "To: " + str(self.clsTo) + "\r\n"

    if( self.clsCallId.Empty() == False ):
      strText += "Call-ID: " + str(self.clsCallId) + "\r\n"
    
    if( self.clsCSeq.Empty() == False ):
      strText += "CSeq: " + str(self.clsCSeq) + "\r\n"

    strText += self.ListToString( self.clsContactList, "Contact" )
    strText += self.ListToString( self.clsAuthorizationList, "Authorization" )
    strText += self.ListToString( self.clsWwwAuthenticateList, "WWW-Authenticate" )
    strText += self.ListToString( self.clsProxyAuthorizationList, "Proxy-Authorization" )
    strText += self.ListToString( self.clsProxyAuthenticateList, "Proxy-Authenticate" )

    if( self.clsContentType.Empty() == False ):
      strText += "Content-Type: " + str(self.clsContentType) + "\r\n"
      
    strText += "Content-Length: " + str(self.iContentLength) + "\r\n"

    if( self.iExpires >= 0 ):
      strText += "Expires: " + str(self.iExpires) + "\r\n"

    if( len(self.strUserAgent) > 0 ):
      strText += "User-Agent: " + self.strUserAgent + "\r\n"
    
    for clsHeader in self.clsHeaderList:
      strText += clsHeader.strName + ": " + clsHeader.strValue + "\r\n"
    
    strText += "\r\n"

    if( self.iContentLength > 0 ):
      strText += self.strBody
    
    return strText
  
  def MakePacket( self ):
    if( len(self.strPacket) == 0 ):
      self.strPacket = str(self)
  
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

  def IsEqualCallIdSeq( self, clsMessage ):
    if( self.clsCallId == clsMessage.clsCallId and self.clsCSeq.iDigit == clsMessage.clsCSeq.iDigit ):
      return True
    
    return False

  def GetCallId( self ):
    return str(self.clsCallId)

  def AddIpPortToTopVia( self, strIp, iPort, eTransport ):
    if( len(self.clsViaList) == 0 ):
      return

    self.clsViaList[0].AddIpPort( strIp, iPort, eTransport )

  def AddVia( self, strIp, iPort, strBranch, eTransport ):
    clsVia = SipVia.SipVia()

    clsVia.strProtocolName = "SIP"
    clsVia.strProtocolVersion = "2.0"
    clsVia.strTransport = SipGetTransport( eTransport )
    clsVia.strHost = strIp
    clsVia.iPort = iPort
    clsVia.InsertParam( "rport", "" )

    if( len(strBranch) == 0 ):
      strBranch = SipMakeBranch()
    
    clsVia.InsertParam( "branch", strBranch )

    self.clsViaList.append( clsVia )
  
  def AddRoute( self, strIp, iPort, eTransport ):
    clsFrom = SipFrom.SipFrom()

    clsFrom.clsUri.m_strProtocol = SipGetProtocol( eTransport )
    clsFrom.clsUri.m_strHost = strIp
    clsFrom.clsUri.m_iPort = iPort

    clsFrom.clsUri.InsertParam( "lr", "" )
    clsFrom.clsUri.InsertTransport( eTransport )

    self.clsRouteList.insert( 0, clsFrom )

  def AddRecordRoute( self, strIp, iPort, eTransport ):
    clsFrom = SipFrom.SipFrom()

    clsFrom.clsUri.m_strProtocol = SipGetProtocol( eTransport )
    clsFrom.clsUri.m_strHost = strIp
    clsFrom.clsUri.m_iPort = iPort

    clsFrom.clsUri.InsertParam( "lr", "" )
    clsFrom.clsUri.InsertTransport( eTransport )

    self.clsRecordRouteList.insert( 0, clsFrom )

  def AddHeader( self, strName, strValue ):
    clsHeader = SipHeader.SipHeader()

    clsHeader.strName = strName
    clsHeader.strValue = strValue

    self.clsHeaderList.append( clsHeader )

  def CreateResponse( self, iStatusCode, strToTag ):
    clsResponse = SipMessage()

    clsResponse.iStatusCode = iStatusCode
    clsResponse.clsTo = self.clsTo
    clsResponse.clsFrom = self.clsFrom
    clsResponse.clsViaList = self.clsViaList
    clsResponse.clsCallId = self.clsCallId
    clsResponse.clsCSeq = self.clsCSeq
    clsResponse.eTransport = self.eTransport

    if( iStatusCode != SipStatusCode.SIP_TRYING ):
      clsResponse.clsRecordRouteList = self.clsRecordRouteList

    if( len(strToTag) > 0 ):
      clsResponse.clsTo.InsertParam( "tag", strToTag )
    
    return clsResponse
  
  def CreateResponseWithToTag( self, iStatusCode ):
    clsResponse = SipMessage()

    clsResponse.iStatusCode = iStatusCode
    clsResponse.clsTo = self.clsTo
    clsResponse.clsFrom = self.clsFrom
    clsResponse.clsViaList = self.clsViaList
    clsResponse.clsCallId = self.clsCallId
    clsResponse.clsCSeq = self.clsCSeq
    clsResponse.eTransport = self.eTransport

    if( iStatusCode != SipStatusCode.SIP_TRYING ):
      clsResponse.clsRecordRouteList = self.clsRecordRouteList

    if( len(clsResponse.clsTo.SelectParam( "tag" )) == 0 ):
      clsResponse.clsTo.InsertTag( )
    
    return clsResponse

  def GetTopViaIp( self ):
    if( len(self.clsViaList) == 0 ):
      return ''

    strIp = self.clsViaList[0].SelectParam( "received" )
    if( len(strIp) > 0 ):
      return strIp
    
    return self.clsViaList[0].strHost
  
  def GetTopViaPort( self ):
    if( len(self.clsViaList) == 0 ):
      return ''

    strPort = self.clsViaList[0].SelectParam( "rport" )
    if( len(strPort) > 0 ):
      return int(strPort)
    
    return self.clsViaList[0].iPort

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
      
      iPos += 1
    
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
      
      iPos += 1
    
    return -1
  
  def ListToString( self, clsList, strName ):
    strText = ''
    for clsRow in clsList:
      strText += strName + ": " + str(clsRow) + "\r\n"
    
    return strText
