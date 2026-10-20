import os
import re
import tempfile
import unittest

TEMP = tempfile.TemporaryDirectory()
os.environ.setdefault('SECRET_KEY', 'test-secret-key-with-more-than-32-characters-123456')
os.environ.setdefault('ADMIN_PASSWORD', 'test-admin-password-long-enough')
os.environ['APP_DB'] = os.path.join(TEMP.name, 'test.db')
os.environ['UPLOAD_DIR'] = os.path.join(TEMP.name, 'uploads')

from app import app, conn, init_db


class SecurityFlowsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        with conn() as db:
            for table in ('documents', 'costs', 'visits', 'quotes', 'catalog', 'clients', 'logs'):
                db.execute(f'DELETE FROM {table}')
            db.execute("DELETE FROM users WHERE email IN ('owner-a@example.test','owner-b@example.test','staff@example.test')")
            db.execute("INSERT INTO users(email,password,role,company_id,auth_provider) VALUES(?,?,?,?,?)",
                       ('owner-a@example.test', 'unused', 'owner', 1, 'google'))
            db.execute("INSERT INTO users(email,password,role,company_id,auth_provider) VALUES(?,?,?,?,?)",
                       ('owner-b@example.test', 'unused', 'owner', 2, 'google'))
            db.execute("INSERT INTO users(email,password,role,company_id,auth_provider) VALUES(?,?,?,?,?)",
                       ('staff@example.test', 'unused', 'staff', 1, 'google'))
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as session:
            session['csrf'] = 'test-csrf'

    def login(self, email, password):
        page = self.client.get('/login')
        token = re.search(rb'name="csrf" value="([^"]+)"', page.data).group(1).decode()
        return self.client.post('/login', data={'email': email, 'password': password, 'csrf': token})

    def test_password_login_logout_and_database_persistence(self):
        response = self.login('admin@estofados.local', os.environ['ADMIN_PASSWORD'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.post('/logout', data={'csrf': self.csrf()}).status_code, 302)
        with conn() as db:
            found = db.execute("SELECT id FROM users WHERE email='owner-a@example.test'").fetchone()
        self.assertIsNotNone(found)

    def test_tenant_scope_ignores_requested_company_id(self):
        with conn() as db:
            user = db.execute("SELECT * FROM users WHERE email='owner-a@example.test'").fetchone()
        self.authenticate_as(user)
        response = self.client.post('/clients', data={'csrf': self.csrf(), 'company_id': '2', 'name': 'Cliente A'})
        self.assertEqual(response.status_code, 302)
        with conn() as db:
            row = db.execute("SELECT company_id FROM clients WHERE name='Cliente A'").fetchone()
        self.assertEqual(row['company_id'], 1)

    def test_staff_cannot_open_finance_and_role_changes_apply_to_existing_session(self):
        with conn() as db:
            staff = db.execute("SELECT * FROM users WHERE email='staff@example.test'").fetchone()
        self.authenticate_as(staff)
        self.assertEqual(self.client.get('/finance').status_code, 403)
        with conn() as db:
            db.execute("UPDATE users SET role='owner' WHERE id=?", (staff['id'],))
        self.assertEqual(self.client.get('/settings').status_code, 200)
        with conn() as db:
            db.execute("UPDATE users SET active=0 WHERE id=?", (staff['id'],))
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_post_without_csrf_token_is_rejected(self):
        with conn() as db:
            user = db.execute("SELECT * FROM users WHERE email='owner-a@example.test'").fetchone()
        self.authenticate_as(user)
        self.assertEqual(self.client.post('/clients', data={'name': 'Blocked'}).status_code, 400)

    def csrf(self):
        with self.client.session_transaction() as session:
            return session['csrf']

    def authenticate_as(self, user):
        with self.client.session_transaction() as session:
            session['csrf'] = 'test-csrf'
            session['user'] = dict(id=user['id'], email=user['email'], role=user['role'], company_id=user['company_id'])
            session['active_company_id'] = user['company_id'] or 1


if __name__ == '__main__':
    unittest.main()
