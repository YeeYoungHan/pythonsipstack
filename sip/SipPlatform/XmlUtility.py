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

def XmlGetDataString( clsParent, strName, strValue ):
  """ 하위 Element 의 값 문자열을 리턴한다.

  Args:
      clsParent (Element): XML Element 객체
      strName (string): 하위 Element 이름
      strValue (string): 하위 Element 가 존재하지 않을 경우 리턴할 기본값

  Returns:
      string: 입력된 strName 과 같은 하위 Element 가 존재하면 해당 Element 의 값 문자열을 리턴하고 존재하지 않으면 입력된 strValue 를 리턴한다.
  """
  clsChild = clsParent.find( strName )
  if( clsChild != None ):
    return clsChild.text
  
  return strValue

def XmlGetDataInt( clsParent, strName, iValue ):
  """ 하위 Element 의 값 숫자를 리턴한다.

  Args:
      clsParent (Element): XML Element 객체
      strName (string): 하위 Element 이름
      iValue (int): 하위 Element 가 존재하지 않을 경우 리턴할 기본값

  Returns:
      int: 입력된 strName 과 같은 하위 Element 가 존재하면 해당 Element 의 값 숫자를 리턴하고 존재하지 않으면 입력된 iValue 를 리턴한다.
  """
  clsChild = clsParent.find( strName )
  if( clsChild != None ):
    return int(clsChild.text)
  
  return iValue

def XmlGetDataBool( clsParent, strName, bValue ):
  """ 하위 Element 의 값 bool 를 리턴한다.

  Args:
      clsParent (Element): XML Element 객체
      strName (string): 하위 Element 이름
      bValue (bool): 하위 Element 가 존재하지 않을 경우 리턴할 기본값

  Returns:
      bool: 입력된 strName 과 같은 하위 Element 가 존재하면 해당 Element 의 값 bool 을 리턴하고 존재하지 않으면 입력된 bValue 를 리턴한다.
  """
  clsChild = clsParent.find( strName )
  if( clsChild != None and clsChild.text.lower() == "true" ):
    return True
  
  return bValue

def XmlGetAttrString( clsNode, strName, strValue ):
  """ 입력된 Element 의 애트리뷰트 값 문자열을 리턴한다.

  Args:
      clsNode (Element): XML Element 객체
      strName (string): 애트리뷰트 이름
      strValue (string): 애트리뷰트가 존재하지 않을 경우 리턴할 기본값

  Returns:
      string: 애트리뷰트가 존재하면 해당 애트리뷰트의 값 문자열을 리턴하고 존재하지 않으면 입력된 strValue 를 리턴한다.
  """
  strAttr = clsNode.attrib.get( strName )
  if( strAttr != None ):
    return strAttr
  
  return strValue

def XmlGetAttrInt( clsNode, strName, iValue ):
  """ 입력된 Element 의 애트리뷰트 값 숫자를 리턴한다.

  Args:
      clsNode (Element): XML Element 객체
      strName (string): 애트리뷰트 이름
      iValue (int): 애트리뷰트가 존재하지 않을 경우 리턴할 기본값

  Returns:
      int: 애트리뷰트가 존재하면 해당 애트리뷰트의 값 숫자를 리턴하고 존재하지 않으면 입력된 iValue 를 리턴한다.
  """
  strAttr = clsNode.attrib.get( strName )
  if( strAttr != None ):
    return int(strAttr)
  
  return iValue

def XmlGetAttrBool( clsNode, strName, bValue ):
  """ 입력된 Element 의 애트리뷰트 값 bool 을 리턴한다.

  Args:
      clsNode (Element): XML Element 객체
      strName (string): 애트리뷰트 이름
      bValue (bool): 애트리뷰트가 존재하지 않을 경우 리턴할 기본값

  Returns:
      bool: 애트리뷰트가 존재하면 해당 애트리뷰트의 값 bool 을 리턴하고 존재하지 않으면 입력된 bValue 를 리턴한다.
  """
  strAttr = clsNode.attrib.get( strName )
  if( strAttr != None and strAttr.lower() == "true" ):
    return True
  
  return bValue