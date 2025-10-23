module.exports = {
  apps: [
    {
      name: 'streamlit-app',
      script: 'streamlit',
      args: 'run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true',
      cwd: '/home/user/webapp',
      interpreter: 'python3',
      env: {
        PYTHONPATH: '/home/user/webapp',
      },
      watch: false,
      instances: 1,
      exec_mode: 'fork'
    }
  ]
}
