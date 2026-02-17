class FollowersService:
    def __init__(self, page):
        self.page = page
        self.seguidores = []

    def _coleta_seguidores(self, response):
        if "friendships" in response.url and "followers" in response.url:
                try:
                    data = response.json()

                    users = data.get("users", [])
                    self.seguidores.extend(users)
                except Exception:
                    pass

    def inicia_coleta(self):
        self.page.on("response", self._coleta_seguidores)

    def get_seguidores(self):
        return self.seguidores