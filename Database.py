from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


# جدول درخواست‌ها
class Ticket(Base):
    __tablename__ = 'tickets'

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    requester_name = Column(String(255), nullable=False)
    requester_unit = Column(String(255), nullable=False)
    request_number = Column(String(50), unique=True, nullable=False)
    request_date = Column(String, nullable=False)
    request_description = Column(Text, nullable=False)
    request_priority = Column(Enum('عادی', 'فوری'), nullable=False)
    need_date = Column(String, nullable=False)
    attachment_path = Column(String(255))
    project_code = Column(String(50))
    status = Column(Enum('در حال انجام', 'انجام شده', 'رویت نشده'), default='رویت نشده')
    rejection_description = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # ارتباط با جدول ارجاع به مهندسی
    engineering_assignments = relationship("EngineeringAssignment", back_populates="ticket")
    # ارتباط با جدول ارجاع به ساخت
    manufacturing_assignments = relationship("ManufacturingAssignment", back_populates="ticket")


# جدول ارجاع به مهندسی
class EngineeringAssignment(Base):
    __tablename__ = 'engineering_assignments'

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('tickets.ticket_id'), nullable=False)
    engineer_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    engineering_comment = Column(Text)
    status = Column(Enum('در حال انجام', 'انجام شده', 'رویت نشده'), default='رویت نشده')
    completion_date = Column(Date)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # ارتباط با جدول درخواست‌ها
    ticket = relationship("Ticket", back_populates="engineering_assignments")
    # ارتباط با جدول کاربران
    engineer = relationship("Users", back_populates="engineering_assignments")


# جدول ارجاع به ساخت
class ManufacturingAssignment(Base):
    __tablename__ = 'manufacturing_assignments'

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('tickets.ticket_id'), nullable=False)
    technician_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    manufacturing_comment = Column(Text)
    status = Column(Enum('در حال انجام', 'انجام شده', 'رویت نشده'), default='رویت نشده')
    completion_date = Column(Date)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # ارتباط با جدول درخواست‌ها
    ticket = relationship("Ticket", back_populates="manufacturing_assignments")
    # ارتباط با جدول کاربران
    technician = relationship("Users", back_populates="manufacturing_assignments")


# جدول کاربران
class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum('درخواست‌دهنده', 'رییس مهندسی', 'کارشناس مهندسی', 'رییس ساخت', 'کارشناس ساخت'), nullable=False)
    factory = Column(Enum("01", "02", "03", "04", "05", "06", "07", "08", "09"), nullable=False)
    unit = Column(String(255))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # ارتباط با جدول ارجاع به مهندسی
    engineering_assignments = relationship("EngineeringAssignment", back_populates="engineer")
    # ارتباط با جدول ارجاع به ساخت
    manufacturing_assignments = relationship("ManufacturingAssignment", back_populates="technician")


# ساخت دیتابیس
def create_database():
    engine = create_engine('sqlite:///data/ticketing_system.db', echo=True)  # مسیر فایل دیتابیس SQLite
    Base.metadata.create_all(engine)
    print("Database created successfully!")


if __name__ == '__main__':
    create_database()

# تنظیمات اتصال به دیتابیس
DATABASE_URL = 'sqlite:///data/ticketing_system.db'  # آدرس دیتابیس
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


# افزودن تیکت جدید
def add_ticket(requester_name, requester_unit, request_number, request_date, request_description,
               request_priority, need_date, project_code, attachment_path=None ):
    try:
        ticket = Ticket(
            requester_name=requester_name,
            requester_unit=requester_unit,
            request_number=request_number,
            request_date=request_date,
            request_description=request_description,
            request_priority=request_priority,
            need_date=need_date,
            attachment_path=attachment_path,
            project_code=project_code,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(ticket)
        session.commit()
        print(f"Ticket {request_number} added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error adding ticket: {e}")


# مشاهده تمام تیکت‌ها
def get_all_tickets():
    try:
        tickets = session.query(Ticket).all()
        return tickets
    except Exception as e:
        print(f"Error fetching tickets: {e}")


# مشاهده تیکت‌های کاربر خاص
def get_user_tickets(requester_name):
    try:
        tickets = session.query(Ticket).filter_by(requester_name=requester_name).all()
        return tickets
    except Exception as e:
        print(f"Error fetching tickets for user {requester_name}: {e}")
        return []


# مشاهده تیکت‌های ارجاع شده به کاربر مهندسی
def get_engineering_assigned_tickets(engineer_id):
    try:
        assignments = session.query(EngineeringAssignment).filter_by(engineer_id=engineer_id).all()
        tickets = [assignment.ticket for assignment in assignments]
        return tickets
    except Exception as e:
        print(f"Error fetching assigned tickets for engineer {engineer_id}: {e}")
        return []


# حذف تیکت
def delete_ticket(ticket_id):
    try:
        ticket = session.query(Ticket).filter_by(ticket_id=ticket_id).first()
        if ticket:
            session.delete(ticket)
            session.commit()
            print(f"Ticket {ticket_id} deleted successfully!")
        else:
            print(f"Ticket {ticket_id} not found!")
    except Exception as e:
        session.rollback()
        print(f"Error deleting ticket: {e}")


# به‌روزرسانی وضعیت تیکت
def update_ticket_status(ticket_id, new_status, rejection_description=None):
    try:
        ticket = session.query(Ticket).filter_by(ticket_id=ticket_id).first()
        if ticket:
            ticket.status = new_status
            if new_status == 'رد شده':
                ticket.rejection_description = rejection_description
            ticket.updated_at = datetime.now()
            session.commit()
            print(f"Ticket {ticket_id} updated successfully!")
        else:
            print(f"Ticket {ticket_id} not found!")
    except Exception as e:
        session.rollback()
        print(f"Error updating ticket: {e}")


# افزودن ارجاع به مهندسی
def add_engineering_assignment(ticket_id, engineer_id, engineering_comment):
    try:
        assignment = EngineeringAssignment(
            ticket_id=ticket_id,
            engineer_id=engineer_id,
            engineering_comment=engineering_comment,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(assignment)
        session.commit()
        print(f"Engineering assignment for ticket {ticket_id} added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error adding engineering assignment: {e}")


# افزودن ارجاع به ساخت
def add_manufacturing_assignment(ticket_id, technician_id, manufacturing_comment):
    try:
        assignment = ManufacturingAssignment(
            ticket_id=ticket_id,
            technician_id=technician_id,
            manufacturing_comment=manufacturing_comment,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(assignment)
        session.commit()
        print(f"Manufacturing assignment for ticket {ticket_id} added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error adding manufacturing assignment: {e}")


# مشاهده کاربران
def get_all_users():
    try:
        users = session.query(Users).all()
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")


# افزودن کاربر جدید
def add_user(username, password, full_name, role, unit=None, factory="02"):
    try:
        user = Users(
            username=username,
            password=password,
            full_name=full_name,
            role=role,
            unit=unit,
            factory=factory,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(user)
        session.commit()
        print(f"User {username} added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error adding user: {e}")


# حذف کاربر
def delete_user(user_id):
    try:
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"User {user_id} deleted successfully!")
        else:
            print(f"User {user_id} not found!")
    except Exception as e:
        session.rollback()
        print(f"Error deleting user: {e}")
