import os
import pandas as pd

class ProcessaDados:
    def __init__(self):
        pass

    def salvaXls(self, tipo, seguidores, perfil):
        df = pd.DataFrame(seguidores, columns=["username"])
        df.to_excel(f"{tipo}/{tipo}{perfil}.xlsx", index=False)

    def recuperaXls(self, tipo, perfil):
        caminho = f"{tipo}/{tipo}{perfil}.xlsx"
        
        if os.path.exists(caminho):
            df = pd.read_excel(caminho)
            return df["username"].tolist()
        else:
            return []

    def comparaSeguidores(self, seguidoresAntigos, seguidoresNovos):
        setAntigos = set(seguidoresAntigos)
        setNovos = set(seguidoresNovos)
        
        print(len(setAntigos))
        print(len(setNovos))
        
        novosSeguidores = list(setNovos - setAntigos)
        deixaramDeSeguir = list(setAntigos - setNovos)
        
        return {
            "novos_seguidores": novosSeguidores,
            "deixaram_de_seguir": deixaramDeSeguir
        }

    def comparaSeguindoSeguidores(self, seguidores, seguindo):
        setSeguidores = set(seguidores)
        setSeguindo = set(seguindo)
        naoSegue = list(setSeguindo - setSeguidores)
        naoSigo = list(setSeguidores - setSeguindo)

        return naoSegue, naoSigo
