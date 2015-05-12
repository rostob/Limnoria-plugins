Listens for Youtube URLs and retrieves video info.

YouTube Data API documentation:
https://developers.google.com/youtube/v3/docs/videos

IMPORTANT:

Edit plugin.py and enter your key in the following section:
    """Google Developers YouTube Data API-key
    Obtain one following the instructions on:
    https://developers.google.com/youtube/v3/getting-started
    """
    apiKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


Config:
        supybot.plugins.Youtube.youtubeSnarfer (default: True)
		Enable/Disable youtube snarfer.

        supybot.plugins.Youtube.showDuration (default: True)
		Show the duration ( - 0:04:47).

        supybot.plugins.Youtube.showViews (default: True)
		Show number of views ( - 2544 views).

        supybot.plugins.Youtube.showLikes (default: True)
		Show likes/dislikes ( - 34578 likes / 368 dislikes).

        supybot.plugins.Youtube.showChannel (default: False)
		Show video channel ( - channel: Some Channel).

        supybot.plugins.Youtube.showDate (default: False) ->
		Show publish date ( - published: 2011-09-03 07:23:54+02:00).

        The following is "hidden", not asked about by the configurator:
        supybot.plugins.Youtube.separator (default: '-')
		The character or string separating the above strings. ( - ).
