import sys
import os
import json

def main():
  if len(sys.argv) != 2:
    print('Expected file path as first argument to script.')
    return
  
  src_p = sys.argv[1]
  with open(src_p, 'r') as f:
    js = json.loads(f.read())

  if 'trials' not in js:
    print('Expected key `trials` in json data file.')
    return
  
  base_fname = os.path.basename(src_p)
  dst_p = os.path.join(os.path.split(src_p)[0], 'yoke', base_fname)
  
  infos = []
  for trial in js['trials']:
    interact_res = trial['interact']
    hit_ts = interact_res['implement_hit_timestamp']
    entry_ts = interact_res['entered_timestamp']

    implement_hit_trial = True
    ts = float('nan')
    if hit_ts is None:
      implement_hit_trial = False
    else:
      ts = hit_ts - entry_ts

    infos.append({'implement_hit': implement_hit_trial, 'timestamp': ts})

  with open(dst_p, 'wt') as f:
    f.write(json.dumps(infos))  

if __name__ == '__main__':
  main()