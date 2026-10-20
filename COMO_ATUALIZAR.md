# Como atualizar

As instruções atuais de instalação, login Google, banco e hospedagem estão em [README.md](README.md).

Antes de atualizar uma instalação existente, faça backup do banco e dos uploads. Preserve a `SECRET_KEY` e as credenciais de conexão; a sessão expira em até 12 horas e logout encerra o cookie. As colunas Google são adicionadas de forma aditiva à tabela de usuários. Migrar dados existentes de SQLite para PostgreSQL precisa ser feito separadamente.

Depois da publicação, teste login/logout, acesso às rotas de cada perfil, isolamento entre empresas, persistência dos registros e acesso autenticado a anexos. O Google exige credenciais OAuth e callback HTTPS cadastrado no Google Cloud Console. Não use hospedagem com filesystem efêmero para manter banco SQLite ou uploads.
