# both Body class works same (findings till now)
# from fastapi import Body
# from fastapi.params import Body

from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. database import get_db
from typing import List, Optional
from .. import oauth2

router = APIRouter(
	prefix='/posts',
	tags=['Posts'] # This will group the paths operations based on this tags in the Swagger UI
)
# this router connects path-operations lives in this file with main.py

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db :Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]=""):
	"""
	'current_user: int = Depends(oauth2.get_current_user)' will make sure the user is logged in and will return the 'user_id'
	"""
	# cursor.execute("""SELECT * FROM posts ORDER BY id DESC;""")
	# posts = cursor.fetchall()
	# posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
	# Above query will only return the Posts of the current user
	
	# posts = db.query(models.Post).filter(models.Post.title.contains(search.lower())).limit(limit).offset(skip).all()
	posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes'))\
					.join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
					.group_by(models.Post.id)\
					.filter(models.Post.title.contains(search.lower()))\
					.order_by(models.Post.id)\
					.limit(limit).offset(skip)\
					.all()
	
	#print the query w/o '.all()' to see the generated sql query
	#the 'LEFT Join' by default is 'LEFT Inner Join' in SQLAlchemy, so we need to set 'isouter=True'
	#cause we need the 'LEFT Outer Join' for our query
	"""
	select posts.*, count(votes.post_id) as votes from posts LEFT JOIN votes on posts.id = votes.post_id
	group by posts.id
	order by id asc (copied from pgAdmin)
	"""
	
	#insert '%20' instead of 'space' if you wish to include 'space' in your search string, cause api url cannot contains space directly
	#limit: number of posts will be returned
	#offset: number of posts from the begining to skip
	#after offset if number of available posts is more/equal to limit, then it will return the limit number of post
	#after offset if number of available posts is less then limit, then returned number of post will be (limit-offset)
	#limit and skip mechanism is related to pagination

	return posts



# when there could be multiple type of status
# @router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	"""
	'current_user: int = Depends(oauth2.get_current_user)' will make sure the user is logged in and will return the 'user_id'
	"""
	# cursor.execute("""SELECT * FROM posts where id = %s """, (str(id), ))
	# cursor.execute("""SELECT * FROM posts where id = %(id)s """, {'id': id})
	# post = cursor.fetchone()

	# post = db.query(models.Post).filter(models.Post.id == id).first()
	#add .first() at the end to successfully execute the query and since we are expecting only one result

	post = db.query(models.Post, func.count(models.Vote.post_id).label('votes'))\
					.join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
					.group_by(models.Post.id)\
					.filter(models.Post.id ==id)\
					.first()
	# post = find_post(id)

	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f'Post with id: {id} was not found')
		# response.status_code = status.HTTP_404_NOT_FOUND
		# return {'message': f'Post with id {d} was not found'}

	# if post.owner_id != current_user.id:
	# 	raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
	# 				  		detail="Not authorised to perfom the requestd action")
	# #will return the post if and only if the user is the owener of that post
	
	return post


"""
@router.post("/posts")
def create_posts(payload: dict = Body(...)):
	'''
	the Body class will convert the HTTP request Body into a dict and store in payload parameter.
	'''
	print(payload)
	return {"message": f"title: {payload['title']} content: {payload['content']}"}
"""

# it is very painful to extract data from HTTP Body, what we can do is given below


# when there is only one success status code
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	"""
	'current_user: int = Depends(oauth2.get_current_user)' will make sure the user is logged in and will return the 'user_id'
	"""
	"""
	the pydantic (schema model) Post class will validate the data sent by user via HTTP Body.
	It will look for the defined attributes and defined type attributes
	if it finds everything okk then the data will be stored in post else
	error will be thrown
	"""
	# print(post) # printing pydantic model
	# print(post.dict()) # converted into regular dict using dict() method of pydantic model
	# post_dict = post.dict()
	# post_dict["id"] = randrange(0, 100000)
	# my_posts.append(post_dict)
	# return {"data": post_dict}

	# cursor.execute(
		# """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
	'''
		fstring or formatted string is not encouraged here, since it may be vulnerable for Postgre
		f"""INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published}) RETURNING * """),
		if the user passes any sql-query or reserved word into title/content... the query will be excuted and affect the DB.
		what will not be occured into '%s' fashion
	'''
	# new_post = cursor.fetchone()
	# conn.commit()
	# new_post = models.Post(title=post.title, content=post.content, published=post.published)
	# new_post = models.Post(**post.dict()) # unpacking the dictionary, same as above

	# print(current_user.email)
	new_post = models.Post(owner_id=current_user.id, **post.model_dump()) # unpacking the dictionary, same as above
	#as the 'PostCreate' schema does not contain 'owner_id' we are setting the 'owner_id' outside of the schema from 'current_user'
	db.add(new_post) # adding new data to the db
	db.commit() # commiting
	db.refresh(new_post) # Returning or getting back the newly added data
	return new_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	"""
	'current_user: int = Depends(oauth2.get_current_user)' will make sure the user is logged in and will return the 'user_id'
	"""
	# cursor.execute(
	#     """ DELETE FROM posts where id = %s returning * """, (str(id),))
	# deleted_post = cursor.fetchone()
	# conn.commit()
	# index = find_index_post(id)

	post_query = db.query(models.Post).filter(models.Post.id == id) #getting the query only
	# print('post_query', type(post_query))
	# print('post_query.first()', post_query.first())

	if post_query.first() == None: # getting the first result from the query
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f'Post with id: {id} does not exist')

	if post_query.first().owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
					  		detail="Not authorised to perfom the requestd action")
	post_query.delete(synchronize_session=False)
	db.commit()
	# my_posts.pop(index)

	'''
	since this is a delete request that's why the status code is 204
	and when the status code is 204 the convention or fastapi does not want us to return any data but a response
	'''

	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	"""
	'current_user: int = Depends(oauth2.get_current_user)' will make sure the user is logged in and will return the 'user_id'
	"""
	# cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s where id = %s returning * """,
	#                (post.title, post.content, post.published, str(id)))
	# updated_post = cursor.fetchone()
	# conn.commit()
	# index = find_index_post(id)

	post_query = db.query(models.Post).filter(models.Post.id == id) #getting the query only

	if post_query.first() == None: # getting the first result from the query
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f'Post with id: {id} does not exist')
	
	if post_query.first().owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
						detail="Not authorised to perfom the requestd action")

	# post_query.update(post.dict(), synchronize_session=False)
	post_query.update(post.model_dump(), synchronize_session=False)
	db.commit()
	updated_post = post_query.first() #getting the updated post from the query

	# post_dict = post.dict()
	# post_dict['id'] = id
	# my_posts[index] = post_dict
	return updated_post

# def find_post(id):
#     for post in my_posts:
#         if post['id'] == id:
#             return post

# def find_index_post(id):
#     for i, post in enumerate(my_posts):
#         if post['id'] == id:
#             return i