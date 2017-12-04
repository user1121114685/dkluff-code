'init

'1731,878,"B172D"
pc1=GetPixelColor(1731,878)
pc2=GetPixelColor(1738,680)
pc3=GetPixelColor(1723,481)



Function mybot(col)
	mybot = -1

	FindColor 0,0,1657,812,col,intX,intY
	'boss
	'FindColor 0,0,1657,812,"B7AFED",intX,intY
	If intX > 0 And intY > 0 Then 

	MoveTo intX, intY
	Delay 500
	LeftClick 2

	mybot = 1

	End If
	
	
	Delay 2000
End Function


Function chkover()
chkover = -1
IfColor 1731,878,pc1,0 Then
IfColor 1738,680,pc2,0 Then
IfColor 1723,481, pc3, 0 Then
chkover = 1
End If
End If
End If

End Function

Function chkstart()
	chkstart = -1
	IfColor 1262,793,"5EB2F3",0 Then
	IfColor 1371, 794, "5EB2F3", 0 Then
	chkstart = 1
    End If
	End If
	
End Function


Sub startgui
If chkover() > 0 Then 
	MoveTo 1731,878
	Delay 100
	LeftClick 1
	Delay 3000
	
	If chkstart() > 0 Then 
		MoveTo 1262, 793
		Delay 100
		LeftClick 1
	End If
	
End If
Delay 3000

End Sub

redge=0
Sub walk()
  If redge < 5 Then
	If mybot("A29AE9")>0 Then
		Exit Sub
	End If
	MoveTo 1332, 700
	LeftClick 1
	Delay 1000
	redge=redge+1
  ElseIf redge < 15 And redge >=5 Then
  	If mybot("A29AE9")>0 Then
		Exit Sub
	End If
	
	MoveTo 332, 700
	LeftClick 1
	Delay 1000
	redge=redge+1
  ElseIf redge >=15
    redge = 0
  End If
 

  
End Sub

call startgui()

'start to farm
a=1
While a >0
  If mybot("A29AE9")<0 Then
    'check paper man
    mybot("CDDDE9")
    call startgui()
	If mybot("A29AE9")<0 Then
		call walk()
	End If
  End If
  
  MoveTo 1381, 371
  Delay 500
  LeftClick 1
  Delay 2000
  
  a=a+1

Wend




