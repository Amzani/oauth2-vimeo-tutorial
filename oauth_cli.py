import sys
import urlparse
import oauth2 as oauth
import pprint
import getopt
import json

consumer_key = "YOUR_CONSUMER_KEY or Client ID"
consumer_secret = "YOUR_CONSUMER_SECRET or Client Secret"

request_token_url = "https://vimeo.com/oauth/request_token"
authorize_url = "https://vimeo.com/oauth/authorize"
access_token_url = "https://vimeo.com/oauth/access_token"
callback_url = "http://www.yourWebSite.com"


def authorize_cli():
	consumer = oauth.Consumer(consumer_key, consumer_secret)
	client   = oauth.Client(consumer)
	final_request_token_url = request_token_url + "?oauth_callback=" + callback_url
	resp, content = client.request(final_request_token_url, "GET", "oauth_callback=http://www.goodbarber.com")
	if resp['status'] != '200':
		pprint.pprint(content)
		pprint.pprint(resp)
		raise Exception("Invalide response %s." % resp['status'])
	
	
	request_token = dict(urlparse.parse_qs(content))
	pprint.pprint(request_token)
	print "Request Token:"
	print "    - oauth_token        = %s" % request_token['oauth_token'][0]
	print "    - oauth_token_secret = %s" % request_token['oauth_token_secret'][0]

	print "Copiez ce lien dans votre navigateur "
	print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'][0])

	answer = 'n'
	while answer.lower() == 'n':
	    answer = raw_input('Have you authorized me ? (y/n) ')
	oauth_verifier = raw_input('Have you the oauth_verifier ?')
	
	#you can pick the oauth_verifier from callback url after your authorization
	
	token = oauth.Token(request_token['oauth_token'][0], request_token['oauth_token_secret'][0])
	token.set_verifier(oauth_verifier)
	client = oauth.Client(consumer, token)
	final_access_token_url = access_token_url + "?oauth_callback=" + callback_url
	resp, content = client.request(final_access_token_url, "POST")
	if resp['status'] != '200':
		pprint.pprint(content)
		pprint.pprint(resp)
		raise Exception("Invalide response %s." % resp['status'])
	access_token = dict(urlparse.parse_qs(content))
	print "Access Token:"
	print "    - oauth_token        = %s" % access_token['oauth_token'][0]
	print "    - oauth_token_secret = %s" % access_token['oauth_token_secret'][0]
	print
	print "You can access to my private ressources now :))."
	print "You need to store oauth_token and oauth_token_secret in a secure location (Database...)"

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "ha", ["help", "action="])
	except getopt.GetoptError, e:
		print str(e)
		usage()
		sys.exit()
	opts = dict(opts)
	if 'h' in opts or '--help' in opts:
		usage()
		sys.exit()
	if '--action' in opts:
		if opts['--action'] == "authorize":
			authorize_cli()
			sys.exit()	
	usage()
			
def usage():
	print "client_oauth.py --help|h"
	print "client_oauth.py --action=authorize"
	sys.exit()	
	
if __name__ == "__main__":
	main(sys.argv[1:])
