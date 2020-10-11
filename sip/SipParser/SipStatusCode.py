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

class SipStatusCode():
  """ SIP 응답 코드 저장 클래스
  """
  SIP_TRYING = 100
  SIP_RINGING = 180
  SIP_SESSION_PROGRESS = 183
  SIP_OK = 200
  SIP_ACCEPTED = 202
  SIP_MULTIPLE_CHOICES = 300
  SIP_MOVED_TEMPORARILY = 302
  SIP_BAD_REQUEST = 400
  SIP_UNAUTHORIZED = 401
  SIP_FORBIDDEN = 403
  SIP_NOT_FOUND = 404
  SIP_PROXY_AUTHENTICATION_REQUIRED = 407
  SIP_REQUEST_TIME_OUT = 408
  SIP_GONE = 410
  SIP_INTERVAL_TOO_BRIEF = 423
  SIP_CALL_TRANSACTION_DOES_NOT_EXIST = 481
  SIP_BUSY_HERE = 486
  SIP_REQUEST_TERMINATED = 487
  SIP_NOT_ACCEPTABLE_HERE = 488
  SIP_INTERNAL_SERVER_ERROR = 500
  SIP_NOT_IMPLEMENTED = 501
  SIP_DECLINE = 603
  SIP_CONNECT_ERROR = 660

def GetReasonPhrase( iSipCode ):
  """ SIP 응답 코드에 해당하는 설명 문자열을 리턴한다.

  Args:
      iSipCode (int): SIP 응답 코드

  Returns:
      string: SIP 응답 코드에 해당하는 설명 문자열을 리턴한다.
  """
  if( iSipCode == 100 ):
    return "Trying"
  elif( iSipCode == 180 ):
    return "Ringing"
  elif( iSipCode == 181 ):
    return "Call Is Being Forwarded"
  elif( iSipCode == 182 ):
    return "Queued"
  elif( iSipCode == 183 ):
    return "Session Progress"
  elif( iSipCode == 200 ):
    return "OK"
  elif( iSipCode == 202 ):
    return "Accepted"
  elif( iSipCode == 300 ):
    return "Multiple Choices"
  elif( iSipCode == 301 ):
    return "Moved Permanently"
  elif( iSipCode == 302 ):
    return "Moved Temporarily"
  elif( iSipCode == 305 ):
    return "Use Proxy"
  elif( iSipCode == 380 ):
    return "Alternative Service"
  elif( iSipCode == 400 ):
    return "Bad Request"
  elif( iSipCode == 401 ):
    return "Unauthorized"
  elif( iSipCode == 402 ):
    return "Payment Required"
  elif( iSipCode == 403 ):
    return "Forbidden"
  elif( iSipCode == 404 ):
    return "Not Found"
  elif( iSipCode == 405 ):
    return "Method Not Allowed"
  elif( iSipCode == 406 ):
    return "Not Acceptable"
  elif( iSipCode == 407 ):
    return "Proxy Authentication Required"
  elif( iSipCode == 408 ):
    return "Request Timeout"
  elif( iSipCode == 409 ):
    return "Conflict"
  elif( iSipCode == 410 ):
    return "Gone"
  elif( iSipCode == 411 ):
    return "Length Required"
  elif( iSipCode == 412 ):
    return "Conditional Request Failed"
  elif( iSipCode == 413 ):
    return "Request Entity Too Large"
  elif( iSipCode == 414 ):
    return "Request-URI Too Large"
  elif( iSipCode == 415 ):
    return "Unsupported Media Type"
  elif( iSipCode == 416 ):
    return "Unsupported Uri Scheme"
  elif( iSipCode == 420 ):
    return "Bad Extension"
  elif( iSipCode == 421 ):
    return "Extension Required"
  elif( iSipCode == 422 ):
    return "Session Interval Too Small"
  elif( iSipCode == 423 ):
    return "Interval Too Brief"
  elif( iSipCode == 480 ):
    return "Temporarily not available"
  elif( iSipCode == 481 ):
    return "Call Leg/Transaction Does Not Exist"
  elif( iSipCode == 482 ):
    return "Loop Detected"
  elif( iSipCode == 483 ):
    return "Too Many Hops"
  elif( iSipCode == 484 ):
    return "Address Incomplete"
  elif( iSipCode == 485 ):
    return "Ambiguous"
  elif( iSipCode == 486 ):
    return "Busy Here"
  elif( iSipCode == 487 ):
    return "Request Cancelled"
  elif( iSipCode == 488 ):
    return "Not Acceptable Here"
  elif( iSipCode == 489 ):
    return "Bad Event"
  elif( iSipCode == 491 ):
    return "Request Pending"
  elif( iSipCode == 493 ):
    return "Undecipherable"
  elif( iSipCode == 500 ):
    return "Internal Server Error"
  elif( iSipCode == 501 ):
    return "Not Implemented"
  elif( iSipCode == 502 ):
    return "Bad Gateway"
  elif( iSipCode == 503 ):
    return "Service Unavailable"
  elif( iSipCode == 504 ):
    return "Server Timeout"
  elif( iSipCode == 505 ):
    return "SIP Version not supported"
  elif( iSipCode == 513 ):
    return "Message Too Large"
  elif( iSipCode == 600 ):
    return "Busy Everywhere"
  elif( iSipCode == 603 ):
    return "Decline"
  elif( iSipCode == 604 ):
    return "Does not exist anywhere"

  return "Not Acceptable"