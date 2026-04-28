from flask import Flask, jsonify, request
from flask_cors import CORS
from TestAPP.backend.services.task_service import TaskService
import logging
import sys

app = Flask(__name__)
CORS(app)

task_service = TaskService()


@app.get("/api/tasks")
def get_tasks():
    filters = {
        "status": request.args.get("status"),
        "priority": request.args.get("priority"),
        "search": request.args.get("search"),
    }
    
    tasks = task_service.get_all_tasks(filters)
    return jsonify(tasks), 200


@app.get("/api/tasks/<int:task_id>")
def get_task(task_id):
    try:
        task = task_service.get_task_by_id(task_id)
        return jsonify(task.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.post("/api/tasks")
def create_task():
    data = request.get_json() or {}

    try:
        task = task_service.create_task(data)
        return jsonify(task.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json() or {}

    try:
        task = task_service.update_task(task_id, data)
        return jsonify(task.to_dict()), 200
    except ValueError as e:
        status_code = 404 if str(e) == "Task not found" else 400
        return jsonify({"error": str(e)}), status_code


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    try:
        task_service.delete_task(task_id)
        return jsonify({"message": f"Task {task_id} deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.get("/api/stats")
def get_stats():
    stats = task_service.get_stats()
    return jsonify(stats), 200

@app.get("/api/health")
def health():
    app.logger.debug("GET /api/health called")
    return jsonify({"status": "ok"})


@app.get("/api/error")
def force_error():
    app.logger.debug("GET /api/error called")
    raise ValueError("Intentional test error")


@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.exception("Unhandled error on %s %s", request.method, request.path)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)