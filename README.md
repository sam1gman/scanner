The scanner instrument for Linux(use socket,paramiko and subprocess libraries)
it determines if the target machine is reachable by sending ICMP packets by the module of subprocess
that allowed me to execute the ping command.
If the ping fails the script terminates otherwise, it proceeds.
after the succesfull ping it scan the ports of the target by using socket try to connect to the port and if
it's found open ones it tries to access them by creating ssh using Paramiko and guessing the credentials
of the target .
(cracking the credentials of the machine by asking the user two lists of usernames and passwords. After
receiving the two lists it's using brute force on the machine to try to guess the true arguments of
credentials to access the machine.)
When it's got valid credentials it copies them to a file and saves them for future use.
After you get the valid credentials you can send commands over the SSH connection and it returns the
results of the executed commands.
