import cv2
import numpy as np
import pyaudio
import wave
import os
import threading
from moviepy.editor import *
from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import subprocess
import socket
import keyboard

def run_server():
        import cv2
        import numpy as np
        import pyaudio
        import wave
        import os
        import threading
        from pydub import AudioSegment
        from pydub.utils import make_chunks
        import os
        import subprocess
        import socket
        import keyboard
        from moviepy.editor import VideoFileClip
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", 8888))
        server_socket.listen(1)

        client_socket, client_address = server_socket.accept()
        print("Client connected:", client_address)

    # Specify the output directory
        output_directory = "E:/cap"
        oD = "E:/cap/temp"

    # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)
        os.makedirs(oD, exist_ok=True)
        # Video settings
        frame_width = 640
        frame_height = 480
        fps = 30
        video_filename = os.path.join(oD, 'result.avi')

        # Audio settings
        audio_filename = os.path.join(output_directory, 'output_audio_b.wav')
        audio_format = pyaudio.paInt16
        channels = 1
        sample_rate = 44100
        chunk_size = 1024

        # Recording duration
        # record_seconds = 5

        # # Initialize video capture from default webcam
        # cap = cv2.VideoCapture(0)

        # # Initialize video writer
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # video_writer = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

        # # Initialize audio recording
        # audio = pyaudio.PyAudio()
        # stream = audio.open(format=audio_format, channels=channels,
        #                     rate=sample_rate, input=True,
        #                     frames_per_buffer=chunk_size)

        # print("Recording for {} seconds...".format(record_seconds))

        # # Function to stop recording after specified duration
        # def stop_recording():
        #     global is_recording
        #     cv2.waitKey(record_seconds * 1000)
        #     is_recording = False

        # # Start a thread to stop recording after specified duration
        # stop_thread = threading.Thread(target=stop_recording)
        # stop_thread.start()

        # # Record video and audio
        # frames = []
        # audio_frames = []
        # is_recording = True
        # while is_recording:
        #     # Record audio
        #     audio_data = stream.read(chunk_size)
        #     audio_frames.append(audio_data)
            
        #     # Record video
        #     ret, frame = cap.read()
        #     frame = cv2.resize(frame, (frame_width, frame_height))
        #     frames.append(frame)
        #     video_writer.write(frame)

        # # Release resources
        # stream.stop_stream()
        # stream.close()
        # audio.terminate()
        # video_writer.release()
        # cap.release()
        # cv2.destroyAllWindows()

        # print("Recording finished.")

        import time  # Import the time module

        record_seconds = 10

        # Initialize video capture from default webcam
        cap = cv2.VideoCapture(0)

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

        # Initialize audio recording
        audio = pyaudio.PyAudio()
        stream = audio.open(format=audio_format, channels=channels,
                            rate=sample_rate, input=True,
                            frames_per_buffer=chunk_size)

        print("Recording for {} seconds...".format(record_seconds))

        # Record start time
        start_time = time.time()

        # Record video and audio
        frames = []
        audio_frames = []
        while (time.time() - start_time) < record_seconds:
            # Record audio
            audio_data = stream.read(chunk_size)
            audio_frames.append(audio_data)
            
            # Record video
            ret, frame = cap.read()
            frame = cv2.resize(frame, (frame_width, frame_height))
            frames.append(frame)
            video_writer.write(frame)

        # Release resources
        stream.stop_stream()
        stream.close()
        audio.terminate()
        video_writer.release()
        cap.release()
        cv2.destroyAllWindows()

        print("Recording finished.")



        # Write audio to file
        wf = wave.open(audio_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(audio_frames))
        wf.close()

        # Merge audio and video
        video_clip = VideoFileClip(video_filename)
        audio_clip = AudioFileClip(audio_filename)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(os.path.join(output_directory, 'final_output_b.mp4'), codec='libx264')


        output_directory_c = "E:/cap"
        os.makedirs(output_directory, exist_ok=True)
        song = AudioSegment.from_wav("E:/cap/output_audio_b.wav")
        chunk_length_ms = 60000
        chunks = make_chunks(song, chunk_length_ms)
        chunk_folder = os.path.join(output_directory_c, "chunk_folder")
        os.makedirs(chunk_folder, exist_ok=True)
        for i, chunk in enumerate(chunks):
            out_file = os.path.join(chunk_folder, f"chunk{i}.wav")
            print("Exporting", out_file)
            chunk.export(out_file, format="wav")


        DIR = "E:/cap/chunk_folder"
        len_file = (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))


        speechlist = []
        for i in range(len_file):

            #@title Initiate Google's recognizer, record audio and recognize the speech
            import speech_recognition as spr
            spr.__version__

            recognizer=spr.Recognizer()
            audio=spr.AudioFile("chunk_folder/chunk{0}.wav".format(i))

            with audio as source:
                #recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.record(source)

            try:
                speechtext = recognizer.recognize_google(audio,
                                                language="en-US")
            except:
                print("chunk_folder/chunk{0}.wav".format(i))
                continue
            speechlist.append(speechtext)

        text = " ".join(speechlist)
        print(text)

        from googletrans import Translator
        translator= Translator()
        translation = translator.translate(text, src = 'en', dest='ta')
        print(translation.text)

        #@title Convert translated text to audio file using gTTS
        from gtts import gTTS
        tts = gTTS(translation.text, lang= "ta", slow = True)
        tts.save('E:/cap/temp/temp.wav')





        import librosa
        aud_dur = librosa.get_duration(filename='E:/cap/temp/temp.wav')
        print(aud_dur)
        clip = VideoFileClip("E:/cap/temp/result.avi")
        vid_dur = clip.duration
        print(vid_dur)


        import os
        import librosa
        import soundfile as sf
        from scipy.signal import resample

        def speed_change(audio_path, speed=1.0):
            # Load the audio file
            y, sr = librosa.load(audio_path, sr=None)
            
            # Resample the audio to change the speed
            y_resampled = resample(y, int(len(y) / speed))
            
            # Save the resampled audio back to disk
            sf.write(audio_path, y_resampled, sr, 'PCM_16')

        # Define the directory and filename
        directory = 'E:/cap/temp'
        filename = 'temp.wav'

        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Get the duration ratio (speed factor)
        aud_dur = librosa.get_duration(filename=file_path)
        spd = aud_dur / vid_dur

        # Change the speed of the audio file
        speed_change(file_path, spd)


        aud_dur = librosa.get_duration(filename='E:/cap/temp/temp.wav')
        print(aud_dur)

        # command = ["wget", "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth",
        #            "-O", "Wav2Lip/face_detection/detection/sfd/s3fd.pth"]

        # # Execute the command
        # subprocess.run(command)





        command = ["python", "E:/cap/Wav2Lip/inference.py",
                "--checkpoint_path", "E:/cap/Wav2Lip/checkpoints/wav2lip.pth",
                "--face", "E:/cap/final_output_b.mp4",
                "--audio", "E:/cap/temp/temp.wav",
                "--nosmooth"]

        subprocess.run(command)

        from moviepy.editor import VideoFileClip

        def separate_video_audio(input_video, output_video):
            video_clip = VideoFileClip(input_video)

            # Separate video and audio
            video_clip.write_videofile(output_video, codec='rawvideo', audio=False)
        

            # Close the video and audio clips
            video_clip.close()
            

        # Specify input video file path
        input_video_path = "results/result_voice.mp4"

        # Specify output video file path and name (without audio)
        output_video_path = "temp/result.avi"

        # Specify output audio file path and name


        # Separate video and audio
        separate_video_audio(input_video_path, output_video_path)

        print("Separation completed.")


        command = ["python", "E:/cap/Wav2Lip/inference.py",
                "--checkpoint_path", "E:/cap/Wav2Lip/checkpoints/wav2lip.pth",
                "--face", "E:/cap/results/result_voice.mp4",
                "--audio", "E:/cap/temp/temp.wav",
                "--nosmooth"]

        subprocess.run(command)


        def read_video_file(video_file_path):
            with open(video_file_path, "rb") as f:
                return f.read()

        # Read the video file
        video_file_path = "results/result_voice.mp4"  # Path to your video file
        video_data = read_video_file(video_file_path)

        # Function to send the video data
        def send_video_data():
            client_socket.sendall(video_data)
            print("Video file sent successfully.")

        # Check for 's' keypress to send the video data
        print("Press 's' to send the video file.")
        while True:
            if keyboard.is_pressed('s'):
                send_video_data()
                break

        # Close the connection
        client_socket.close()
        server_socket.close()

def run_receiver():
        
        import cv2
        import numpy as np
        import pyaudio
        import wave
        import os
        import threading
        
        from pydub import AudioSegment
        from pydub.utils import make_chunks
        import os
        import subprocess
        import socket
        import keyboard
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 8888))

        # Receive video data from the server
        video_data = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            video_data += data

        # Specify the path to store the received video file
        output_video_path = "received_video.mp4"  # Path to store the received video file

        # Write the received video data to a file
        with open(output_video_path, "wb") as f:
            f.write(video_data)

        # Close the connection
        client_socket.close()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 8888))

        # Receive video data from the server
        video_data = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            video_data += data

        # Specify the path to store the received video file
        output_video_path = "received_video.mp4"  # Path to store the received video file

        # Write the received video data to a file
        with open(output_video_path, "wb") as f:
            f.write(video_data)

        # Close the connection
        client_socket.close()


def main():
    user_input = input("Enter 't' to run the server or 'y' to run the receiver: ")
    if user_input == 't':
        run_server()
    elif user_input == 'y':
        run_receiver()
    else:
        print("Invalid input. Please enter 't' or 'y'.")

if __name__ == "__main__":
    main()