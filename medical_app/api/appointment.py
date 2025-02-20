
import frappe
import requests
import time


@frappe.whitelist()
def create_appointment(PID, doctor_practitioner, doct_amount):
    create_doc  =frappe.new_doc("Que")
    create_doc.payable_amount = doct_amount
    create_doc.patient=PID
    create_doc.mode_of_payment = "Cash"
    create_doc.practitioner=doctor_practitioner
    create_doc.cost_center = "Main - HH"


    create_doc.insert()
    frappe.db.commit()

    if create_doc:
        frappe.response['http_status_code'] = 200
        return "appointment Success"
    else:
        frappe.response['http_status_code'] = 404
        return 'Erro while creating appointment'




@frappe.whitelist()
def get_appointments(patient_id=None):
 
    # Validate input
    if not patient_id:
        frappe.response['http_status_code'] = 400
        return {
            "status": "error",
            "message": "Patient ID is required."
        }

    try:
        # Fetch all appointments (Que docs) linked to this patient
        appointments = frappe.get_all(
            "Que",
            filters={"patient": patient_id, "status": ["!=", "Canceled"]},
            fields=["name", "patient", "practitioner", "paid_amount", "creation"]
        )

        # If no appointments found, return 404
        if not appointments:
            frappe.response['http_status_code'] = 404
            return {
                "status": "error",
                "message": f"No appointments found for patient: {patient_id}"
            }

        # Return appointments list
        frappe.response['http_status_code'] = 200
        return {
            "status": "success",
            "message": "Appointments retrieved successfully",
            "Data": appointments
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Appointments Error")
        frappe.response['http_status_code'] = 500
        return {
            "status": "error",
            "message": "An error occurred while retrieving appointments.",
            "error": str(e)
        }
