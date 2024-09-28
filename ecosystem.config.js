module.exports = {
  apps: [
    {
      name: 'flask-backend',
      cwd: './server',
      script: './venv/bin/gunicorn',
      args: 'app:app -c gunicorn.conf.py',
      interpreter: 'python3',
      env: {
        PORT: 3000
      }
    },
    {
      name: 'nextjs-frontend',
      cwd: './frontend',
      script: 'npm',
      args: 'start',
      env: {
        PORT: 5000
      }
    }
  ]
};
