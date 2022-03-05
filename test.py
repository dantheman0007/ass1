'''
message = "hello there"
print(message)
encodeMessage= message.encode('utf-8')
print(encodeMessage)
decodemessage = encodeMessage.decode('utf-8')
print(decodemessage)
'''

import sys, time
import threading
import queue # thread-safe

class CleanExit:
  pass

ipq = queue.Queue()

def testexit(ipq):
  time.sleep(5)
  ipq.put(CleanExit)
  return

threading.Thread(target=testexit, args=(ipq,)).start()
while True:
  print ("Working...")
  time.sleep(1)
  try:
    if ipq.get_nowait() == CleanExit:
      sys.exit()
  except queue.Empty:
    pass
