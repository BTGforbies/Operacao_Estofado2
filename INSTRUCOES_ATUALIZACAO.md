# ATELIÊ OS — Atualização de acessos com banco persistente

## O que foi alterado
- Mantidos os painéis e o visual existentes.
- Um login mantém a sessão ao navegar no menu; `SECRET_KEY` deve ser **fixa** e igual em todas as instâncias.
- O administrador pode cadastrar e-mail, senha inicial e perfil, atribuindo Abreu ou Luiz a cada conta. Não há confirmação por e-mail.
- Cada conta owner/staff fica vinculada apenas à própria empresa. O administrador pode alternar as duas.
- Persistência dos cadastros agora pode usar PostgreSQL externo (`DATABASE_URL`). Na Vercel, a aplicação **exige** esse banco.

## Antes de publicar na Vercel
1. Faça backup do código e do banco atual, caso tenha registros importantes. Não envie bancos nem arquivos `.env` ao GitHub.
2. Crie um banco PostgreSQL gerenciado (por exemplo, Neon ou Supabase) e copie a **string de conexão** PostgreSQL. Não a compartilhe em mensagens ou prints.
3. Em Vercel > seu projeto > Settings > Environment Variables, configure:
   - `DATABASE_URL`: URL completa do PostgreSQL (`postgresql://...`)
   - `SECRET_KEY`: valor aleatório forte com pelo menos 32 caracteres; **não altere em cada deploy**
   - `ADMIN_PASSWORD`: senha inicial forte do administrador, usada na criação do primeiro banco. Não altera senha já cadastrada.
4. Faça upload **do conteúdo** da pasta `estofados_sistema` na raiz do repositório, ou mantenha a pasta completa e configure Root Directory como `estofados_sistema`. Não misture as duas estruturas.
5. Confirme que `vercel.json`, `app.py`, `requirements.txt` e a pasta `api` estão na raiz configurada na Vercel.
6. Faça deploy. Abra `/login`. Conta inicial: `admin@estofados.local`, com a senha do `ADMIN_PASSWORD` do primeiro deploy.
7. Em **Usuários e acessos**, crie um acesso `owner` para cada tapeçaria, cada qual com seu e-mail e senha inicial. Teste em janela anônima e confirme que Luiz não acessa Abreu, nem vice-versa.

## Importante
- O banco é persistente **somente se** `DATABASE_URL` apontar para um PostgreSQL externo ativo. O arquivo local SQLite não resolve persistência da Vercel.
- **Fotos, PDFs assinados e anexos ainda NÃO são persistentes na Vercel**, pois continuam armazenados no filesystem temporário da função. Não os use com clientes reais até integrar armazenamento de objetos (ex.: S3/R2/Supabase Storage).
- Antes de uso real, revise política de backup, redefinição de senha, LGPD, isolamento entre empresas e proteção de arquivos.
- Esta versão preserva o esquema de tabelas do código enviado, e não migra automaticamente dados antigos de SQLite para PostgreSQL.
- Se ocorrer erro 500, copie o traceback no painel Vercel > Logs (ocultando credenciais).
