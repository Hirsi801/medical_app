import frappe
import requests
import time




@frappe.whitelist()
def register_patient(pat_full_name, pat_gender, pat_age,pat_age_type, pat_mobile_number, pat_district):
    try:
        # Convert age to integer (if it's not already an integer)
        if not pat_full_name:
            frappe.response['http_status_code'] = 400
            return {"status": "error", "message": "Full Name is required."}
        # pat_full_name = 'Ibrahim ALI abddala'
        # Create the patient record
        create_doc = frappe.new_doc("Patient")
        create_doc.first_name = pat_full_name
        create_doc.sex = pat_gender
        create_doc.p_age = pat_age
        create_doc.age_type = pat_age_type
        create_doc.mobile_no = pat_mobile_number
        create_doc.district = pat_district

        create_doc.insert()
        frappe.db.commit()

        if create_doc:
            frappe.response['http_status_code'] = 200
            return {"status": "success", "msg": "Patient registered successfully."}
        else:
            frappe.response['http_status_code'] = 404
            return {"status": "error", "msg": "Patient registration failed."}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Patient Registration Error")
        frappe.response['http_status_code'] = 500
        return {"status": "error", "message": "An error occurred while registering the patient.", "error": str(e)}




@frappe.whitelist()
def patient_login(mobile_number):
    if not mobile_number:
        frappe.response['http_status_code'] = 400
        frappe.response['message'] = {"msg": "Mobile number is required!"}
        return frappe.response['message']
    
    try:
        # Fetch patient ID based on the mobile number
        patient = frappe.get_value("Patient", {"mobile_no": mobile_number}, "name")
        
        if patient:
            # Fetch the patient's details
            patient_info = frappe.get_doc("Patient", patient)

            frappe.response['http_status_code'] = 200
            frappe.response['message'] = {
                "msg": "Login successful",
                "Data": {
                    "patient_id": patient_info.name,
                    "first_name": patient_info.first_name,
                    "mobile": patient_info.mobile_no,
                    "district": patient_info.territory,
                    "age": patient_info.p_age,
                    "Gender": patient_info.sex
                  
                   
                }
            }
            
            return frappe.response['message']
        
        else:
            frappe.response['http_status_code'] = 404
            frappe.response['message'] = {"msg": "Patient not found with the provided mobile number."}
            return frappe.response['message']
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Patient Login Error")
        frappe.response['http_status_code'] = 500
        frappe.response['message'] = {"msg": "An error occurred while logging in", "error": str(e)}
        return frappe.response['message']


@frappe.whitelist()
def get_patients_with_same_mobile(mobile_number):
    """
    Return all patients (their name and age) who have the same mobile number.
    Example API Call:
      /api/method/medical_app.api.patient.get_patients_with_same_mobile?mobile_number=123456
    """
    if not mobile_number:
        frappe.response['http_status_code'] = 400
        return {
            "status": "error",
            "message": "Mobile number is required."
        }

    try:
        # Get a list of all Patient docs matching the mobile number
        patients = frappe.get_all(
            "Patient",
            filters={"mobile_no": mobile_number},
            # Only return the fields you want in your response
            fields=["name", "first_name", "p_age"]
        )

        if not patients:
            frappe.response['http_status_code'] = 404
            return {
                "status": "error",
                "message": f"No patients found for mobile number: {mobile_number}"
            }

        frappe.response['http_status_code'] = 200
        return {
            "status": "success",
            "message": "Patients found successfully.",
            "Data": patients  # List of dicts with name, first_name, p_age
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Patients with Same Mobile Error")
        frappe.response['http_status_code'] = 500
        return {
            "status": "error",
            "message": "An error occurred while retrieving patients.",
            "error": str(e)
        }


@frappe.whitelist()
def get_patient_profile(patient_id):
    try:
        # Fetch the Patient Registeration document
        patient_doc = frappe.get_doc("Patient Registeration", patient_id)

        # Get the profile image URL, if set
        profile_image = patient_doc.profile_image

        if profile_image:
            # Check if profile image starts with /files/
            if not profile_image.startswith('/files/'):
                profile_image = f"/files/{profile_image}"

            # Add cache-busting query parameter (timestamp)
            system_host_url = "http://104.237.2.9:81"  # Use your actual host URL here
            full_image_url = f"{system_host_url}{profile_image}?v={int(time.time())}"
        else:
            full_image_url = None

        # Return patient details along with the image URL
        return {
            "status": "success",
            "patient_id": patient_doc.name,
            "full_name": patient_doc.full_name,
            "gender": patient_doc.gender,
            "age": patient_doc.age,
            "mobile_number": patient_doc.mobile_number,
            "district": patient_doc.district,
            "image": full_image_url,  # Return the formatted image URL
        }

    except frappe.DoesNotExistError:
        # Handle the case where the patient does not exist
        frappe.response['http_status_code'] = 404
        return {
            "status": "error",
            "message": f"Patient with ID '{patient_id}' does not exist."
        }
    except Exception as e:
        # Handle unexpected errors
        frappe.log_error(frappe.get_traceback(), "Get Patient Profile Error")
        frappe.response['http_status_code'] = 500
        return {
            "status": "error",
            "message": "An unexpected error occurred.",
            "error": str(e),
        }




# api secre  key :  37e28ea0d4de028

# Authorization: token <API_KEY>:<API_SECRET>