module.exports = {
  apps: [
    {
      name: 'flask-backend',
      cwd: './server',
      script: 'python3.8',
      args: '-m gunicorn app:app --config gunicorn.conf.py',
      interpreter: '',
      env: {
        PORT: 3000,
        PYTHONUNBUFFERED: 'true'
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
