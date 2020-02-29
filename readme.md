Project 1: Recursive DNS

Check out the Demo Video!
<video src="./test.mp4" width="320" height="200" controls preload></video>

a client,two server programs: RS (a simplified root DNS server) and TS (a simplified top-level DNS server).

In project 0, you have already seen a client-server program with one socket each
in the client and the server. In this project, you will extend that
implementation to have two sockets in the client program. One socket will
be used to communicate with RS and the other with TS.

The RS and TS programs each maintain a DNS_table consisting of three fields:

- Hostname
- IP address
- Flag (A or NS)

You need to choose the appropriate data structure to store the values for each
entry. The client always connects first to RS, sending the queried hostname as a
string. The RS program does a look up in its DNS_table, and if there is a match,
sends the entry as a string

Hostname IPaddress A

If there is no match, RS sends the string

TSHostname - NS

where TShostname is the name of the machine on which the TS program is running.

If the client receives a string with "A" field, it outputs the received string
as is. On the other hand, if the client receives a string with "NS" field, it
uses the TSHostname part of the received string to determine the IP address of
the machine running the TS program and connects to the TS program using a second
socket.

The client then sends the queried hostname as a string to TS. The TS program
looks up the hostname in its DNS_table, and if there is a match, sends the entry
as a string

Hostname IP address A

to the client. Otherwise, it sends an error string

Hostname - Error:HOST NOT FOUND

In the TS outputs above, Hostname is the queried hostname. The client outputs
the string received from TS as is.

Note that all DNS lookups are case-insensitive. If there is a hit in the local
DNS table, the server programs must respond with the version of the string that
is in their local DNS table.
