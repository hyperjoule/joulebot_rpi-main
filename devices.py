import speech_recognition as sr

for i, device_name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {device_name}")