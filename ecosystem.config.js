module.exports = {
  apps: [
    {
      name: "logistics-backend",
      cwd: "./backend",
      script: "venv/Scripts/python.exe",
      args: "-m uvicorn main:app --port 8000 --reload",
      interpreter: "none",
      env: {
        PATH: process.env.PATH + ";C:\\Program Files\\Python311;C:\\Program Files\\Python311\\Scripts"
      }
    },
    {
      name: "logistics-frontend",
      cwd: "./frontend",
      script: "C:\\Program Files\\nodejs\\npm.cmd",
      args: "run dev",
      interpreter: "none"
    }
  ]
};
