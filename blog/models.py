import uuid
from passlib.hash import bcrypt
from common import GRAPH, BaseNode, neo4jutils


class User(BaseNode):
    def __init__(self, username):
        BaseNode.__init__(self, 'User', 'username', username, allow_update = False)

    def register(self, password):
        if not self.find():
            values = {
                "password": bcrypt.encrypt(password)
            }
            self.update(values)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, tags, text):
        user = self.find()

        new_post_values = {
            "title": title,
            "text": text,
            "timestamp": neo4jutils.Neo4jUtils.timestamp(),
            "date": neo4jutils.Neo4jUtils.date()
        }

        post = BaseNode('Post', 'id', str(uuid.uuid4()), new_post_values)
        self.join(post, 'PUBLISHED')

        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tag = BaseNode('Tag', 'name', name)
            post.join(tag, 'TAGGED', None, False)

    def like_post(self, post_id):
        self.join_simple_relationship(
            'Post',
            'id',
            post_id,
            'LIKED')

    def get_recent_posts(self):
        query = '''
        MATCH (user:USER)-[:PUBLISHED]->(post:POST)
        OPTIONAL MATCH (post)<-[:TAGGED]-(tag:TAG)
        WHERE user.username = {username}
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT 5
        '''

        return GRAPH.run(query, username=self.identity_value)

    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = '''
        MATCH (you:USER)-[:PUBLISHED]->(:POST)<-[:TAGGED]-(tag:TAG),
              (they:USER)-[:PUBLISHED]->(:POST)<-[:TAGGED]-(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags
        ORDER BY SIZE(tags) DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        '''

        return GRAPH.run(query, username=self.identity_value)

    def get_commonality_of_user(self, other):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = '''
        MATCH (they:USER {username: {they} })
        MATCH (you:USER {username: {you} })
        OPTIONAL MATCH (they)-[:PUBLISHED]->(:POST)<-[:TAGGED]-(tag:TAG),
                       (you)-[:PUBLISHED]->(:POST)<-[:TAGGED]-(tag)
        RETURN SIZE((they)-[:LIKED]->(:POST)<-[:PUBLISHED]-(you)) AS likes,
               COLLECT(DISTINCT tag.name) AS tags
        '''

        return GRAPH.run(query, they=other.identity_value, you=self.identity_value).next()


def get_todays_recent_posts():
    query = '''
    MATCH (user:USER)-[:PUBLISHED]->(post:POST)<-[:TAGGED]-(tag:TAG)
    WHERE post.date = {today}
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    '''

    return GRAPH.run(query, today=neo4jutils.Neo4jUtils.date())
