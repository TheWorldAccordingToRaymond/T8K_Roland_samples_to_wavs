# Extract SMPL from a t8k or t8p file, add wav header and put them in a WAVS directory
import sys
import os
with open(sys.argv[1], "rb") as binary_file:
    binary_file.seek(0, 2)  # Seek the end
    num_bytes = binary_file.tell()  # Get the file size
    print(sys.argv[1])
    count = 0
    smpl_count = 0
    waves_names_list = []
    t8k_keywords = [
        b'T8K ',
        b'NAME',
        b'KIT ',
        b'TONE',
        b'PCMT',
        b'WAVE',
        b'SMPL']
        
    for i in range(num_bytes):
        binary_file.seek(i)
        keyword_bytes = binary_file.read(4)
        if keyword_bytes == t8k_keywords[3]:    # TONE
            #print("Found TONE Keyword #" + str(count) + " at " + str(i))
            # Go to beginning Wave names
            binary_file.seek(i+0x10)
            nb_waves_bytes= binary_file.read(4)
            nb_waves = int.from_bytes(nb_waves_bytes, byteorder='little', signed=False)
            print("Found waves names number #" + str(nb_waves))
            for j in range(nb_waves):
                binary_file.seek(i+0x20+(j*0x24))
                # Read the size of image plus the keyword
                name_data = binary_file.read(16)
                name_txt=name_data.decode().strip("\00")
                print(name_txt)
                waves_names_list.append(name_txt)
            
        if keyword_bytes == t8k_keywords[6]:    # SMPL
            count += 1
            print("Found SMPL Keyword #" + str(count) + " at " + str(i))
            
            # Next four bytes after keyword is the data length
            smpl_size_bytes = binary_file.read(4)
            smpl_size = int.from_bytes(smpl_size_bytes, byteorder='little', signed=False)
            print("Data length #" + hex(smpl_size) + " bytes " )
            
            #Next four bytes after data the length is the crc32 of datas
            #Next four bytes after crc32 of datas is the crc32 of the 12 above bytes
            # Go to beginning datas
            binary_file.seek(i+0x10)
            # Read the size of image plus the keyword
            smpl_data = binary_file.read(smpl_size)
            
            #Save samples files
            '''
            newpath = r'.\SMPLS'
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            with open("smpls/" + str(i) + ".smpl", "wb") as outfile:
                outfile.write(smpl_data)
            '''
            #Save waves files
            header_wav_RIFF = b"\x52\x49\x46\x46"    #('RIFF')
            header_wav_end = b"\x57\x41\x56\x45\x66\x6D\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x44\xAC\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00\x64\x61\x74\x61"  #(end by 'data')
            
            newpath = r'.\WAVS'
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            #with open("wavs/" + str(i) + ".wav", "wb") as outfile:
            wave_name=str(i)
            if smpl_count<len(waves_names_list):
                wave_name=waves_names_list[smpl_count]
            with open("wavs/" + wave_name + ".wav", "wb") as outfile:
                print("Create wav file: wavs/" + wave_name + ".wav")
                outfile.write(header_wav_RIFF)
                outfile.write((smpl_size+0x20).to_bytes(4, byteorder = 'little'))
                outfile.write(header_wav_end)
                outfile.write(smpl_data)
            smpl_count+= 1
        
'''
SMPL from Roland TR-8S .t8k file to wav file
Header for .wav file
0x52,0x49,0x46,0x46,    ('RIFF');
0xnn,0xnn,0xnn,0xnn,    dataSize +32 
0x57,0x41,0x56,0x45,    ('WAVE');
0x66,0x6D,0x74,0x20,    ('fmt ')
0x10,0x00,0x00,0x00,    (16)
0x01,0x00,              (format) 1: PCM
0x01,0x00,              (numChannels) 1: MONO
0x44,0xAC,0x00,0x00,    (sampleRate) 44100
0x88,0x58,0x01,0x00,    (byteRate)   44100x2
0x02,0x00,              (blockAlign) 2
0x10,0x00,              (bytesPerSample * 8) 16
0x64,0x61,0x74,0x61     ('data')
'''
