import io
import os

from paramiko import RSAKey
from pysftp import CnOpts 
from snakemake.remote.SFTP import RemoteProvider as SFTPRemoteProvider
from base64 import b64decode

configfile: "config.yaml"

def get_rsa_key_from_env():
  if "REMOTE_PKEY" not in os.environ:
    print (f"REMOTE_PKEY variable not set. Try with: \n  export REMOTE_PKEY=`cat some_private_key_file`")
    raise KeyError("REMOTE_PKEY")
  
  private_key_file = io.StringIO()
  private_key_file.write(str(b64decode(os.environ['REMOTE_PKEY']), 'ASCII'))
  private_key_file.seek(0)
  return RSAKey.from_private_key(private_key_file)


# Connection options 
cnopts = CnOpts()
cnopts.hostkeys = None

# Connection Provider to INFN Cloud
SFTPProvider = SFTPRemoteProvider(
  username="cloudftp", 
  private_key=get_rsa_key_from_env(), 
  cnopts=cnopts
)

# Remote modifier
def remote(filename, *args, **kwargs):
  if isinstance(filename, str):
    return SFTPProvider.remote(f"{config['sftp_server']}{config['sftp_prefix']}{filename}", *args, **kwargs)
  elif isinstance (filename, (list,tuple)):
    return [remote(s) for s in filename]


# Specify environment vars from configuration
for key, value in config['environment'].items():
  os.environ[key] = str(value)

envvars: 
  "REMOTE_PKEY", 
  *list(config['environment'].keys())
