# core/player.py
# Music player & queue management logic

class Player:
    def __init__(self):
        self.queue = []
        self.is_playing = False

    async def play(self, chat_id, song):
        self.is_playing = True
        # TODO: integrate PyTgCalls streaming here

    async def pause(self):
        self.is_playing = False

    async def resume(self):
        self.is_playing = True

    async def stop(self):
        self.is_playing = False
        self.queue.clear()

    async def skip(self):
        pass

player_instance = Player()
