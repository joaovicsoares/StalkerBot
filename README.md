# StalkerBot

## Principais mudanças
Devido a necessidade de interceptar os requests feitos na pagina, a tecnologia principal do projeto foi alterada para playwright visto que fazer isto com playwright é muito mais simples. O motivo de precisar ser feita esta interceptação se deve ao fato de que o frontend não mostra a lista total de seguidore. EX: perfil com 200 seguidores, a lista mostrada carrega apenas 190, e este numero pode variar, mesmo que na response da requisição esteja vindo todos os 200 seguidores. 