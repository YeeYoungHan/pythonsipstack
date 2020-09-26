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

class SipFrom(SipParameterList):

  def __init__( self ):
    super().__init__()
    self.strDisplayName = ''
    self.clsUri = SipUri()

  def Parse( self, strText, iStartPos ):
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
              self.strDisplayName = strText[iStartPos:i]
              break
      elif( strText[iPos] == ';' or strText[iPos] == ',' ):
        break

      iPos += 1
    
    if( iUriStartPos != -1 and iUriEndPos != -1 ):
      strUri = strText[iStartPos:iUriEndPos]
    else:
      strUri = strText[iStartPos:]

    self.clsUri.Parse( strUri )

    super().HeaderListParamParse( strText, iPos )

  def __str__( self ):
    if( len(self.strDisplayName) > 0 ):
      strText = '"' + self.strDisplayName + '" <'
    else:
      strText = '<'
    
    strText += str(self.clsUri)
    strText += '>' + super().__str__()

    return strText


  def Clear( self ):
    self.strDisplayName = ''
    self.clsUri.Clear()
    super().ClearParam()
  
