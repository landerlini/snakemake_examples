# Example 2. Transform and reduce, with FUNNEL
This example elaborates on Example 1 to submit the jobs to remote 
executors using FUNNEL. 

### Remote files
In order to process files in a remote cluster, it is crucial to define 
a repository for the input and output files and a protocol to access them. 
Files are passed from a task to another sending them to the remote storage 
and then pulling from the successive task. 

In a final configuration, a service such as MinIO to access data via s3 is 
recommended, however the MinIO instance of INFN Cloud that we are targeting
requires access via OIDC tokens which opens another field of complexity.
Here, to explore the capabilities of Snakemake and FUNNEL, we operate with 
an SFTP remote server which is accessed via an RSA key pair. 

The configuration of the SFTP server is extremely simple:
 * Open an instance on INFN Cloud or another service
 * Login via ssh and create a new user with
   `adduser cloudftp -s /bin/false`
 * Generate an RSA key pair with `ssh-keygen` and copy the 
   public key (`<filename_you_chose>.pub`) in `/home/cloudftp/.ssh/authorized_keys`
   (you might need to create both the `.ssh` folder and the `authorized_keys` file).
 
Then you will need to configure the Snakemake client. Edit the file 
`config.yaml` in this repository and set the IP for the INFN Cloud instance you 
setup for storage. In case you named the user differently from `cloudftp` or 
you set a different home folder, or you want to store the file in some different 
partition, you will need to modify the field `sftp_prefix`, as well. 

The private key must be stored in the envioronment variable 
`$REMOTE_PKEY` with `base64` encoding (to avoid problems encoding
the new line characters).
An easy way to achieve this is copying the private key in a local file, 
say `private_key` and then put it in the `$REMOTE_PKEY` environment 
variable with
```
export REMOTE_PKEY=`cat private_key | base64`
```

### Submitting the jobs 
Once the setup is complete, you can try to execute the jobs locally with
```
snakemake -jall --forceall 
```
if everything works locally, you can try to submit to FUNNEL with
```
snakemake -j999 --forceall --tes <tes_ip>
```


