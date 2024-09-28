module.exports = {
  apps: [
    {
      name: 'flask-backend',
      cwd: './server',
      script: 'gunicorn',
      args: 'app:app -c gunicorn.conf.py',
      interpreter: '/usr/bin/python3.8',
      env: {
        PORT: 3000,
        PYTHONUNBUFFERED: 'true',
        FLASK_ENV: 'development',
        FLASK_DEBUG: '1'
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
