module.exports = {
  apps: [
    {
      name: 'flask-backend',
      cwd: '/root/ranoberead/server',
      script: '/usr/local/bin/gunicorn',
      args: 'app:application --config /root/ranoberead/server/gunicorn.conf.py --preload',
      interpreter: '/usr/bin/python3.8',
      env: {
        PORT: 3000,
        PYTHONUNBUFFERED: 'true',
        FLASK_ENV: 'production', // продакшн-режим
        FLASK_DEBUG: '0' // отключаем отладку
      },
      error_file: '/root/ranoberead/logs/pm2-flask-backend-error.log',
      out_file: '/root/ranoberead/logs/pm2-flask-backend-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      combine_logs: true
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
