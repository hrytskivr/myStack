# myStack
##### Production-grade solution for Django application deployment

### About
This whole thing is set-up with idea of microservices architecture in head. Using docker stack, reverse proxy and other 
    tools this app will wrap your Django application with fancy production ribbon.

### Prerequisites
- Any Django application with structure similar to this one - 
    [Example Django/React application](https://github.com/hrytskivr/mySkeleton "mySkeleton")

### Software requirements
- **docker** (version _18.02.0-ce_ tested)
- **fabric3** (version _1.14_ tested)

### Usage
- clone this repository onto your host machine
- set required environment variables
- run `fab init` and watch the magic happen

**NOTE:** there is a set of useful commands defined in _fabfile.py_ to orchestrate the process, e.g. updating your app
    on the fly as easy as `fab update:app`
