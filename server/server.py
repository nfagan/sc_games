from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

port = 8080

def gen_run_command(response):
  cmd = 'python main.py'
  cmd = '{} --difficulty {}'.format(cmd, response['difficulty'])

  if response['yoking']['enabled']:
    cmd = '{} --yoke_file "{}"'.format(cmd, os.path.join('data', 'yoke', response['yoking']['file_name']))

  part_id = response['participant']['id']
  cmd = '{} --participant_id "{}"'.format(cmd, part_id)

  if response['debug']['enabled']:
    cmd = '{} --debug_keys'.format(cmd)

  if not response['labjack']['enabled']:
    cmd = '{} --no_labjack'.format(cmd)

  if response['mri']['enabled']:
    cmd = '{} --mri'.format(cmd)

  scr_info = response['screen']
  if scr_info['full_screen']:
    cmd = '{} --full_screen'.format(cmd)

  cmd = '{} --screen_width {}'.format(cmd, scr_info['width'])
  cmd = '{} --screen_height {}'.format(cmd, scr_info['height'])

  with open(os.path.join(os.getcwd(), '../run.sh'), 'w') as f:
    f.write(cmd)

  with open(os.path.join(os.getcwd(), '../run-{}.sh'.format(part_id)), 'w') as f:
    f.write(cmd)

class Server(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    with open(os.path.join(os.getcwd(), 'index.html'), 'rb') as f:
      self.wfile.write(bytes(f.read()))

  def do_POST(self):
    content_len = int(self.headers['Content-Length'])
    content = self.rfile.read(content_len)
    json_content = json.loads(str(content, 'utf8'))
    print('Received: ', json_content)
    gen_run_command(json_content)

if __name__ == "__main__":
  server = HTTPServer(('localhost', port), Server)

  try:
    server.serve_forever()
  except KeyboardInterrupt:
    pass

  server.server_close()