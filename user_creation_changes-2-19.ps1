#Get Parameter in the first arguement position
param (
    [Parameter(Position=0)]
    $netid
)

if (-not $netid)
{
	write-error	-Message "Specify a netid"
	return
}

#Static Variables for folders to be created
$HOME_PATH = "G:\home"
$MUSIC_PATh = "G:\media\music"

#Import active directory module
#-Needed to add the user to the AD group
Import-Module ActiveDirectory


"$netid"
try {
    #Check if the user actually exists
    if (dsquery user -samid $netid)
    {
        "$netid"
        if (!(Test-Path -Path "$HOME_PATH\$netid")){
            #Add user to active directory group
            Add-ADGroupmember -Identity "engr-acm-users" -Members $netid
            $Result|Add-Member -MemberType NoteProperty -Name "ADGROUP" -Value "Added"

            #Create home folder if it doesnt exist
            New-item -ItemType Directory -Path "$HOME_PATH\$netid"
            $Result|Add-Member -MemberType NoteProperty -Name "HOME" -Value "created"
            
            $HomeFolderACL=(Get-Item "$HOME_PATH\$netid").GetAccessControl('Access')

            $Group = New-Object System.Security.Principal.NTAccount("ad.uillinois.edu", $netid)
            $HomeFolderACL.SetOwner($Group)

            #Get-Acl "$HOME_PATH\$netid" | Format-List

            #Reset Permissions
            #$HomeFolderACL.Access | % {
            #    $HomeFolderACL.purgeaccessrules($_.IdentityReference)
            #}

            $HomeFolderAcl.SetAccessRuleProtection($false,$false)

            $InheritanceFlag = @([System.Security.AccessControl.InheritanceFlags]::ContainerInherit,[System.Security.AccessControl.InheritanceFlags]::ObjectInherit)
            $PropagationFlag = [System.Security.AccessControl.PropagationFlags]::None
            $objType = [System.Security.AccessControl.AccessControlType]::Allow 

            #Add Permissions
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule($netid,"FullControl",$InheritanceFlag,$PropagationFlag,$objType)
            #$HomeFolderACL.AddAccessRule($ACL)
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule("NT AUTHORITY\SYSTEM","FullControl",$InheritanceFlag,$PropagationFlag,$objType)
            #$HomeFolderACL.AddAccessRule($ACL)
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule("UOFI\engr-ACM-Admins","FullControl",$InheritanceFlag,$PropagationFlag,$objType)
            #$HomeFolderACL.AddAccessRule($ACL)
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule("Administrators","FullControl",$InheritanceFlag,$PropagationFlag,$objType)
            #$HomeFolderACL.AddAccessRule($ACL)
    
            #Set Permissions
            Set-Acl -Path "$HOME_PATH\$netid" $HomeFolderACL
        }
            
        #Create music folder if it doesnt exist
        if (!(Test-Path -Path "$MUSIC_PATH\$netid")){
            New-item -ItemType Directory -Path "$MUSIC_PATH\$netid"
            $Result|Add-Member -MemberType NoteProperty -Name "MEDIA" -Value "created"

            $MusicFolderACL=(Get-Item $MUSIC_PATH).GetAccessControl('Access')
            
            $Group = New-Object System.Security.Principal.NTAccount("ad.uillinois.edu", $netid)
            $MusicFolderACL.SetOwner($Group)

            #Reset Permissions
            #$MusicFolderACL.Access | % {
            #    $MusicFolderACL.PurgeAccessRules($_.IdentityReference)
            #}

            $MusicFolderACL.SetAccessRuleProtection($false,$false)

            $InheritanceFlag = @([System.Security.AccessControl.InheritanceFlags]::ContainerInherit,[System.Security.AccessControl.InheritanceFlags]::ObjectInherit)
            $PropagationFlag = [System.Security.AccessControl.PropagationFlags]::None
            $objType = [System.Security.AccessControl.AccessControlType]::Allow 

            #Add Permissions
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule($netid,"FullControl",$InheritanceFlag,$PropagationFlag,$objType)
            #$MusicFolderACL.AddAccessRule($ACL)
            #The reset of the permissions get inherited
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule("NT AUTHORITY\SYSTEM","FullControl",$InheritanceFlag,$PropagationFlag,$objType)
            #$MusicFolderACL.AddAccessRule($ACL)
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule("UOFI\engr-ACM-Admins","FullControl",$InheritanceFlag,$PropagationFlag,$objType)
            #$MusicFolderACL.AddAccessRule($ACL)
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule("Administrators","FullControl",$InheritanceFlag,$PropagationFlag,$objType)
            #$MusicFolderACL.AddAccessRule($ACL)
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule("UOFI\engr-acm-fs-music-read","ReadAndExecute,ListDirectory,Read",$InheritanceFlag,$PropagationFlag,$objType)
            #$MusicFolderACL.AddAccessRule($ACL)
            #$ACL = New-Object  system.security.accesscontrol.filesystemaccessrule("UOFI\engr-acm-fs-music-write","Modify,Write,ReadAndExecute,ListDirectory,Read",$InheritanceFlag,$PropagationFlag,$objType)
            #$MusicFolderACL.AddAccessRule($ACL)
        
            #Set Permissions
            Set-Acl -Path "$MUSIC_PATH\$netid" $MusicFolderACL
        }
    }
    #If not just exit
    else {
        "User does not exist"
    }
}
catch {
    "Failed!"
}