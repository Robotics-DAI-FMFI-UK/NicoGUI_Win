import os
import numpy as np
import cv2
from agentspace import Agent, space, Trigger
from datetime import datetime

class RecorderAgent(Agent):

    def init(self):
        self.lastName = ""
        self.number = 0
        self.out = None
        self.fps = 10
        self.size = (1280,960)
        self.hsize = (self.size[0]//2,self.size[1]//2)
        self.blank = np.zeros((self.hsize[1],self.hsize[0],3),np.uint8)
        self.attach_timer(1.0/self.fps)
        space.attach_trigger('experiment',self,Trigger.NAMES)
        
    def senseSelectAct(self):
        experiment = space(default=False)['experiment']
        if self.triggered() == 'experiment':
            if experiment:
                name = space['name']
                if name != self.lastName:
                    if self.out is not None:
                        self.out.release()
                    try:
                        os.mkdir("experiment/")
                    except FileExistsError: 
                        pass
                    filename = "experiment/" + name + ".avi"
                    self.out = cv2.VideoWriter()
                    self.out.open(filename,cv2.VideoWriter_fourcc('M','J','P','G'),self.fps,self.size)
        else:
            if experiment:
                tl = cv2.resize(space(default=self.blank)['humanImage'],self.hsize)
                tr = cv2.resize(space(default=self.blank)['robotImage'],self.hsize)
                bl = cv2.resize(space(default=self.blank)['touchImage'],self.hsize)
                br = np.copy(self.blank)
                cv2.putText(br,str(datetime.now()),(10,25),0,1.0,(255,255,255),1)
                frame = cv2.vconcat([cv2.hconcat([tl,tr]),cv2.hconcat([bl,br])])
                self.out.write(frame)
