#coding: utf-8
def user_first_auth(client):
	timeline=client.get.statuses__user_timeline()
	id=timeline.statuses[0].user.id
	screen_name=timeline.statuses[0].user.screen_name
	description=timeline.statuses[0].user.description
	profile_image_url=timeline.statuses[0].user.profile_image_url
	followers_count=timeline.statuses[0].user.followers_count
	