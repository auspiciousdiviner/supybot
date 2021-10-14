###
# Copyright (c) 2019, waratte
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *

import urllib.request, urllib.parse, urllib.error
import json

try:
	from supybot.i18n import PluginInternationalization
	_ = PluginInternationalization('PredictIt')
except ImportError:
	# Placeholder that allows to run the plugin on a bot
	# without the i18n module
	_ = lambda x: x


class PredictIt(callbacks.Plugin):
	"""Gets price data from PredictIt's api"""
	threaded = True

	def predictit(self, irc, msg, args, market_id):
		"""<market_id>
		
		Provides the current market data on the market specified on PredictIt		
		"""
		
		url = "https://www.predictit.org/api/marketdata/markets/" + str(market_id)
		user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		headers = {'User-Agent':user_agent,} 

		request = urllib.request.Request(url,None,headers)  # The assembled request
		 
		with urllib.request.urlopen(request) as response:
			file = response.read()
		 
		data = json.loads(file.decode('utf-8'))
		 
		output = data["shortName"]
		 
		if len(data["contracts"]) == 1:
			yes = int(data["contracts"][0]["lastTradePrice"]*100)
			no = 100 - yes
			output = output + " Yes: {:d}%; No: {:d}%;".format(yes, no)
			
		else:
			for contract in data["contracts"][:6]:
				name = contract["shortName"]
				price = int(contract["lastTradePrice"]*100)
				output = output + " {:s}: {:d}%;".format(name, price)
		 
		output = output + " https://www.predictit.org/markets/detail/" + str(market_id)
		
		irc.reply(output)

	predictit = wrap(predictit, ['int'])

Class = PredictIt


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
