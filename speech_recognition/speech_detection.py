import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import speech_recognition as sr

class VoiceControlNode(Node):
    def __init__(self):
        super().__init__('voice_control')
        self.publisher_ = self.create_publisher(String, 'voice_commands', 10)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen_and_publish(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        try:
            # Google Speech Recognitionを使用
            command = self.recognizer.recognize_google(audio)
            self.publisher_.publish(String(data=command))
        except sr.UnknownValueError:
            # 認識できなかった場合の処理
            pass
        except sr.RequestError as e:
            # APIリクエストに失敗した場合の処理
            pass

def main(args=None):
    rclpy.init(args=args)
    node = VoiceControlNode()
    # 定期的に音声認識とパブリッシュを実行
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

