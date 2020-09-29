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

class SipTransactionList():

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