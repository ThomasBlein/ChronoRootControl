# App architecture

The app is composed of two components.

1. The web interface which is a Flask web app.
2. uwisgi Mule module
3. Scheduler (BackgroundScheduler from apscheduler module)

## uwisgi Mule

From uwisgi documentation :

*Mules are worker processes living in the uWSGI stack but not reachable via
socket connections, they are used as a generic subsystem to offload tasks.
You can see them as a more primitive spooler. They can access the entire uWSGI
API and can manage signals and be communicated with through a simple
string-based message system.*

The Mule acts as a messenger between the web app and the scheduler.

The mule is implemented in uwsgiMules/shutting_director_mule.py file.

## Phototron module

This module implements all Raspberry Pi module features.

The RpiModule class implemented in rpimodule implements all ChronoRoot robot
features; Basically, image taking with or without light. RpiModule class calls
SelectorFactory and CameraFactory classes. Those two are Factory design pattern
implementations. Each of them will provide Camera or camera multiplexer
object as specified in the configuration file.