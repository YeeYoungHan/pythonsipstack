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

class SipParameter():
  strName = ''
  strValue = ''

  def Parse( self, strText, iStartPos ):
    self.Clear()

    iPos = iStartPos
    iValuePos = -1
    iTextLen = len(strText)
    bStartQuote = False

    while( iPos < iTextLen ):
      if( strText[iPos] == '"' ):
        if( bStartQuote ):
          bStartQuote = False
        else:
          bStartQuote = True
      elif( strText[iPos] == '=' ):
        if( bStartQuote ):
          continue
        self.strName = strText[iStartPos:iPos]
        iValuePos = iPos + 1
      elif( strText[iPos] == ',' or strText[iPos] == ';' or strText[iPos] == '&' or strText[iPos] == '?' ):
        if( bStartQuote ):
          continue
        break
      elif( strText[iPos] == '\r' ):
        break

      iPos += 1

    if( iPos > iStartPos ):
      if( iValuePos != -1 ):
        self.strValue = strText[iValuePos:iPos]
      else:
        self.strName = strText[iStartPos:iPos]
      return iPos
    
    return -1

  def Clear( self ):
    self.strName = ''
    self.strValue = ''

  def __str__(self):
    if( len(self.strName) == 0 ):
      return ""

    if( len(self.strValue) == 0 ):
      return self.strName
    
    return self.strName + "=" + self.strValue


def ParseSipParameter( clsList, strText, iStartPos ):
  clsParam = SipParameter()
  
  iPos = clsParam.Parse( strText, iStartPos )
  if( iPos == -1 ):
    return -1
  
  clsList.append( clsParam )

  return iPos

def MakeSipParameterString( clsList ):
  iCount = len( clsList )
  strText = ''

  for i in range(0, iCount):
    strText += ';' + str( clsList[i] )

  return strText
