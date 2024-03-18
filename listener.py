#!/usr/bin/env python3
import rospy
from std_msgs.msg import String, Char  

import bz2

class BZ2Listener:  
    def __init__(self):
        self.rate = rospy.Rate(3)
        self.listener=''
        self.solution = Char()
        rospy.Subscriber('/bz2_message', String, self.callback)  
        self.pub = rospy.Publisher('/solution', Char, queue_size=10)
      
    #decompressing data
    def decode_bz2(self, hex_data):  
        compressed_data = bytes.fromhex(hex_data)
        decompressed_data = bz2.decompress(compressed_data)
        return decompressed_data.decode('utf-8')

    #finding most common character
    def most_common_character(self, data):  
        counter = {}
        for char in data:
            if char in counter:
                counter[char] += 1  
            else:
                counter[char] = 1
        max_char = max(counter, key=counter.get)
        return max_char

    def callback(self, data):  
        compressed_data_hex = data.data
        uncompressed_data = self.decode_bz2(compressed_data_hex)  
        common_char = self.most_common_character(uncompressed_data)  
        ascii_value = ord(common_char)
        self.pub.publish(ascii_value) 
        rospy.loginfo(rospy.get_caller_id() + ' most common character: %c', chr(ascii_value))

if __name__ == '__main__':  
    try:
        rospy.init_node("bz2_listener", anonymous=False)
        listener = BZ2Listener()  
        rospy.spin()  
    except rospy.ROSInterruptException:
        pass

