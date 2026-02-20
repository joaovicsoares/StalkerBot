class FollowersService:
    def __init__(self, page):
        self.page = page
        self.seguidores = []
        self.usernamesVistos = set()

    def _coleta_seguidores(self, response):
        if "friendships" in response.url and "followers" in response.url:
                try:
                    data = response.json()

                    users = data.get("users", [])
                    for user in users:
                        username = user.get("username")
                        if username and username not in self.usernamesVistos:
                            self.usernamesVistos.add(username)
                            self.seguidores.append(user)
                except Exception:
                    pass

    def inicia_coleta(self):
        self.page.on("response", self._coleta_seguidores)

    def get_seguidores(self):
        return self.seguidores