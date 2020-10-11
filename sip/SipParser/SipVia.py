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
from .SipTransport import SipTransport

class SipVia( SipParameterList ):
  """ SIP Via 헤더의 값 저장 클래스

  Args:
      SipParameterList (SipParameterList): SIP 파라미터 리스트 저장 클래스
  """

  def __init__( self ):
    super().__init__()
    self.strProtocolName = ''
    self.strProtocolVersion = ''
    self.strTransport = ''
    self.strHost = ''
    self.iPort = -1
  
  def Parse( self, strText, iStartPos ):
    """ SIP Via 헤더의 값을 파싱한다.

    Args:
        strText (string): SIP Via 헤더의 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
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
    """ SIP Via 헤더의 값 문자열을 리턴한다.

    Returns:
        string: SIP Via 헤더의 값 문자열을 리턴한다.
    """
    strVia = self.strProtocolName + "/" + self.strProtocolVersion + "/" + self.strTransport + " "

    strVia += SipIpv6Print( self.strHost )

    if( self.iPort > 0 ):
      strVia += ":" + str( self.iPort )

    strVia += super().__str__()

    return strVia

  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.strProtocolName = ''
    self.strProtocolVersion = ''
    self.strTransport = ''
    self.strHost = ''
    self.iPort = -1
    super().ClearParam()

  def AddIpPort( self, strIp, iPort, eTransport ):
    """ SIP Via 헤더에 IP, Port, transport 를 저장한다.

    Args:
        strIp (string): IP 주소
        iPort (int): 포트 번호
        eTransport (SipTransport): transport
    """
    strPort = str(iPort)
    if( super().UpdateParam( "rport", strPort ) == False and self.iPort != iPort ):
      super().InsertParam( "rport", strPort )
    if( super().UpdateParam( "received", strIp ) == False and self.strHost != strIp ):
      super().InsertParam( "received", strIp )
    if( eTransport == SipTransport.TCP and self.strTransport.lower() != "tcp" ):
      super().InsertParam( "transport", "tcp" )


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


def ParseSipVia( clsList, strText ):
  """ SIP 헤더 문자열을 파싱하여 SipVia 객체 리스트에 저장한다.

  Args:
      clsList (list): SIP Via 헤더 리스트
      strText (string): SIP Via 헤더 값을 저장한 문자열

  Returns:
      int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
  """
  iCurPos = 0
  iTextLen = len(strText)

  while( iCurPos < iTextLen ):
    if( strText[iCurPos] == ' ' or strText[iCurPos] == '\t' or strText[iCurPos] == ',' ):
      iCurPos += 1
      continue

    clsVia = SipVia()
    iPos = clsVia.Parse( strText, iCurPos )
    if( iPos == -1 ):
      return -1
    iCurPos = iPos

    clsList.append( clsVia )
  
  return iCurPos
