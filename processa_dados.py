import os
import pandas as pd

class ProcessaDados:
    def __init__(self):
        pass

    def salvaXls(self, seguidores, perfil):
        df = pd.DataFrame(seguidores, columns=["username"])
        df.to_excel(f"seguidores/seguidores{perfil}.xlsx", index=False)

    