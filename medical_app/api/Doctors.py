
import frappe
import requests
import time

@frappe.whitelist()
def get_all_doctors():
    try:
        # Fetch all healthcare practitioners (doctors) with their name, charges, department, and image
        doctors = frappe.get_all(
            "Healthcare Practitioner",
            filters={"status": "Active"},
            fields=["practitioner_name", "op_consulting_charge", "department", "image", "services"]
        )

        # Format the image URLs if available
        system_host_url = "http://102.214.169.195"  # Replace with your actual host URL
        for doctor in doctors:
            if doctor.image:
                # Ensure image starts with /files/ and add a cache-busting query parameter
                if not doctor.image.startswith('/files/'):
                    doctor.image = f"/files/{doctor.image}"
                doctor.image = f"{system_host_url}{doctor.image}?v={int(time.time())}"
            else:
                doctor.image = None  # If no image, set it to None

        # Return the list of doctors with their formatted image URLs
        frappe.response['http_status_code'] = 200
        return {
            "status": "success",
            "Data": doctors
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get All Doctors Error")
        frappe.response['http_status_code'] = 500
        return {
            "status": "error",
            "msg": "An error occurred while fetching doctors.",
            "error": str(e),
        }
