from Database import add_user, add_ticket, add_engineering_assignment, get_user_tickets, \
    get_engineering_assigned_tickets
from datetime import datetime

# add_user("TO", "123", "بابک کریم پور",
#          "درخواست‌دهنده", "واحد ابزار", "02")
#
# add_user("Heydari", "123", "حسن حیدری", "کارشناس مهندسی", "مهندسی")

# # افزودن یک تیکت
# add_ticket(
#     requester_name="بابک کریم پور",
#     requester_unit="واحد ابزار",
#     request_number="REQ12345",
#     request_date=datetime(2024, 11, 28),
#     request_description="درخواست ارتقای سیستم",
#     request_priority="فوری",
#     need_date=datetime(1403, 9, 11),
#     project_code="PROJ001"
# )

add_user("CA",
         "123",
         "مهدی حکیمیان",
         "درخواست‌دهنده",
         "واحد ریخته گری",
         "02"
         )

