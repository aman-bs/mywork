import json
from functools import wraps

API_VERSIONS = {
    "get_samples": {
        "retired": ["2022-10-31"],
        "sunset": ["2023-06-30"],
        "active": ["2023-02-21", "2023-08-01"]
    }
}

def jsonify(data):
    return json.dumps(data)

def api_request_version_check(api_function):
    """Decorator to check API version status automatically based on the version in the payload."""
    @wraps(api_function)
    def decorated_function(*args, **kwargs):
        data = get_request_json_payload()
        api_version = data.get("api_version", None)

        if not api_version:
            return jsonify({
                "status": "error",
                "message": "API version is required.",
                "error_code": 400,
                "is_deprecated": False
            }), 400

        api_name = api_function.__name__  # Get the name of the decorated function

        api_versions = API_VERSIONS.get(api_name, {})
        retired_versions = api_versions.get("retired", [])
        sunset_versions = api_versions.get("sunset", [])
        active_versions = api_versions.get("active", [])

        if api_version in retired_versions:
            return jsonify({
                "status": "error",
                "message": f"API version {api_version} is retired and no longer supported.",
                "error_code": 410,
                "is_deprecated": True
            }), 410

        if api_version in sunset_versions:
            response = api_function(*args, **kwargs)
            return jsonify({
                "status": "warning",
                "data": json.loads(response),  # Parsing response since it's a JSON string
                "message": f"API version {api_version} is in the sunset phase and will be deprecated soon.",
                "error_code": 299,
                "is_deprecated": True
            })

        if api_version in active_versions:
            response = api_function(*args, **kwargs)
            return jsonify({
                "status": "success",
                "data": json.loads(response),
                "message": "Request processed successfully.",
                "error_code": None,
                "is_deprecated": False
            })

        return jsonify({
            "status": "error",
            "message": f"API version {api_version} is not recognized.",
            "error_code": 400,
            "is_deprecated": False
        }), 400

    return decorated_function
    
@api_request_version_check
def get_samples():
    """gather sample data"""
    data = ["Hello", "World"]
    sample_data = data
    response = {
        "sample_info": sample_data
    }
    return json.dumps(response)


def get_request_json_payload():
    return {
        "api_version": "2023-06-30",
        "other_data": "example"
    }

response = get_samples()
print("Response:", response)