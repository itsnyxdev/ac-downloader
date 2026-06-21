[Setup]
AppName=ac-downloader
AppVersion=1.0.0
AppPublisher=ac-downloader
DefaultDirName={autopf}\ac-downloader
DefaultGroupName=ac-downloader
OutputDir=..\dist\installer
OutputBaseFilename=ac-downloader-amd64
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
ChangesEnvironment=yes

[Files]
Source: "..\dist\ac-downloader\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "..\dist\ffmpeg\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\ffmpeg\ffprobe.exe"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; \
    ValueData: "{olddata};{app}"; Flags: uninsdeletevalue

[Icons]
Name: "{group}\ac-downloader"; Filename: "{app}\ac-downloader.exe"
Name: "{group}\Uninstall ac-downloader"; Filename: "{uninstallexe}"
