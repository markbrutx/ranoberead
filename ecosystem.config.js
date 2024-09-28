module.exports = {
  apps: [
    {
      name: 'flask-backend',
      cwd: './server',
      script: '/bin/bash',
      args: '-c "source venv/bin/activate && venv/bin/gunicorn app:app -c gunicorn.conf.py"',
      interpreter: '',
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
