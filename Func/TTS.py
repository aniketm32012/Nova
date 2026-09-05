import asyncio, os, subprocess, edge_tts

def TTS(text):
    if not text.strip(): return
    asyncio.run(edge_tts.Communicate(text, "en-US-ChristopherNeural").save("voice.mp3"))
    subprocess.run(f'powershell -c "Add-Type -AssemblyName presentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open(\'{os.path.abspath("voice.mp3")}\'); $p.Play(); Start-Sleep -Seconds 2"', shell=True)
