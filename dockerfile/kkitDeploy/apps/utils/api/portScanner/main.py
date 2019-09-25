import argparse
import portScanner as ps
# from ..handleCommand import wsScheduleJob
# from rest_framework.views import APIView

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='********** Port Scanner v1.0 **********')
    parser.add_argument('-d', metavar='--domain', dest='hostname', help=' please make sure the input host name is in\
                                                                            the form of "something.com" , "http://something.com! " or ip. ')
    parser.add_argument('-p', metavar='--port', dest='port', help='If target_ports is a list, this list of ports will be used as\
                                                                   the port list to be scanned. If the target_ports is a int, it\
                                                                   should be 50, 100 or 1000, indicating'
                                                                   )
    parser.add_argument('-t', metavar='--thread', dest='thread', help='set the maximum number of thread for port scanning.\
                                                                       default to 1000.'
                                                                     )
    parser.add_argument('-w', metavar='--wait', dest='time', help='Set the time out delay for port scanning in seconds\
                                                                        the time in seconds that a TCP socket waits until \
                                                                        timeout, default to 10s.'
                                                                        )
    parser.add_argument('-s', metavar='show', dest='top', help='show the top50, 100 or 1000 ports list')
    args = parser.parse_args()
    message = 'hello'
    if args.top:
        scanner = ps.PortScanner()
        scanner.show_top_ports(args.top)
    if args.hostname == None:
        print('please input the website that you want to scan or input -h to show this help message and exit')
        exit(0)
    else:
        if args.port:
            scanner = ps.PortScanner(int(args.port))
        else:
            scanner = ps.PortScanner()
        if args.thread:
            scanner.set_thread_limit(int(args.thread))
        if args.time:
            scanner.set_delay(int(args.time))
        scanner.show_thread_limit()
        scanner.show_delay_time()
        output = scanner.scan(args.hostname, message)
        # print(output)
        # return output

if __name__ == '__main__':
    main()