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

class SipHeader():

  def __init__( self ):
    self.strName = ''
    self.strValue = ''

  def Parse( self, strText, iStartPos ):
    """ SIP 헤더의 이름, 값을 파싱한다.

    Args:
        strText (string): SIP 헤더의 이름, 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)
    iType = 0

    while( iPos < iTextLen ):
      if( iType == 0 ):
        if( strText[iPos] == ':' or strText[iPos] == ' ' or strText[iPos] == '\t' ):
          self.strName = strText[iStartPos:iPos]
          iType += 1
        elif( strText[iPos] == '\r' ):
          if( iPos + 1 >= iTextLen or strText[iPos+1] != '\n' ):
            return -1
          return iPos + 2
      elif( strText[iPos] == ':' or strText[iPos] == ' ' or strText[iPos] == '\t' ):
        iPos += 1
        continue
      else:
        break

      iPos += 1
    
    iValuePos = iPos

    while( iPos < iTextLen ):
      if( iType == 10 ):
        if( strText[iPos] != ' '  and strText[iPos] != '\t' ):
          iType = 11
          iPos -= 1
          iValuePos = iPos
      elif( strText[iPos] == '\r' ):
        if( iValuePos != -1 ):
          self.strValue += strText[iValuePos:iPos]
          iValuePos = -1

        iPos += 1
        if( iPos == iTextLen or strText[iPos] != '\n' ):
          return -1
        
        iPos += 1
        if( iPos == iTextLen ):
          break

        if( strText[iPos] == ' ' or strText[iPos] == '\t' ):
          iType = 10
          self.strValue += " "
        else:
          break

      iPos += 1

    return iPos

  def __str__( self ):
    """ SIP 헤더의 이름, 값 문자열을 리턴한다.

    Returns:
        string: SIP 헤더의 이름, 값 문자열을 리턴한다.
    """
    if( len(self.strValue) == 0 ):
      return self.strName + ": \r\n"
    
    return self.strName + ": " + self.strValue + "\r\n"
  
  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.strName = ''
    self.strValue = ''
