import win32com.client as win32

olApp = win32.Dispatch('Outlook.Application')
olNS = olApp.GetNameSpace('MAPI')

mailItem = olApp.CreateItem(0)
mailItem.Subject = 'Hello 123'
mailItem.BodyFormat = 1
mailItem.Body = 'Hello There'
mailItem.To = 'alzlmsiyab@outlook.com'
mailItem.Sensitivity  = 2
mailItem._oleobj_.Invoke(*(64209, 0, 8, 0, olNS.Accounts.Item('SalmanSiy2002@outlook.com')))

mailItem.Send()