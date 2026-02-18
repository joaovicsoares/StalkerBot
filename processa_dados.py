from datetime import datetime
import pandas as pd

class ProcessaDados:
    def __init__(self):
        pass

    def salvaXls(seguidores):
        df = pd.DataFrame(seguidores, columns=["username"])
        df.to_excel(f"seguidores{datetime.now()}.xlsx", index=False)

    