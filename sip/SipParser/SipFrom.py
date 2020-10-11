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
from .SipUri import SipUri
from .SipUtility import SipMakeTag

class SipFrom(SipParameterList):

  def __init__( self ):
    super().__init__()
    self.strDisplayName = ''
    self.clsUri = SipUri()

  def Parse( self, strText, iStartPos ):
    """ SIP From, To, Contact, Route, Record-Route 등의 헤더의 값을 파싱한다.

    Args:
        strText (string): SIP From 헤더의 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)
    iDisplayNamePos = -1
    iUriStartPos = -1
    iUriEndPos = -1

    while( iPos < iTextLen ):
      if( iDisplayNamePos != -1 ):
        if( strText[iPos] == '"' ):
          self.strDisplayName = strText[iDisplayNamePos:iPos]
          iDisplayNamePos = -1
      elif( iUriStartPos != -1 ):
        if( strText[iPos] == '>' ):
          iUriEndPos = iPos
          iPos += 1
          break
      elif( strText[iPos] == '"' ):
        iDisplayNamePos = iPos + 1
      elif( strText[iPos] == '<' ):
        iUriStartPos = iPos + 1

        if( len(self.strDisplayName) == 0 and iPos > iStartPos ):
          i = iPos - 1
          while( i > iStartPos ):
            if( strText[i] != ' ' and strText[i] != '\t' ):
              self.strDisplayName = strText[iStartPos:i+1]
              break
            i -= 1
      elif( strText[iPos] == ';' or strText[iPos] == ',' ):
        break

      iPos += 1
    
    if( iUriStartPos != -1 and iUriEndPos != -1 ):
      strUri = strText[iUriStartPos:iUriEndPos]
    else:
      strUri = strText[iStartPos:iPos]

    self.clsUri.Parse( strUri, 0 )

    iPos = super().HeaderListParamParse( strText, iPos )
    if( iPos == -1 ):
      return -1

    return iPos

  def __str__( self ):
    """ SIP From, To, Contact, Route, Record-Route 등의 헤더의 값 문자열을 리턴한다.

    Returns:
        string: SIP From, To, Contact, Route, Record-Route 등의 헤더의 값 문자열을 리턴한다.
    """
    if( len(self.strDisplayName) > 0 ):
      strText = '"' + self.strDisplayName + '" <'
    else:
      strText = '<'
    
    strText += str(self.clsUri)
    strText += '>' + super().__str__()

    return strText


  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.strDisplayName = ''
    self.clsUri.Clear()
    super().ClearParam()
  
  def InsertTag( self ):
    """ tag 파라미터를 추가한다.
    """
    super().InsertParam( "tag", SipMakeTag() )
  

def ParseSipFrom( clsList, strText ):
  """ SIP 헤더 문자열을 파싱하여 SipFrom 객체 리스트에 저장한다.

  Args:
      clsList (list): SipFrom 객체 리스트
      strText (string): 파싱할 문자열

  Returns:
      int: 성공하면 파싱한 문자열의 길이를 리턴하고 그렇지 않으면 -1 을 리턴한다.
  """
  iCurPos = 0
  iTextLen = len(strText)

  while( iCurPos < iTextLen ):
    if( strText[iCurPos] == ' ' or strText[iCurPos] == '\t' or strText[iCurPos] == ',' ):
      iCurPos += 1
      continue

    clsFrom = SipFrom()
    iPos = clsFrom.Parse( strText, iCurPos )
    if( iPos == -1 ):
      return -1
    iCurPos = iPos

    clsList.append( clsFrom )
  
  return iCurPos
