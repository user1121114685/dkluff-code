'init
MoveTo 0,0
'1731,878,"B172D"
pc1=GetPixelColor(1731,878)
pc2=GetPixelColor(1738,680)
pc3=GetPixelColor(1723,481)

mobcol="A29AE9"
papmancol="C4CCDC"

Function ifwin()
ifwin=-1
FindColor 756,627,1058,854,"14182D",intX,intY
If intX > 0 And intY > 0 Then 
FindColor 756,627,1058,854,"141836",intX,intY
If intX > 0 And intY > 0 Then 
FindColor 756,627,1058,854,"8255E",intX,intY
If intX > 0 And intY > 0 Then 

ifwin=1
TracePrint "I-----win"

End If
End If
End If
End Function

Function selectmob(col)
TracePrint "start Mob..."
	selectmob = -1
	'boss
	'FindColor 0,0,1657,812,"B7AFED",intX,intY
	FindColor 0,0,1657,812,col,intX,intY
	If intX > 0 And intY > 0 Then 

	MoveTo intX, intY
	Delay 500
	LeftClick 2
	Delay 500
	'a=ifwin()
	'While a<0
	'TracePrint "checking win"
	'  a=ifwin()
	'  MoveTo 1381, 371
  '  Delay 500
  '  LeftClick 1
  '  Delay 1000
	'Wend
	selectmob = 1

	End If
	
	'MessageBox "delay..@selectmob"
	Delay 2000


End Function


Function selectpm(col)
TracePrint "start selectpm"
	selectpm = 0
	'boss
	'FindColor 0,0,1657,812,"B7AFED",intX,intY
	FindColor 0,0,1657,812,col,intX,intY
	If intX > 0 And intY > 0 Then 
	yn=intY-50

	MoveTo intX, yn
	Delay 500
	LeftClick 2

	selectpm = 1

	End If
	
	
	Delay 2000

End Function

Function testbot()
TracePrint "start testbot"
	testbot = -1
	'boss
	'FindColor 0,0,1657,812,"B7AFED",intX,intY
	FindColor 0,0,1657,812,mobcol,intX,intY
	If intX > 0 And intY > 0 Then 
		testbot = 1

	Else
		
		FindColor 0,0,1657,812,papmancol,x,y
		If x > 0 And y > 0 Then 
		testbot = 1
		End If

	End If
	
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

Sub walk()
TracePrint "start walk"
'MoveTo 1379, 793
i=7
While i>0
MoveTo 1379, 793
LeftClick 1
Delay 1000
i=i-1
If testbot()>0 Then
Exit Sub
End If
Wend

i=7
While i>0
MoveTo 487, 772
LeftClick 1
Delay 1000
i=i-1
If testbot()>0 Then
Exit Sub
End If
Wend

End Sub

call startgui()

'start to farm
LogStart "c:\a.log"
a=1
While a >0
 
  b=0
  If selectmob(mobcol)<0 Then
    'check paper man

    b=b+selectpm(papmancol)
	b=b+selectpm(papmancol)
	b=b+selectpm(papmancol)

	call startgui()

  End If
  

  If b>0 Then
   TracePrint "find papman"
    MoveTo 1381, 371
    Delay 500
    LeftClick 1
    Delay 3000
  call startgui()
  End If
  a=a+1

  'MessageBox "call walk"
  call walk()

    MoveTo 1381, 371
    Delay 500
    LeftClick 1
    Delay 1000

Wend
LogStop



