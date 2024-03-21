# seed fake data to the database using the faker library
from faker import Faker
from flask_security.utils import hash_password
from app import user_datastore
from models.db import db
from models.users import User, Role
from models.posts import UserPost, UserPostComments, UserPostLikes
from models.users import Followers
from models.users import RolesUsers
from models.users import Role
from models.db import db

fake = Faker()


class DataSeeder:
    def __init__(self):
        self.fake = Faker()
        self.seed_iterations = 50
        self.seed_posts_iterations = 75
        self.seed_comments_iterations = 100
        self.seed_likes_iterations = 100
        self.seed_follows_iterations = 100

    def seed_roles(self):
        db.create_all()
        user_datastore.create_role(name="admin", description="Administrator")
        user_datastore.create_role(name="user", description="User")
        db.session.commit()

    def seed_admin(self):
        # if admin exists, do not seed
        if User.query.filter_by(username="admin").first():
            return
        db.create_all()
        user_datastore.create_user(
            email="admin@stjernstrom.me",
            username="stjernapps",
            password=hash_password("qweqweqwe"),
            roles=["Admin"],
        )

    def seed_users(self):
        for _ in range(self.seed_iterations):
            user_random_id = (
                f"{fake.user_name()}{fake.random_int(1, self.seed_iterations)}"
            )
            user_datastore.create_user(
                email=fake.email(),
                username=user_random_id,
                password=fake.password(),
            )
        db.session.commit()

    def seed_posts(self):
        for _ in range(self.seed_posts_iterations):
            user = User.query.get(fake.random_int(1, self.seed_iterations))
            if user:
                if fake.boolean(chance_of_getting_true=50):
                    img = f"https://source.unsplash.com/random?sig={fake.random_int(1, 1000)}"
                else:
                    img = None
                post = UserPost(
                    title=fake.sentence(),
                    splash_url=img,
                    splash_caption=fake.sentence(),
                    splash_credit=fake.name(),
                    content=fake.text(),
                    date_posted=fake.date_time_this_year(),
                    comments_disabled=fake.boolean(chance_of_getting_true=20),
                    user_id=user.id,
                )
                db.session.add(post)
            else:
                print("User not found")
                continue
        db.session.commit()

    def seed_comments(self):
        for _ in range(self.seed_comments_iterations):
            user = User.query.get(fake.random_int(1, self.seed_iterations))
            post = UserPost.query.get(fake.random_int(1, self.seed_posts_iterations))
            if user and post:
                comment = UserPostComments(
                    user_id=user.id,
                    post_id=post.id,
                    content=fake.text(),
                    date_commented=fake.date_time_this_year(),
                )
                db.session.add(comment)
                post.comments += 1
                db.session.add(post)

        db.session.commit()

    def seed_likes(self):
        for _ in range(self.seed_likes_iterations):
            user = User.query.get(fake.random_int(1, self.seed_iterations))
            post = UserPost.query.get(fake.random_int(1, self.seed_likes_iterations))
            if user and post:
                like = UserPostLikes(
                    user_id=user.id,
                    post_id=post.id,
                    date_liked=fake.date_time_this_year(),
                )
                db.session.add(like)
                post.likes += 1
                db.session.add(post)
        db.session.commit()

    def seed_follows(self):
        for _ in range(self.seed_follows_iterations):
            follower = User.query.get(fake.random_int(1, self.seed_iterations))
            followed = User.query.get(fake.random_int(1, self.seed_iterations))
            if follower and followed:
                if follower.id != followed.id:
                    follow = Followers(follower_id=follower.id, followed_id=followed.id)
                    db.session.add(follow)
        db.session.commit()

    def seed_all(self):
        # check if the database is empty
        if not User.query.first():
            self.seed_admin()
            self.seed_users()
            self.seed_follows()
            print("Seeded Users")
        if not UserPost.query.first():
            self.seed_posts()
            self.seed_comments()
            self.seed_likes()
            print("Seeded Posts, Comments and Likes")
