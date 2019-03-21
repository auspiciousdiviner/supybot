Hm. Yes. Found this plugin somewhere on the internets, then modified it. Haven't been able to locate the sources again. Don't think I have the original source anymore either. According to __init__.py it was written by Ed Summers.
Anyway, what it does is: It queries wolframalpha, returns what the query was interpreted as, then the first line in the result. WA actually returns quite a lot at times, often over 30 lines, and often the answer you are looking for isn't the first result. But still works in most cases.

Apikey needs to be added with 'config plugins.wolfram.apikey yourapikeyhere'. You can get an apikey from https://developer.wolframalpha.com/.

Examples:
12:46:12 <@Hoaas> !wa 5+5
12:46:14 <@Bunisher> Input: 5+5
12:46:15 <@Bunisher> Result: 10

12:46:29 <@Hoaas> !wa 527 USD in EUR
12:46:33 <@Bunisher> Input interpretation: convert $527  (US dollars) to euros
12:46:34 <@Bunisher> Result: euro419.4  (euros)

12:47:03 <@Hoaas> !wa 1 attoparsec / microforthnight in inches per second
12:47:06 <@Bunisher> Input interpretation: convert 1 apc/microfortnight  (attoparsec per microfortnight) to inches per second
12:47:07 <@Bunisher> Result: 1.004326797 in/s  (inches per second)

12:47:29 <@Hoaas> !wa distance Paris London
12:47:32 <@Bunisher> Input interpretation: distance: from: Paris, Ile-de-France, France, to: London, Greater London, United Kingdom
12:47:33 <@Bunisher> Result: 342 km  (kilometers)

12:48:00 <@Hoaas> !wa population France, England, United States
12:48:02 <@Bunisher> Input interpretation: France: population :  England, United Kingdom  (home nation): population :  United States: population
12:48:03 <@Bunisher> Results: France: 64.8 million people  (world rank: 21st)  (2010 estimate), England, United Kingdom: 51.09 million people  (84% of total for United Kingdom), United States: 309 million people  (world rank: 3rd)  (2010 estimate)
