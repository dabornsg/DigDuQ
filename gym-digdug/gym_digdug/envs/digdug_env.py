import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from pynput.keyboard import Key, Controller
from PIL import ImageGrab
import win32gui
import win32pipe
import win32file
import pywintypes
import win32com.client #Needed for weird foreground window bug
import time

def WaitForPipe(pipe):
    while True:
        try:
            print('Waiting for pipe connection...')
            win32pipe.ConnectNamedPipe(pipe, None)
            break
        except pywintypes.error as e:
            if e.args[0] == 536:
                print("No connection, trying again in 1 second")
                time.sleep(1)

class DigdugEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=np.zeros((190, 190)), #og had shape 256, 244, 3
                                            high=np.ones((190, 190)),
                                            dtype=np.float16)
        
        self._lives = 3
        self._score = 0
        self._enemies = 0
        self._reward_type = 'score'
        
        self._kb_controller = Controller()
        self.action_map = {0: Key.up, 1: Key.down, 2: Key.left, 3: Key.right, 4: 'f'}

        #Handy Windows hwnd getter from https://stackoverflow.com/questions/3260559/how-to-get-a-window-or-fullscreen-screenshot-without-pil
        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)

        nes_emu = [(hwnd, title) for hwnd, title in winlist if 'fceux 2.6.4' in title.lower()]
        self._hwnd = nes_emu[0][0]
        self._win_bb = list(win32gui.GetWindowRect(self._hwnd))

        self._win_bb[0] += 18
        self._win_bb[2] -= 64
        self._win_bb[1] += 83
        self._win_bb[3] -= 10

        self._shell = win32com.client.Dispatch("WScript.Shell")
        self._first_run = True

        self._pipe = win32pipe.CreateNamedPipe(R'\\.\pipe\digdug_read_pipe',
                                        win32pipe.PIPE_ACCESS_DUPLEX,
                                        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
                                        1, 16, 16, 0, None)
        
        WaitForPipe(self._pipe)

    def setRewardType(self, type='score'):
        if type in ['score', 'enemies']:
            self._reward_type = type
        else:
            print('Tried to set reward type to an invalid value.')

    def step(self, action):
        assert self.action_space.contains(action), "Invalid action"
        action = self.action_map[action]

        win32gui.SetForegroundWindow(self._hwnd)
        self._kb_controller.press('k')
        #self._kb_controller.press('l')
        #self._kb_controller.release('l')
        self._kb_controller.press(action)
        data = ''
        try:
            data = win32file.ReadFile(self._pipe, 16)
            if data != b'':
                print(f'Got: {data}')
            else:
                print("Didn't get anything bruv")
                time.sleep(1)
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("no pipe, trying again in a sec")
                time.sleep(1)
            elif e.args[0] == 109:
                print("Broken pipe, trying connection again...")
                win32pipe.DisconnectNamedPipe(self._pipe)
                WaitForPipe(self._pipe)
        #self._kb_controller.press('l')
        #self._kb_controller.release('l')
        self._kb_controller.release('k')
        self._kb_controller.release(action)

        obs = np.array(ImageGrab.grab(self._win_bb).convert(mode='L'))
        
        data = [int(i) for i in data[1].decode().split('|')]
        reward = 0
        if self._reward_type == 'score':
            reward = data[2] - self._score
        else:
            if data[1] < self._enemies:
                reward = data[1] - self._enemies
        self._score = data[2]
        self._enemies = data[1]
        done = False
        if data[0] < self._lives:
            done = True #Change later?

        return obs, reward, done, []

    def reset(self):
        self._lives = 3
        self._score = 0
        self._enemies = 0
        if self._first_run:
            self._shell.SendKeys('%')
            self._first_run = False
        win32gui.SetForegroundWindow(self._hwnd)
        self._kb_controller.press('p')
        self._kb_controller.release('p')
        obs = ImageGrab.grab(self._win_bb).convert(mode='L')
        return np.array(obs)

    def render(self, mode="human"):
        pass

    def close(self):
        win32gui.SetForegroundWindow(self._hwnd)
        self._kb_controller.press('p')
        self._kb_controller.release('p')