from slacker import Slacker

slack = Slacker('<your-api-token>')

channel_id = slack.channels.get_channel_id('general')

if channel_id is not None:

	last_read = None

	channel_info_request = slack.channels.info(channel_id)
	if channel_info_request is not None and channel_info_request.successful == True:
		channel_info_json = channel_info_request.body

		if 'channel' in channel_info_json:
			last_read = channel_info_json['channel']['last_read']
		
	if last_read is not None:
		print slack.channels.history(channel_id, last_read, None, True, False).body

# Send a message to #general channel
# slack.chat.post_message('#general', 'Hello fellow slackers!')

