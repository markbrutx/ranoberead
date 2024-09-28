module.exports = {
  apps: [
    {
      name: 'flask-backend',
      cwd: './server',
      script: '/bin/bash',
      args: '-c "pip3 install gunicorn && python3.8 -m gunicorn app:app -c gunicorn.conf.py"',
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
