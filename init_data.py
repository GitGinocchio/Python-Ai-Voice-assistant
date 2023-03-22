from datastructures import Djson
import pyaudio

p = pyaudio.PyAudio()
listofdevices = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]

def check_output_pyaudio_devices():
    output_devices = [(listofdevices[i]["index"],listofdevices[i]["name"]) for i in range(len(listofdevices)) if listofdevices[i]['maxOutputChannels'] > 0 and listofdevices[i]['maxInputChannels'] < 1]

    unique_output_devices = [(int(item[0]),str(item[1])) for item in output_devices if not any(item[1] in item_two[1] and item[1] != item_two[1] for item_two in output_devices)]
    
    content = Djson.content()
    if unique_output_devices != content["sys_data"]["output_devices"]["devices"]:
        content["sys_data"]["output_devices"]["devices"].clear()
        content["sys_data"]["output_devices"]["devices"].extend(unique_output_devices)

        Djson.save_to_file(content)    
    return unique_output_devices

def check_input_pyaudio_devices():
    input_devices = [(listofdevices[i]["index"],listofdevices[i]["name"]) for i in range(len(listofdevices)) if listofdevices[i]['maxOutputChannels'] < 1 and listofdevices[i]['maxInputChannels'] > 0]

    unique_input_devices = [(int(item[0]),str(item[1])) for item in input_devices if not any(item[1] in item_two[1] and item[1] != item_two[1] for item_two in input_devices)]
    
    content = Djson.content()
    if unique_input_devices != content["sys_data"]["input_devices"]["devices"]:
        content["sys_data"]["input_devices"]["devices"].clear()
        content["sys_data"]["input_devices"]["devices"].extend(unique_input_devices)

        Djson.save_to_file(content)
    return unique_input_devices
