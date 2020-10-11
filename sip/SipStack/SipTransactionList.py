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

import os

class SipTransactionList():
  """ SIP transaction list 에서 공통적으로 사용되는 메소드 정의 클래스
  """

  MAX_ICT_RESEND_COUNT = 11
  arrICTReSendTime = [ 0.5
    , 1.5
    , 3.5
    , 7.5
    , 11.5
    , 15.5
    , 19.5
    , 23.5
    , 27.5
    , 31.5
    , 32.0]
  
  def GetKey( self, clsMessage ):
    """ SIP 메시지로 자료구조에 저장할 KEY 문자열을 생성한다.

    Args:
        clsMessage (SipMessage): SIP 메시지 객체

    Returns:
        string: 성공하면 KEY 문자열을 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
    """
    if( len(clsMessage.clsViaList) == 0 ):
      return ""
    
    strKey = ""
    strBranch = clsMessage.clsViaList[0].SelectParam( "branch" )
    if( len(strBranch) > 0 ):
      if( strBranch[:7] == "z9hG4bK" ):
        strKey = strBranch[7:] + " " + str(clsMessage.clsCSeq.iDigit)

        if( clsMessage.clsCSeq.strMethod == "ACK" ):
          strKey += "INVITE"
        else:
          strKey += clsMessage.clsCSeq.strMethod
    
    if( len(strKey) == 0 ):
      strKey = str(clsMessage.clsCallId)
    
    return strKey
  
  def GetKeyMethod( self, clsMessage, strMethod ):
    """ SIP 메시지와 SIP 메소드 문자열로 자료구조에 저장할 KEY 문자열을 생성한다.

    Args:
        clsMessage (SipMessage): SIP 메시지 객체
        strMethod (string): SIP 메소드 문자열

    Returns:
        string: 성공하면 KEY 문자열을 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
    """
    if( len(clsMessage.clsViaList) == 0 ):
      return ""
    
    strKey = ""
    strBranch = clsMessage.clsViaList[0].SelectParam( "branch" )
    if( len(strBranch) > 0 ):
      if( strBranch[:7] == "z9hG4bK" ):
        strKey = strBranch[7:] + " " + str(clsMessage.clsCSeq.iDigit) + strMethod
    
    if( len(strKey) == 0 ):
      strKey = str(clsMessage.clsCallId)
    
    return strKey