import time
import pickle 

def produce (output_filename, config):
  with open(output_filename, 'wb') as f:
    pickle.dump(int(config), f)

def transform (input_filename, output_filename, config):
  with open(input_filename[0], 'rb') as fin:
    with open(output_filename, 'wb') as fout:
      loaded = pickle.load(fin)
      pickle.dump(loaded*2, fout)
  
def reduce (input_filename, output_filename, config):
  with open(output_filename, 'wb') as fout:
      loaded = sum([pickle.load(open(f, 'rb')) for f in input_filename])
      print ("reduced:", loaded)
      pickle.dump(loaded, fout)
  


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('command', type=str,
    help="Command",
    )
  parser.add_argument('--input', '-i', nargs='*',
    help="Input"
  )
  parser.add_argument('--output', '-o', type=str, default=None,
    help="Output"
  )
  parser.add_argument('--config', '-c', type=str, default=None,
    help="Configuration"
  )
  parser.add_argument('--waited-time', '-t', type=float, default=0.0,
    help="Waited time"
  )
  args = parser.parse_args()
  time.sleep (args.waited_time)
  
  if args.command.lower() == 'produce':
    produce(output_filename=args.output, config=args.config)
  elif args.command.lower() == 'transform': 
    transform(input_filename=args.input, output_filename=args.output, config=args.config)
  elif args.command.lower() == 'reduce': 
    reduce(input_filename=args.input, output_filename=args.output, config=args.config)

