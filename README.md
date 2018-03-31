# myStack
##### Production-grade solution for Django application deployment

### About
This whole thing is set-up with idea of microservices architecture in head. Using docker stack, tls, reverse proxy and 
    other tools this app will wrap your Django application with a fancy production ribbon :ribbon:

### Prerequisites
- Any Django application with structure and settings similar to this one - 
    [**Example Django/React application**](https://git.io/vxEl4 'hrytskivr/mySkeleton')

### Software requirements
- **docker** (version _18.02.0-ce_ tested)
- **fabric3** (version _1.14_ tested)

### Usage
- install software requirements
- make sure to [**init docker swarm**](https://docs.docker.com/engine/reference/commandline/swarm_init/)
- clone this repository onto your host machine
- set required environment variables
- run `fab init` and watch the magic happen

**NOTE:** there is a set of useful commands defined in [**fabfile.py**](https://git.io/vxElt) 
    to orchestrate the process e.g scaling your app service on the fly as easy as - `fab scale:app,5`.

**WARNING:** default tls certificate will contain no user data and is not CA verified, if you would like to use your own 
    certificate please alter [**nginx configuration**](https://git.io/vxEWr 'nginx/sites-enabled/django').
