# Atualização do Ateliê OS

Use o [README](README.md) como fonte atual para instalar, configurar OAuth Google, PostgreSQL e publicar. Este documento mantém somente os passos de atualização do banco e implantação.

## Atualizar uma instalação

1. Faça backup consistente do banco e da pasta de arquivos enviados.
2. Publique o código e instale as dependências de `requirements.txt`.
3. Preserve `SECRET_KEY`, `DATABASE_URL` e o diretório persistente de uploads.
4. Mantenha `ADMIN_PASSWORD` como variável protegida; ela só inicializa a conta admin quando a base ainda não contém usuários.
5. Configure `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET`, e cadastre no Google o callback HTTPS `/auth/google/callback` do domínio.
6. A aplicação executa migrações aditivas para associar `google_sub` sem recriar dados de usuários. SQLite não é migrado automaticamente para PostgreSQL.
7. Depois da publicação, valide login, logout, papéis e isolamento entre as empresas.

Em Vercel, use PostgreSQL gerenciado; o armazenamento local de funções é efêmero. Anexos precisam de volume persistente ou serviço de arquivos privado. Não use credenciais de produção em desenvolvimento nem envie `.env`, bancos ou uploads ao GitHub.
