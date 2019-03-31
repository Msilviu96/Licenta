import pusher


class Pusher:
    pusher_client = None

    @classmethod
    def create_instance(cls):
        cls.pusher_client = pusher.Pusher(
            app_id='732495',
            key='4df52d9bd8bcf616c85c',
            secret='54e285d0324b0e65fcc8',
            cluster='eu',
            ssl=True
        )
        print("instance is created")

    @classmethod
    def get_instance(cls):
        if cls.pusher_client is None:
            cls.create_instance()
        return cls.pusher_client
