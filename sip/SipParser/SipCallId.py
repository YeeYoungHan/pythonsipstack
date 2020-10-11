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

from .SipUtility import SipMakeCallIdName

class SipCallId():

  def __init__( self ):
    self.strName = ''
    self.strHost = ''

  def Parse( self, strText, iStartPos ):
    """ SIP Call-ID 헤더의 값을 파싱한다.

    Args:
        strText (string): SIP Call-ID 헤더의 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치
    """
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)

    while( iPos < iTextLen ):
      if( strText[iPos] == '@' ):
        self.strName = strText[iStartPos:iPos]
        self.strHost = strText[iPos+1:]
        break
      iPos += 1

    if( len(self.strName) == 0 ):
      self.strName = strText[iStartPos:]

  def __str__( self ):
    """ SIP Call-ID 헤더의 값 문자열을 리턴한다.

    Returns:
        string: SIP Call-ID 헤더의 값 문자열을 리턴한다.
    """
    if( len(self.strHost) == 0 ):
      return self.strName
    
    return self.strName + "@" + self.strHost

  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.strName = ''
    self.strHost = ''
  
  def Empty( self ):
    """ 멤버 변수에 값이 저장되지 않았는지 검사한다.

    Returns:
        bool: 멤버 변수에 값이 저장되지 않았으면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    if( len(self.strName) == 0 ):
      return True
    
    return False
  
  def Make( self, strHost ):
    """ SIP Call-ID 를 생성한다.

    Args:
        strHost (string): 도메인 이름 또는 IP 주소 문자열
    """
    self.strName = SipMakeCallIdName()
    self.strHost = strHost

  def __eq__( self, clsCallId ):
    """ SIP Call-ID 객체가 동일한 값을 저장하고 있는지 검사한다.

    Args:
        clsCallId (SipCallId): SIP Call-ID 객체

    Returns:
        bool: SIP Call-ID 객체가 동일한 값을 가지고 있다면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    if( self.strName == clsCallId.strName and self.strHost == clsCallId.strHost ):
      return True
    
    return False
