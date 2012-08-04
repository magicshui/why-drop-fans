#coding: utf-8
from confign import *
class WeiboUser(Base):
	__tablename__=''

class WeiboToAuth(MethodView):
	def get(self):
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		url = client.get_authorize_url()
		return render_template('weibo_auth.html',url=url)
class WeiboAuthBack(MethodView):
	def get(self):
		code = request.args.get('code')
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		r = client.request_access_token(code)
		access_token = r.access_token # 新浪返回的token，类似abc123xyz456
		expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
		# TODO: 在此可保存access token
		client.set_access_token(access_token, expires_in)
		timeline=client.get.statuses__user_timeline()
		id=timeline.statuses[0].user.id
		screen_name=timeline.statuses[0].user.screen_name
		description=timeline.statuses[0].user.description
		profile_image_url=timeline.statuses[0].user.profile_image_url
		followers_count=timeline.statuses[0].user.followers_count

		u=WeiboUser(id=id,screen_name=screen_name,description=description,profile_image_url=profile_image_url,
			followers_count=followers_count,access_token=access_token,expires_in=expires_in)
		try:
			dbSession.add(u)
			dbSession.commit()
		else:
			continue
		return render_template('')


