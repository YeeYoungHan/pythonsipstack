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
  
from ..SipParser.SipStatusCode import SipStatusCode

def RecvRequest( self, clsMessage ):
  """ SIP 요청 메시지 수신 이벤트 핸들러

  Args:
      clsMessage (SipMessage): SIP 메시지 객체

  Returns:
      bool: SIP 메시지가 처리되었다면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  if( clsMessage.IsMethod("INVITE") ):
    return self.RecvInviteRequest( clsMessage )
  elif( clsMessage.IsMethod("BYE") ):
    return self.RecvByeRequest( clsMessage )
  elif( clsMessage.IsMethod("CANCEL") ):
    return self.RecvCancelRequest( clsMessage )
  elif( clsMessage.IsMethod("PRACK") ):
    return self.RecvPrackRequest( clsMessage )
  elif( clsMessage.IsMethod("REFER") ):
    return self.RecvReferRequest( clsMessage )
  elif( clsMessage.IsMethod("NOTIFY") ):
    return self.RecvNotifyRequest( clsMessage )
  elif( clsMessage.IsMethod("MESSAGE") ):
    return self.RecvMessageRequest( clsMessage )
  elif( clsMessage.IsMethod("OPTIONS") ):
    return self.RecvOptionsRequest( clsMessage )

  return False

def RecvResponse( self, clsMessage ):
  """ SIP 응답 메시지 수신 이벤트 핸들러

  Args:
      clsMessage (SipMessage): SIP 메시지 객체

  Returns:
      bool: SIP 메시지가 처리되었다면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  if( clsMessage.IsMethod("REGISTER") ):
    return self.RecvRegisterResponse( clsMessage )
  elif( clsMessage.IsMethod("INVITE") ):
    return self.RecvInviteResponse( clsMessage )
  elif( clsMessage.IsMethod("BYE") or clsMessage.IsMethod("CANCEL") or clsMessage.IsMethod("PRACK") ):
    return True
  elif( clsMessage.IsMethod("REFER") ):
    return self.RecvReferResponse( clsMessage )
  elif( clsMessage.IsMethod("NOTIFY") or clsMessage.IsMethod("MESSAGE") or clsMessage.IsMethod("OPTIONS") ):
    return True

  return False

def SendTimeout( self, clsMessage ):
  """ SIP 메시지 전송 timeout 이벤트 핸들러

  Args:
      clsMessage (SipMessage): SIP 메시지 객체
  
  Returns:
      bool: False 를 리턴한다.
  """
  strCallId = clsMessage.GetCallId()
  self.clsCallBack.EventCallEnd( strCallId, SipStatusCode.SIP_GONE )
  self.Delete( strCallId )

  return False
