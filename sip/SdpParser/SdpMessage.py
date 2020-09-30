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

from .SdpOrigin import SdpOrigin
from .SdpConnection import SdpConnection
from .SdpBandWidth import SdpBandWidth

class SdpMessage():

  def __init__( self ):
    self.strVersion = ''
    self.strSessionName = ''
    self.strSessionInformation = ''
    self.strUri = ''
    self.strTimeZone = ''
    self.clsOrigin = SdpOrigin()
    self.clsConnection = SdpConnection()
    self.clsEmailList = []
    self.clsPhoneList = []
    self.clsBandWidthList = []
    self.clsTimeList = []
    self.clsAttributeList = []
    self.clsMediaList = []

  def Parse( self, strText ):
    self.Clear()

    iPos = 0
    iStartPos = 0
    iTextLen = len(strText)
    clsMedia = None

    while( iPos < iTextLen ):
      if( strText[iPos] == '\r' ):
        if( strText[iStartPos] == 'v' ):
          self.strVersion = strText[iStartPos+2:iPos]
        elif( strText[iStartPos] == 'o' ):
          if( self.clsOrigin.Parse( strText[iStartPos+2:iPos] ) == -1 ):
            return -1
        elif( strText[iStartPos] == 's' ):
          self.strSessionName = strText[iStartPos+2:iPos]
        elif( strText[iStartPos] == 'i' ):
          if( clsMedia == None ):
            self.strSessionInformation = strText[iStartPos+2:iPos]
        elif( strText[iStartPos] == 'u' ):
          self.strUri = strText[iStartPos+2:iPos]
        elif( strText[iStartPos] == 'e' ):
          self.clsEmailList.append( strText[iStartPos+2:iPos] )
        elif( strText[iStartPos] == 'p' ):
          self.clsPhoneList.append( strText[iStartPos+2:iPos] )
        elif( strText[iStartPos] == 'c' ):
          if( clsMedia != None ):
            if( clsMedia.clsConnection.Parse( strText[iStartPos+2:iPos] ) == -1 ):
              return -1
          else:
            if( self.clsConnection.Parse( strText[iStartPos+2:iPos] ) == -1 ):
              return -1
        elif( strText[iStartPos] == 'b' ):
          clsBandWidth = SdpBandWidth()
          if( clsBandWidth.Parse( strText[iStartPos+2:iPos] ) == -1 ):
            return -1
          
          if( clsMedia != None ):
            clsMedia.clsBandWidthList.append( clsBandWidth )
          else:
            self.clsBandWidthList.append( clsBandWidth )
    
        iPos += 1
        iStartPos = iPos + 1
      iPos += 1

  def Clear( self ):
    self.strVersion = ''
    self.strSessionName = ''
    self.strSessionInformation = ''
    self.strUri = ''
    self.strTimeZone = ''
    self.clsOrigin.Clear()
    self.clsConnection.Clear()
    self.clsEmailList.clear()
    self.clsPhoneList.clear()
    self.clsBandWidthList.clear()
    self.clsTimeList.clear()
    self.clsAttributeList.clear()
    self.clsMediaList.clear()
    
