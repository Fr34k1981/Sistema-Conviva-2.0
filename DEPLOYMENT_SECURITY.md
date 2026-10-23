# Publicacao segura

## Identidade e acesso

Em producao, o app exige OpenID Connect (OIDC). Configure o provedor de identidade na secao `[auth]` dos Secrets do Streamlit e defina as contas autorizadas. O Streamlit Cloud e detectado como producao; em outros provedores, configure `APP_ENV=production`. Para desenvolvimento local, use `APP_ENV=development` em um `.env` nao versionado.

Exemplo de Secrets do Streamlit (substitua os valores e nunca versiona este arquivo):

```toml
APP_ENV = "production"
APP_ALLOWED_EMAILS = ["equipe@exemplo.org"]
APP_MANAGER_EMAILS = ["gestao@exemplo.org"]
APP_TEACHER_BY_EMAIL = { "professora@exemplo.org" = "NOME NO CADASTRO" }
APP_PORTAL_RA_BY_EMAIL = { "responsavel@exemplo.org" = "RA_DO_ESTUDANTE" }
DATABASE_URL = "postgresql://usuario:senha@host/banco?sslmode=require"

[auth]
redirect_uri = "https://SEU-APP.streamlit.app/oauth2callback"
cookie_secret = "VALOR_ALEATORIO_LONGO_E_PRIVADO"
client_id = "CLIENT_ID_DO_PROVEDOR"
client_secret = "CLIENT_SECRET_DO_PROVEDOR"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

Somente enderecos em `APP_ALLOWED_EMAILS` podem usar as funcoes da equipe. Enderecos em `APP_MANAGER_EMAILS` recebem permissoes de gestao, inclusive exclusoes. Para o Caderno de Tutoria, associe cada e-mail institucional ao nome exato do cadastro em `APP_TEACHER_BY_EMAIL`; nao e permitido escolher outra identidade em producao. Cada responsavel deve ter uma conta OIDC e um unico RA em `APP_PORTAL_RA_BY_EMAIL`; contas nao listadas sao bloqueadas. Nao use RA ou senha compartilhada como autenticacao.

O acesso de desenvolvimento local nao deve ser exposto na rede. Em qualquer hospedagem publica, confirme `APP_ENV=production`, configure OIDC e valide que uma conta nao autorizada seja recusada antes de importar dados.

## Banco, arquivos e dados

- Configure um PostgreSQL gerenciado com TLS e credenciais de menor privilegio; aplique e valide o esquema e a migracao numa copia antes de importar dados reais.
- O disco local de hospedagens gerenciadas pode ser efemero. Backups e uploads que precisem persistir devem ficar em armazenamento duravel, separado do codigo, com criptografia e politica de retencao.
- Nao faca deploy de `data/`, planilhas, dumps ou backups. O `.gitignore` nao remove arquivos ja rastreados nem os apaga do historico Git. Revise os arquivos versionados e o historico antes de publicar; a limpeza de historico precisa de coordenacao com todos os colaboradores.
- Antes de usar dados reais, valide com a instituicao a finalidade, os perfis autorizados, a retencao, o processo de correcao/exclusao e o tratamento de incidentes, conforme a LGPD e as regras da rede de ensino.

## Validacao antes de liberar

1. Teste login de funcionario permitido e negado.
2. Teste login de responsavel e confirme que so aparece o estudante vinculado ao e-mail.
3. Tente abrir diretamente a pagina de Lista Provisoria como responsavel; o acesso deve ser negado.
4. Valide escrita, leitura, backup e restauracao no banco de teste.
5. Confirme persistencia dos arquivos apos reiniciar a aplicacao.