Sub runClean()
Dim st As Outlook.Store
Dim myRules As Outlook.Rules
Dim rl As Outlook.Rule
Dim runrule As String
Dim rulename As String

rulename_prefix = "notAutoRUN-"

Set st = Application.Session.DefaultStore

Set myRules = st.GetRules

For Each rl In myRules

    If rl.RuleType = olRuleReceive Then
    
        If Left(rl.Name, 11) = rulename_prefix Then
            rl.Execute ShowProgress:=True
            runrule = rl.Name
    
        End If
    End If
Next

ruleList = "This rule was executed against the Inbox:" & vbCrLf & runrule
MsgBox ruleList, vbInformation, "Macro: Run Rules start with notAutoRUN-"

Set rl = Nothing
Set st = Nothing
Set myRules = Nothing

End Sub

