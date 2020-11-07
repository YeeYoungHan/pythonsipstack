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

import audioop
import pyaudio
import select
import socket
import struct
import threading
from ..SipPlatform.Log import Log, LogLevel

class RtpThread():

  def __init__( self ):
    self.hUdpSocket = None
    self.iUdpPort = 10000
    self.strDestIp = ''
    self.iDestPort = 0
    self.bStopEvent = False
  
  def Start( self ):
    self.hUdpSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    bBind = False

    while bBind == False:
      try:
        self.hUdpSocket.bind( ('0.0.0.0', self.iUdpPort) )
        bBind = True
      except:
        self.iUdpPort += 2
    
  def SetDestIpPort( self, strDestIp, iDestPort ):
    self.strDestIp = strDestIp
    self.iDestPort = iDestPort

    '''
    p = threading.Thread( target=RtpSendThread, args=(self,))
    p.daemon = True
    p.start()
    '''
    
    p = threading.Thread( target=RtpRecvThread, args=(self,))
    p.daemon = True
    p.start()
  
  def Stop( self ):
    self.bStopEvent = True
  
def RtpSendThread( clsRtpThread ):
  clsAudio = pyaudio.PyAudio()
  clsStream = clsAudio.open( format = 8, channels = 1, rate = 8000, input = True )

  iFlags = 0x80
  iPayload = 0
  iSeq = 0
  iTimeStamp = 0
  iSsrc = 200

  while( clsRtpThread.bStopEvent == False ):
    iSeq += 1
    iTimeStamp += 160

    arrPcm = clsStream.read( 160 )
    arrPayload = audioop.lin2ulaw( arrPcm, 2 )
    szPacket = struct.pack( '!BBHII', iFlags, iPayload, iSeq, iTimeStamp, iSsrc ) + arrPayload
    clsRtpThread.hUdpSocket.sendto( szPacket, (clsRtpThread.strDestIp, clsRtpThread.iDestPort) )

  clsStream.close()
  clsAudio.terminate()


def RtpRecvThread( clsRtpThread ):
  read_list = [ clsRtpThread.hUdpSocket ]

  clsAudio = pyaudio.PyAudio()
  clsStream = clsAudio.open( format = 8, channels = 1, rate = 8000, output = True )
  
  while( clsRtpThread.bStopEvent == False ):
    iRecvLen = 0

    try:
      read_socket_list, write_socket_list, except_socket_list = select.select( read_list, [], [], 1.0 )
      for read_socket in read_socket_list:
        szPacket, clsClientIpPort = read_socket.recvfrom( 8192 )
        iRecvLen = len(szPacket)
    except Exception as other:
      Log.Print( LogLevel.ERROR, "RtpRecvThread exception - " + str(other) )

    if( iRecvLen > 0 ):
      arrPayload = szPacket[12:]
      arrPcm = audioop.ulaw2lin( arrPayload, 2 )
      clsStream.write( arrPcm )
  
  clsStream.close()
  clsAudio.terminate()
