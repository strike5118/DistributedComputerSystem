# DistributedComputerSystem
Research into distributed computing system.

Source is seperated into two sections. Client and Server.

The Server runs the main program and stores the master queue that keeps track of work for clients to do.

The client monitors the system usage and asks the server for work to do when it detects the system is not under heavy usage.

This project is a prototype only and for investigaion only. I'm aware that performing this in python is not sensible and that the matrix inversion is horribly innefficent.

TODO
====

+ Implement a way for the clients to raise work tickets within the network
+ Make server resilent against malicious clients
