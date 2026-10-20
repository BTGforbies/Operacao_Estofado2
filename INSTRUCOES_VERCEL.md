# Publicação na Vercel

Consulte [README.md](README.md) para a configuração completa e atualizada. Na Vercel, configure `SECRET_KEY`, `DATABASE_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `ADMIN_PASSWORD` (necessário apenas se a base estiver vazia), `APP_ENV=production` e o endereço de upload persistente compatível com sua arquitetura.

Cadastre no Google Cloud Console a URI exata `https://SEU_DOMINIO/auth/google/callback`. A tela de login só mostra a opção Google depois que as duas credenciais OAuth estão configuradas. O acesso é fechado para e-mails que não foram cadastrados pelo administrador.

O SQLite e arquivos em `/tmp` não persistem entre execuções serverless. Configure PostgreSQL gerenciado e armazenamento durável/privado de anexos antes de usar dados reais. O sistema não migra dados SQLite para PostgreSQL automaticamente.

Se ocorrer um erro, consulte os logs da função e remova segredos e dados pessoais antes de compartilhar um traceback.
