from pyclmuapp import usp_clmu

# initialize
o = usp_clmu(container_type='singularity')  # important to define the container_type. The default is docker

# the clmu-app_1.0.sif image will be download from docker hub at the current work dir.
o.docker(cmd="pull", cmdlogfile="None",)  # This will pull the image from the docker hub