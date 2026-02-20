import os
import pandas as pd

class ProcessaDados:
    def __init__(self):
        pass

    def salvaXls(self, seguidores, perfil):
        df = pd.DataFrame(seguidores, columns=["username"])
        df.to_excel(f"seguidores/seguidores{perfil}.xlsx", index=False)

    def recuperaXls(self, perfil):
        caminho = f"seguidores/seguidores{perfil}.xlsx"
        
        if os.path.exists(caminho):
            df = pd.read_excel(caminho)
            return df["username"].tolist()
        else:
            return []

    def comparaSeguidores(self, seguidoresAntigos, seguidoresNovos):
        setAntigos = set(seguidoresAntigos)
        setNovos = set()
        for seguidor in seguidoresNovos:
            setNovos.add(seguidor["username"])
        print(len(setAntigos))
        print(len(setNovos))
        
        novosSeguidores = list(setNovos - setAntigos)
        deixaramDeSeguir = list(setAntigos - setNovos)
        
        return {
            "novos_seguidores": novosSeguidores,
            "deixaram_de_seguir": deixaramDeSeguir
        }