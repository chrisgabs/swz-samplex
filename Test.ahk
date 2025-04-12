!k::  ; Alt+K for Edge
    if WinExist("ahk_exe msedge.exe")
        WinActivate
    else
        Run "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    return

!j::  ; Alt+J for Cursor
    if WinExist("ahk_exe Cursor.exe")
        WinActivate
    else
        Run "C:\Users\chris\AppData\Local\Programs\cursor\Cursor.exe"
    return

!\::  ; Alt+\ for terminal
    if WinExist("ahk_exe cmd.exe")
        WinActivate
    else
        Run "cmd.exe"
    return

!`::  ; Alt+Backtick to cycle through windows of the same application
    ; Get the process name of the active window
    WinGet, ActiveProcess, ProcessName, A
    if (ActiveProcess = "")
        return
    
    ; Get all windows with the same process
    WinGet, WindowList, List, ahk_exe %ActiveProcess%
    if (WindowList <= 1)  ; Only one window or none, do nothing
        return
        
    ; Get the ID of active window
    WinGet, CurrentID, ID, A
    
    ; Find current window's position in the list
    CurrentIndex := 0
    Loop, %WindowList%
    {
        ThisID := WindowList%A_Index%
        if (ThisID = CurrentID)
        {
            CurrentIndex := A_Index
            break
        }
    }
    
    ; Determine the next window to activate
    if (CurrentIndex = WindowList)  ; If current window is the last in the list
        NextIndex := 1  ; Cycle to the first window
    else
        NextIndex := CurrentIndex + 1  ; Go to next window
     
    ; Activate the next window
    NextID := WindowList%NextIndex%
    WinActivate, ahk_id %NextID%
    return