param (
    [Parameter(Position=0)]
    $netid
)

if (-not $netid)
{
	write-error	-Message "Empty"
	return
}
$ACM = Get-ADGroupMember -Identity "engr-acm-users" -Recursive | Select -ExpandProperty Name

If ($members -contains $user) {
    "1"
}
Else {
    "0"
}
