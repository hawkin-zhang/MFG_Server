#!/usr/bin/env python3.5


class SshChannel():
    """Basic ssh channel"""

    def __init__(self, user, password, host, port=22):
        """Save the target configs"""
        ChannelBase.__init__(self, user, password, host, port)

    def connect(self):
        """Create a ssh client and try to connect to the server"""
        self.client = ssh.SSHClient()
        self.client.set_missing_host_key_policy(ssh.AutoAddPolicy())
        self.client.load_system_host_keys()
        self.client.connect(self.hostName, self.portNum, self.userName, self.passWord)
        self.channel = self.client.invoke_shell()
        self.channel.settimeout(self.timeout)

    def disconnect(self):
        if self.channel is not None:
            self.channel.close()
            self.channel = None
        if self.client is not None:
            self.client.close()
            self.client = None

    def set_timeout(self, timeout):
        """Set the socket timeout in seconds"""
        if timeout > 0:
            self.timeout = timeout
            self.channel.settimeout(timeout)
