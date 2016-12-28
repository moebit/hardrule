import xml.etree.cElementTree as ET
import time, argparse, sys
from subprocess import call


#config file resides in /cf/conf


def add(config_file, interface, protocol, src_ip, dst_ip, realdst_ip, virtual_port, real_port, rule, user, pfSense_ip):
	time_now = int(time.time())	
	username = user + "@" + str(pfSense_ip)
	rule_string = "\t\t\t<rule>\n" \
                 "\t\t\t<source>\n" \
                 "\t\t\t\t<address>" + str(src_ip) + "</address>\n" \
                 "\t\t\t</source>\n" \
                 "\t\t\t<destination>\n" \
                 "\t\t\t\t<network>" + str(dst_ip) + "</network>\n" \
                 "\t\t\t\t<port>" + str(virtual_port) + "</port>\n" \
                 "\t\t\t</destination>\n" \
                 "\t\t\t<protocol>" + str(protocol) + "</protocol>\n" \
                 "\t\t\t<target>" + str(realdst_ip) + "</target>\n" \
                 "\t\t\t<local-port>" + str(real_port) + "</local-port>\n" \
                 "\t\t\t<interface>" + str(interface) + "</interface>\n" \
                 "\t\t\t<descr/>\n" \
                 "\t\t\t<associated-rule-id>" + str(rule) + "</associated-rule-id>\n" \
                 "\t\t\t<created>\n" \
                 "\t\t\t\t<time>" + str(time_now) + "</time>\n" \
                 "\t\t\t\t<username>" + str(username) + "</username>\n" \
                 "\t\t\t</created>\n" \
                 "\t\t\t<updated>\n" \
                 "\t\t\t\t<time>" + str(time_now) + "</time>\n" \
                 "\t\t\t\t<username>" + str(username) + "</username>\n" \
                 "\t\t\t</updated>\n" \
                 "\t\t\t</rule>\n\n"
	
	tree = ET.parse(config_file)
	root = tree.getroot()
	element = root.find("nat")
	element.append(ET.XML(str(rule_string)+'\n'))
	tree.write(config_file, xml_declaration=True)
	# delete cache to apply changes
	cache_update()
	print("Record is added successfully!")



def delete(config_file, virtual_port):
	flag = False
	tree = ET.parse(config_file)	
	root = tree.getroot()
	for nat in root.findall("nat"):
		for rule in nat.findall("rule"):
			for address in rule.findall("destination/port"):
				# we remove based on opened virtual port, but can be customized based on your requirement
				if address.text == str(virtual_port):
					nat.remove(rule)
					tree.write(config_file, xml_declaration=True)
					# delete cache to apply changes
					cache_update()
					flag = True
	return flag



def cache_update():
	call(["rm","/tmp/config.cache"])
	call(["/etc/rc.interfaces_wan_configure"])


# print help for subparser
class NewParser(argparse.ArgumentParser):
	def error(self, message):
		self.print_help()
		sys.exit(0)



if __name__ == '__main__':
	
	parser = NewParser(description="Example of changing pfSense configuration (port forwarding) from terminal.")
	subparser = parser.add_subparsers(dest='subparser_name')
	parser_add = subparser.add_parser('add', help="Add rules.") 
	parser_del = subparser.add_parser('delete', help="Delete rules.")
	
	# == Add rules ==
	parser_add.add_argument('-c','--config', help="pfSense configuration file.", required=True)
	parser_add.add_argument('-sip','--source-ip', help="Source IP of client who wants to connect to the interanl server from outside.", required=True)
	
	parser_add.add_argument('-dip','--destination-ip', help="Usually should be wanip (e.g. wanip).", default='wanip')
	parser_add.add_argument('-rip','--realip', help="Internal server's IP.", required=True)
	parser_add.add_argument('-rp','--realport', help="Internal server's port (e.g. 22)", required=True)
	parser_add.add_argument('-vp','--virtual-port', help="Virtual port which you to be seen from outside. (e.g. 2000)", required=True)	
	parser_add.add_argument('-prot','--protocol', help="e.g. tcp", required=True)		
	
	parser_add.add_argument('-r','--rule', help="e.g. pass", default='pass')	
	parser_add.add_argument('-u','--user', help="User who sets the rule (e.g. admin)", default='admin')
	parser_add.add_argument('-i','--interface', help="Rule should be applied on this interface. (e.g. wan)", default='wan')	
	parser_add.add_argument('-pip', '--pfsense-ip', help="pfSense's (internal) IP", required=True)
	

	# == Del rules ==
	parser_del.add_argument('-c', '--config', help="pfSense configuration file.", required=True)
	parser_del.add_argument('-vp', '--virtual-port', help="This script deletes rules based on the given virtual port.", required=True)

	args = parser.parse_args()

	if args.subparser_name == 'add':
		add(args.config, args.interface, args.protocol, args.source_ip, args.destination_ip, args.realip, args.virtual_port, args.realport, args.rule, args.user, args.pfsense_ip)

	elif args.subparser_name == 'delete':
		if delete(args.config, args.virtual_port):
			print("Successfully deleted!")
		else:
			print("Record doesn't exist!") 	
