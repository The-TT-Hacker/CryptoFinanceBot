data = [
    {
       'guild': 1234, # one dictionary for each guild that the bot is in
       'autopost_channel': 1234, # which channel should autoposts go in
       'watch_list': ['BTC', 'ETH', 'XRP'], # which currencies to watch
       'price_pings': [ #pings for particular price drops
            {
                'user': 1234,
                'coin': 'BTC',
                'price': 10000,
                'higher': True,
            },
        ]
    },
]