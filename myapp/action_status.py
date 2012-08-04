#coding: utf-8
from config import *
class Status(Base):
	__tablename__=''
class Friends(Base):
	__tablename__=''
def fetch_queue():
	queue = TaskQueue('fr1')
	for x in 200:
		queue.add(Task("/statuses/fetch"))
		queue.add(Task("/followers/fetch"))
class SQueue(MethodView):
	def get(self):
		fetch_queue()
class StatusesFetch(MethodView):
	def get(self):
		i=20
		while (i>0):
			user=dbSession.query(WeiboUser).filter(WeiboUser.checked=0).first()
			fetch_status(user.uid)
			i-=1
class FollowersFetch(MethodView):
	def get(self):
		i=20
		while :
			user=dbSession.query(WeiboUser).filter(WeiboUser.checked=0).first()
			fetch_followers(user.uid)
			i-=1



def fetch_status(uid):
	u=dbSession.query(WeiboUser).filter(WeiboUser.uid==uid).first()
	client=client.set_access_token(u.access_token, u.expires_in)
	try:
		timeline=client.get.statuses__user_timeline()
		if 1:
			for x in timeline.statuses:
				created_at=datetime.strptime(x.created_at,'%a %b %d %H:%M:%S +0800 %Y')
				id=x.id
				text=x.text
				source=x.source
				s=Status(created_at=created_at,id=id,text=text,source=source)
				try:
					dbSession.add(s)
					dbSession.commit()
				except:
					continue
		else:
			continue
	except:
		continue
def set_user_followers_check_time(uid,t):
	pass
def fetch_followers(uid):
	u=dbSession.query(WeiboUser).filter(WeiboUser.uid==uid).first()
	client=client.set_access_token(u.access_token, u.expires_in)
	t=time.now()
	set_user_followers_check_time(uid,t)
	try:
		cursor=0
		friends=client.get.friendships_followers(count=200,cursor=0)
		pages=friends.total_number%200+1
		cursor=friends.next_cursor
		for i in [2,pages]:
			friends=client.get.friendships_followers(count=200,cursor=cursor)
			cursor=friends.next_cursor
			for x in friends.users:
				f=Friends(id=x.id,screen_name=x.screen_name,name=x.name,location=x.location,check_time=t,
					description=x.description,profile_image_url=x.profile_image_url,followers_count=x.followers_count)
				try:
					dbSession.add(f)
					dbSession.commit()
				except:
					print ''
	except:
		print ''

def diff_followers(uid):
	old,new=get_user_check_time(uid)
	old_followers=get_user_followers(uid,old)
	new_followers=get_user_followers(uid,new)
	data=[]
	for x in old_followers:
		if x not in new_followers:
			data.append(x)
	return check_time,data

def gen_diff_why(check_time,data):
	statuses=get_user_status_1_hour_in(check_time)

