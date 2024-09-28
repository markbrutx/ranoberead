module.exports = {
  apps: [
    {
      name: 'flask-backend',
      cwd: '/root/ranoberead/server',
      script: '/usr/local/bin/gunicorn',
      args: 'app:app --config gunicorn.conf.py --log-level debug --preload',
      interpreter: '/usr/bin/python3.8',
      env: {
        PORT: 3000,
        PYTHONUNBUFFERED: 'true',
        FLASK_ENV: 'development',
        FLASK_DEBUG: '1'
      },
      error_file: '/root/ranoberead/logs/flask-backend-error.log',
      out_file: '/root/ranoberead/logs/flask-backend-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'nextjs-frontend',
      cwd: '/root/ranoberead/frontend',
      script: 'npm',
      args: 'start',
      env: {
        PORT: 5000
      }
    }
  ]
};
