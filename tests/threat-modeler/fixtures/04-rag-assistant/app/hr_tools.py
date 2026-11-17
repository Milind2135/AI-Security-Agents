import requests

def create_hr_ticket(employee_id: str, category: str, description: str):
    # uses a service account that can open tickets for ANY employee
    return requests.post("https://hr-tickets.internal.example/api/tickets",
                         json={"employee_id": employee_id, "category": category, "description": description},
                         headers={"Authorization": "Bearer " + open("/etc/hr/service-token").read()})
