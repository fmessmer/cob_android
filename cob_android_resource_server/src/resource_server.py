#! /usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import path
import subprocess
import sys
import threading
import time

import roslib
roslib.load_manifest('cob_android_resource_server')
import rospy

default_img_path = '../'

class MyHandler(BaseHTTPRequestHandler):            
    def do_GET(self):
        global default_img_path
        print "\nIncoming request!"
        try:
            spath = self.path[1:]
            if spath.endswith('.jpg') or spath.endswith('.jpeg'):
                self.send_response(200)
                self.send_header('Content-type','image/ipg')
                self.end_headers()
                fn = path.abspath(default_img_path+spath)
                with open(fn, 'rb') as f:
                    self.wfile.write(f.read())
                return

            elif spath.endswith('.png'):
                self.send_response(200)
                self.send_header('Content-type','image/png')
                self.end_headers()
                fn = path.abspath(default_img_path+spath)
                print 'fn: ', fn
                with open(fn, 'rb') as f:
                    self.wfile.write(f.read())
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

class ResourceServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = None
        self.daemon = True
        self.ns_global_prefix="/android/resource_server"
        if rospy.has_param(self.ns_global_prefix + "/default_img_path"):
            global default_img_path
            default_img_path = rospy.get_param(self.ns_global_prefix + "/default_img_path")
            if not default_img_path.endswith("/"):
                default_img_path = default_img_path + "/"

    def run(self):
        self.server = HTTPServer(('', 44644), MyHandler)
        print '\nStarted Android resource server on port 44644'
        self.server.serve_forever()

    def close(self):
        self.server.shutdown()
        self.server.socket.close()

if __name__ == '__main__':
    rospy.init_node('android_resource_server')
    resServer = ResourceServer()
    resServer.start()
    rospy.spin()
    resServer.close()
