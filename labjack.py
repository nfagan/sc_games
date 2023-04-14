import os
import sys
import threading
import time
from typing import Dict

HAS_U3 = True
LOCAL_U3 = True
DEBUG_U3 = True

if HAS_U3:
  if LOCAL_U3:
    # otherwise, don't append to path and use (presumably) globally installed library
    sys.path.append(os.path.join(os.getcwd(), 'deps/LabJackPython/src'))
  import u3

def labjack_event_handler(device, fio_num: int):
  if DEBUG_U3:
    print('Labjack: fio: {} | state = 1'.format(fio_num))

  if device is not None:
    device.setFIOState(fio_num, state=1)

  time.sleep(1)

  if DEBUG_U3:
    print('Labjack: fio: {} | state = 0'.format(fio_num))

  if device is not None:
    device.setFIOState(fio_num, state=0)

class LabJack(object):
  def __init__(self, *, enable: bool, events: Dict[str, int], log_file_path: str) -> None:
    self.device = None

    if HAS_U3:
      if enable:
        self.device = u3.U3()
    elif enable:
      raise Exception('Cannot enable LabJack implementation because HAS_U3 is False.')

    self.events = events
    self.log_file_path = log_file_path

    if (self.device is not None) or DEBUG_U3:
      self.log_file = open(self.log_file_path, 'w')
      if self.device is not None:
        self.log("#" + str(self.device.getCalibrationData()) + "\n")
        self.log("time\tport\tdescription\n")
    else:
      self.log_file = None

  def shutdown(self):
    self.flush_log()

  def log(self, txt: str):
    if self.log_file is not None:
      self.log_file.write(txt)

  def flush_log(self):
    if self.log_file is not None:
      self.log_file.flush()

  def send_event(self, event_type: str, timestamp: float):
    if self.device is None and not DEBUG_U3:
      return
    
    if event_type not in self.events:
      print('Warning: invalid event type (%s) could not be handled as a GSR trigger.' % event_type)
      return
    
    fio_num = self.events[event_type]
    self.log("{:6f}\t{:d}\t{:s}\n".format(timestamp, fio_num, event_type))
    self.flush_log()

    trigger_thread = threading.Thread(target=labjack_event_handler, args=(self.device, fio_num))
    trigger_thread.start()