import win32com.client
i = win32com.client.Dispatch('idrisi32.IdrisiAPIServer')
wd = i.GetWorkingDir();
list = ['sierra1', 'sierra2', 'sierra3']
for x in list[:]:
    i.DisplayFile(wd + x + '.rst','qual')
